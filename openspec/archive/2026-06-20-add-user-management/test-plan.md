---
title: add-user-management 测试计划
purpose: 映射 REQ-0005 验收标准至单元/集成/E2E 测试
content: 基于 acceptance.md 与 tasks.md
source: AI 根据 OpenSpec change 生成
update_method: 实现或验收变更时同步更新
owner: 测试负责人
status: ready
note: Sprint 002 / REQ-0005
---

# 测试计划

## 映射概览

```yaml
change_id: add-user-management
requirement_id: REQ-0005-user-management
iteration: sprint-002
```

## AC → Test Case

### AC-001 ~ AC-005 访问与权限

```yaml
AC-001:
  integration:
    - admin GET /admin/users page renders
  e2e:
    - admin login → /admin/users shows 用户管理

AC-002:
  unit:
    - AdminSidebar hides 用户管理 when role=employee

AC-003:
  unit:
    - navigate /admin/users as employee → forbidden or redirect dashboard
  integration:
    - employee GET /api/v1/admin/users → 403

AC-004:
  integration:
    - unauthenticated /admin/users → /admin/login

AC-005:
  integration:
    - store_owner admin API → 403
```

### AC-006 ~ AC-013 列表与筛选

```yaml
AC-006:
  unit:
    - filter card renders 6 controls height 40px

AC-007:
  integration:
    - GET /admin/users?keyword=foo matches username/display_name/email/phone

AC-009:
  unit:
    - summary grid 4 metric cards

AC-013:
  unit:
    - pagination default 10; page size select 10/20/50
```

### AC-014 ~ AC-020 弹窗

```yaml
AC-014:
  unit:
    - modal field order: username, avatar, nickname, role (single column)

AC-016:
  unit:
    - username validation 4-32 + format
  integration:
    - POST invalid username → 400 USER_INVALID_USERNAME

AC-017:
  unit:
    - edit mode username input readOnly

AC-020:
  unit:
    - create success toast 用户已创建
```

### AC-021 ~ AC-028 操作

```yaml
AC-021:
  integration:
    - reset password returns password length >= 12

AC-026:
  unit:
    - delete button disabled when last_login_at set
  integration:
    - PATCH deleted on logged-in user → 400

AC-025:
  integration:
    - disabled user login → 403
```

### AC-029 ~ AC-045 布局 / API / 技术

```yaml
AC-032:
  integration:
    - all admin/users endpoints employee → 403

AC-033:
  manual:
    - orval generate succeeds

AC-035:
  integration:
    - schema supports deleted status and avatar_object_key

AC-039:
  manual:
    - TSX grep no raw hex in user-management feature

AC-041:
  unit:
    - vitest coverage per tasks §7
```

## 回归范围

- REQ-0001 auth login/logout/me 不退化
- REQ-0004 AdminLayout / dashboard 仍可访问（employee/admin）

## 验收命令

```bash
cd src/backend && uv run pytest tests/ -k "user or admin_users"
cd src/web && npx vitest run src/features/admin src/pages/admin
cd src/web && npm run build
./scripts/generate-openapi-client.sh
```
