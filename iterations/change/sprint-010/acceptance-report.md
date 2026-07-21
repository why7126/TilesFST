---
note: workflow-sync — 0/1 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-010
status: planning
lifecycle_stage: change
created_at: 2026-07-20 22:30:24
updated_at: 2026-07-20 22:31:50
---

# sprint-010 验收报告

## 1. 验收范围

| 类型 | 编号 | Change | 当前状态 | 验收结论 |
|---|---|---|---|---|
| REQ | REQ-0063-password-validation-policy-simplification | update-password-validation-policy | in_sprint，待实现（`update-password-validation-policy` proposed） | 待实现 |

## 2. 功能验收要点

- [ ] 密码长度少于 5 位失败。
- [ ] 密码长度等于 5 位且包含英文和数字成功。
- [ ] 密码长度等于 32 位且包含英文和数字成功。
- [ ] 密码长度超过 32 位失败。
- [ ] 缺少英文字符失败。
- [ ] 缺少数字失败。
- [ ] 修改本人密码、创建用户、重置密码策略一致。
- [ ] 旧提示“至少 8 位”、大小写、特殊字符不再显示。

## 3. 横切验收

- [ ] 管理端字段级密码错误在字段附近展示，不只依赖全局 Toast。
- [ ] 修改密码弹窗保持 520px computed width。
- [ ] 弹窗矮视口下 body scroll 和 footer 可访问。
- [ ] 成功反馈使用 fixed toast 或既有 AdminLayout toast，不造成 layout shift。

## 4. 测试与证据

| 项 | 状态 | 证据 |
|---|---|---|
| 后端密码策略测试 | pending | 待 `/opsx-apply` |
| 修改密码 API 测试 | pending | 待 `/opsx-apply` |
| 用户创建/重置密码测试 | pending | 待 `/opsx-apply` |
| Web 管理端提示测试 | pending | 待 `/opsx-apply` |
| OpenAPI/Orval 同步 | pending | 若实现阶段触发则补充 |

## 5. 结论

当前为 Sprint 规划阶段，验收结论待实现与测试后更新。
