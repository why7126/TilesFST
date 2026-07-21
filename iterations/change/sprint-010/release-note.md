---
sprint_id: sprint-010
status: planning
lifecycle_stage: change
created_at: 2026-07-20 22:30:24
updated_at: 2026-07-20 22:30:24
---

# sprint-010 发布说明草案

## 发布主题

密码校验规则简化。

## 关联范围

| 类型 | 编号 | 标题 | 发布影响 |
|---|---|---|---|
| REQ | REQ-0063-password-validation-policy-simplification | 密码校验规则简化 | 新设置/重置密码入口统一为 5-32 位、包含英文字符和数字 |
| Change | update-password-validation-policy | 密码策略规范更新 | 修改 auth、admin-password-change、user-management 能力规范 |

## 用户可见变化

- 管理端密码规则提示将从旧规则调整为：密码需为 5-32 位，并同时包含英文字符和数字。
- 修改密码、创建用户初始密码、管理员重置密码的基础策略保持一致。

## 技术发布注意

- 如实现阶段修改 OpenAPI schema 或错误码示例，发布前必须同步 Orval 和 API 文档。
- 不涉及数据库结构、MinIO、Docker Compose 或小程序发布。

## 当前状态

规划中，待 `/opsx-apply update-password-validation-policy` 实现。
