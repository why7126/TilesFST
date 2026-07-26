## 1. Fact Source Governance

- [x] 1.1 Create or update `data/ai-usage/` documentation that defines local-only inputs, committable outputs, file naming, retention, and redaction boundaries.
- [x] 1.2 Add ignore or sample-data rules so raw Codex session JSONL and unsafe command-run details cannot be committed accidentally.
- [x] 1.3 Update workflow documentation or skill guidance to explain how usage facts relate to REQ/BUG trace files and Sprint retrospectives.

## 2. Session Extraction

- [x] 2.1 Implement a parser for local Codex session JSONL that recognizes session metadata, user turns, token_count events, tool calls, and tool results.
- [x] 2.2 Group events into command runs using the user-message boundary.
- [x] 2.3 Aggregate model_call_count, input_tokens, cached_input_tokens, output_tokens, reasoning_output_tokens, total_tokens, tool_call_count, tool_output_chars, retry_count, and retry_count_method.
- [x] 2.4 Treat unknown event types and malformed JSONL rows as warnings without aborting the entire extraction.

## 3. Attribution And Redaction

- [x] 3.1 Associate command runs with requirements, bugs, OpenSpec changes, Sprint IDs, and workflow events using explicit IDs and Workflow Sync arguments first.
- [x] 3.2 Add fallback attribution from trace time windows, Sprint scope reverse lookup, or manual mapping with medium/low confidence.
- [x] 3.3 Implement redaction for prompts, system/developer instructions, skill text, absolute local paths, secrets, `.env` values, customer data, and tool output bodies.
- [x] 3.4 Persist safe command-run records with source hashes or equivalent provenance instead of raw local paths.

## 4. Sprint Aggregation And Retrospective Integration

- [x] 4.1 Generate Sprint-level usage snapshots from command-run records.
- [x] 4.2 Integrate usage snapshots into the Sprint Fact Sheet or `/sprint-exps` input flow.
- [x] 4.3 Update `/sprint-exps` output to show command-stage usage metrics, high-consumption causes, and optimization suggestions.
- [x] 4.4 Keep an explicit estimated fallback when no real usage snapshot exists.

## 5. Tests And Validation

- [x] 5.1 Add parser tests for token_count extraction, user-turn grouping, malformed rows, and unknown events.
- [x] 5.2 Add aggregation tests for token totals, tool output character counts, retry_count_method, and idempotent re-extraction.
- [x] 5.3 Add attribution tests for explicit IDs, Workflow Sync arguments, multi-Issue commands, and low-confidence fallback.
- [x] 5.4 Add redaction tests that fail when raw prompts, local absolute paths, secrets, `.env` content, or tool output bodies are persisted.
- [x] 5.5 Validate the OpenSpec change and run affected script/test suites.
