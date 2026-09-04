---
title: release-propose 下一步调整测试计划
created_at: 2026-08-31 08:35:48
updated_at: 2026-08-31 08:35:48
---

# Test Plan

## 自动化校验

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `python scripts/validate-directory-structure.py`
- `openspec validate make-release-propose-next-step-prepare`
- `python scripts/validate-doc-prose-hygiene.py <focused-paths>`

## 人工复核点

- `/release-propose <version>` 输出文案默认指向 `/release-prepare <version>`。
- `/release-status <version>` 仍表达为只读状态面板和阻塞排查入口。
