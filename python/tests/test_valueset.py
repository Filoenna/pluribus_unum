import pytest

from clinic_diagnoses.services.valueset import ValueSetIndex
from clinic_diagnoses.schemas.valueset import ValueSet

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

def test_is_valid_true_for_known_active_code(index):
    assert index.is_valid(ICD10_SYSTEM, "A00") is True

def test_is_valid_false_for_unknown_code(index):
    assert index.is_valid(ICD10_SYSTEM, "C00") is False

def test_is_valid_false_for_wrong_system(index):
    assert index.is_valid(OTHER_SYSTEM, "A00") is False

def test_is_valid_false_for_inactive_code(index):
    assert index.is_valid(ICD10_SYSTEM, "B00") is False

def test_lookup_returns_none_for_unknown_code(index):
    assert index.lookup(ICD10_SYSTEM, "C00") is None

def test_lookup_returns_concept_for_active_code(index):
    concept = index.lookup(ICD10_SYSTEM, "A00")
    assert concept.system == ICD10_SYSTEM
    assert concept.code == "A00"
    assert concept.display == "Cholera"
    assert concept.inactive is False

def test_lookup_returns_concept_for_inactive_code(index):
    concept = index.lookup(ICD10_SYSTEM, "B00")
    assert concept.system == ICD10_SYSTEM
    assert concept.code == "B00"
    assert concept.display == "Retired thing"
    assert concept.inactive is True

def test_display_for_active_code(index):
    assert index.display_for(ICD10_SYSTEM, "A00") == "Cholera"

def test_display_for_inactive_code(index):
    assert index.display_for(ICD10_SYSTEM, "B00") == "Retired thing"

def test_display_for_none_for_unknown_code(index):
    assert index.display_for(ICD10_SYSTEM, "C00") is None

def test_value_set_property_is_readable(index):
    assert isinstance(index.value_set, ValueSet)

def test_value_set_property_raises_on_assignment(index):
    with pytest.raises(AttributeError):
        index.value_set = None
