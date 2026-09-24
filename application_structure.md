# Zoho Creator Parent Portal Application Structure

## 1. Application Overview
The **Parent Portal Application** in Zoho Creator is a secure, responsive, parent-facing web application that provides real-time access to student profiles, attendance registers, report cards, fee schedules, and online payment submissions.

---

## 2. Forms & Data Models in Zoho Creator

### 2.1. Form: `Student_Profile`
*Synced automatically from Zoho CRM `Students` Module*

- `Student_ID`: Single Line (Key, Unique)
- `Full_Name`: Single Line
- `Parent_Email`: Email (Used for `zoho.loginuserid` security criteria)
- `Parent_Phone`: Phone
- `Current_Class`: Single Line
- `Current_Section`: Single Line
- `Attendance_Percentage`: Decimal
- `Overall_Grade`: Single Line (`A+`, `A`, `B`, `C`, `F`)
- `Fee_Status`: Single Line (`Paid`, `Partial`, `Overdue`)
- `Outstanding_Balance`: Currency

---

### 2.2. Form: `Attendance_Log`
*Synced from Zoho CRM `Attendance` Module*

- `Student_ID`: Single Line
- `Parent_Email`: Email
- `Attendance_Date`: Date
- `Status`: Picklist (`Present`, `Absent`, `Late`, `Excused`)
- `Subject`: Single Line
- `Teacher_Notes`: Multi-line Text

---

### 2.3. Form: `Academic_Report_Card`
*Synced from Zoho CRM `Student_Marks` Module*

- `Student_ID`: Single Line
- `Parent_Email`: Email
- `Exam_Name`: Single Line
- `Subject`: Single Line
- `Marks_Obtained`: Decimal
- `Max_Marks`: Decimal
- `Percentage`: Decimal
- `Grade`: Single Line
- `Pass_Status`: Single Line (`Pass`, `Fail`)

---

### 2.4. Form: `Parent_Fee_Payments`
*Parent-facing Payment Submission Form*

- `Student_ID`: Lookup to `Student_Profile`
- `Parent_Email`: Email (Auto-filled with `zoho.loginuserid`)
- `Payment_Amount`: Currency
- `Payment_Method`: Picklist (`Credit Card`, `UPI`, `Bank Transfer`)
- `Transaction_Ref_ID`: Single Line
- `Payment_Date`: Date (Default: Today)
- `Payment_Receipt_File`: File Upload
- `Status`: Picklist (`Submitted`, `Verified`, `Rejected`)

---

## 3. Views & Custom Pages

1. **My Child Dashboard**: Executive view showing Student Profile Card, Attendance %, GPA gauge, and Fee status badge.
2. **Attendance Register View**: Detailed month-by-month grid with color-coded status badges (Green = Present, Red = Absent, Yellow = Late).
3. **Report Card Portal**: Tabular view grouped by Exam Terms with downloadable PDF report card action button.
4. **Fee & Payment History View**: Itemized installment timeline showing Total Fee, Paid Amount, Balance Remaining, and "Pay Now" trigger form.

---

## 4. Row-Level Security Strategy

Zoho Creator enforces complete data isolation between parents using **On Load Criteria**:

```deluge
// Applied on all Reports & Custom Page Widgets
Criteria: Parent_Email == zoho.loginuserid
```

This guarantees that a logged-in parent can **ONLY** view, inspect, or query records where the parent email matches their verified Zoho account login ID (`zoho.loginuserid`).
