---
title: 需求追踪
purpose: REQ-0002 追溯补登与 OpenSpec 关联
content: 实现先于文档，本文档补齐闭环
source: 追溯补登
update_method: change 归档时更新 status
owner: 产品负责人
status: resolved
note: 追溯补登，实现已在 src/ 完成
---

# 需求追踪

## 1. 基本信息

```yaml
requirement_id: REQ-0002
requirement_name: 产品品牌与登录页简化
requirement_type: 产品策略 / UI 调整
priority: P0
status: resolved
implementation_mode: retroactive  # 追溯补登
source: 产品方 Sprint 001 收尾确认
iteration: sprint-001
change_id: update-tilesfst-login-simplify
related_requirements:
  - REQ-0001-user-login
```

## 2. 已实现文件清单（追溯）

| 路径 | 变更摘要 |
|---|---|
| `src/web/index.html` | 页面标题 → TilesFST |
| `src/web/src/app/App.tsx` | 首页标题 → TilesFST |
| `src/web/src/features/auth/components/AuthBrandPanel.tsx` | Logo/主标题 → TilesFST |
| `src/web/src/pages/admin/AdminLayout.tsx` | 顶栏品牌 → TilesFST |
| `src/backend/app/main.py` | OpenAPI 标题 → TilesFST API |
| `src/web/src/features/auth/components/LoginForm.tsx` | 移除 ThirdPartyLoginSection |
| `src/web/src/features/auth/styles/login-page.css` | 视口锁定、移除企微 CSS |
| `src/web/src/features/auth/components/LoginForm.test.tsx` | 断言无企微入口 |
| `src/web/README.md` | 更新登录组件树说明 |

**已删除：**

- `src/web/src/features/auth/components/ThirdPartyLoginSection.tsx`
- `src/web/src/features/auth/components/WeComLoginButton.tsx`
- `src/web/src/features/auth/components/ThirdPartyLoginSection.test.tsx`

## 3. OpenSpec 追踪

```yaml
openspec_changes:
  - change_id: update-tilesfst-login-simplify
    type: update
    status: archived
    archive_path: openspec/changes/archive/2026-06-14-update-tilesfst-login-simplify/
    requirement_id: REQ-0002-product-brand-login-simplify
    modified_capabilities:
      - web-client
```

| 阶段 | 路径 | 状态 |
|---|---|---|
| Change | `openspec/changes/archive/2026-06-14-update-tilesfst-login-simplify/` | archived |
| 正式 Spec | `openspec/specs/web-client/spec.md` | 已更新 |

## 4. 冲突决议（相对 REQ-0001 原型）

| 检查项 | REQ-0001 HTML/PNG | REQ-0002 | 决议 |
|---|---|---|---|
| 产品 Logo 文案 | STONEX | TilesFST | REQ-0002 |
| 主标题 | 瓷砖信息管理平台 | TilesFST | REQ-0002 |
| 企微入口 | 有 | 无 | REQ-0002 REMOVED |
| 页面滚动 | 未强制 | 禁止整页纵向滚动 | REQ-0002 ADDED |

## 5. 状态流转

| 日期 | 状态 | 说明 |
|---|---|---|
| 2026-06-14 | draft | 代码先行合入（追溯补登） |
| 2026-06-14 | resolved | REQ 五件套 + OpenSpec change 补齐 |
