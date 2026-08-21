---
purpose: sprint-exps AI usage fresh gate 治理优化日志
content: 强化 Sprint 复盘 AI usage snapshot 刷新、二次 summary 与真实矩阵写入门禁
source: /spec-opt strengthen-sprint-exps-ai-usage-fresh-gate
update_method: 本日志作为单次治理迭代事实源；后续同类优化新建日志并维护 CHANGELOG
created_at: 2026-08-12 14:27:27
updated_at: 2026-08-12 14:27:27
---

# sprint-exps AI usage fresh gate 治理优化日志

## 迭代目标

强化 `/sprint-exps` 的 AI usage 真实矩阵输出门禁，解决首次复盘 summary 因 snapshot stale 或覆盖不足阻断真实矩阵展示时，必须先刷新 snapshot、刷新后重新 summary，再决定是否写入矩阵的问题。

## 变更摘要

- `/sprint-exps` Skill 明确：fresh gate blocker 时先刷新 snapshot，刷新后必须重新运行 Fact Sheet summary，未重新 summary 不得直接渲染真实矩阵。
- `scripts/generate-sprint-fact-sheet.py` 新增矩阵写入 gate：只有 fresh gate pass、snapshot present、usage mode actual 且矩阵存在时，`--ai-usage-markdown` 才输出真实矩阵。
- Fact Sheet summary 区分 `raw_present` 与 `available`：原始矩阵存在不代表可写入复盘。
- OpenSpec Change、Sprint scope、验收记录与治理日志同步更新。

## 影响范围

| 维度 | 影响 |
|---|---|
| API | 无 |
| DB | 无 |
| Web | 无 |
| 小程序 | 无 |
| 管理端 | 无 |
| Orval | 无 |
| Docker | 无 |
| 治理资产 | `.agents/skills/sprint-exps/SKILL.md`、`scripts/generate-sprint-fact-sheet.py`、`openspec/changes/strengthen-sprint-exps-ai-usage-fresh-gate/`、`iterations/change/sprint-023/`、`docs/spec-logs/` |

## 更新文件

- `.agents/skills/sprint-exps/SKILL.md`
- `scripts/generate-sprint-fact-sheet.py`
- `openspec/changes/strengthen-sprint-exps-ai-usage-fresh-gate/`
- `iterations/change/sprint-023/sprint.yaml`
- `iterations/change/sprint-023/sprint.md`
- `docs/spec-logs/CHANGELOG.md`

## 验证结果

- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-023 --summary`：通过；summary 显示 `matrix_write_gate.status=blocker` 且 `usage_matrices_summary.available=false`。
- `python scripts/generate-sprint-fact-sheet.py --sprint sprint-023 --ai-usage-markdown`：通过；未输出四张真实矩阵，保留刷新后重新 summary 指引。
- `python scripts/validate-sprint-scope.py sprint-023 --item strengthen-sprint-exps-ai-usage-fresh-gate`：通过。
- 最终治理校验结果见本次命令输出。

## 后续建议

- 后续 `/sprint-exps` 执行时优先读取 `usage_matrices_summary.matrix_write_gate`，不要只看 `raw_present`。
- 若其他项目已有 AI usage snapshot，但没有 fresh gate 与 Markdown 渲染双重阻断，可复用本变更的 gate 模型。
