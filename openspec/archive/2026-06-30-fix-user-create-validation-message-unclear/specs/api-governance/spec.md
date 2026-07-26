---
change_id: fix-user-create-validation-message-unclear
capability: api-governance
created_at: 2026-06-30 18:35:35
updated_at: 2026-06-30 18:35:35
---

## MODIFIED Requirements

### Requirement: Unified response envelope

All public JSON APIs MUST return a unified envelope `{ code, message, data }` for success and error responses documented in `docs/standards/api-governance.md`. Request body validation errors that are returned to Web clients MUST also use this envelope, instead of exposing a raw framework-default error body as the only response structure.

#### Scenario: Successful JSON response shape

- **WHEN** a public API returns HTTP 2xx with a JSON body
- **THEN** the body MUST include `code`, `message`, and `data` fields
- **AND** `code` MUST be `0` or the documented success code for the endpoint family

#### Scenario: Error JSON response shape

- **WHEN** a public API returns HTTP 4xx or 5xx with a JSON body
- **THEN** the body MUST include `code`, `message`, and MAY include `data` as null or error detail
- **AND** `code` MUST match a registered business or auth error code

#### Scenario: Request validation error response shape

- **WHEN** a Web client submits an invalid JSON request body to a public API
- **THEN** the response body MUST include `code`, `message`, and `data`
- **AND** `message` MUST be suitable for display or mapping by the Web client
- **AND** the response body MUST NOT only expose FastAPI/Pydantic default `detail` as the user-facing error contract

#### Scenario: User create username validation response

- **WHEN** `POST /api/v1/admin/users` receives `username="abc"`
- **THEN** the response MUST follow the unified envelope
- **AND** the response message MUST identify the username length problem
