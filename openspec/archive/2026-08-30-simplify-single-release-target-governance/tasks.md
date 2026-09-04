---
title: 单一项目发布治理任务
created_at: 2026-08-30 16:10:00
updated_at: 2026-08-30 22:01:44
---

# Tasks

- [x] 创建 OpenSpec Change 并纳入 `sprint-029`。
- [x] 调整 release / upgrade validator，统一 `project` scope，忽略旧 `--target` 对门禁和文件名的影响。
- [x] 将升级计划文件名改为无 `.development` / `.production` 后缀，并更新 v1.2.2 计划。
- [x] 更新 release / upgrade 技能、`rules/release.md`、`rules/agent-context-budget.md` 和 `AGENTS.md` 的当前发布口径。
- [x] 更新 `releases/templates/release.json` 与 `releases/v1.2.2` 发布事实源。
- [x] 补充聚焦测试，覆盖旧 target 兼容但不触发双轨门禁。
- [x] 运行 OpenSpec、目录结构、上下文预算、文档卫生、release / upgrade validator 与聚焦 pytest。
- [x] 运行 Workflow Sync 与 AI Usage hook。
