from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager

from pathlib import Path

from clinic_diagnoses.services.valueset import load_value_set_index, ValueSetIndex
from clinic_diagnoses.dependencies import get_value_set_index


VALUE_SET_PATH = Path(__file__).resolve().parent.parent.parent.parent / "icd10_value_set.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.value_set_index = load_value_set_index(VALUE_SET_PATH)
    yield
    app.state.value_set_index = None

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root(value_set_index: ValueSetIndex = Depends(get_value_set_index)):
    return {"message": value_set_index.display_for(system="http://hl7.org/fhir/sid/icd-10", code="K21.0")}