---
created_at: 2026-08-12 10:30:00
updated_at: 2026-08-12 10:30:00
---

# 设计说明

## 目标

把 AI usage 真实矩阵输出从“执行者遵守文档约定”推进到“脚本和 Skill 双重 gate”：

- summary 阶段给出 refresh-first 指引。
- refresh 后必须重新 summary，不能沿用旧 blocker。
- Markdown 渲染入口自身阻断 stale/blocker，避免误写真实矩阵。

## 方案

1. `/sprint-exps` Skill 增加明确步骤：
   - 先运行 `--summary`。
   - 若 fresh gate blocker，优先运行 post-command hook 或按 recommended action 刷新 snapshot。
   - 刷新后必须重新运行 `--summary`。
   - 只有二次 summary gate pass 后才运行 `--ai-usage-markdown`。
2. `scripts/generate-sprint-fact-sheet.py` 增加矩阵写入 gate：
   - `usage_matrices_summary.available` 仅表示真实矩阵可用于复盘写入。
   - 保留 `raw_present` 表示 snapshot 中存在原始矩阵，便于诊断。
   - `--ai-usage-markdown` gate 未通过时只输出 blocker 表与 recommended action，不输出四张真实矩阵。

## 影响

- API：无。
- DB：无。
- Web：无。
- 小程序：无。
- 管理端：无。
- Orval：不需要。
- Docker Compose：不需要。
