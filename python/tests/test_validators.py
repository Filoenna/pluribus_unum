import pytest

from datetime import date

from clinic_diagnoses.domain.validators import validate_diagnosis_date, validate_icd_code
from clinic_diagnoses.services.valueset import ValueSetIndex
from clinic_diagnoses.schemas.valueset import ValueSet


# =================== TEST DATE VALIDATION ===============
def test_empty_list_for_past_diagnosis_date():
    today = date(2026, 10, 29)
    diagnosis_date = date(2026, 10, 28)  # A date in the past
    result = validate_diagnosis_date(diagnosis_date, today)
    assert result == []

def test_empty_list_for_today_diagnosis_date():
    today = date(2026, 10, 29)
    diagnosis_date = today  # Today's date
    result = validate_diagnosis_date(diagnosis_date, today)
    assert result == []

def test_single_violation_for_future_diagnosis_date():
    today = date(2026, 10, 29)
    diagnosis_date = date(2026, 10, 30)  # A date in the future
    result = validate_diagnosis_date(diagnosis_date, today)
    assert len(result) == 1
    assert result[0].field == "diagnosis_date"
    assert result[0].code == "future_date"
    assert result[0].message == "Diagnosis date cannot be in the future."

def test_single_violation_for_future_year():
    today = date(2026, 10, 29)
    diagnosis_date = date(2027, 1, 1)  # A date in the future year
    result = validate_diagnosis_date(diagnosis_date, today)
    assert len(result) == 1
    assert result[0].field == "diagnosis_date"
    assert result[0].code == "future_date"
    assert result[0].message == "Diagnosis date cannot be in the future."

# =================== TEST ICD10 VALIDATION ===============

ICD10_SYSTEM = "http://hl7.org/fhir/sid/icd-10"
OTHER_SYSTEM = "http://snomed.info/sct"

@pytest.fixture
def index() -> ValueSetIndex:
    value_set = ValueSet.model_validate(
        {
            "resourceType": "ValueSet",
            "id": "test",
            "url": "urn:test:valueset",
            "version": "1.0.0",
            "name": "TestValueSet",
            "title": "Test ValueSet",
            "status": "active",
            "experimental": True,
            "description": "fixture data for tests",
            "compose": {"include": []},
            "expansion": {
                "identifier": "urn:uuid:test",
                "timestamp": "2026-01-01T00:00:00Z",
                "total": 2,
                "contains": [
                    {"system": ICD10_SYSTEM, "code": "A00", "display": "Cholera"},
                    {"system": ICD10_SYSTEM, "code": "B00", "display": "Retired thing", "inactive": True},
                ],
            },
        }
    )

    return ValueSetIndex(value_set)

def test_empty_list_for_known_active_code(index):
    result = validate_icd_code(ICD10_SYSTEM, "A00", index)
    assert result == []

def test_single_violation_for_unknown_code(index):
    result = validate_icd_code(ICD10_SYSTEM, "C00", index)
    assert len(result) == 1
    assert result[0].field == "icd_code"
    assert result[0].code == "invalid_icd_code"
    assert result[0].message == "ICD-10 code is not valid for the specified coding system."

def test_single_violation_for_wrong_coding_system(index):
    result = validate_icd_code(OTHER_SYSTEM, "A00", index)
    assert len(result) == 1
    assert result[0].field == "icd_code"
    assert result[0].code == "invalid_icd_code"
    assert result[0].message == "ICD-10 code is not valid for the specified coding system."

def test_single_violation_for_inactive_code(index):
    result = validate_icd_code(ICD10_SYSTEM, "B00", index)
    assert len(result) == 1
    assert result[0].field == "icd_code"
    assert result[0].code == "invalid_icd_code"
    assert result[0].message == "ICD-10 code is not valid for the specified coding system."