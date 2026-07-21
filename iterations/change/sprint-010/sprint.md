---
note: workflow-sync — workflow-sync 自动同步 — 0/1 Change archived；0 applied；1 进行中；Sprint `planning`
sprint_id: sprint-010
status: planning
lifecycle_stage: change
created_at: 2026-07-20 22:30:24
updated_at: 2026-07-20 22:31:50
---

# sprint-010 迭代规划

## 1. Sprint 目标

本 Sprint 聚焦密码校验规则简化，将 `REQ-0063-password-validation-policy-simplification` 和 OpenSpec Change `update-password-validation-policy` 纳入正式迭代范围。目标是在不改变既有认证安全边界的前提下，将系统设置新密码的基础策略统一为 5-32 位、包含英文字符、包含数字，并同步后端校验、管理端提示、API 错误 message 与测试。

正式目标：

- `REQ-0063-password-validation-policy-simplification`：统一修改本人密码、创建用户初始密码、管理员重置密码等入口的新密码策略，清理旧的 8 位、大小写和特殊字符提示，确保前后端规则一致。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0063-password-validation-policy-simplification | 密码校验规则简化 | in_sprint | 1.0 人天 | proposed `update-password-validation-policy` |

BUG：无 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 1 个范围项关联 Change；0 archived，0 applied，0 in_progress，1 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 开发人数 | 2 |
| 测试人数 | 1 |
| Sprint 容量 | 30 人天 |
| 已纳入估算 | 1.0 人天 |
| 容量占用 | 3.33% |
| fix 缓冲 | 29.0 人天 |
| fix 缓冲比例 | 96.67% |

容量门禁：Pass。当前仅纳入一个 S 级 update 型 Change，远低于 120% 硬阻断阈值。

## 4. 里程碑

| 里程碑 | 目标日期 | 说明 |
|---|---|---|
| Sprint 规划完成 | 2026-07-20 22:30:24 | 纳入 `REQ-0063` 与 `update-password-validation-policy` |
| 实现与自测 | 2026-08-22 18:00:00 | 完成后端密码策略、API、管理端提示和测试 |
| 验收收口 | 2026-08-28 18:00:00 | 完成 acceptance、Workflow Sync 和归档前检查 |

## 5. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 旧密码提示散落在前端组件或测试中 | 用户看到 8 位、大小写、特殊字符等旧文案 | 实现阶段搜索旧提示并补前端测试 |
| 后端入口规则漂移 | 修改密码、创建用户、重置密码规则不一致 | 优先修改统一校验/生成函数，并补多入口测试 |
| 安全策略被误删 | 弱密码表、限流、token_version 或受保护账号逻辑回退 | tasks 明确保留既有安全边界，测试覆盖不回退 |
| API 错误结构变化影响前端 | 前端无法展示具体失败项 | 如 schema 变化，同步 OpenAPI、Orval 与 API 文档 |

## 6. 知识库承接

| 来源 | 承接项 | 本 Sprint 处理 |
|---|---|---|
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 容量超过 100% 时冻结范围更早执行 | sprint-010 当前只纳入 1.0 人天，避免复现 sprint-008 / sprint-009 容量边界问题 |
| `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` | 复盘继续只消费 Fact Sheet / 摘要 | 本 Sprint 范围小，仍要求 apply/archive 输出保持 compact summary |
| `docs/knowledge-base/best-practices/admin-form-page-consistency.md` | 字段级错误和 fixed toast 避免 layout shift | 密码字段错误必须在字段附近展示，成功反馈使用 fixed toast |
| `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` | 管理端弹窗宽度与 CSS cascade 防回归 | 修改密码弹窗保持 520px computed width，避免 `modal-card` 与专属类并存 |

## 7. 横切预防清单

| 标签 | 适用性 | 验收 gate |
|---|---|---|
| admin-list | N/A | 不涉及管理端列表页 |
| admin-form | applicable | 字段级密码错误显示在字段附近；保存/成功反馈不得造成布局位移；如触及表单页，保存 CTA 保持单一 |
| admin-modal | applicable | 修改密码弹窗保持 520px computed width；TSX 不得同时挂载 `modal-card` 与专属类；矮视口下 body scroll 无回归 |
| media-upload | N/A | 不涉及上传 |

## 8. 依赖 ASCII 树

```text
sprint-010
└── REQ-0063 密码校验规则简化
    ├── parent: REQ-0015 管理端修改密码
    ├── change: update-password-validation-policy
    ├── specs: auth / admin-password-change / user-management
    ├── backend: 统一密码校验与随机密码生成
    ├── web-admin: 修改密码弹窗与用户管理密码提示
    └── next: /opsx-apply update-password-validation-policy
```

## 9. 发布计划

- 本 Sprint 可作为认证/用户管理规则调整随产品小版本发布。
- 发布前必须确认是否同步 OpenAPI、Orval、API 文档和错误码文档。
- 不涉及 DB migration、MinIO、Docker 配置或小程序发布。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| REQ | `issues/requirements/review/REQ-0063-password-validation-policy-simplification/` |
| Change | `openspec/changes/update-password-validation-policy/` |
| Knowledge | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
| Knowledge | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` |

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 22:30:24 | `/sprint-propose` | 创建 sprint-010，纳入 REQ-0063 与 update-password-validation-policy |
