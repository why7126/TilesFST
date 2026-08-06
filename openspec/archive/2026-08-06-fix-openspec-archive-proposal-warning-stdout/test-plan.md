---
change_id: fix-openspec-archive-proposal-warning-stdout
status: proposed
created_at: 2026-08-06 13:45:35
updated_at: 2026-08-06 13:45:35
---

# 测试计划

## 自动化测试

- 新增或更新 `tests/test_archive_change_output.py`。
- 模拟 OpenSpec CLI stdout 仅包含已知 proposal scaffold warning，断言归档成功输出不展示该块。
- 模拟未知 stdout，断言输出保留。
- 模拟未知 stderr，断言输出保留。
- 模拟 OpenSpec CLI 非零退出，断言 wrapper 返回非零并保留错误诊断。
- 覆盖 BUG-0119 的自定义固定说明噪音不回归。

## 手工验证

- 使用中文优先 Change 执行 `/opsx-archive` 或 `scripts/archive-change.sh <change-id>`。
- 确认归档成功输出清晰，不展示已知 proposal scaffold warning。
- 确认未知诊断输出仍可见。

## 不适用测试

- 不涉及 API、数据库、Web、小程序、管理端或 Docker Compose。
