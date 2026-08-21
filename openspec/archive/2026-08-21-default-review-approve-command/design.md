---
change_id: default-review-approve-command
status: implemented
created_at: 2026-08-21 13:58:00
updated_at: 2026-08-21 13:58:00
---

# 设计说明

## 设计边界

本变更仅调整工作流命令语义和治理文档提示，不涉及业务运行时代码、API、数据库、权限、部署、对象存储、Web、小程序或管理端实现。

## 命令语义

- `/req-review <REQ-id>` 无 flag 时默认评审通过，继续执行与兼容别名 `--approve` 相同的状态更新、目录迁移、Workflow Sync 和 AI Usage hook。
- `/bug-review <BUG-id>` 无 flag 时默认评审通过，继续执行与兼容别名 `--approve` 相同的状态更新、目录迁移、Workflow Sync 和 AI Usage hook。
- 反向结果必须显式表达：REQ 使用 `--reject` 或 `--defer`；BUG 使用 `--reject`、`--defer` 或 `--wont-fix`。

## 同步策略

正向示例统一改为无 flag，保留 `--approve` 兼容说明，避免历史命令立即失效。长期事实源以 `.agents/skills/req-review/SKILL.md`、`.agents/skills/bug-review/SKILL.md` 和本 Change delta spec 为准；入口文件和规则只保留摘要。

## 验证策略

归档前复核上下文预算、OpenSpec 语言、目录结构、目标 Change、Sprint scope 和聚焦文档表达卫生校验。业务测试、Orval 和 Docker Compose 不适用。
