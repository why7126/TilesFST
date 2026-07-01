---
review_id: REV-REQ-0019-001
date: 2026-06-30 18:10:29
participants:
  - product
result: approved
created_at: 2026-06-30 18:10:29
updated_at: 2026-06-30 18:10:29
---

# REQ-0019 需求评审

## 评审结论

`REQ-0019-admin-superuser-protection` 评审通过，状态变更为 `approved`。

本需求作为 `REQ-0005-user-management` 的权限策略扩展进入后续 OpenSpec。实现时保持现有 `admin` / `employee` / `store_owner` 角色模型，不新增 `super_admin` 或 `root` 角色；以 `ADMIN_USERNAME` 对应账号的 `is_protected` 标识承载系统保底账号保护。

## 评审清单

- [x] 范围清晰，Out of Scope 明确：不新增角色、不改 RBAC、不影响店主端和小程序。
- [x] 验收标准可测试：覆盖 API 字段、编辑、重置密码、状态变更、本人改密、错误码、前端置灰与自动化测试。
- [x] 优先级与依赖合理：P1；依赖 `REQ-0005-user-management` 与 `REQ-0015-password-change`。
- [x] UI 类策略已决：复用用户管理页，轻量 prototype 表达受保护账号行置灰状态。
- [x] 与现有 REQ 重复关系已说明：属于 `REQ-0005-user-management` refinement，不是独立 RBAC 新模块。

## 条件通过项

- [x] 默认禁止受保护账号本人通过管理端修改密码；若后续产品策略改变，必须通过评审更新 AC-019~AC-023。
- [x] OpenSpec design 必须引用 `trace.md` 的 `knowledge_base_refs`，并保留 `admin-list` 横切 AC。
- [x] 后续实现必须登记错误码并同步 OpenAPI / Orval。
- [x] 后续实现必须保留 `.env` 级运维恢复能力，不得删除 `ADMIN_RESET_PASSWORD_ON_STARTUP` 边界。

## 建议 Change

```text
update-admin-superuser-protection
```

## 下一步

```text
/req-opsx REQ-0019-admin-superuser-protection
```
