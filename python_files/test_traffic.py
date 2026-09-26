import unittest
import pandas as pd

from python_files.classes import (
    Violation, SpeedingViolation, ParkingViolation, SignalJumpViolation, Driver, InvalidViolationDataError
)

from python_files.analysis import (
    build_dataframe, validate_dataframe, summary_statistics, find_repeat_offenders
)

# TESTING FOR VIOLATIONS VALIDATION: purposely made the data incorrect to test errors
class TestViolations(unittest.TestCase):
    def test_valid_speeding_violation_created(self):
        violation = SpeedingViolation("D001", 250, 20, "Unpaid", 9)
        self.assertEqual(violation.driver_id, "D001")
        self.assertEqual(violation.violation_type(), "Speeding")

    def test_rejected_violation_with_empty_driver_id(self):
        with self.assertRaises(InvalidViolationDataError):
            ParkingViolation("", 150, "Paid", 3) # the driver ID is purposely left empty to test this

    def test_rejected_violation_with_negative_fine(self):
        with self.assertRaises(InvalidViolationDataError):
            ParkingViolation("D003", -50, "Unpaid", 5) # fine amount is purposely left as negative to test this

    def test_rejected_violation_with_invalid_payment_status(self):
        with self.assertRaises(InvalidViolationDataError):
            ParkingViolation("D002", 120, "Pending", 2) # the payment status is purposely left as Pending to test this

    def test_rejected_month_zero(self):
        with self.assertRaises(InvalidViolationDataError):
            ParkingViolation("D010", 100, "Paid", 0) # the month is purposely left as 0 to test this

    def test_rejected_month_thirteen(self):
        with self.assertRaises(InvalidViolationDataError):
            ParkingViolation("D007", 50, "Unpaid", 13) # the month is purposely left as 13 to test this

    def test_rejected_violation_with_negative_speed(self):
        with self.assertRaises(InvalidViolationDataError):
            SpeedingViolation("D005", 200, -10, "Paid", 8) # the speed over limit is purposely left as negative to test this

    def test_rejected_violation_with_non_numeric_fine(self):
        with self.assertRaises(InvalidViolationDataError):
            ParkingViolation("D004", "one hundred", "Unpaid", 10) # the fine amount is purposely left as non-numeric to test this

# TESTING INHERITANCE AND POLYMORPHISM
class TestInheritance(unittest.TestCase):
    def test_subclasses_are_violations(self):
        for violation_class, args in [
            (SpeedingViolation, ("D001", 250, 20, "Unpaid", 9)),
            (ParkingViolation, ("D001", 150, "Paid", 6)),
            (SignalJumpViolation, ("D001", 350, "Paid", 7)),
        ]:
            self.assertIsInstance(violation_class(*args), Violation)

    def test_violation_type_is_polymorphic(self):
        self.assertEqual(SpeedingViolation("D001", 250, 20, "Unpaid", 9).violation_type(), "Speeding")
        self.assertEqual(ParkingViolation("D001", 150, "Paid", 6).violation_type(), "Parking")
        self.assertEqual(SignalJumpViolation("D001", 350, "Paid", 7).violation_type(), "Signal Jump")

    def test_speeding_category_boundaries(self): # the categories are based on classes file
        self.assertEqual(SpeedingViolation("D001", 100, 9, "Paid", 6).speeding_category(), "Low")
        self.assertEqual(SpeedingViolation("D001", 100, 10, "Paid", 6).speeding_category(), "Medium")
        self.assertEqual(SpeedingViolation("D001", 100, 24, "Paid", 6).speeding_category(), "Medium")
        self.assertEqual(SpeedingViolation("D001", 100, 25, "Paid", 6).speeding_category(), "High")

    def test_non_speeding_has_zero_speed_in_dict(self): # checks whether non speeding violation are set to 0 speed over limit
        self.assertEqual(ParkingViolation("D001", 100, "Paid", 6).to_dict()["Speed Over Limit"], 0)

