from pydantic import BaseModel

class Concept(BaseModel):
    code: str
    display: str

class FlattenedConcept(Concept):
    system: str
    inactive: bool = False

class Include(BaseModel):
    system: str
    concept: list[Concept]

class Compose(BaseModel):
    include: list[Include]

class Expansion(BaseModel):
    identifier: str
    timestamp: str
    total: int
    contains: list[FlattenedConcept]

class ValueSet(BaseModel):
    resourceType: str
    id: str
    url: str
    version: str
    name: str
    title: str
    status: str
    experimental: bool
    description: str
    compose: Compose
    expansion: Expansion