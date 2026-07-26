## ADDED Requirements

### Requirement: API Request Logging
The system SHALL capture API request log summaries for operational troubleshooting and audit correlation.

#### Scenario: Request id is generated or propagated
- **WHEN** a client sends an API request without a request id
- **THEN** the system SHALL generate a request id for the request lifecycle
- **AND** the request log SHALL store that request id.

#### Scenario: Request summary is persisted
- **WHEN** an API request completes
- **THEN** the system SHALL persist method, path, status code, duration in milliseconds, request id, client type, actor context when available, summary, and creation time.

#### Scenario: Error request stores sanitized error context
- **WHEN** an API request fails with an application or server error
- **THEN** the request log SHALL store the status code, error code when available, error summary, request id, and sanitized metadata
- **AND** it SHALL NOT store raw secrets, passwords, authorization headers, cookies, or database connection strings.

#### Scenario: Noise routes are excluded by default
- **WHEN** a request targets health checks, static assets, Swagger/OpenAPI docs, or media passthrough routes
- **THEN** the system SHALL exclude the request from default request log capture.

### Requirement: Product Usage Event Collection
The system SHALL collect product usage events according to a human-defined event dictionary.

#### Scenario: Allowed event is accepted
- **WHEN** a client submits a usage event whose event name exists in the event dictionary and includes all required properties
- **THEN** the system SHALL validate the event
- **AND** persist it with server-derived user, role, client type, request id, timestamp, user agent summary, and IP summary.

#### Scenario: Unknown event is rejected
- **WHEN** a client submits a usage event whose event name is not defined in the event dictionary
- **THEN** the system SHALL reject the event with a documented validation error
- **AND** the rejection SHALL NOT interrupt the user's primary business workflow.

#### Scenario: Forbidden properties are blocked
- **WHEN** a usage event includes forbidden properties such as token, password, authorization, cookie, raw payload, or raw filename
- **THEN** the system SHALL reject or remove those properties before persistence according to the server-side validation policy
- **AND** it SHALL NOT trust frontend masking as the security boundary.

#### Scenario: MVP event dictionary is enforced
- **WHEN** implementation handles MVP events
- **THEN** it SHALL support at least page_view, search_submit, filter_change, detail_view, copy_request_id, entity_create, entity_update, entity_delete, status_change, media_upload, login_success, login_failed, and api_error.

#### Scenario: Web admin emits usage events
- **WHEN** an authenticated admin or employee opens any registered Web admin page
- **THEN** the Web client SHALL submit a `page_view` usage event through the shared tracking client with module, page path, route pattern, page title, entity type, and entity id.
- **WHEN** an authenticated admin changes log audit filters, runs a search, copies a request id, or opens a detail drawer
- **THEN** the Web client SHALL submit the corresponding interaction usage event through the shared tracking client
- **AND** tracking failures SHALL NOT block the visible user workflow.

### Requirement: Log Storage and Retention
The system SHALL store request logs and usage events in relational storage with queryable indexes and retention governance.

#### Scenario: Relational storage supports demo and production
- **WHEN** the app runs in local or Docker demo mode
- **THEN** logs SHALL be stored in SQLite-compatible schema
- **AND** when the app runs in production with MySQL
- **THEN** logs SHALL use MySQL-compatible schema without SQLite-only DDL.

#### Scenario: Common filters are indexed
- **WHEN** logs are queried by created time, log type, actor, request id, status code, or path
- **THEN** the system SHALL use indexed or otherwise optimized database access
- **AND** SHALL NOT load all logs into memory before filtering.

#### Scenario: Retention policy is defined
- **WHEN** log retention is evaluated
- **THEN** request logs and usage events SHALL follow the existing audit retention policy or an explicitly documented dedicated retention setting.

#### Scenario: Metadata remains displayable
- **WHEN** a log has metadata
- **THEN** the system SHALL store metadata as JSON or an equivalent parseable structure after masking and truncation
- **AND** if metadata parsing fails the list view SHALL still show the core log fields.

### Requirement: Admin Log Query API
The system SHALL provide admin-only APIs for log list and detail lookup.

#### Scenario: Admin queries log list
- **WHEN** an authenticated admin calls `GET /api/v1/admin/logs`
- **THEN** the system SHALL return a unified response containing paginated log items, total, page, page_size, and metric summary.

#### Scenario: Log list filters are supported
- **WHEN** an admin filters by log type, time range, actor, client type, status code or result, resource id, path, keyword, or request id
- **THEN** the system SHALL return only matching logs ordered by newest first.

