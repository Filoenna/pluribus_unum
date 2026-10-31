import pytest

from dataclasses import FrozenInstanceError

from clinic_diagnoses.domain.result import RegistrationOutcome, Success
from clinic_diagnoses.domain.value_objects import SubmissionStatus

def test_create_registration_outcome():
    registration_outcome = RegistrationOutcome(
        diagnosis_id=7,
        created=True, 
        submission_status=SubmissionStatus.PENDING
    )
    assert registration_outcome.diagnosis_id == 7
    assert registration_outcome.created is True
    assert registration_outcome.submission_status is SubmissionStatus.PENDING

def test_registration_outcome_reassign_throws_frozen_instance_error():
    registration_outcome = RegistrationOutcome(
        diagnosis_id=7,
        created=True, 
        submission_status=SubmissionStatus.PENDING
    )
    with pytest.raises(FrozenInstanceError):
        registration_outcome.created = False

def test_registration_outcome_as_success():
    registration_outcome = RegistrationOutcome(
        diagnosis_id=7,
        created=True, 
        submission_status=SubmissionStatus.PENDING
    )
    success = Success(registration_outcome)
    assert success.value.diagnosis_id == 7
    assert success.value.created is True
    assert success.value.submission_status is SubmissionStatus.PENDING