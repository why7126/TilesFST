---
title: release-propose 下一步调整验收
created_at: 2026-08-31 08:35:48
updated_at: 2026-08-31 08:41:22
---

# Acceptance

## 验收标准

- `/release-propose <version>` 成功路径默认下一步为 `/release-prepare <version>`。
- `/release-status <version>` 被描述为只读状态面板和阻塞排查入口。
- 发布流程图将 `/release-status` 放在 prepare 后的按需只读检查位置。

## 验收结果

```yaml
acceptance_status: passed
accepted_at: 2026-08-31 08:40:10
accepted_by: Codex / spec-opt
evidence:
  - "release-propose 技能默认下一步已调整为 /release-prepare <version>。"
  - "release-status 技能、rules/release.md、rules/agent-context-budget.md 和 AGENTS.md 已同步只读状态面板定位。"
  - "OpenSpec validate、目录结构、上下文预算、Sprint scope、Workflow Sync 和 AI Usage hook 校验通过。"
  - "文档卫生校验仅返回既有启发式 warning，无阻断。"
pending_items: []
failed_items: []
notes: 纯治理 Change；API、DB、Web、小程序业务实现、管理端、Orval 与 Docker Compose 不适用。
```
