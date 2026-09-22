#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Error handling
class InvalidViolationDataError(Exception):
    ""
    pass

# Superclass
class Violation:
  def __init__(self, driver_id, fine_amount, payment_status, violation_month):
    self.driver_id = driver_id
    self.fine_amount = fine_amount
    self.payment_status = payment_status
    self.violation_month = violation_month

    if not driver_id:
      raise InvalidViolationDataError("driver_id cannot be empty.")
    if not isinstance(fine_amount, (int, float)):
      raise InvalidViolationDataError(f"fine_amount must be a number, got {type(fine_amount).__name__}")
    if fine_amount < 0:
      raise InvalidViolationDataError("fine_amount cannot be negative.")
    if payment_status not in ["Paid", "Unpaid"]:
      raise InvalidViolationDataError(f"payment_status must be Paid or Unpaid, "f"got '{payment_status}'.")
    if not (1 <= violation_month <= 12):
      raise InvalidViolationDataError(f"violation_month must be between 1 and 12, got {violation_month}.")

  def get_violation_details(self):
    print("Driver ID: ", self.driver_id)
    print("Fine Amount: ", self.fine_amount)
    print("Payment Status: ", self.payment_status)
    print("Violation Month: ", self.violation_month)

  def to_dict(self):
    return {
        "Driver ID": self.driver_id,
        "Fine Amount": self.fine_amount,
        "Payment Status": self.payment_status,
        "Violation Month": self.violation_month,
        "Violation Type": self.violation_type(),
        "Speed Over Limit": getattr(self, "speed_over_limit", 0)

    }

# Subclass Speeding
class SpeedingViolation(Violation):
  def __init__(self, driver_id, fine_amount,speed_over_limit, payment_status, violation_month):
    super().__init__(driver_id, fine_amount, payment_status, violation_month)
    self.speed_over_limit = speed_over_limit

    if speed_over_limit < 0:
      raise InvalidViolationDataError("Speed over limit must be positive number")

  def violation_type(self):
    return "Speeding"

  def speeding_category(self):
    if self.speed_over_limit <10:
      return "Low"
    elif self.speed_over_limit <25:
      return "Medium"
    else:
      return "High"




# Subclass Parking
class ParkingViolation(Violation):

  def violation_type(self):
    return "Parking"

# Subclass Signal Jump 
class SignalJumpViolation(Violation):

  def violation_type(self):
    return "Signal Jump"


class Driver:
  def __init__(self, driver_id):
    if not driver_id:
      raise InvalidViolationDataError("Driver ID cannot be empty.")
    self.driver_id = driver_id
    self.violations: list[Violation] = []

  def add_violation(self, violation: Violation):
    if not isinstance(violation, Violation):
      raise TypeError("The input data is wrong/not completed")

    if violation.driver_id != self.driver_id:
      raise InvalidViolationDataError("Violation driver ID does not match this Driver's id.")
    self.violations.append(violation)

#  Calculate number of violations
  def number_of_violations(self) -> int:
    return len(self.violations)

#  Calculate total fines
  def total_fines(self) -> float:
    return sum(v.fine_amount for v in self.violations)

# Calculate unpaid fines
  def unpaid_fines(self) -> float:
    return sum(v.fine_amount for v in self.violations
      if v.payment_status == "Unpaid")

  def list_of_violations(self) -> list[dict]:
    return [v.to_dict() for v in self.violations]

  def __repr__(self):
    return (f"Driver({self.driver_id}, "f"violations={self.number_of_violations()}, "f"total_fines=${self.total_fines():.2f})")


