# Zoho CRM Analytics, Reports & Dashboards Specification

## 1. Executive Overview
This specification details the comprehensive **Reports and Analytics Dashboards** configured in Zoho CRM for School Management Leadership (Principal, Vice-Principal, Admissions Director, Finance Head, and Academic Coordinators).

---

## 2. Dashboard 1: Admission & Enrolment Funnel

### Key Performance Indicators (KPI Widgets)
- **Total Admission Enquiries**: Count of records in `Leads` module for the active academic year.
- **Conversion Rate %**: `(Confirmed Admissions / Total Enquiries) * 100`.
- **Target vs. Admitted Students**: Comparison bar chart against grade capacities.

### Charts & Components
1. **Admission Funnel Chart**:
   - Stages: `Enquiry Received` -> `Document Verification` -> `Interview Scheduled` -> `Confirmed` / `Rejected`.
2. **Enquiries by Grade (Donut Chart)**:
   - Visual breakdown of applications across Grades 1 through 12.
3. **Monthly Enquiry Trend (Line Chart)**:
   - Tracks application volume month-over-month to optimize marketing campaigns.

---

## 3. Dashboard 2: Attendance & Student Risk Analytics

### Key Performance Indicators (KPI Widgets)
- **School Average Attendance Rate**: Aggregate percentage across all students.
- **At-Risk Attendance Count**: Number of active students with attendance < 75%.

### Charts & Components
1. **Class-Wise Average Attendance (Bar Chart)**:
   - Compares attendance percentages across Grade 1 to Grade 12.
2. **Daily Attendance Heatmap**:
   - Visual map highlighting high-absence days (e.g. Fridays/Mondays).
3. **At-Risk Attendance List View**:
   - Real-time tabular list filtering students with `< 75%` attendance, displaying student name, grade, parent contact details, and current percentage.

---

## 4. Dashboard 3: Academic & Exam Performance

### Key Performance Indicators (KPI Widgets)
- **School Average Percentage Score**: Cumulative average across all subjects and term exams.
- **Overall Pass Percentage**: Percentage of students passing all registered subjects.
- **Honor Roll Count**: Count of students achieving `A+` overall grade.

### Charts & Components
1. **Subject-Wise Class Performance (Grouped Column Chart)**:
   - Displays average score per subject across classes (e.g. Math vs Physics vs English).
2. **Grade Distribution Spectrum (Pie Chart)**:
   - Proportion of students scoring `A+`, `A`, `B`, `C`, and `F`.
3. **Failing Subjects Escalation List**:
   - Table of students scoring `< 40%` in any subject for targeted remedial classes.

---

## 5. Dashboard 4: Fee & Revenue Analytics

### Key Performance Indicators (KPI Widgets)
- **Total Revenue Target**: Sum of all `Total_Fee_Amount` in `Student_Fees`.
- **Total Revenue Collected**: Sum of all `Amount_Collected`.
- **Total Outstanding Revenue**: Sum of all `Outstanding_Balance`.
- **Collection Efficiency %**: `(Total Collected / Total Target) * 100`.

### Charts & Components
1. **Fee Collection Status (Donut Chart)**:
   - Distribution of students by status (`Paid`, `Partial`, `Overdue`, `Pending`).
2. **Outstanding Fee Aging Matrix**:
   - Categorizes pending payments: `< 30 Days Overdue`, `30-60 Days`, `60+ Days`.
3. **Defaulting Parent Contact List**:
   - Tabular view listing students with `Fee_Status == 'Overdue'`, parent phone number, and outstanding balance for automated call reminders.
