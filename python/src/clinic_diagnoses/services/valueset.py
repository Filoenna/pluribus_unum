from clinic_diagnoses.schemas.valueset import ValueSet, FlattenedConcept

from pathlib import Path

def load_value_set_index(path: Path) -> ValueSetIndex:
    value_set = ValueSet.model_validate_json(path.read_text(encoding="utf-8"))
    return ValueSetIndex(value_set=value_set)


class ValueSetIndex:
    def __init__(self, value_set: ValueSet):
        self._by_key: dict[tuple[str, str], FlattenedConcept] = {
            (concept.system, concept.code): concept
            for concept in value_set.expansion.contains
        }
        self._value_set = value_set

    def lookup(self, system: str, code: str) -> FlattenedConcept | None:
        return self._by_key.get((system, code))

    def is_valid(self, system: str, code: str) -> bool:
        concept = self.lookup(system, code)
        return concept is not None and not concept.inactive

    def display_for(self, system: str, code: str) -> str | None:
        concept = self.lookup(system, code)
        return concept.display if concept else None

    @property
    def value_set(self) -> ValueSet:
        return self._value_set

