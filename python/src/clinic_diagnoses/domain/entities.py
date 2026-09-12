from datetime import date
from dataclasses import dataclass

from clinic_diagnoses.domain.value_objects import SourceSystem, ClinicalStatus, ConfirmationDegree, Onset

@dataclass(frozen=True)
class Diagnosis:
    patient_id: str
    source_system: SourceSystem
    source_record_id: str
    icd10_code: str
    coding_system: str
    description: str
    diagnosis_date: date
    clinical_status: ClinicalStatus
    confirmation: ConfirmationDegree
    onset: Onset
    visit_id: str | None = None
    id: str | None = None
