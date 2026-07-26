---
title: add-admin-home 测试计划
purpose: 映射 REQ-0004 验收标准至单元/集成/E2E 测试
content: 基于 acceptance.md 与 tasks.md
source: AI 根据 OpenSpec change 生成
update_method: 实现或验收变更时同步更新
owner: 测试负责人
status: ready
note: Sprint 002 / REQ-0004
---

# 测试计划

## 映射概览

```yaml
change_id: add-admin-home
requirement_id: REQ-0004-admin-home
iteration: sprint-002
```

## AC → Test Case

### AC-001 ~ AC-005 布局与鉴权

```yaml
AC-001:
  unit:
    - DashboardPage renders when authenticated
  integration:
    - ProtectedRoute allows admin to /admin/dashboard
  e2e:
    - login → dashboard visible

AC-005:
  integration:
    - unauthenticated navigate to /admin/dashboard → /admin/login
```

### AC-006 ~ AC-010 Sidebar 导航

```yaml
AC-006:
  unit:
    - AdminSidebar renders TILESFST logo text
    - no STONEX in document

AC-007:
  unit:
    - OPERATIONS section contains 5 nav items

AC-009:
  unit:
    - home nav item has active class on /admin/dashboard

AC-010:
  unit:
    - non-home nav click shows placeholder (toast or noop)
```

### AC-011 ~ AC-018 用户菜单

```yaml
AC-011:
  unit:
    - user menu rendered at sidebar footer

AC-013:
  unit:
    - no standalone logout button below user trigger

AC-014:
  unit:
    - click user trigger toggles aria-expanded and dropdown visible

AC-015:
  unit:
    - dropdown contains 个人资料、密码修改、退出登录

AC-017:
  integration:
    - logout menuitem calls logout and navigates to /admin/login
```

### AC-019 ~ AC-029 Dashboard 内容

```yaml
AC-019:
  unit:
    - DashboardMetrics renders 4 metric cards

AC-022:
  unit:
    - DashboardQuickActions renders exactly 4 items
    - titles match 新增 SKU/品牌/类目/Banner

AC-023:
  unit:
    - no 导入 SKU/导入图片/价格管理/操作日志 in document

AC-026:
  unit:
    - DashboardRecentUpdates table has 4 columns

AC-029:
  unit:
    - no welcome/todo/quality/risk modules in document
```

### AC-030 ~ AC-036 技术

```yaml
AC-035:
  unit:
    - AdminLayout.test.tsx smoke
    - AdminUserMenu.test.tsx dropdown + logout
    - DashboardPage.test.tsx content modules

AC-036:
  manual:
    - /design-system shows Admin Shell preview (if implemented)
```

### AC-037 ~ AC-042 UI

```yaml
AC-037:
  manual:
    - 1280×1024 side-by-side admin-home.png vs /admin/dashboard
    - trace.md PNG checklist all pass or documented deviation
```

## 测试命令

```bash
cd src/web && npx vitest run src/features/admin src/pages/admin
cd src/web && npm run build
./scripts/docker-up.sh
```

## 回归范围

- REQ-0001：登录、路由守卫、logout API（行为不变，入口 UI 变更）
- 无后端回归

## 通过标准

1. 全部 automated tests pass
2. build / docker web pass
3. PNG checklist ≥18 项 pass（或记录可接受偏差）
4. acceptance-report.md 功能项全部勾选
