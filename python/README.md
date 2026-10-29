After cloning repo, start with:
uv sync

Start the server with:
uv run fastapi dev src/clinic_diagnoses/main.py

# Architecture Notes — Clinic Diagnoses API

## 1. General approach

The application registers patient diagnoses, validates business rules, stores diagnoses locally, and submits them to an external registry.

The architecture should prioritize:

- Separation of responsibilities (SRP).
- Explicit business results instead of exceptions for expected validation failures.
- Aggregation of independent validation errors.
- Idempotent diagnosis registration.
- Reliable persistence and observable external submission status.
- Simplicity — avoid unnecessary infrastructure.

## 2. Diagnosis registration flow

```text
register_diagnosis(request)
    |
    +-- Check whether the source diagnosis already exists
    |     |
    |     +-- Same data → Success(existing diagnosis)
    |     |
    |     +-- Different data → Conflict(differing fields)
    |
    +-- Resolve patient
    |
    +-- Validate diagnosis
    |     +-- Validate diagnosis date
    |     +-- Validate ICD-10 code and coding system
    |     +-- Validate other diagnosis fields
    |
    +-- Collect all independent validation violations
    |     |
    |     +-- Violations found → Failure(violations)
    |
    +-- Save diagnosis locally with PENDING submission status
    |
    +-- Submit diagnosis to external registry
    |     +-- Retry transient failures (up to 3 attempts)
    |     +-- Persist submission status
    |
    +-- Success(new diagnosis)
```

The local diagnosis must remain saved even if external submission fails.

## 3. Validation responsibilities

Keep validation functions small and focused:

- `resolve_patient()` — identify the patient using PESEL or a source-scoped medical record number.
- `validate_diagnosis()` — coordinate diagnosis-specific validation.
- `validate_date()` — reject future diagnosis dates.
- `validate_icd()` — verify the code and coding system against the local ValueSet.
- Other validators — handle clinical status, confirmation status, onset and other applicable rules.

Independent violations should be collected using a simple list:

```python
errors = []
errors.extend(validate_diagnosis(...))
```

Return all collected violations together. Avoid stopping at the first validation failure unless further processing depends on missing or invalid data.

## 4. Business result model

Use explicit results at the application-service boundary:

```python
Result = Success[T] | Failure | Conflict
```

- `Success` — diagnosis created or an existing identical diagnosis found.
- `Failure` — one or more validation violations.
- `Conflict` — the same source diagnosis identifier refers to different data.

A successful registration outcome should include at least the diagnosis ID and whether a new record was created.

Suggested REST mapping:

| Business result | HTTP response |
|---|---|
| Newly created diagnosis | `201 Created` + `Location` |
| Existing identical diagnosis | `200 OK` |
| Validation failure | `400 Bad Request` + `application/problem+json` |
| Conflicting source diagnosis | `409 Conflict` |

The application service should not decide HTTP status codes. REST and GraphQL adapters translate business results into their respective response formats.

## 5. Idempotency and concurrency

A diagnosis is uniquely identified by:

```text
(source_system, source_record_id)
```

This is distinct from patient identification using:

```text
(source_system, medical_record_number)
```

Registration should first check whether the source diagnosis already exists.

However, checking before inserting is not sufficient to prevent concurrent duplicates.

Use a database `UNIQUE` constraint as the final safeguard. If insertion fails specifically because of this constraint, retrieve the existing diagnosis and determine whether the request is an identical duplicate or a conflict.

Do not rely on Python's GIL or an application-level lock for database consistency across processes.

## 6. External registry integration

Local persistence and external submission are separate operations.

Store the diagnosis and its initial submission state in the same database transaction.

Possible submission states:

```text
PENDING
SENT
FAILED
```

The submission mechanism should:

- Use HTTP to communicate with the mock registry.
- Retry transient failures up to three times, with pauses.
- Avoid retrying permanent validation errors such as HTTP 400.
- Persist the outcome of submission attempts.
- Keep failed submissions visible through the API.
- Allow pending work to be recovered after application restart.

For this project's scope, SQLite-backed submission state is preferable to introducing Kafka, RabbitMQ or Redis.

Repeated submissions may occur after crashes. A stable submission identifier and idempotency support in the receiving system are needed to prevent duplicate external registrations.

## 7. Open decisions and implementation notes

- **Conflicting duplicates:** Returning `409` when the source identifier matches but the diagnosis content differs is our proposed behavior, not an explicitly specified requirement.
- **Data comparison:** Compare normalized business values rather than raw JSON representations.
- **Recovery:** Decide whether startup recovery or a separate worker will process pending submissions.
- **Concurrency:** Define transaction boundaries and handle database errors precisely.
- **External idempotency:** The mock registry's specified behavior does not guarantee deduplication; do not assume it does.
- **Other API requirements:** Patient search, diagnosis listing with pagination/filtering, ICD-10 aggregation via SQL, clinical status transitions and GraphQL still need implementation.

## 8. Implementation strategy

Build incrementally:

1. Implement focused validation functions and tests.
2. Introduce the registration service with explicit business results.
3. Add local persistence and database uniqueness constraints.
4. Implement duplicate and conflict handling.
5. Integrate the external registry with retries and persisted submission status.
6. Implement the remaining REST and GraphQL operations.

**Guiding principle:** Implement the simplest reliable solution that satisfies the requirements. Introduce additional abstractions only when they solve a concrete problem.