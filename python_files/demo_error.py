from python_files.classes import ParkingViolation, SpeedingViolation, InvalidViolationDataError

try:
    ParkingViolation("D999", -50, "Paid", 5)
except InvalidViolationDataError as e:
    print(f"Rejected as expected: {e}")