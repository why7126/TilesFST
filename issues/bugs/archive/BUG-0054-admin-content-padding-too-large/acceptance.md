---
bug_id: BUG-0054-admin-content-padding-too-large
title: 管理端全局右侧内容区域内边距过大 - 验收标准
severity: medium
status: pending_review
owner: product
created_at: 2026-07-03 18:24:49
updated_at: 2026-07-03 18:24:49
related_requirement: REQ-0013-admin-shell-padding-refine
---

# 验收标准

## AC-001 Desktop 主内容 padding 明显收窄

- [ ] 在 desktop 视口（>1023px）下，`.admin-shell .main-content` 使用 `padding: 24px 24px 48px` 或经评审确认的等价值。
- [ ] bottom padding 不再沿用旧的 `72px`，应按本 BUG 修正为 `48px` 量级。
- [ ] 主内容仍保持 `overflow: auto`，Shell 层不出现横向滚动条。

## AC-002 Content-inner 不再使用 1080px 硬上限

- [ ] `.admin-shell .content-inner` 不再使用 `max-width: 1080px`。
- [ ] 最终策略采用 `max-width: 100%` 或 `max-width: min(1440px, 100%)`，并在 Change 设计中明确。
- [ ] 1440px 与 1920px 视口下，内容区可明显利用更多横向空间。

## AC-003 页面级宽度分叉已清理

- [ ] SKU 页不再保留 `:has(.sku-page-hero) .content-inner { max-width: 1120px }` 这类 divergent override。
- [ ] 系统设置页不再通过 `settings-content-inner { max-width: 1080px }` 将页面重新限制到旧宽度。
- [ ] 全仓 Web 管理端 CSS 不新增与全局 Shell 策略冲突的 `content-inner` / `settings-content-inner` max-width。

## AC-004 Tablet 与 mobile padding 联动调整

- [ ] ≤1023px 视口下，`.main-content` padding 调整到 `20px 16px 40px` 量级或经评审确认的等价值。
- [ ] ≤639px 视口下，`.main-content` padding 调整到 `16px 12px 32px` 量级或经评审确认的等价值。
- [ ] tablet / mobile 下侧栏、用户菜单、折叠按钮既有响应式行为不被破坏。

## AC-005 基准页面视觉回归

- [ ] `/admin/logs`：指标卡、筛选区、日志表格显示面积明显增大。
- [ ] `/admin/tile-skus`：筛选区和 SKU 表格不再被旧 1120px 上限限制。
- [ ] `/admin/users`：用户列表、分页和操作列无错位。
- [ ] `/admin/dashboard`：指标卡和快捷入口不显得贴边、不过度拥挤。
- [ ] `/admin/system-settings`：表单区域跟随全局内容宽度策略，不再被旧 1080px 容器锁定。

## AC-006 视觉规范与 Token

- [ ] 修改使用既有 admin semantic token 或布局尺寸值，不新增裸 Hex。
- [ ] 不新增卡片套卡片、浮动页面段落卡等违反 Design System 的结构。
- [ ] 暗色旗舰风下仍保留必要呼吸感，内容不得贴住侧栏分割线或视口边缘。

## AC-007 自动化与静态回归

- [ ] `AdminLayout.test.tsx` 通过。
- [ ] `AdminSidebar.collapse.test.tsx` 通过。
- [ ] 新增或更新测试/静态断言，覆盖 `.main-content` padding、`.content-inner` max-width 与页面级 divergent override。
- [ ] 前端构建或等价校验通过。

## AC-008 范围不扩散

- [ ] 不修改后端 API。
- [ ] 不修改数据库结构。
- [ ] 不需要 Orval。
- [ ] 不影响店主端和小程序。
- [ ] 不改变侧栏展开/收起的持久化行为。
