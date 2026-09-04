---
title: release-propose 下一步设计
created_at: 2026-08-31 08:35:48
updated_at: 2026-08-31 08:35:48
---

# Design

## 设计决策

- `/release-propose` 仍负责生成发布计划和回显 usage docs、公开公告、镜像构建三类决策摘要。
- `/release-propose` 的成功路径下一步改为 `/release-prepare <version>`，因为 prepare 是第一个会补齐版本源、公告和门禁证据的变更型命令。
- `/release-status` 保留为只读面板，用于操作者需要先理解阶段、阻塞分类、默认 upgrade 路径或安全下一步时主动调用。

## 影响范围

- 技能说明：`.agents/skills/release-propose/SKILL.md`。
- 发布规则：`rules/release.md`、`rules/agent-context-budget.md`。
- 项目入口摘要：`AGENTS.md`。
- OpenSpec delta：`product-release-management`。

## 验证策略

- 运行 OpenSpec、目录结构、上下文预算和文档卫生校验。
- 运行 Workflow Sync，确认纯治理 Change 已纳入 `sprint-029` 并同步为 applied。