# TESTING FOR DRIVER CLASS
class TestDriver (unittest.TestCase):
    def setUp(self):
        self.driver = Driver("D001")
        self.driver.add_violation(SpeedingViolation("D001", 250, 20, "Unpaid", 9))
        self.driver.add_violation(ParkingViolation("D001", 150, "Paid", 6))

    def test_number_of_violations(self):
        self.assertEqual(self.driver.number_of_violations(), 2)

    def test_total_fines(self):
        self.assertEqual(self.driver.total_fines(), 400)

    def test_unpaid_fines_only(self):
        self.assertEqual(self.driver.unpaid_fines(), 250)

    def test_rejected_mismatched_driver_id(self):
        with self.assertRaises(InvalidViolationDataError):
            self.driver.add_violation(ParkingViolation("D696", 150, "Paid", 6))

    def test_rejected_non_violation_object(self):
        with self.assertRaises(TypeError):
            self.driver.add_violation("not a violation")

    def test_rejected_empty_driver_id(self):
        with self.assertRaises(InvalidViolationDataError):
            Driver("")

    def test_list_of_violations_returns_dicts(self):
        result = self.driver.list_of_violations()
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], dict)

# TESTING FOR ANALYSIS PIPELINE
class TestAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df, cls.drivers = build_dataframe()

    def test_minimum_of_fifty_records(self):
        self.assertGreaterEqual(len(self.df), 50)

    def test_all_required_columns_present(self):
        required = {"Driver ID", "Violation Type", "Fine Amount", "Speed Over Limit", 
                    "Number of Violations", "Payment Status", "Violation Month"}
        self.assertTrue(required.issubset(set(self.df.columns)))

    def test_dataframe_passed_validation(self):
        self.assertTrue(validate_dataframe(self.df))

    def test_no_negative_fines(self):
        self.assertFalse(self.df["Fine Amount"].lt(0).any())

    def test_months_within_range(self):
        self.assertTrue(self.df["Violation Month"].between(1, 12).all())

    def test_payment_status_value(self):
        self.assertTrue(set(self.df["Payment Status"].unique()).issubset({"Paid", "Unpaid"}))

    def test_summary_statistics(self):
        stats = summary_statistics(self.df)
        self.assertIn("Total number of records", stats)
        self.assertEqual(stats["Total number of records"], len(self.df))

    def test_total_fines_both_paid_and_unpaid(self):
        stats = summary_statistics(self.df)
        self.assertAlmostEqual(stats["Fines collected (Paid)"] + stats["Fines outstanding (Unpaid)"], stats["Total fines issued"], places=2)

    def test_repeat_offenders_meet_threshold(self):
        offenders = find_repeat_offenders(self.df, threshold=3)
        self.assertTrue((offenders >= 3).all())

# TEST DATAFRAME VALIDATION WHEN IT CATCHES CORRUPTED DATASETS
class TestDataFrameValidation(unittest.TestCase):

    def setUp(self):
        self.good = pd.DataFrame([{
            "Driver ID": f"D{i:03d}", "Violation Type": "Parking", "Fine Amount": 100, 
            "Speed Over Limit": 0, "Number of Violations": 1, "Payment Status": "Paid", 
            "Violation Month": 6,
        } for i in range(1, 52)])

    def test_good_dataframe_passes(self):
        self.assertTrue(validate_dataframe(self.good))

    def test_rejected_too_few_records(self):
        with self.assertRaises(InvalidViolationDataError):
            validate_dataframe(self.good.head(10))

    def test_rejected_missing_column(self):
        with self.assertRaises(InvalidViolationDataError):
            validate_dataframe(self.good.drop(columns=["Fine Amount"]))

    def test_rejected_negative_fine(self):
        bad = self.good.copy()
        bad.loc[0, "Fine Amount"] = -10
        with self.assertRaises(InvalidViolationDataError):
            validate_dataframe(bad)

    def test_rejected_invalid_month(self):
        bad = self.good.copy()
        bad.loc[0, "Violation Month"] = 13
        with self.assertRaises(InvalidViolationDataError):
            validate_dataframe(bad)

    def test_rejected_inconsistent_speed(self):
        bad = self.good.copy()
        bad.loc[0, "Speed Over Limit"] = 25
        with self.assertRaises(InvalidViolationDataError):
            validate_dataframe(bad)

if __name__ == "__main__":
    unittest.main(verbosity=2)