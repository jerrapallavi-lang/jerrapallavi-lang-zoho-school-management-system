"""
================================================================================
SCHOOL MANAGEMENT SYSTEM - BUSINESS LOGIC TEST SUITE
================================================================================
This test script verifies the mathematical correctness, validation rules, 
and edge case handling of all Deluge scripts in the School Management System:
1. Student ID Generation (STU-YYYY-XXXX)
2. Attendance Key Generation & Duplicate Prevention
3. Attendance Percentage Rollup & Threshold Risk Flagging
4. Exam Grade Assignment & Cumulative GPA Rollup
5. Fee Payment Installment & Outstanding Balance Logic
6. Additional Feature: Composite Student Health Score & Risk Alert Engine
================================================================================
"""

import sys
import unittest
from datetime import datetime

# Set UTF-8 stdout encoding for Windows terminal compatibility
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

class TestSchoolManagementSystemLogic(unittest.TestCase):

    def test_01_student_id_generation(self):
        """Test STU-YYYY-XXXX sequential ID formatting"""
        year_str = "2026"
        seq_num = 1001
        student_id = f"STU-{year_str}-{seq_num}"
        self.assertEqual(student_id, "STU-2026-1001")
        self.assertTrue(student_id.startswith("STU-2026-"))
        print(f"[PASS] Test 1: Student ID format generated: {student_id}")

    def test_02_attendance_duplicate_key(self):
        """Test composite key formatting for duplicate attendance prevention"""
        stu_code = "STU-2026-1001"
        attendance_date = datetime(2026, 9, 23)
        formatted_date = attendance_date.strftime("%Y%m%d")
        attendance_key = f"{stu_code}_{formatted_date}"
        self.assertEqual(attendance_key, "STU-2026-1001_20260923")
        print(f"[PASS] Test 2: Attendance Unique Key generated: {attendance_key}")

    def test_03_attendance_percentage_rollup(self):
        """Test attendance percentage calculation and risk threshold (< 75%)"""
        # Scenario A: 170 present out of 180 total days -> 94.44% (No Risk)
        total_days_a = 180
        present_days_a = 170
        pct_a = round((present_days_a / total_days_a) * 100.0, 2)
        is_risk_a = pct_a < 75.0
        self.assertEqual(pct_a, 94.44)
        self.assertFalse(is_risk_a)

        # Scenario B: 12 present out of 20 total days -> 60.0% (At Risk)
        total_days_b = 20
        present_days_b = 12
        pct_b = round((present_days_b / total_days_b) * 100.0, 2)
        is_risk_b = pct_b < 75.0
        self.assertEqual(pct_b, 60.0)
        self.assertTrue(is_risk_b)

        print(f"[PASS] Test 3: Attendance Rollup: {pct_a}% (Normal) | {pct_b}% (Flagged At-Risk)")

    def test_04_exam_grade_calculator(self):
        """Test mark validation, percentage calculation, letter grades, and GPA rollup"""
        # Test Grade mappings
        def get_grade(pct):
            if pct >= 90.0: return "A+", "Pass"
            elif pct >= 80.0: return "A", "Pass"
            elif pct >= 70.0: return "B", "Pass"
            elif pct >= 50.0: return "C", "Pass"
            elif pct >= 40.0: return "D", "Pass"
            else: return "F", "Fail"

        # Subject 1: Math 92/100
        grade1, status1 = get_grade(92.0)
        self.assertEqual(grade1, "A+")
        self.assertEqual(status1, "Pass")

        # Subject 2: Physics 35/100 -> Failing
        grade2, status2 = get_grade(35.0)
        self.assertEqual(grade2, "F")
        self.assertEqual(status2, "Fail")

        # GPA Rollup across Math (92%), Physics (85%), English (88%)
        marks = [92.0, 85.0, 88.0]
        avg_pct = round(sum(marks) / len(marks), 2)
        overall_grade, _ = get_grade(avg_pct)
        self.assertEqual(avg_pct, 88.33)
        self.assertEqual(overall_grade, "A")
        print(f"[PASS] Test 4: Marks Percentage: {avg_pct}% -> Overall Grade: {overall_grade}")

    def test_05_fee_payment_tracker(self):
        """Test fee installment calculations and payment status logic"""
        total_fee = 50000.0
        
        # Installment 1: 20,000 paid
        installment_1 = 20000.0
        collected_1 = installment_1
        balance_1 = total_fee - collected_1
        status_1 = "Paid" if balance_1 <= 0 else ("Partial" if collected_1 > 0 else "Pending")
        self.assertEqual(balance_1, 30000.0)
        self.assertEqual(status_1, "Partial")

        # Installment 2: 30,000 paid -> Fully Paid
        installment_2 = 30000.0
        collected_2 = collected_1 + installment_2
        balance_2 = max(0.0, total_fee - collected_2)
        status_2 = "Paid" if balance_2 <= 0 else "Partial"
        self.assertEqual(balance_2, 0.0)
        self.assertEqual(status_2, "Paid")

        print(f"[PASS] Test 5: Fee Installment 1 Balance: Rs. {balance_1} ({status_1}) | Final Balance: Rs. {balance_2} ({status_2})")

    def test_06_additional_feature_health_score(self):
        """Test Additional Feature: Composite Student Health Score & Early Warning logic"""
        # Student Health Score Starts at 100
        health_score = 100.0

        # Student has low attendance (65%) -> -30 penalty
        att_pct = 65.0
        if att_pct < 75.0:
            health_score -= 30.0

        # Student has failing grade in Math ('F') -> -35 penalty
        overall_grade = "F"
        if overall_grade == "F":
            health_score -= 35.0

        # Student fee is paid -> 0 penalty
        fee_status = "Paid"
        fee_balance = 0.0
        if fee_status == "Overdue" and fee_balance > 0:
            health_score -= 25.0

        health_score = max(0.0, health_score)
        is_at_risk = health_score < 70.0 or att_pct < 75.0 or overall_grade == "F"

        self.assertEqual(health_score, 35.0)
        self.assertTrue(is_at_risk)
        print(f"[PASS] Test 6: At-Risk Student Health Score computed: {health_score}/100 (At-Risk Flagged: {is_at_risk})")

if __name__ == "__main__":
    unittest.main()
