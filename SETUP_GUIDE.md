# Step-by-Step Deployment & Configuration Guide

Follow these sequential steps to configure the **School Management System** in a Zoho One trial instance or standalone Zoho CRM + Zoho Creator account.

---

## 1. Zoho CRM Setup

### Step 1.1: Create Custom Modules
Navigate to **Zoho CRM Setup > Customization > Modules and Fields**. Click **+ New Module** for each of the following:

1. **Students**
   - Mandatory Fields: `Name` (Single Line), `Student_ID` (Single Line, Unique), `Parent_Name` (Single Line), `Parent_Email` (Email), `Parent_Phone` (Phone), `Academic_Year` (Lookup), `Class` (Lookup), `Section` (Lookup), `Date_of_Birth` (Date), `Enrollment_Date` (Date), `Student_Status` (Picklist: `Active`, `Graduated`, `Withdrawn`), `Attendance_Percentage` (Percent), `Overall_Grade` (Picklist), `Fee_Status` (Picklist).
2. **Academic_Years**
   - Fields: `Name` (Single Line), `Start_Date` (Date), `End_Date` (Date), `Is_Current` (Checkbox).
3. **Classes**
   - Fields: `Name` (Single Line), `Code` (Single Line).
4. **Sections**
   - Fields: `Name` (Single Line), `Class` (Lookup to `Classes`), `Class_Teacher` (Single Line).
5. **Subjects**
   - Fields: `Name` (Single Line), `Code` (Single Line), `Class` (Lookup to `Classes`).
6. **Attendance**
   - Fields: `Name` (Single Line), `Student` (Lookup to `Students`), `Attendance_Date` (Date), `Status` (Picklist: `Present`, `Absent`, `Late`, `Excused`), `Attendance_Key` (Single Line, Unique).
7. **Student_Marks**
   - Fields: `Name` (Single Line), `Student` (Lookup to `Students`), `Examination` (Single Line), `Subject` (Lookup to `Subjects`), `Marks_Obtained` (Decimal), `Max_Marks` (Decimal), `Percentage` (Percent), `Grade` (Picklist), `Result_Status` (Picklist).
8. **Student_Fees**
   - Fields: `Name` (Single Line), `Student` (Lookup to `Students`), `Academic_Year` (Lookup to `Academic_Years`), `Total_Fee_Amount` (Currency), `Amount_Collected` (Currency), `Outstanding_Balance` (Currency), `Fee_Status` (Picklist: `Paid`, `Partial`, `Overdue`), `Due_Date` (Date).
9. **Fee_Payments**
   - Fields: `Name` (Single Line), `Student_Fee` (Lookup to `Student_Fees`), `Student` (Lookup to `Students`), `Amount_Paid` (Currency), `Payment_Method` (Picklist), `Transaction_ID` (Single Line), `Payment_Date` (Date).

---

### Step 1.2: Install Deluge Automation Scripts
Navigate to **Zoho CRM Setup > Developer Space > Functions**. Click **+ New Function**:

1. **`01_admission_lead_conversion`**:
   - Trigger: Workflow Rule on `Leads` module when `Admission_Status == 'Confirmed'`.
   - Copy code from `crm/deluge/01_admission_lead_conversion.deluge`.
2. **`02_attendance_validation_and_rollup`**:
   - Trigger: Workflow Rule on `Attendance` on record creation/edit.
   - Copy code from `crm/deluge/02_attendance_validation_and_rollup.deluge`.
3. **`03_exam_result_calculator`**:
   - Trigger: Workflow Rule on `Student_Marks` on record creation/edit.
   - Copy code from `crm/deluge/03_exam_result_calculator.deluge`.
4. **`04_fee_payment_tracker`**:
   - Trigger: Workflow Rule on `Fee_Payments` on record creation/edit.
   - Copy code from `crm/deluge/04_fee_payment_tracker.deluge`.
5. **`05_crm_to_creator_sync`**:
   - Trigger: Workflow Rule on `Students` on record creation/edit.
   - Copy code from `crm/deluge/05_crm_to_creator_sync.deluge`.
6. **`06_additional_feature_risk_alert`**:
   - Trigger: Scheduled Function (Daily at 08:00 AM).
   - Copy code from `crm/deluge/06_additional_feature_risk_alert.deluge`.

---

### Step 1.3: Webform Deployment
1. Go to **Zoho CRM Setup > Developer Space > Webforms**.
2. Select `Leads` module and generate form HTML.
3. Open `crm/webform/admission_webform.html`.
4. Replace `YOUR_ZOHO_CRM_WEB_FORM_ENCRYPTED_ID_HERE` (`xnQsjsdp`) and `YOUR_ZOHO_CRM_WEB_FORM_ACTION_KEY_HERE` (`xmMsjsdp`) with your generated Zoho credentials.
5. Embed or open `admission_webform.html` in your browser.

---

## 2. Zoho Creator Parent Application Setup

1. Log into **Zoho Creator** (`creator.zoho.com`).
2. Click **Create Application > Create from Scratch**. Name: `Parent Portal`.
3. Create Forms: `Student_Profile`, `Attendance_Log`, `Academic_Report_Card`, `Parent_Fee_Payments` according to `creator/application_structure.md`.
4. Navigate to **Workflows > Form Workflows > On Load**:
   - Add Deluge filter script from `creator/deluge_workflows/parent_security_filter.deluge`.
5. Navigate to **Workflows > Form Workflows > On Success (Parent_Fee_Payments)**:
   - Add Deluge sync script from `creator/deluge_workflows/creator_to_crm_sync.deluge`.
6. Create a Custom Page **My Child Dashboard**:
   - Embed HTML widget from `creator/views/parent_dashboard_widgets.html`.

---

## 3. Analytics & Dashboard Setup
1. In Zoho CRM, go to **Analytics**.
2. Create Dashboards:
   - Admissions Funnel
   - Attendance & Risk Dashboard
   - Academic Performance Dashboard
   - Fee Collection & Financial Analytics
3. Follow layout configurations specified in `reports/crm_dashboards_spec.md`.
