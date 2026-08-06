---
change_id: fix-openspec-archive-multiline-proposal-warning-stdout
type: fix
source_bug: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
source_sprint: sprint-021
created_at: 2026-08-06 14:56:07
updated_at: 2026-08-06 14:56:07
---

# 修复 OpenSpec 归档多行 proposal warning stdout 噪音

## 背景

BUG-0124 记录了 `fix-openspec-archive-proposal-warning-stdout` 已归档后仍存在的真实输出问题：`scripts/archive-change.sh` 成功路径仍会展示 OpenSpec CLI stdout 中的多行 proposal warning 块，例如 `Proposal warnings in proposal.md` 与后续 `Missing required sections` 详情行。

该 warning 属于本项目中文优先 OpenSpec 文档与上游 CLI 英文脚手架标题之间的兼容性提示，不应在归档成功路径干扰 `/opsx-archive` 验收体验。

## 变更内容

- 调整 `scripts/archive-change.sh` 已知 warning 过滤逻辑，将真实 OpenSpec CLI 多行 proposal warning 块作为整体吸收。
- 保留未知 stdout/stderr，避免吞掉真实异常、诊断信息或上游 CLI 行为变化信号。
- 补充 `tests/test_archive_change_script.py` 回归测试，覆盖多行 stdout warning、未知 stdout/stderr 保留、既有单行 warning 不回归。
- 不修改 API、数据库、Web、小程序、管理端运行时代码、Orval 或 Docker Compose。

## 回滚计划

- 若过滤逻辑误吞未知输出，回滚 `scripts/archive-change.sh` 的多行块识别逻辑。
- 保留新增测试样例作为回归证据，回滚后应重新评估是否需要更窄的匹配边界。
- 若上游 OpenSpec CLI warning 形态再次变化，优先新增真实样例测试，再调整过滤状态机。

## 关联

- BUG：`BUG-0124-openspec-archive-multiline-proposal-warning-stdout`
- Sprint：`sprint-021`
- 关联历史 BUG：`BUG-0123-openspec-archive-proposal-warning-stdout`
