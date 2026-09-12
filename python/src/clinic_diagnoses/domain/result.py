from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")

@dataclass(frozen=True)
class Violation:
    field: str
    code: str
    message: str

@dataclass(frozen=True)
class Success(Generic[T]):
    value: T

@dataclass(frozen=True)
class Failure:
    violations: tuple[Violation, ...]

Result = Success[T] | Failure
