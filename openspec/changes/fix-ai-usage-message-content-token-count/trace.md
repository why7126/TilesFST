---
change_id: fix-ai-usage-message-content-token-count
type: fix
status: proposed
source_bug: BUG-0141-ai-usage-token-count-jsonl
sprint: sprint-026
created_at: 2026-08-25 15:28:00
updated_at: 2026-08-25 18:18:35
---

# 追溯

## 来源

- BUG：`BUG-0141-ai-usage-token-count-jsonl`
- Sprint：`sprint-026`
- 能力：`agent-workflow-tooling`

## 根因状态

`confirmed`

## 证据摘要

- 新版 session 用户消息结构为 `payload.type=message`、`payload.role=user`、`payload.content` 文本片段列表。
- 当前 `safe_text()` 只处理字符串字段，导致 `user_text()` 返回空字符串。
- `parse_session_jsonl()` 未建立 command run 时会跳过后续 token_count 事件。
- `sprint-025` snapshot 已出现 `snapshot_status=failed`、`usage_mode=estimated_fallback`、`required-metrics-empty`。

## 同步状态

```yaml
bug_id: BUG-0141-ai-usage-token-count-jsonl
change_id: fix-ai-usage-message-content-token-count
sprint: sprint-026
status: proposed
workflow_event: bug.opsx
```

## 实现验证

```yaml
implemented_at: 2026-08-25 15:36:30
checks:
  - command: python -m pytest tests/test_ai_usage.py
    result: pass
    summary: 33 passed
  - command: python scripts/extract-ai-usage.py --session-jsonl <local-codex-session> --sprint sprint-025 --json
    result: pass
    summary: refreshed sprint-025 with 18 parsed command runs and no parser warnings
  - command: python scripts/extract-ai-usage.py --check-snapshot --sprint sprint-025 --json
    result: pass
    summary: snapshot_status=present, usage_mode=actual, fresh_gate.status=pass, warning_count=0
incident_note: 已有 BUG root-cause、OpenSpec trace 与聚焦回归测试承载可复用经验；本次不新增 docs/knowledge-base/incidents/ 事故复盘。
```

## 范围扩展

```yaml
expanded_at: 2026-08-25 16:05:00
reason: sprint-025 retrospective matrix rendered unattributed workflow stages as plain 0, which is easy to misread as true zero usage.
added_scope:
  - sprint AI usage matrix unknown/unattributed rendering semantics
  - post-command hook same-score target run tie-breaker
  - sprint-025 snapshot refresh and retrospective token explanation update
  - sprint-025 session directory backfill with Sprint scope trimming
status: done
checks:
  - command: uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py
    result: pass
    summary: 60 passed
  - command: python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --summary
    result: pass
    summary: fresh_gate.status=pass, usage_mode=actual, snapshot_status=present, unknown_columns_count=20
  - command: python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --ai-usage-markdown
    result: pass
    summary: rendered unknown for unobserved workflow columns and 0 for observed zero-token BUG-Capture column
  - command: python scripts/validate-agent-context-budget.py
    result: pass
  - command: python scripts/validate-openspec-language.py
    result: pass
  - command: python scripts/validate-directory-structure.py
    result: pass
  - command: openspec validate fix-ai-usage-message-content-token-count
    result: pass
  - command: python scripts/validate-sprint-scope.py sprint-026 --item fix-ai-usage-message-content-token-count
    result: pass
  - command: python scripts/validate-doc-prose-hygiene.py <focused-paths>
    result: pass-with-warnings
    summary: 10 heuristic history-narration warnings, no blocker
  - command: python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change fix-ai-usage-message-content-token-count --sprint sprint-026 --json
    result: pass
    summary: status=ok, usage_mode=actual, warning_count=0
  - command: python scripts/generate-sprint-fact-sheet.py --sprint sprint-026 --summary
    result: pass
    summary: fresh_gate.status=pass, snapshot_status=present, usage_mode=actual
  - command: ~/.codex/sessions directory backfill for sprint-025
    result: pass
    summary: scanned 520 JSONL files, selected 23 sessions and 100 unique lifecycle command runs; total_tokens=8039162
  - command: python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --ai-usage-markdown
    result: pass
    summary: matrix rows trimmed to Total, sprint-025, 9 sprint requirements and 7 sprint bugs; unknown_columns_count=10
```

## 验收返修

```yaml
modified_at: 2026-08-25 18:18:35
feedback: AI Usage 矩阵中未观测阶段不要显示 unknown，应显示短横线。
root_cause_status: confirmed
root_cause: Fact Sheet Markdown 渲染层直接输出列状态名 unknown，导致复盘表格单元格过长；数据层列状态语义本身无需改变。
scope_decision: in_scope
adjustment:
  - 保留 usage_matrices.columns[].status=unknown 作为机器可读状态。
  - 将 Markdown 矩阵未观测单元渲染为 `-`。
  - 将复盘口径、sprint-exps 技能与 OpenSpec delta 更新为展示 `-`、真实 0 保留数字 `0`。
visual_comparison:
  - screenshot: Image #1
    page_state: sprint-025 AI Usage matrix rendered in retrospective
    expected: 未观测 workflow 单元显示 `-`
    actual_before: 未观测 workflow 单元显示 `unknown`
    disposition: adjust Markdown renderer
validation_status: pass
validation:
  - command: uv run pytest tests/test_ai_usage.py tests/test_generate_sprint_fact_sheet.py
    result: pass
    summary: 61 passed
  - command: python scripts/generate-sprint-fact-sheet.py --sprint sprint-025 --ai-usage-markdown
    result: pass
    summary: unobserved workflow cells rendered as `-`; observed zero values remained `0`
  - command: openspec validate fix-ai-usage-message-content-token-count --strict
    result: pass
  - command: python scripts/sync-workflow-status.py --event opsx.modify --change fix-ai-usage-message-content-token-count --sprint auto
    result: pass
    summary: updated=5, errors=0, blockers=0
  - command: python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change fix-ai-usage-message-content-token-count --sprint sprint-026 --json
    result: pass
    summary: status=ok, usage_mode=actual, warning_count=0
```
