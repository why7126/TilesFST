---
change_id: tighten-bug-review-root-cause-confirmed-gate
created_at: 2026-08-24 16:35:51
updated_at: 2026-08-24 16:35:51
---

# 测试计划

## 聚焦验证

- `uv run pytest tests/test_validate_root_cause_evidence.py`
- `python scripts/validate-root-cause-evidence.py --bug BUG-0137-miniapp-lightweight-image-variant-consumption --require-confirmed`
- `python scripts/validate-root-cause-evidence.py --bug BUG-0134-miniapp-certificate-detail-display-url --require-confirmed`

## 治理门禁

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate tighten-bug-review-root-cause-confirmed-gate`
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`

## 不适用验证

- API：不涉及。
- 数据库：不涉及。
- Web：不涉及。
- 小程序：不涉及。
- 管理端：不涉及。
- Orval：不需要。
- Docker Compose：不需要。
