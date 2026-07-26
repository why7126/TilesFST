---
title: REQ-0075 Audit Log Task Trace Checklist
created_at: 2026-07-26 16:05:00
updated_at: 2026-07-26 16:05:00
---

# Audit Log Task Trace Checklist

## First Batch Sensitive Operation Review

| Area | Current writer | Task context status | Decision |
|---|---|---|---|
| System settings | `SystemSettingsService.patch_group/reset_group` -> `AuditLogRepository.insert` | Can read `request.state.task_trace_id` or `x-task-trace-id` from admin route | Connected. Persist optional `task_trace_id` / `task_type` when present; nullable when absent. |
| Brand certificates | `BrandCertificateAdminService._audit` -> `AuditLogRepository.insert` | Can read `request.state.task_trace_id` or `x-task-trace-id` from admin route | Connected. Persist optional `task_trace_id` / `task_type` when present; nullable when absent. |
| Media/uploads | Upload endpoints currently create Task Trace spans and return `task_trace_id`; they do not write `audit_logs` directly | Task Trace exists in upload route state/file attributes | No direct `audit_logs` writer found in current code. Keep Task Trace coverage; audit writer hookup is N/A until an audit operation is introduced. |
| SKU | SKU admin routes use `TaskTraceService` for create/update/publish/unpublish | Task Trace context exists in route state and response | No direct `audit_logs` writer found in current code. Keep Task Trace coverage under REQ-0074/REQ-0073; audit writer hookup is N/A until SKU audit writer is introduced. |
| Banner | Banner admin service/repository currently has no direct `AuditLogRepository.insert` writer | No audit writer context found | No direct `audit_logs` writer found in current code. Record as follow-up candidate only if Banner audit logging becomes a scoped requirement. |
| Other existing audit writers | `rg AuditLogRepository` found system settings and brand certificates only | Covered above | No additional direct audit writers found. |

## Implementation Notes

- `AuditLogRepository.insert()` now accepts optional `task_trace_id` and `task_type`.
- Invalid task trace ids are ignored rather than trusted.
- `task_type` is persisted only when `task_trace_id` is valid.
- Audit metadata is parsed when it is JSON object metadata and sanitized through the shared usage logging metadata sanitizer before persistence.
- Task fields are observability links only; permission checks stay in existing route dependencies and service resource validation.
