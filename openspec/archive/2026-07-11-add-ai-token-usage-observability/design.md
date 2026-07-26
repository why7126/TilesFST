## Context

REQ-0034 asks for real token usage analysis by command stage. Codex keeps local session JSONL under `~/.codex/sessions`, including token usage events, but those files may contain prompts, system/developer instructions, local paths, and tool output. The durable project artifact must therefore be a derived, redacted fact table, not a copy or excerpt of the session files.

The existing `agent-workflow-tooling` capability already owns Sprint Fact Sheet and `/sprint-exps` behavior, so this change extends that capability instead of creating a separate workflow silo.

## Goals / Non-Goals

**Goals:**

- Produce command-run usage records in `data/ai-usage/` from local session inputs.
- Use one user message turn as the command boundary.
- Aggregate token, tool, and retry metrics per command run and per Sprint command stage.
- Preserve links to REQ/BUG/Change/Sprint/workflow event through structured IDs.
- Make `/sprint-exps` prefer real usage snapshots and clearly mark fallback estimates.
- Prevent raw prompt, raw session JSONL, system/developer instructions, absolute local paths, secrets, and tool output bodies from entering repo artifacts.

**Non-Goals:**

- Modify Codex Desktop, model APIs, or live token accounting.
- Build a billing or cost allocation system.
- Add product-facing Web, miniapp, admin UI, backend API, database tables, or Orval output.
- Store full command prompts or raw tool outputs for debugging.

## Decisions

### Derived Fact Source

Use `data/ai-usage/` for derived usage facts. Raw `~/.codex/sessions` remains an input path supplied at extraction time and is never copied into the repository.

Alternative considered: write token totals into each REQ/BUG `trace.md`. That would make trace files noisy and would not support Sprint-stage analysis cleanly, so trace remains workflow state and usage stays in a separate fact source.

### Command Boundary

Treat each user message turn as one command run. The run starts at the user message and includes subsequent model calls, tool calls, and outputs until the next user message or session end.

Alternative considered: split by each model call. That is easier to parse but loses the user-visible command boundary and makes `/req-complete` or `/opsx-apply` cost harder to understand.

### Token Aggregation

Aggregate per-call `last_token_usage` values. Do not use session-level `total_token_usage` as a command cost because it is cumulative and would double count.

### Attribution

Associate command runs using explicit IDs first, then Workflow Sync arguments, trace/Sprint time windows, Sprint scope reverse lookup, and finally low-confidence manual or heuristic attribution. Ambiguous attribution remains multi-valued with `attribution_confidence`.

### Redaction

Persist numeric metrics, stable workflow IDs, relative repository paths, hashes, timestamps, and short safe labels only. Any text that could include prompts, instructions, local absolute paths, secrets, `.env` values, customer data, or raw tool output is skipped or replaced with a warning.

## Risks / Trade-offs

- [Risk] Codex session event shapes may change -> Parser treats unknown events as warnings and keeps extracting known fields.
- [Risk] Retry count is approximate -> Store `retry_count_method` so reports do not imply exactness.
- [Risk] Attribution can be ambiguous -> Allow multiple IDs and confidence levels instead of forcing a single owner.
- [Risk] Usage records may accidentally include sensitive text -> Add redaction tests and default to numeric-only persistence when safety is uncertain.
- [Risk] `data/ai-usage/` may mix local-only and committable files -> Document the boundary with README and ignore rules before persisting detailed records.

## Migration Plan

1. Add the AI usage extraction and aggregation scripts without changing live workflow behavior.
2. Introduce `data/ai-usage/` documentation and safe sample or aggregate outputs.
3. Add parser, aggregation, attribution, redaction, and snapshot-regeneration tests.
4. Update `/sprint-exps` to consume Sprint usage snapshots when present and retain an explicit estimate fallback.
5. Validate OpenSpec and workflow sync before applying in a Sprint.

## Open Questions

- Which command-line interface should be the canonical entry point: a dedicated AI usage script or an option on the existing Sprint Fact Sheet generator?
- Should detailed command-run files be committed, or should the repo only keep Sprint aggregate snapshots plus local regenerated details?
