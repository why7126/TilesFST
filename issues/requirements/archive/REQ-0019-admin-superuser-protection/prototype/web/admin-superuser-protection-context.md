---
title: 管理端超级管理员账号保护原型说明
purpose: 说明 REQ-0019 用户管理列表受保护账号行的 UI 策略
content: prototype/web/admin-superuser-protection.html 配套说明
source: AI 根据 requirement.md 与 acceptance.md 生成
update_method: UI 策略或评审结论变更时同步更新
owner: product
status: draft
note: REQ-0019-admin-superuser-protection
created_at: 2026-06-30 13:56:49
updated_at: 2026-06-30 13:56:49
---

# 原型说明

## 1. 原型文件

| 文件 | 说明 |
|------|------|
| `prototype/web/admin-superuser-protection.html` | 用户管理列表中受保护账号行的轻量静态参考 |
| `prototype/web/admin-superuser-protection.png` | 待导出；非阻塞 |

## 2. 目标

本原型仅表达 REQ-0019 的增量 UI：

- 受保护账号仍显示在用户管理列表中。
- 操作按钮保留但置灰。
- 显示系统保护徽章或等价提示。
- 普通用户行保持原有可操作状态。

## 3. 实现约束

- 实际实现 MUST 复用现有 `UserManagementPage` 与 `user-management.css`。
- 前端 MUST 读取 API 返回的 `is_protected` 与 `protected_reason`。
- TSX MUST NOT 以 `username === 'admin'` 作为保护判断。
- 受保护账号行不需要新增弹窗；若用户绕过置灰直接请求 API，由后端返回统一错误。

## 4. 验收关注

```text
1. 受保护账号行按钮置灰
2. 普通用户行按钮可用
3. 不改变分页 DOM
4. 不引入 window.confirm
5. 不造成 toast / notice layout shift
```

## 5. 与 Golden Reference 的关系

本原型优先级低于已归档 `REQ-0005-user-management` 的用户管理页面视觉基准，只用于说明“受保护账号行”的增量状态。后续 `/req-opsx` design 中应声明：

```text
1. REQ-0005 用户管理页面既有实现
2. 本 prototype 的受保护行增量状态
3. rules/ui-design.md
4. docs/knowledge-base/best-practices/admin-list-page-consistency.md
```
