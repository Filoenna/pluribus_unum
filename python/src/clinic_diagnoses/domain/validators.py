from datetime import date

from clinic_diagnoses.domain.result import Violation


def validate_diagnosis_date(
    diagnosis_date: date,
    today: date,
) -> list[Violation]:
    if diagnosis_date > today:
        violation = Violation(
            field="diagnosis_date",
            code="future_date",
            message="Diagnosis date cannot be in the future.",
        )
        return [violation]
    return []