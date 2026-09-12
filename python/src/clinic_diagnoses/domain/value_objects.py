from dataclasses import dataclass
from datetime import date
from enum import Enum

class SourceSystem(Enum):
    SYS_A = "SYS_A"
    SYS_B = "SYS_B"

class ClinicalStatus(Enum):
    ACTIVE = "active"
    CURED = "cured"
    RECURRENCE = "recurrence"

class ConfirmationDegree(Enum):
    SUSPECTED = "suspected"
    CONFIRMED = "confirmed"

@dataclass(frozen=True)
class OnsetAsDate:
    date: date

@dataclass(frozen=True)
class OnsetAsAge:
    age: int


Onset = OnsetAsDate | OnsetAsAge