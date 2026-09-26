#!/usr/bin/env python
# coding: utf-8

# In[12]:


from python_files.classes import *

violations = [

    SpeedingViolation("D001", 67, 30, "Unpaid", 7),
    ParkingViolation("D001", 120, "Paid", 6),
    SignalJumpViolation("D001", 300, "Unpaid", 3),

    SpeedingViolation("D002", 180, 12, "Paid", 2),
    ParkingViolation("D002", 80, "Unpaid", 12),

    SignalJumpViolation("D003", 500, "Unpaid", 1),
    SpeedingViolation("D003", 220, 18, "Paid", 5),
    ParkingViolation("D003", 100, "Paid", 9),

    SpeedingViolation("D004", 250, 25, "Unpaid", 3),
    SignalJumpViolation("D004", 350, "Paid", 4),

    ParkingViolation("D005", 60, "Paid", 2),
    SpeedingViolation("D005", 150, 8, "Unpaid", 8),

    SignalJumpViolation("D006", 450, "Unpaid", 4),
    ParkingViolation("D006", 90, "Paid", 10),

    SpeedingViolation("D007", 300, 35, "Unpaid", 9),
    ParkingViolation("D007", 110, "Unpaid", 12),

    SignalJumpViolation("D008", 400, "Paid", 10),
    SpeedingViolation("D008", 175, 14, "Paid", 6),

    SpeedingViolation("D009", 120, 10, "Unpaid", 8),
    ParkingViolation("D009", 75, "Paid", 1),

    SpeedingViolation("D010", 500, 45, "Unpaid", 9),
    SignalJumpViolation("D010", 320, "Paid", 2),

    ParkingViolation("D011", 120, "Paid", 4),
    SpeedingViolation("D011", 210, 20, "Unpaid", 11),

    SignalJumpViolation("D012", 500, "Unpaid", 2),
    ParkingViolation("D012", 85, "Paid", 7),

    SpeedingViolation("D013", 200, 30, "Unpaid", 5),
    ParkingViolation("D013", 120, "Paid", 7),
    SignalJumpViolation("D013", 280, "Unpaid", 11),

    SignalJumpViolation("D014", 200, "Unpaid", 11),
    SpeedingViolation("D014", 140, 9, "Paid", 6),

    SpeedingViolation("D015", 400, 40, "Unpaid", 2),
    ParkingViolation("D015", 95, "Paid", 3),

    ParkingViolation("D016", 89, "Paid", 1),
    SignalJumpViolation("D016", 350, "Unpaid", 8),

    SignalJumpViolation("D017", 250, "Unpaid", 12),
    SpeedingViolation("D017", 160, 15, "Paid", 4),

    SpeedingViolation("D018", 275, 28, "Unpaid", 6),
    ParkingViolation("D018", 70, "Paid", 5),

    SignalJumpViolation("D019", 340, "Unpaid", 5),
    SpeedingViolation("D019", 190, 17, "Paid", 9),

    ParkingViolation("D020", 40, "Paid", 12),
    SignalJumpViolation("D020", 420, "Unpaid", 6),

    SpeedingViolation("D021", 330, 32, "Unpaid", 8),
    ParkingViolation("D021", 130, "Unpaid", 9),

    ParkingViolation("D022", 120, "Paid", 9),
    SignalJumpViolation("D022", 300, "Paid", 3),

    SignalJumpViolation("D023", 500, "Unpaid", 2),
    SpeedingViolation("D023", 230, 22, "Paid", 10),

    SpeedingViolation("D024", 350, 38, "Unpaid", 4),
    ParkingViolation("D024", 100, "Paid", 11),

]

def build_drivers_and_records(violation_list=None):
    if violation_list is None:
        violation_list = violations

    drivers: dict[str, Driver] = {}
    for v in violation_list:
        if v.driver_id not in drivers:
            drivers[v.driver_id] = Driver(v.driver_id)
        drivers[v.driver_id].add_violation(v)

    records = []
    for v in violation_list:
        row = v.to_dict()
        row["Number of Violations"] = drivers[v.driver_id].number_of_violations()
        records.append(row)

    return drivers, records


if __name__ == "__main__":
    drivers, records = build_drivers_and_records()
    print(f"Loaded {len(records)} violation records across {len(drivers)} drivers.")
    for r in records[:50]:
        print(r)


