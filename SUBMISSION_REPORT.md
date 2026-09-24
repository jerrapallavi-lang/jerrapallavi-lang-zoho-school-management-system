# Official Submission Report: School Management System

**System Architecture**: Zoho CRM & Zoho Creator Integration  
**Organization / School**: St. Jude International School  
**Repository & Source Directory**: `D:\zoho-school-management-system`  

---

## 1. System Access & Credential Placeholders

> [!NOTE]
> Below are the access details and account handles for reviewing the live implementation:

- **Zoho Account Email**: `admin@stjude-school.edu` *(or Evaluator Trial Account)*
- **Zoho CRM Instance**: `https://crm.zoho.com` (Org ID: `891230491`)
- **Zoho Creator Parent Application**: `https://creatorapp.zoho.com/school_admin/parent-portal`
- **Working Admission Webform File**: [`crm/webform/admission_webform.html`](file:///D:/zoho-school-management-system/crm/webform/admission_webform.html)

---

## 2. Overall Data Structure & Module Relationships

The database architecture is designed with **normalized relational mapping** across Zoho CRM custom modules, guaranteeing data integrity, scalable lookup querying, and historical record preservation:

```
[Leads]  --->  (Admission Confirmed)  --->  [Students]
                                              |
      +-----------------+---------------------+-----------------+
      |                 |                     |                 |
[Attendance]    [Student_Marks]         [Student_Fees]    [Student_Enrolments]
      |                 |                     |
[Sections]       [Examinations]        [Fee_Payments]
      |                 |
  [Classes]         [Subjects]
```

### Key Structural Highlights:
1. **Admissions to Student Conversion**: Admission enquiries captured in `Leads` convert to permanent records in the `Students` custom module.
2. **Unique Student ID**: The system generates an immutable sequential code `STU-YYYY-XXXX` upon enrolment.
3. **Academic Structure Hierarchy**: Interconnected modules for `Academic_Years`, `Classes`, `Sections`, `Subjects`, and `Teachers`.
4. **Historical Enrolment Tracking**: `Student_Enrolments` preserves class and section assignments across multiple academic years.
5. **Attendance Duplicate Prevention**: Daily attendance uses an enforced composite key `Student_ID + YYYYMMDD` (`Attendance_Key`).
6. **Fee Payment Installment Tracking**: `Fee_Payments` links to `Student_Fees`, computing collected vs. balance amounts dynamically.

---

## 3. CRM – Creator Integration Approach

Zoho CRM serves as the **Single Source of Truth** for internal administration, while Zoho Creator delivers a **secured, parent-facing experience**.

### Integration Workflow & Flow Diagram:
```
CRM Webform -> Leads -> Admission Confirmed -> Deluge Conversion -> Students Record
                                                                          |
                                                               (Sync Deluge Function)
                                                                          v
Parent Portal (Zoho Creator) <--- Row-Level Filter (zoho.loginuserid) <--- Synced Records
         |
  (Parent Payment Upload)
         v
Creator-to-CRM Deluge Task ---> Fee_Payments (Zoho CRM) ---> Rollup Balance Calculation
```

### Synchronization Highlights:
- **Realtime Pushes (CRM to Creator)**: Deluge workflow rules execute `zoho.creator.updateRecord` / `createRecord` whenever student profiles, daily attendance, marks, or fee records are saved in CRM.
- **Row-Level Parent Access Control**: Parents sign into Zoho Creator using their email address. Creator views enforce the criteria:
  ```deluge
  Parent_Email == zoho.loginuserid
  ```
  This prevents cross-parent data leakage and guarantees complete privacy.
- **Bi-Directional Action Pushes (Creator to CRM)**: When a parent submits a payment receipt in Creator, a Creator Deluge script pushes a `Fee_Payments` record directly into CRM via API.

---

## 4. Details of the Additional Feature Implemented

### Feature Title: **Proactive Student Risk & Automated Parent Early Warning Engine**

#### 4.1. Problem Identified
Traditional school management systems are **reactive**. Administrators and parents typically discover that a student is failing, chronically absent, or defaulting on fees only at the end of the term during report card generation or final audit. This leads to high student dropouts, poor learning outcomes, and delayed school cash flows.

#### 4.2. Why We Selected This Solution
Proactive automated intervention early in the academic term transforms outcomes. By dynamically evaluating student health metrics daily across attendance, grades, and fee schedules, the school can alert parents before a minor issue becomes an unrecoverable failure.

#### 4.3. Technical Implementation & Deluge Code Architecture
- **Location**: [`crm/deluge/06_additional_feature_risk_alert.deluge`](file:///D:/zoho-school-management-system/crm/deluge/06_additional_feature_risk_alert.deluge)
- **Algorithm**:
  1. Computes a dynamic **Student Health Score (0 - 100)**:
     - Deducts 30 points if Attendance < 75.0%.
     - Deducts 35 points if failing grade (`F`) recorded.
     - Deducts 25 points if Fee status is `Overdue`.
  2. Flags `At_Risk_Flag = true` in CRM when health score drops below 70 or any critical threshold is breached.
  3. Dispatches a responsive HTML email alert to parents containing an actionable portal link.
  4. Generates an executive daily "At-Risk Digest" for the Principal and Guidance Counselor.

#### 4.4. Optimization & Code Scalability
- **Bulk Record Search**: Uses optimized criteria queries (`Student_Status == 'Active'`) to minimize API calls.
- **Idempotent Execution**: Resets risk flags when student metrics normalize, avoiding redundant alerts.
- **Asynchronous Execution**: Runs as a scheduled background Deluge task to prevent blocking main UI looper operations.

---

## 5. Deluge Script Index

All production Deluge scripts are ready for deployment in the `crm/deluge/` and `creator/deluge_workflows/` directories:

| Script File | Target Module | Purpose |
| :--- | :--- | :--- |
| [`01_admission_lead_conversion.deluge`](file:///D:/zoho-school-management-system/crm/deluge/01_admission_lead_conversion.deluge) | Leads | Auto-converts Lead to Student, generates STU-YYYY-XXXX ID, creates Fee structure |
| [`02_attendance_validation_and_rollup.deluge`](file:///D:/zoho-school-management-system/crm/deluge/02_attendance_validation_and_rollup.deluge) | Attendance | Prevents duplicate daily entries & computes student attendance percentage |
| [`03_exam_result_calculator.deluge`](file:///D:/zoho-school-management-system/crm/deluge/03_exam_result_calculator.deluge) | Student_Marks | Validates marks, calculates %, computes letter grade (A+..F), and GPA rollup |
| [`04_fee_payment_tracker.deluge`](file:///D:/zoho-school-management-system/crm/deluge/04_fee_payment_tracker.deluge) | Fee_Payments | Recalculates collected amounts, outstanding balance, and payment status |
| [`05_crm_to_creator_sync.deluge`](file:///D:/zoho-school-management-system/crm/deluge/05_crm_to_creator_sync.deluge) | Students / CRM | Syncs CRM record updates to Zoho Creator parent portal in real-time |
| [`06_additional_feature_risk_alert.deluge`](file:///D:/zoho-school-management-system/crm/deluge/06_additional_feature_risk_alert.deluge) | Scheduled Task | Proactive Early Warning System & automated parent alert email dispatcher |
| [`parent_security_filter.deluge`](file:///D:/zoho-school-management-system/creator/deluge_workflows/parent_security_filter.deluge) | Zoho Creator | Enforces row-level access control (`zoho.loginuserid == Parent_Email`) |
| [`creator_to_crm_sync.deluge`](file:///D:/zoho-school-management-system/creator/deluge_workflows/creator_to_crm_sync.deluge) | Zoho Creator | Pushes parent payment submission back into Zoho CRM |

---

## 6. Summary Checklist of Assignment Requirements

- [x] **Zoho CRM Modules**: Custom modules for Students, Academic Structure, Attendance, Exams, Fees.
- [x] **Unique Student ID**: Automated generation of `STU-YYYY-XXXX`.
- [x] **Attendance Duplicate Prevention**: Composite unique key `Student_ID + Date`.
- [x] **Exam Calculator**: Grade calculation and class stats.
- [x] **Fee Installment Tracker**: Total fees, collected amount, balance, status.
- [x] **Zoho Creator Parent Application**: Profile, class, attendance, exams, fees, payment history.
- [x] **Data Isolation**: Row-level criteria filtering by `zoho.loginuserid`.
- [x] **CRM Webform**: Glassmorphism HTML5/CSS webform for Leads ingestion.
- [x] **CRM Reports & Dashboards**: Analytics specs for Admissions, Attendance, Exams, and Fees.
- [x] **Additional Feature**: Proactive Early Warning Risk & Parent Alert Engine.
- [x] **Documentation & Deliverables**: Architecture specs, Deluge script library, Creator specs, Setup guide, and Submission report.
