---
bug_id: BUG-0054-admin-content-padding-too-large
title: 管理端全局右侧内容区域内边距过大
severity: medium
status: approved
owner: product
discovered_at: 2026-07-03 13:15:19
environment: local
related_requirement: REQ-0013-admin-shell-padding-refine
related_change: null
created_at: 2026-07-03 18:11:20
updated_at: 2026-07-03 18:32:09
---

# BUG-0054 管理端全局右侧内容区域内边距过大

## 现象

管理端右侧主内容区域的全局内边距和内容宽度限制偏保守，导致多个管理页面在桌面宽屏下有效内容区域偏小。用户以「系统 / 日志审计」页面截图举例：主内容与侧栏之间、主内容右侧边缘以及页面顶部均存在较明显空白，指标卡、筛选区和表格没有充分利用横向空间。

该问题不是日志审计页单页问题，而是管理端 Shell / 主内容容器的全局布局策略问题。

## 复现步骤

1. 使用后台账号登录 Web 管理端。
2. 打开任一使用管理端 Shell 主内容容器的页面，例如 `/admin/logs`、`/admin/tile-skus`、`/admin/users`、`/admin/dashboard`。
3. 在桌面视口下观察右侧主内容区域与侧栏、视口右侧、页面顶部之间的留白。
4. 对照 `screenshots/admin-content-padding-example.png`，确认中间有效内容区被过大 padding 和宽度上限压缩。

## 期望结果

- 管理端全局主内容区域应明显收窄无效留白，提升列表、筛选、指标卡、表格和表单的可用宽度。
- Desktop 全局主内容 padding 建议调整为 `24px 24px 48px`，兼顾信息密度与暗色界面的呼吸感。
- `content-inner` 不应继续使用 `1080px` 硬上限；建议放宽为 `max-width: 100%` 或 `max-width: min(1440px, 100%)`。
- SKU、系统设置等页面不应继续保留与全局策略冲突的页面级 `content-inner` / `settings-content-inner` 宽度上限。
- Tablet / mobile 也应联动收窄，例如 tablet 可参考 `20px 16px 40px`，mobile 可参考 `16px 12px 32px`。
- 调整后仍应遵守 Design System：暗色旗舰风、semantic token、无新增裸 Hex、无 Shell 级横向滚动。

## 实际结果

当前实现仍保留较大的历史布局值：

- `.admin-shell .main-content` 使用 `padding: 48px 56px 72px`。
- `.admin-shell .content-inner` 使用 `max-width: 1080px`。
- SKU 页存在 `.admin-shell:has(.sku-page-hero) .content-inner { max-width: 1120px; }` 页面级覆盖。
- 系统设置页存在 `.settings-content-inner { max-width: 1080px; }` 页面级宽度限制。

这些规则叠加后，在宽屏和复杂列表页中会形成明显无效暗区，使页面看起来偏小、偏空。

## 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 Shell | 全局主内容区域信息密度偏低 |
| 日志审计页 | 指标卡、筛选区、日志表格显示面积偏小 |
| SKU / 用户 / Banner / 类目 / 规格等列表页 | 表格和筛选区域无法充分利用横向空间 |
| Dashboard | 指标卡与快捷入口在宽屏下可读但空间利用不足 |
| 系统设置页 | 仍受独立 `settings-content-inner` 宽度限制影响 |
| 店主端 / 小程序 | 不涉及 |
| 后端 API / 数据库 / Orval | 不涉及 |

## 严重等级说明

严重等级为 `medium`。

理由：

- 该问题不阻断用户登录、查询、编辑、保存等核心功能。
- 该问题影响管理端全局页面的信息密度与视觉体验，尤其对宽屏下高频使用的列表、筛选和日志审计场景影响明显。
- 该问题与 `REQ-0013-admin-shell-padding-refine` 的目标一致，但当前实现仍保留旧 spacing / width 策略，属于既有 UI 布局体验偏差。

## 待确认

- `content-inner` 最终采用 `max-width: 100%` 还是 `max-width: min(1440px, 100%)`。
- 是否需要同步修订 `REQ-0013` 既有验收标准中 `32px 32px 72px`、`min(1400px, 100%)` 等旧目标值。
- 视觉验收是否以 1440px、1920px、collapsed、tablet 四组视口作为最低覆盖。
