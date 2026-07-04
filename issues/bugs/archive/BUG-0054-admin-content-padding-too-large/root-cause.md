---
bug_id: BUG-0054-admin-content-padding-too-large
title: 管理端全局右侧内容区域内边距过大 - 根因分析
severity: medium
status: pending_review
owner: product
created_at: 2026-07-03 18:24:49
updated_at: 2026-07-03 18:24:49
related_requirement: REQ-0013-admin-shell-padding-refine
---

# 根因分析

## 直接原因

管理端全局 Shell 仍保留早期宽松布局值：

| 位置 | 当前表现 | 问题 |
|---|---|---|
| `.admin-shell .main-content` | `padding: 48px 56px 72px` | 左右与顶部留白偏大，压缩有效内容区 |
| `.admin-shell .content-inner` | `max-width: 1080px` | 宽屏下内容被硬上限限制，形成明显左右暗区 |
| SKU 页 `.content-inner` override | `max-width: 1120px` | 页面级宽度策略与全局 Shell 策略分裂 |
| 系统设置页 `.settings-content-inner` | `max-width: 1080px` | 继续绕开全局内容宽度策略 |

这些规则叠加后，即使视口宽度充足，管理端页面仍以较窄的中间内容区展示，造成用户反馈的“右侧内容区域内边距太大、内容显示略小”。

## 根本原因

`REQ-0013-admin-shell-padding-refine` 已定义过管理端 Shell 收窄与 content fluid 方向，但当前代码仍保留旧的 `48px 56px 72px`、`1080px` 等实现值，且部分业务页面继续通过页面级 CSS 覆盖内容宽度。

根因可以归纳为：

1. 全局 Shell spacing token 未完成落地或后续变更未覆盖当前页面体系。
2. 内容宽度策略没有单一事实源，`content-inner`、SKU 页 override、系统设置页内层容器各自控制 max-width。
3. 旧验收目标 `32px 32px 72px` 对当前用户反馈仍偏保守，且用户已确认希望更明显地收窄全局内容区留白。
4. 现有测试更偏向功能与导航行为，没有覆盖 Shell padding、content max-width、页面级 divergent override 这类视觉布局约束。

## 触发条件

满足以下条件时稳定触发：

1. 打开任一使用 `AdminLayout` 的 `/admin/*` 页面。
2. 视口为桌面或宽屏，例如 1440px、1920px。
3. 页面内容承载列表、筛选、指标卡或表格等需要横向空间的模块。
4. 观察主内容容器外侧留白和中间内容宽度。

典型页面：

- `/admin/logs`
- `/admin/tile-skus`
- `/admin/users`
- `/admin/dashboard`
- `/admin/system-settings`

## 分类

| 分类 | 判断 |
|---|---|
| code | 是，CSS 中全局 Shell 与页面级 max-width 规则需要调整 |
| design | 是，管理端全局内容密度与 spacing 策略需要重新确认 |
| db | 否，不涉及数据库结构或数据 |
| api | 否，不涉及接口契约或 Orval |
| security | 否，不涉及认证授权或敏感信息 |
| ui | 是，影响管理端全局布局和视觉一致性 |

## 关联实现点

- `src/web/src/features/admin/styles/admin-home.css`
- `src/web/src/features/admin/styles/tile-sku-management.css`
- `src/web/src/features/admin/styles/system-settings.css`
- `src/web/src/pages/admin/AdminLayout.tsx`
- `src/web/src/features/admin/components/AdminLayout.test.tsx`
- `src/web/src/features/admin/components/AdminSidebar.collapse.test.tsx`

## 修复方向建议

后续修复 Change 建议：

1. 将 desktop `.main-content` 调整为 `padding: 24px 24px 48px`。
2. 将 tablet `.main-content` 调整到 `20px 16px 40px` 量级。
3. 将 mobile `.main-content` 调整到 `16px 12px 32px` 量级。
4. 将 `.content-inner` 放宽为 `max-width: 100%` 或 `max-width: min(1440px, 100%)`，最终以评审结论为准。
5. 删除或改造 SKU 页、系统设置页等与全局策略冲突的页面级 max-width。
6. 补充测试或静态校验，防止重新引入 `1080px`、`1120px` 等 divergent content width。
