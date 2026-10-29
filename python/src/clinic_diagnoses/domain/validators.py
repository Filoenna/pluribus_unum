from datetime import date

from clinic_diagnoses.domain.result import Violation
from clinic_diagnoses.services.valueset import ValueSetIndex


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

def validate_icd_code(
        system: str, 
        icd_code: str,
        value_set_index: ValueSetIndex
) -> list[Violation]:
    if not value_set_index.is_valid(system, icd_code):
        violation = Violation(
            field="icd_code",
            code="invalid_icd_code",
            message="ICD-10 code is not valid for the specified coding system.",
        )
        return [violation]
    return []