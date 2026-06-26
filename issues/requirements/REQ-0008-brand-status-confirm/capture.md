---
req_id: REQ-0008-brand-status-confirm
status: captured
recorded_at: 2026-06-26
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0005-brand-management
---

# 一句话

品牌列表页：点击「启用」与「停用」时均需二次确认，避免误操作。

# 原始描述

新增需求，品牌列表页，点击启用和停用的时候，均需要用户进行二次确认。

# 分类结论（需求 vs 缺陷）

| 项 | 归类 | 理由 |
|----|------|------|
| 启停二次确认 | **需求** | 父需求 `REQ-0005-brand-management` 当前为直接启停；删除已有确认弹窗，启停属新增交互策略，非功能错误 |

**非 BUG**：当前实现与既有 PRD/验收一致；属体验增强，对齐类目管理页 `REQ-0007-tile-category-management-refine` 已落地的启停确认模式。

# 参考实现

- 当前品牌页：`src/web/src/pages/admin/BrandManagementPage.tsx`（`handleToggleStatus` 直接调用 API；删除走 `deleteTarget` 确认弹窗）
- 同类参考：`REQ-0007-tile-category-management-refine` → `prototype/web/tile-category-status-confirm-context.md`
- 父需求：`issues/requirements/REQ-0005-brand-management/`

# 待澄清

- [x] 启停确认弹窗文案是否与删除确认、类目启停确认风格一致 → **是**（见下方「文案约定」）
- [x] 停用正文是否需补充业务说明 → **是**，需说明「停用后前台将不再展示该品牌」
- [ ] 变更类型：建议 `fix-brand-status-confirm`（对齐 `fix-tile-category-management-refine`）

# 文案约定

与品牌删除弹窗（`modal-card` / `modal-head` / `modal-footer`）及类目启停确认（REQ-0007）保持一致：

## 停用

| 元素 | 内容 |
|------|------|
| 标题 | 停用品牌 |
| 正文 | 确认停用品牌「{name}」？停用后前台将不再展示该品牌。 |
| 取消 | 取消 |
| 确认 | 确认停用（主按钮） |

## 启用

| 元素 | 内容 |
|------|------|
| 标题 | 启用品牌 |
| 正文 | 确认启用品牌「{name}」？ |
| 取消 | 取消 |
| 确认 | 确认启用（主按钮） |

## 交互

- 点击列表「启用」/「停用」仅打开弹窗，不调用 API
- 确认后调用 `POST .../enable` 或 `POST .../disable`
- ESC / 遮罩 / × 等同「取消」
- 复用现有删除确认弹窗样式类（`modal-backdrop`、`modal-card` 等）

# 探索结论

- **文案风格**：与删除确认、类目启停确认一致——标题为动作名（停用品牌 / 启用品牌），正文以「确认…「{name}」？」开头，主按钮为「确认停用 / 确认启用」。
- **停用说明**：正文 MUST 补充「停用后前台将不再展示该品牌。」，与类目停用「停用后前台将不再展示该类目。」对齐。
- **启用说明**：正文仅确认意图，不额外补充业务说明（与类目启用一致）。
