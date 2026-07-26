## Why

The workflow can already trace REQ/BUG/Sprint/OpenSpec status, but AI command token usage is still estimated during retrospectives. `/sprint-exps` needs a safe, structured fact source to show which command stages consumed tokens, tools, and retries without exposing raw Codex session content.

## What Changes

- Add a redacted AI usage fact source under `data/ai-usage/`.
- Define command run boundaries as one user message turn.
- Aggregate model calls, token metrics, tool calls, tool output size, and retry counts per command run.
- Associate command runs with REQ, BUG, OpenSpec Change, Sprint, and workflow event fields.
- Make `/sprint-exps` consume Sprint-level usage snapshots and report command-stage token analysis.
- Enforce redaction rules so raw prompts, system/developer instructions, local absolute paths, secrets, and raw `~/.codex/sessions` JSONL never enter long-lived repo artifacts.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `agent-workflow-tooling`: add AI command usage fact source, command-run aggregation, safe attribution, and sprint-exps usage analysis requirements.

## Impact

- Affects scripts that parse local Codex session JSONL and generate Sprint/command usage facts.
- Affects `data/ai-usage/` governance, README or ignore boundaries for safe persisted outputs.
- Affects `/sprint-exps` and Fact Sheet consumption of token usage snapshots.
- Affects workflow documentation and tests for parser, aggregation, attribution, and redaction behavior.
- Does not affect backend APIs, database schema, MinIO storage, Web UI, miniapp, admin UI, Orval, or customer-facing behavior.
