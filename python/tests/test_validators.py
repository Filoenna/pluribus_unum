from datetime import date
from clinic_diagnoses.domain.validators import validate_diagnosis_date

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
