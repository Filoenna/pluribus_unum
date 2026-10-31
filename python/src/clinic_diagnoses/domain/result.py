from dataclasses import dataclass
from typing import Generic, TypeVar

from clinic_diagnoses.domain.value_objects import SubmissionStatus


T = TypeVar("T")

@dataclass(frozen=True)
class Violation:
    field: str
    code: str
    message: str

@dataclass(frozen=True)
class RegistrationOutcome:
    diagnosis_id: int
    created: bool
    submission_status: SubmissionStatus

@dataclass(frozen=True)
class Success(Generic[T]):
    value: T

@dataclass(frozen=True)
class Failure:
    violations: tuple[Violation, ...]

Result = Success[T] | Failure
