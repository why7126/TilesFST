---
title: 需求追踪
purpose: 记录 REQ-0004 管理后台首页的来源、关联文档、迭代与 OpenSpec 追踪
content: 基于 requirement.md 与项目目录结构维护
source: AI 根据 PRD 生成，项目团队确认
update_method: 状态、迭代或 OpenSpec 变更时同步更新
owner: 产品负责人
status: archived
note: add-admin-home 已归档至 openspec/changes/archive/2026-06-15-add-admin-home
---

# 需求追踪

## 1. 基本信息

```yaml
requirement_id: REQ-0004
requirement_name: admin-home
requirement_type: 管理端 / 工作台 UI
priority: P0
status: applied
source: 管理端登录后工作台入口 V5 精简版
target_users:
  - 企业内部员工
  - 系统管理员
target_clients:
  web_admin: 本期实现
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
iteration: sprint-002
change_id: add-admin-home
related_requirements:
  - REQ-0001-user-login
related_changes:
  - add-admin-home
openspec_changes:
  - change_id: add-admin-home
    type: add
    status: archived
    iteration: sprint-002
    requirement_id: REQ-0004-admin-home
    strategy: css-port
    archive_path: openspec/changes/archive/2026-06-15-add-admin-home
```

## 2. 关联文档

| 文档 | 路径 | 状态 |
|---|---|---|
| 需求 PRD | `requirement.md` | 已有 |
| 用户故事 | `user-stories.md` | 已补齐 |
| 业务流程 | `business-flow.md` | 已补齐 |
| 验收标准 | `acceptance.md` | 已补齐 |
| Web 原型图 | `prototype/web/admin-home.png` | 已有 |
| Web 原型 HTML | `prototype/web/admin-home.html` | 已有 |
| Web 原型说明 | `prototype/web/admin-home-context.md` | 已有 |

## 3. OpenSpec 追踪

| 阶段 | 路径 | 状态 |
|---|---|---|
| Change | `openspec/changes/archive/2026-06-15-add-admin-home/` | archived |
| 依赖 Spec | `openspec/specs/auth/spec.md` | 已生效（登录、logout、路由守卫） |
| 目标 Spec | `openspec/specs/admin-dashboard/spec.md` | 已合并 |

## 4. 实现追踪（当前代码基线）

| 模块 | 路径 | 现状 |
|---|---|---|
| 路由 | `src/web/src/app/App.tsx` | `/admin/dashboard` 已注册 |
| 布局 | `src/web/src/pages/admin/AdminLayout.tsx` | 顶栏 + 退出按钮，**需重构**为 Sidebar 布局 |
| 首页 | `src/web/src/pages/admin/DashboardPage.tsx` | 占位文案，**需实现**三模块工作台 |
| 目录 Sidebar | `src/web/src/shared/ui/sidebar.tsx` | 店主端筛选 Sidebar，**不可直接复用**为管理导航 |
| 认证 | `src/web/src/features/auth/` | 可复用 logout、me、ProtectedRoute |

## 5. 视觉验收 Trace Checklist

原型优先级（实现 OpenSpec 时 MUST 写入 design.md）：

```text
1. prototype/web/admin-home.html
2. prototype/web/admin-home.png
3. prototype/web/admin-home-context.md
4. issues/.../acceptance.md
5. rules/ui-design.md
6. openspec/specs/
```

- [ ] Logo 为 TILESFST
- [ ] Sidebar 固定 100vh
- [ ] 右侧独立滚动
- [ ] 用户菜单在 Sidebar 底部，无直接退出按钮
- [ ] 下拉框含个人资料、密码修改、退出登录 + 分隔线
- [ ] 快捷操作仅 4 项
- [ ] 无 V4 已删除模块（欢迎区、待办等）
- [ ] PNG 与实现并排验收

## 6. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-14 | 需求入库 | 初始 requirement + prototype |
| 2026-06-14 | `/requirement-to-change` | 补齐 user-stories / business-flow / acceptance / trace |
| 2026-06-14 | `/requirement-to-opsx` | 创建 `add-admin-home` OpenSpec（CSS Port 策略） |
| 2026-06-15 | `/opsx-archive` | `add-admin-home` 归档；specs 合并至 `admin-dashboard` + `web-client` |

## 7. 后续动作

1. Sprint 002 验收：`iterations/sprint-002/acceptance-report.md` 勾选 REQ-0004 项。
2. 继续 **`/opsx-apply add-user-management`**（REQ-0005）。
