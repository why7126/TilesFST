---
change_id: fix-admin-content-padding-too-large
title: 管理端全局内容区域间距与宽度收敛修复 - 设计
created_at: 2026-07-03 18:41:48
updated_at: 2026-07-03 18:41:48
source_bug: BUG-0054-admin-content-padding-too-large
status: proposed
---

# Design

## Context

BUG-0054 指向管理端全局 Shell 内容区的信息密度问题。当前实现与 specs 中仍多处保留旧目标值：

- `.admin-shell .main-content { padding: 48px 56px 72px; }`
- `.admin-shell .content-inner { max-width: 1080px; }`
- SKU 页存在 `1120px` 页面级 override。
- 系统设置页存在 `settings-content-inner { max-width: 1080px; }`。

产品已确认不采用原 `REQ-0013` 中较保守的 `32px 32px 72px` 作为最终目标，而采用更紧凑但仍保留呼吸感的 `24px 24px 48px` 方案。

## Bug Analysis Report

| 项 | 内容 |
|---|---|
| 现象 | 管理端全局右侧主内容区留白偏大，内容显示面积偏小 |
| 复现 | 登录管理端，打开 `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`、`/admin/settings` 等页面，在 1440/1920 桌面视口观察主内容区 |
| 根因分类 | code / design / test |
| 直接原因 | 全局 Shell 仍保留旧 padding 和 1080px content-inner 上限，部分页面继续使用页面级 max-width |
| 根本原因 | 管理端内容宽度策略没有单一事实源，旧 `REQ-0013` 目标值未按当前用户反馈更新，测试未覆盖布局 token |
| 严重等级 | medium |
| 关联需求 | `REQ-0013-admin-shell-padding-refine` |
| API 影响 | 无 |
| DB 影响 | 无 |
| Orval 影响 | 无 |

## 修复方案

### D1. 全局 Main Content Padding

`admin-home.css` 作为 Admin Shell 样式入口，应维护统一布局 token 或等价规则：

- desktop（>1023px）：`padding: 24px 24px 48px`
- tablet（≤1023px）：`padding: 20px 16px 40px`
- mobile（≤639px）：`padding: 16px 12px 32px`

右侧内容区仍 MUST 保持独立纵向滚动，且 Shell 层不得出现横向滚动条。

### D2. Content-inner 宽度策略

全局 `.content-inner` 不再使用 1080px 硬上限。实现可选择以下之一，并在实现 trace 中记录最终选择：

1. `max-width: 100%`
2. `max-width: min(1440px, 100%)`

建议优先采用 `min(1440px, 100%)`，在极宽屏上保留基本阅读舒适度；若验收发现列表页仍偏窄，可切换到 `100%`。

### D3. 清理页面级宽度分叉

实现必须清理或改造以下分叉：

- `tile-sku-management.css` 中 `:has(.sku-page-hero) .content-inner { max-width: 1120px }`
- `system-settings.css` 中 `.settings-content-inner { max-width: 1080px }`

如果系统设置页仍需要较窄表单段落，应使用内部表单 grid / panel max-width，而不是重新锁定整个页面内容容器。

### D4. 页面回归

最小视觉回归页面：

- `/admin/logs`
- `/admin/tile-skus`
- `/admin/users`
- `/admin/dashboard`
- `/admin/settings` 或 `/admin/settings/basic`

验收视口：

- 1440px desktop expanded
- 1920px desktop expanded
- desktop collapsed sidebar
- ≤1023px tablet
- ≤639px mobile smoke

### D5. 测试策略

更新或新增前端测试/静态断言：

1. `AdminLayout` 相关测试断言 Shell 仍渲染 `main-content` / `content-inner` 并支持 sidebar collapsed 状态。
2. 样式静态测试断言 `admin-home.css` 不再包含 `padding: 48px 56px 72px` 与 `.content-inner max-width: 1080px`。
3. 样式静态测试断言 SKU、系统设置等页面不再包含与全局 Shell 冲突的 content max-width。
4. 保持 `AdminSidebar.collapse.test.tsx`、`AdminLayout.test.tsx` 和受影响页面 smoke 测试通过。

## Risks

| 风险 | 缓解 |
|---|---|
| 全局 padding 过小导致 Dashboard 或表单贴边 | 采用 24px desktop 起步，覆盖 Dashboard / settings 视觉回归 |
| 移除页面级 max-width 后宽表格表现不同 | 针对 SKU、日志审计、用户列表做基准页验收 |
| 旧 specs 中仍保留 1080/1120 要求 | 本 Change 同步 MODIFIED 相关 Requirement |
| 与正在开发的日志审计 UI Change 交叉 | 将本 Change 限定为 Shell / content width，不改日志功能、API、数据 |

## Non-Goals

- 不调整 Sidebar 展开/收起宽度（264px / 72px 保持）。
- 不改导航项、权限、路由守卫、登录态或 localStorage 侧栏偏好。
- 不改后端 API、数据库、Orval、Docker Compose、MinIO。
- 不重做管理端页面组件结构或业务字段。
