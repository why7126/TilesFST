---
review_id: REV-REQ-0015-001
date: 2026-06-28
participants: []
result: approved
created_at: 2026-06-28 10:01:12
updated_at: 2026-06-28 10:01:12
---

# 评审结论

**REQ:** REQ-0015-password-change  
**结果:** approved  
**评审日期:** 2026-06-28

## 摘要

管理端修改密码（侧栏入口 + 居中弹窗）需求文档完整，探索阶段四项决策（API 路径、`token_version` 全端失效、弱密码/限流、共享弹窗）已写入 PRD。验收标准可测试（AC-001～AC-044），原型 HTML/PNG/context 齐全。与 REQ-0005 reset-password、REQ-0014 profile 边界清晰。准予 `/req-opsx` 与 Sprint 纳入。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确（忘记密码、管理员 reset-password、独立路由、小程序等已排除）
- [x] 验收标准可测试（弹窗交互、API、token 失效、限流、视觉、自动化）
- [x] 优先级与依赖合理（P1；依赖 REQ-0004 壳层、REQ-0001 认证；REQ-0014 非阻塞）
- [x] UI 类：prototype HTML > PNG > context 策略已决；520px 居中弹窗
- [x] 无与现有 REQ 重复未说明（与 REQ-0005 reset-password 差异见 business-flow）

## 亮点

- `/req-explore` 结论完整落盘：全端 token 失效方案明确，安全策略可实施。
- 共享 `ChangePasswordModal` + `AdminLayout` 托管，REQ-0014 可后接 callback，避免重复 UI。
- FR-001～FR-011 与 AC 一一对应，前后端边界清晰。

## 风险与备注

| 项 | 说明 |
|---|---|
| DB 迁移 | `users.token_version` 影响所有已登录 JWT；login/deps 须同步改 |
| 错误码 | 40020–40023、42901 须在 apply 时登记 error_codes 与 docs |
| REQ-0014 | Profile 页「修改密码」在 REQ-0014 complete 时改为 openModal，非独立页 |
| OpenSpec | 建议 change id：`add-admin-password-change` |

## 条件通过项

- [ ] apply 阶段 PNG 与实现页 1440×1024 并排验收（AC-029）
- [ ] archive 时同步 `docs/03-api-index.md` 与 error-codes
- [ ] REQ-0014 `/req-complete` 时修正「跳转独立页面」为共享弹窗

## 下一步

1. `/req-opsx REQ-0015-password-change`
2. `/sprint-propose` 纳入迭代（可选）
3. `/opsx-apply add-admin-password-change`
