---
title: PRODUCT_VERSION 发布准备自动同步任务
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 23:00:41
---

# Tasks

- [x] 创建 OpenSpec Change 并纳入 `sprint-029`。
- [x] 在 release validator 中增加 `--sync-product-version`，同步版本源、release metadata 和公告版本状态。
- [x] 在 release status 中将版本不一致的安全修复路径指向 `/release-prepare <version>`。
- [x] 在 image prepare 中增加版本源未对齐 blocker，要求先回到 release prepare。
- [x] 更新 release-prepare、release-status、release-publish、image-prepare 技能说明。
- [x] 更新 `rules/release.md`、`rules/agent-context-budget.md` 和 `AGENTS.md` 当前口径。
- [x] 补充聚焦测试，覆盖自动同步和 image prepare 前置阻断。
- [x] 运行 OpenSpec、目录结构、上下文预算、文档卫生、脚本编译、release/image validator 与聚焦 pytest。
- [x] 运行 Workflow Sync 与 AI Usage hook。
