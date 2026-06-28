---
title: 需求追踪
purpose: REQ-0003 追溯补登与实现文件关联
content: 产品决策补登，关联登录页 auth 实现路径
source: 追溯补登
update_method: 实现或 OpenSpec 创建时更新
owner: 产品负责人
status: ready
lifecycle_stage: archive
note: 追溯补登；本期仅 REQ 文档，不创建 OpenSpec change
---

# 需求追踪

## 1. 基本信息

```yaml
requirement_id: REQ-0003
requirement_name: 登录页左栏文案与布局微调
requirement_type: UI 调整 / 登录页
priority: P1
status: resolved
implementation_mode: retroactive  # 追溯补登
source: 产品方 Sprint 001 登录页视觉反馈
iteration: sprint-001
change_id: fix-login-left-panel-refine
related_requirements:
  - REQ-0001-user-login
  - REQ-0002-product-brand-login-simplify
openspec_changes:
  - change_id: fix-login-left-panel-refine
    type: fix
    status: archived
    archive_path: openspec/changes/archive/2026-06-14-fix-login-left-panel-refine/
    requirement_id: REQ-0003-login-left-panel-refine
```

## 2. 实现关联文件（变更范围）

| 路径 | 变更摘要 | 状态 |
|---|---|---|
| `src/web/src/features/auth/components/AuthBrandPanel.tsx` | `.brand-title` →「瓷砖信息管理后台」 | ✓ |
| `src/web/src/features/auth/components/LoginForm.tsx` | 移除「忘记密码？」；`.form-options` 左对齐 | ✓ |
| `src/web/src/features/auth/styles/login-page.css` | Logo 间距、stats z-index、material-board 缩小下移 | ✓ |
| `src/web/src/features/auth/components/LoginForm.test.tsx` | 断言无忘记密码 | ✓ |
| `src/web/src/features/auth/components/LoginPage.test.tsx` | 断言主标题文案 | ✓ |

**不在本需求范围（保持 REQ-0002）：**

| 路径 | 说明 |
|---|---|
| `src/web/index.html` | 浏览器标题仍为 TilesFST |
| `src/web/src/pages/admin/AdminLayout.tsx` | 管理端顶栏 TilesFST 不变 |
| `src/web/src/features/auth/components/AuthBrandPanel.tsx` `.logo` | 金色 TilesFST Logo 不变 |

## 3. 需求项与文件映射

```yaml
FR-001_brand_title:
  files:
    - src/web/src/features/auth/components/AuthBrandPanel.tsx
  field: .brand-title → 瓷砖信息管理后台

FR-002_hide_forgot_password:
  files:
    - src/web/src/features/auth/components/LoginForm.tsx
    - src/web/src/features/auth/styles/login-page.css  # 可选 .login-link { display: none }

FR-003_logo_spacing:
  files:
    - src/web/src/features/auth/styles/login-page.css
  selectors:
    - .login-shell .brand-top
    - .login-shell .brand-content

FR-004_stats_not_occluded:
  files:
    - src/web/src/features/auth/styles/login-page.css
  selectors:
    - .login-shell .stats-card
    - .login-shell .material-board
```

## 4. 与 REQ-0002 冲突决议

| 检查项 | REQ-0002 | REQ-0003 | 决议 |
|---|---|---|---|
| `.logo` | TilesFST | TilesFST | 不变 |
| `.brand-title` | TilesFST | 瓷砖信息管理后台 | **REQ-0003** |
| 忘记密码 | 占位可见 | 隐藏 | **REQ-0003** |
| 视口无滚动 | MUST | MUST 仍满足 | REQ-0002 保留 |

## 5. OpenSpec / 迭代

| 项目 | 状态 |
|---|---|
| OpenSpec Change | `openspec/changes/archive/2026-06-14-fix-login-left-panel-refine/` |
| 类型 | fix（CSS Port 微调） |
| 状态 | **archived** |
| 正式 Spec | `openspec/specs/web-client/spec.md`（+6 MODIFIED） |
| Sprint | sprint-001 |

## 6. 状态流转

| 日期 | 状态 | 说明 |
|---|---|---|
| 2026-06-14 | ready | 追溯补登：五件套创建，实现文件路径已登记 |
| 2026-06-14 | proposed | requirement-to-opsx 创建 fix-login-left-panel-refine |
| 2026-06-14 | in_sprint | 纳入 sprint-001（sprint.yaml / sprint.md 已更新） |
| 2026-06-14 | implemented | opsx-apply fix-login-left-panel-refine 完成 |
| 2026-06-14 | archived | `2026-06-14-fix-login-left-panel-refine`；web-client spec +6 MODIFIED |
