---
change_id: fix-openspec-archive-multiline-proposal-warning-stdout
created_at: 2026-08-06 14:56:07
updated_at: 2026-08-06 15:03:07
---

# 任务清单

- [x] 更新 `scripts/archive-change.sh`，整体吸收真实 OpenSpec CLI 多行 proposal warning stdout/stderr 块。
- [x] 保留未知 stdout/stderr 输出，确认失败路径仍输出必要诊断并返回非零退出码。
- [x] 更新 `tests/test_archive_change_script.py`，新增真实多行 proposal warning stdout 样例。
- [x] 确认既有单行 warning、未知 stdout、未知 stderr、BUG-0119 固定噪音过滤测试不回归。
- [x] 运行 `python -m pytest tests/test_archive_change_script.py`。
- [x] 运行 `python scripts/validate-openspec-language.py`。
- [x] 运行 `python scripts/validate-directory-structure.py`。
- [x] 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若仅为治理脚本噪音回归，可在归档验收中记录“不适用”。

## 执行记录

- `python -m pytest tests/test_archive_change_script.py`：9 passed。
- `docs/knowledge-base/incidents/`：不适用；本次为治理脚本成功路径噪音回归，未涉及生产事故、客户数据、API、数据库或运行时故障。