#### Scenario: Admin queries log detail
- **WHEN** an authenticated admin calls `GET /api/v1/admin/logs/{id}` for an existing log
- **THEN** the system SHALL return detail sections for basic information, request information, actor and client, operation context, event properties, and metadata.

#### Scenario: Non-admin access is denied
- **WHEN** an employee, shop-owner client, miniapp user, or anonymous user calls an admin log API
- **THEN** the system SHALL deny access with the documented forbidden response.

#### Scenario: Missing log returns not found
- **WHEN** an admin requests a log id that does not exist
- **THEN** the system SHALL return a documented 404-class error response.

### Requirement: Usage Event Ingestion API
The system SHALL provide a usage event ingestion API for supported clients.

#### Scenario: Event ingestion succeeds
- **WHEN** a supported client posts a valid event to `POST /api/v1/usage-events`
- **THEN** the system SHALL persist the event
- **AND** return a unified success response without exposing internal storage details.

#### Scenario: Event ingestion validation fails
- **WHEN** a supported client posts an event with invalid property types, missing required fields, excessive length, or forbidden data
- **THEN** the system SHALL return a documented validation error
- **AND** the client integration SHALL treat the tracking failure as non-blocking for the primary user workflow.

#### Scenario: Anonymous boundary is controlled
- **WHEN** an anonymous client posts a usage event
- **THEN** the system SHALL accept it only for explicitly supported client types and event names
- **AND** it SHALL NOT collect sensitive personal information.

### Requirement: Admin Log Audit Page
The system SHALL provide a Web admin log audit page aligned with the product v2 Golden Reference.

#### Scenario: Admin opens log audit page
- **WHEN** an authenticated admin opens `/admin/logs`
- **THEN** the system SHALL render the log audit page inside the existing Admin Shell
- **AND** the SYSTEM sidebar SHALL show and activate `日志审计`.

#### Scenario: Metrics and filters are visible
- **WHEN** an admin views the log audit page
- **THEN** the page SHALL show TODAY LOGS, API ERRORS, SLOW REQUESTS, and SENSITIVE OPS metric cards
- **AND** it SHALL show filters for log type, time range, actor, status or result, resource or id, and path or request id.

#### Scenario: Log table supports troubleshooting
- **WHEN** an admin views log rows
- **THEN** the table SHALL show time, type, event or summary, actor, client, status or result, duration, request id, copy action, and detail action.

#### Scenario: Request id can be copied without layout shift
- **WHEN** an admin copies a request id
- **THEN** the system SHALL provide success or failure feedback using a fixed toast or equivalent non-layout-shifting feedback.

#### Scenario: Employee cannot open page
- **WHEN** an authenticated employee opens `/admin/logs`
- **THEN** the system SHALL show a forbidden state or redirect according to existing admin authorization patterns
- **AND** SHALL NOT expose log data.

### Requirement: Log Detail Drawer
The system SHALL display log detail in a right-side drawer without losing list context.

#### Scenario: Detail drawer opens
- **WHEN** an admin selects a log row detail action
- **THEN** the page SHALL open a right-side drawer while keeping the list context visible behind it.

#### Scenario: Detail sections match prototype
- **WHEN** the detail drawer is visible
- **THEN** it SHALL display grouped sections for basic information, request information, actor and client, operation context, event properties, and metadata JSON.

#### Scenario: Drawer closes
- **WHEN** the admin clicks close, clicks the backdrop, or presses Escape
- **THEN** the drawer SHALL close and preserve the current filters and pagination state.

#### Scenario: Metadata is masked and scrollable
- **WHEN** metadata is shown in the drawer
- **THEN** it SHALL use a monospace scrollable display
- **AND** sensitive fields SHALL be masked or omitted.

### Requirement: OpenAPI Orval and Documentation Governance
The system SHALL keep API, database, documentation, and generated client artifacts synchronized for product usage logging.

#### Scenario: API contract is generated
- **WHEN** backend log APIs are implemented or changed
- **THEN** OpenAPI SHALL expose response models, summaries, descriptions, and tags
- **AND** Orval SHALL generate the corresponding Web client methods.

#### Scenario: Documentation is synchronized
- **WHEN** the log capability is implemented
- **THEN** `docs/03-api-index.md`, `docs/04-database-design.md`, and error-code documentation when applicable SHALL describe the new endpoints, schemas, tables, and errors.

#### Scenario: Validation and tests cover the capability
- **WHEN** implementation is complete
- **THEN** backend tests SHALL cover logging, validation, masking, permissions, filters, and not-found behavior
- **AND** frontend tests SHALL cover list rendering, filters, request_id copy, detail drawer, forbidden state, and pagination structure.
