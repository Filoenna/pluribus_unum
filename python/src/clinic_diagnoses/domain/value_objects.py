from dataclasses import dataclass
from datetime import date
from enum import StrEnum

class SourceSystem(StrEnum):
    SYS_A = "SYS_A"
    SYS_B = "SYS_B"

class ClinicalStatus(StrEnum):
    ACTIVE = "active"
    CURED = "cured"
    RECURRENCE = "recurrence"

class ConfirmationDegree(StrEnum):
    SUSPECTED = "suspected"
    CONFIRMED = "confirmed"

class SubmissionStatus(StrEnum):
    SENT = "sent"
    FAILED = "failed"
    PENDING = "pending"

@dataclass(frozen=True)
class OnsetAsDate:
    date: date

@dataclass(frozen=True)
class OnsetAsAge:
    age: int

Onset = OnsetAsDate | OnsetAsAge