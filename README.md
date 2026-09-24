# 🏫 Enterprise School Management System (Zoho CRM & Zoho Creator)

[![Zoho CRM](https://img.shields.io/badge/Zoho-CRM-blue.svg)](https://crm.zoho.com)
[![Zoho Creator](https://img.shields.io/badge/Zoho-Creator-orange.svg)](https://creator.zoho.com)
[![Language](https://img.shields.io/badge/Language-Deluge%20%7C%20HTML5%20%7C%20CSS3-green.svg)](#)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](#)

A comprehensive, scalable **School Management System** engineered using **Zoho CRM** (for school staff administration) and **Zoho Creator** (for parent-facing portal).

---

## 🌟 Executive Overview & Flow

```
[CRM Webform] ➔ [Leads Module] ➔ (Admission Confirmed) ➔ [Deluge Conversion] ➔ [Students Custom Module]
                                                                                      │
                                                                           (Bi-directional Sync)
                                                                                      ▼
[Parent Portal] ◄─── (Row-Level Security: Parent_Email == zoho.loginuserid) ◄─── [Zoho Creator App]
```

---

## 🚀 Key Features & Architectural Modules

### 1. Admissions Management & Automated Enrolment
- **Webform Ingestion**: Custom glassmorphism webform (`crm/webform/admission_webform.html`) capturing enquiries directly into Zoho CRM `Leads`.
- **Automated Conversion**: Deluge script (`01_admission_lead_conversion.deluge`) converts confirmed leads, generates sequential **`STU-YYYY-XXXX`** Student IDs, sets up initial fee structures, and dispatches parent welcome emails.

### 2. Academic Structure & Enrolment History
- **Normalized Mapping**: Modules for `Academic_Years`, `Classes`, `Sections`, `Subjects`, and `Teachers`.
- **Historical Progress**: `Student_Enrolments` records student progress across academic years.

### 3. Attendance Management & Duplicate Prevention
- **Unique Composite Key**: `Attendance_Key` (`Student_ID + Date`) blocks duplicate entries.
- **Rollup Percentages**: Automatically calculates student attendance percentages and flags `< 75%` attendance risk.

### 4. Examination & GPA Calculator
- **Score Validation**: Validates `Marks_Obtained <= Max_Marks`.
- **Grade Rollup**: Computes percentages, assigns letter grades (`A+`, `A`, `B`, `C`, `F`), Pass/Fail status, and updates cumulative GPA.

### 5. Fee & Multi-Installment Tracker
- **Financial Balance Logic**: Recalculates collected amounts and remaining balance across installments, updating payment status (`Paid`, `Partial`, `Overdue`).

### 6. Zoho Creator Parent Portal & Security
- **Row-Level Security**: Parents log into Zoho Creator with their email. Views enforce:
  ```deluge
  Parent_Email == zoho.loginuserid
  ```
  Guarantees complete data privacy between parents.
- **Bi-Directional Integration**: Pushes CRM updates to Creator and syncs parent payment uploads back to CRM.

### 7. Custom Feature: Proactive Early Warning Risk Engine
- **Automated Health Monitoring**: Evaluates attendance (< 75%), academic grades ('F'), and fee defaults daily.
- **Parent Alerts**: Dispatches automated HTML notifications with direct Creator portal resolution links.

---

## 📁 Repository Structure

```
.
├── crm/
│   ├── webform/
│   │   ├── admission_webform.html  # Responsive Admission Webform
│   │   ├── thank_you.html          # Confirmation redirect page
│   │   └── webform_styles.css     # Glassmorphism UI styling
│   └── deluge/
│       ├── 01_admission_lead_conversion.deluge       # Lead to Student conversion
│       ├── 02_attendance_validation_and_rollup.deluge  # Attendance validation & % rollup
│       ├── 03_exam_result_calculator.deluge           # Exam grade assignment & GPA
│       ├── 04_fee_payment_tracker.deluge              # Installments & balance tracker
│       ├── 05_crm_to_creator_sync.deluge              # Real-time sync to Creator
│       └── 06_additional_feature_risk_alert.deluge    # Proactive Risk Alert Engine
├── creator/
│   ├── application_structure.md                     # Creator forms & security spec
│   ├── deluge_workflows/
│   │   ├── parent_security_filter.deluge             # Parent security criteria
│   │   └── creator_to_crm_sync.deluge                # Creator payment sync to CRM
│   └── views/
│       └── parent_dashboard_widgets.html             # Custom HTML portal widgets
├── reports/
│   └── crm_dashboards_spec.md                         # KPI metrics & dashboard specifications
├── docs/
│   ├── ARCHITECTURE.md          # ER diagram & normalized module schemas
│   ├── SETUP_GUIDE.md           # Step-by-step setup & deployment guide
│   └── SUBMISSION_REPORT.md     # Official assignment submission report
└── test_deluge_logic.py          # Python unit test suite for business logic
```

---

## 🧪 Verification & Testing

Execute the local business logic test suite:
```bash
python test_deluge_logic.py
```
Output:
```text
[PASS] Test 1: Student ID format generated: STU-2026-1001
[PASS] Test 2: Attendance Unique Key generated: STU-2026-1001_20260923
[PASS] Test 3: Attendance Rollup: 94.44% (Normal) | 60.0% (Flagged At-Risk)
[PASS] Test 4: Marks Percentage: 88.33% -> Overall Grade: A
[PASS] Test 5: Fee Installment 1 Balance: Rs. 30000.0 (Partial) | Final Balance: Rs. 0.0 (Paid)
[PASS] Test 6: At-Risk Student Health Score computed: 35.0/100 (At-Risk Flagged: True)
```

---

## 📄 Submission Information
For detailed assignment submission reports and deployment steps, refer to [`docs/SUBMISSION_REPORT.md`](docs/SUBMISSION_REPORT.md) and [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md).
