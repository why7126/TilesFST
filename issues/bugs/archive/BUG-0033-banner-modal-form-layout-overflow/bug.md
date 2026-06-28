---
bug_id: BUG-0033-banner-modal-form-layout-overflow
title: Banner 弹窗运营备注宽度不足且底部按钮超出弹窗无滚动
severity: high
status: draft
owner: product
discovered_at: 2026-06-28 16:04:18
environment: local|docker
related_requirement: REQ-0016-banner-management
related_change: add-banner-management
---

# 缺陷说明

Web 管理端 Banner 新增/编辑弹窗（`BannerFormModal`）表单布局与 REQ-0016 / 原型 `banner-management-modal-*.html` 不一致，导致内容溢出弹窗可视区域：

1. **运营备注宽度不足**：DOM 虽含 `banner-form-row full`（`grid-column: 1 / -1`），但 `banner-management.css` 未 port 原型中的 `.textarea { width: 100%; … }` 规则；全局 `user-management.css` 的 `.input/.select { width: 100% }` 也不覆盖 `.textarea`，备注框按浏览器默认宽度渲染。
2. **占位符字号偏大**：未 port 原型 `.textarea { font-size: 12px }` 与 `.textarea::placeholder { color: var(--weak) }`，placeholder 视觉大于同弹窗 `.input` 字段。
3. **弹窗内容区不可滚动**：`.banner-modal-card` 仅设 `max-height: 92vh`，缺少原型 `.modal-card { display:flex; flex-direction:column }` 与 `.modal-body { overflow: auto }`；矮视口或字段较多（如 `SKU_DETAIL`）时，底部「取消」「保存 Banner」被裁切且无法在弹窗内纵向滚动。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local `5173` 或 Docker `3000` 均可）。
2. 进入「Banner 管理」列表页（侧栏 OPERATIONS → Banner 管理，或 `/admin/banners`）。
3. 点击「+ 新增 Banner」或某行「编辑」，打开弹窗。
4. 观察「运营备注」文本框是否横向占满整行、placeholder 字号是否与「Banner 标题」等 input 一致。
5. 将浏览器视口高度缩小至约 900px 以下（或非全屏 1080p），或选择跳转类型 `SKU_DETAIL`（字段最多）。
6. 观察底部「取消」「保存 Banner」是否超出弹窗可视区域；在弹窗内容区尝试滚轮/触控板纵向滚动。
7. 可选：并排对照 `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-no-jump.html`。

# 期望结果

- 弹窗宽 640px、最大高 92vh，结构对齐原型（REQ-0016 AC-024）：
  - `.modal-card` 为纵向 flex 容器；
  - `.modal-body` 可纵向滚动，头/尾固定；
  - 底部操作按钮始终可访问。
- 「运营备注」`textarea` 占满整行（`width: 100%`），固定高度约 72px，`resize: none`，`font-size: 12px`，placeholder 颜色与其他字段一致。
- 视觉验收：1440×1024 及矮视口（≤900px 高）下四套 `jump_type` 弹窗均可完整操作（AC-051 并排参考）。

# 实际结果

- `banner-management.css` 中 `.banner-modal-card` 仅有 `width: 640px; max-height: 92vh`，**未**配置 flex 布局与 `.modal-body` 滚动。
- `BannerFormModal.tsx` 使用 `className="textarea"`，但模块 CSS **未**定义 `.textarea` 宽度、字号与 placeholder 样式。
- 运营备注框宽度不足、placeholder 偏大；矮视口下底部按钮超出弹窗且无法滚动，与 `capture.md` 描述一致。
- `add-banner-management` trace checklist #8 仅验「640px + 无状态块」，**未**关闭 AC-024「内容可滚动」。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / Banner 弹窗 | 新增、编辑弹窗在常见笔记本视口下无法点击保存/取消 |
| REQ-0016 验收 | AC-024（92vh 可滚动）、AC-051（modal PNG/HTML 并排）未达标 |
| 关联 Change | `add-banner-management`（sprint-003，已 applied）交付即存在 |
| 同域 BUG | 可与 BUG-0031～0035（Banner 弹窗 UI）合并为同一 `fix-*` change |
| 同类先例 | BUG-0011（SKU 弹窗滚动）、BUG-0028（规格弹窗 textarea 宽度） |

不影响 API 契约、SQLite  schema、权限边界、小程序或店主端。

# 严重等级说明

严重程度为 `high`。

理由：

- 在典型矮视口下**阻断** Banner 新增/编辑的保存与取消操作，属于功能性缺陷而非纯视觉瑕疵。
- 修复范围小（`banner-management.css` CSS port，必要时微调 `BannerFormModal` 结构），无后端或数据迁移风险。
- 与 REQ-0016 明确要求的内容区可滚动直接冲突；`SKU_DETAIL` 等分支字段较多时最易触发。

# 代码线索

| 线索 | 路径 |
|---|---|
| Banner 弹窗组件 | `src/web/src/features/admin/components/BannerFormModal.tsx` |
| 弹窗样式（缺 scroll + textarea port） | `src/web/src/features/admin/styles/banner-management.css` |
| 全局 input 规则（不含 textarea） | `src/web/src/features/admin/styles/user-management.css` |
| 弹窗原型 HTML | `issues/requirements/archive/REQ-0016-banner-management/prototype/web/banner-management-modal-*.html` |
| SKU 弹窗 scroll 参考 | `src/web/src/features/admin/styles/tile-sku-management.css` → `.sku-modal-card .modal-body` |
| 品牌 textarea 参考 | `src/web/src/features/admin/styles/brand-management.css` → `.brand-textarea` |
| 关联 Change / spec | `openspec/changes/add-banner-management/`（AC-024） |
| UI 规范 | `rules/ui-design.md` |
