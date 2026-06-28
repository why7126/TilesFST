---
bug_id: BUG-0033-banner-modal-form-layout-overflow
status: pending_review
created_at: 2026-06-28 16:17:14
updated_at: 2026-06-28 16:17:14
related_requirement: REQ-0016-banner-management
---

# 回归验收标准

> 修复本缺陷 MUST 满足 REQ-0016 **AC-024**（弹窗 640px / 92vh / 内容可滚动）、**AC-027**（含运营备注公共字段）、**AC-051**（modal 并排），且不得回归 AC-025～AC-039 弹窗功能。

## AC-001 弹窗主体 MUST 可垂直滚动（REQ-0016 AC-024）

**Given** 管理员已登录，视口高度 ≤ 900px（或 1080p 浏览器非最大化）  
**When** 打开「新增 Banner」或「编辑 Banner」弹窗（任一跳转类型）  
**Then** 弹窗 `.modal-body` MUST 出现垂直滚动条或支持滚轮/触控板滚动  
**And** 用户 MUST 能滚动至表单最底部（含运营备注）

## AC-002 页眉与页脚 MUST 保持可达

**Given** 弹窗已打开且内容超出视口  
**When** 用户滚动内容区  
**Then** 标题、关闭按钮 MUST 保持可见（固定于头部）  
**And** 「取消 / 保存 Banner」footer MUST 保持可见且可点击（固定于底部）

## AC-003 运营备注 textarea MUST 占满整行

**Given** 弹窗已打开  
**When** 观察「运营备注」字段  
**Then** `textarea` MUST 在 `.banner-form-row.full` 容器内横向占满弹窗内容区宽度（`width: 100%`）  
**And** MUST 具备固定高度约 72px 与 `resize: none`（对齐 `banner-management-modal-*.html` port CSS）  
**And** MUST NOT 出现仅占半列或浏览器默认窄宽度 textarea

## AC-004 运营备注 placeholder MUST 与其他字段一致

**Given** 弹窗已打开且备注为空  
**When** 对比「运营备注」placeholder 与「Banner 标题」input placeholder  
**Then** 字号 MUST 为 12px（与同弹窗 `.input` 一致）  
**And** placeholder 颜色 MUST 使用 semantic weak/muted token（对齐原型 `var(--weak)`）

## AC-005 弹窗尺寸 MUST 保持 640px / 92vh

**Given** 视口宽度 ≥ 640px  
**When** 打开弹窗  
**Then** 弹窗卡片宽度 MUST 为 640px（`.banner-modal-card`）  
**And** 最大高度 MUST 为 92vh  
**And** MUST NOT 因修复导致弹窗宽度或 max-height 偏离 REQ-0016 规范

## AC-006 四套 jump_type 弹窗 MUST 均通过滚动验收

**Given** 修复完成，视口 1440×900  
**When** 分别打开 `NO_JUMP`、`SKU_DETAIL`、`EXTERNAL_LINK`、`TOPIC_PAGE` 新增弹窗并滚动到底部  
**Then** AC-001～AC-002 MUST 全部通过  
**And** 条件字段显隐 MUST 仍符合 AC-031～AC-038（不得回归）

## AC-007 视口回归矩阵

**Given** 修复完成  
**When** 在以下视口打开 `SKU_DETAIL` 新增弹窗并滚动到底部  
**Then** AC-001～AC-003 MUST 通过：

| 视口 | 说明 |
|------|------|
| 1440×900 | 常见笔记本 |
| 1280×720 | 矮视口 |
| 1920×1080 非全屏 | 浏览器窗口约 900px 高 |

## AC-008 修复范围 MUST 为纯前端布局

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 引入新的后端校验逻辑

## AC-009 Design System 约束 MUST 满足

**Given** 修复完成  
**When** 检查 Web UI 修改  
**Then** MUST 使用 semantic token（`var(--admin-*)` / Tailwind semantic class）  
**And** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的局部样式

## AC-010 弹窗 HTML 并排验收 MUST 通过（REQ-0016 AC-051）

**Given** 修复完成  
**When** 在 1440×1024 并排对比 `/admin/banners` 弹窗与 `prototype/web/banner-management-modal-{type}.html`  
**Then** 640px 弹窗、运营备注整行宽度、modal-body 滚动行为 MUST 视觉/交互对齐原型  
**And** MUST 在 Change `trace.md` 记录并排验收结论

## AC-011 测试与记录 MUST 补齐

**Given** 进入 `fix-banner-modal-form-layout-overflow`（或等价 `fix-banner-modal-ui` Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 `BannerFormModal` 相关 Vitest（modal-body scroll 或 textarea 整行）  
**And** MUST 更新 Change trace checklist，关闭 AC-024 相关项

## AC-012 REQ-0016 AC-024 对齐确认

**Given** BUG-0033 修复完成  
**When** 对照 `issues/requirements/archive/REQ-0016-banner-management/acceptance.md` AC-024  
**Then** 「弹窗宽 640px，最大高 92vh，**内容可滚动**」MUST 全部满足
