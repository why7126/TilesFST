---
bug_id: BUG-0016-admin-list-status-action-confirm-missing
status: pending_review
created_at: 2026-06-27 13:12:51
updated_at: 2026-06-27 13:12:51
root_cause_type: code/design/frontend-ui
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code / design / frontend-ui**（管理端状态操作确认交互未横向统一） |
| 引入阶段 | 用户管理初版（`add-user-management`）、SKU 管理初版（`add-tile-sku-management`）；品牌/类目确认分别在 Sprint-002 专项 change 中补全 |
| 责任模块 | `UserManagementPage.tsx`、`TileSkuManagementPage.tsx` |
| 关联后端 | 无缺陷；`updateUserStatus`、`publishTileSku`、`unpublishTileSku` 调用逻辑正常 |

## 2. 直接原因

### 2.1 用户冻结/解冻：行内 handler 直接调 API

`UserManagementPage.tsx` 中 `handleFreeze` 在按钮 `onClick` 后立即执行：

```tsx
const handleFreeze = async (user: UserAdminItem) => {
  const next = user.status === 'disabled' ? 'active' : 'disabled';
  await updateUserStatus(user.id, next);
  // ...
};
```

未设置 `statusConfirmTarget`（或等价 state），也未渲染 confirm modal。与同项目 `BrandManagementPage` / `TileCategoryManagementPage` 的 `openStatusConfirm` → modal → `handleStatusConfirm` 模式不一致。

### 2.2 用户删除：使用浏览器原生 `window.confirm`

`handleDelete` 使用：

```tsx
if (!window.confirm(`确认删除用户 ${user.username}？`)) return;
```

虽有二次确认门槛，但非 DS modal（`modal-backdrop` / `modal-card`），与品牌/类目/ SKU 删除 modal 形态不一致，且无法统一 a11y 与视觉验收。

### 2.3 SKU 上架/下架/恢复：行内 handler 直接调 API

`TileSkuManagementPage.tsx` 中：

```tsx
const handlePublish = async (item: TileSkuAdminItem) => {
  await publishTileSku(item.id);
};
const handleUnpublish = async (item: TileSkuAdminItem) => {
  await unpublishTileSku(item.id);
};
```

操作列按钮 `onClick={() => void handlePublish(item)}` 无前置确认。同页「删除」已使用 `deleteTarget` modal，上下架未复用相同模式。

### 2.4 测试固化「无确认」行为

- `UserManagementPage.test.tsx`：`shows fixed toast after freeze action` 断言点击「冻结」后 **立即** 调用 `updateUserStatusMock`。
- `TileSkuManagementPage.test.tsx`：`calls publishTileSku when restore is clicked` 断言点击「恢复」后 **立即** 调用 `publishTileSkuMock`。

自动化与实现相互印证，缺陷为稳定现状而非偶发。

## 3. 根本原因

### 3.1 二次确认为「按页专项交付」，非管理端横切规范

REQ-0007（类目启停）、REQ-0008（品牌启停）以独立 fix-* change 落地，归档 scope 限定单页，**未**在 OpenSpec 或共享组件层定义「所有 destructive / 状态变更行内操作 MUST modal 确认」的横切 requirement。后续用户/SKU 页迭代未触发同类专项，继续沿用初版「点击即 API」模板。

### 3.2 各页独立复制 modal 片段，无共享 Confirm 契约

品牌/类目/SKU 删除、品牌/类目启停均在页面内联 JSX 复制 `modal-backdrop` 结构，无 `AdminConfirmDialog` 或 workflow 检查清单。新增列表页或新操作类型时，开发者易遗漏确认步骤。

### 3.3 父需求 AC 对用户/SKU 确认粒度不足

- REQ-0005 `acceptance.md` 明确重置密码「弹出确认」，冻结/删除 AC 仅描述结果与 Toast，**未**规定 modal 结构与「确认前不得调 API」。
- REQ-0006 上下架 business-flow 未写二次确认；OpenSpec `web-client` SKU 上下架 scenario 仅要求「点击 MUST 调用 publish」。

产品一致性缺口在 capture 阶段暴露；品牌侧已由 REQ-0008 闭环，用户/SKU 仍为遗漏面。

### 3.4 capture 记录部分过时

`/capture` 将「品牌列表缺少确认」与用户/SKU 一并记录；`/bug-explore` 证伪品牌缺口（`fix-brand-status-confirm` 已 archive）。根因上 capture 范围偏宽，**实际代码缺口**为用户冻结/解冻、SKU 上下架、用户删除 confirm 形态。

## 4. 触发条件

满足以下条件即可稳定复现：

1. `admin` 登录 Web 管理端（用户管理）；或 `admin` / `employee` 登录（SKU 管理）；
2. 进入 `/admin/users` 或 `/admin/tile-skus`；
3. 点击行内「冻结」「解冻」「上架」「下架」「恢复」→ **无 modal，直接生效**；
4. 用户页点击「删除」（从未登录用户）→ **浏览器原生 confirm**，非 DS modal。

**不应复现（对照）**：`/admin/brands`、`/admin/tile-categories` 启停/删除均有 modal。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| API 未返回或权限错误 | 否；无确认时 API 正常执行 |
| modal CSS 未加载导致「看不见」 | 否；用户/SKU 缺口页根本未渲染 confirm JSX |
| 品牌 fix 回退 | 否；`BrandManagementPage` 仍有 `statusConfirmTarget` 与 vitest |
| 后端缺少 confirm 端点 | 否；纯前端交互缺口 |
| BUG-0017 重置密码 UI | 独立缺陷；本 BUG 不含重置密码 modal 统一 |

## 6. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否 Design System 缺陷 | 是，状态操作 confirm 模式未统一 |
| 主要修复面 | 用户页 freeze/delete modal；SKU 页 publish/unpublish modal；Vitest；OpenSpec delta |

## 7. 修复建议（供 bug-opsx）

1. `UserManagementPage`：新增 `statusConfirmTarget` + 独立 `deleteTarget` modal（对齐类目删除结构）。
2. `TileSkuManagementPage`：新增 `statusConfirmTarget` + action（publish / unpublish / restore）或分 target state。
3. 文案参考：`REQ-0007` / `REQ-0008` prototype context；用户冻结正文含「禁止登录」等后果说明。
4. 更新 vitest：确认前 mock MUST NOT 调用；取消/遮罩后不调用；确认后调用 + Toast。
5. OpenSpec：`fix-admin-list-status-action-confirm`；ADDED/MODIFIED `web-client` 用户冻结/解冻与 SKU 上下架确认 requirement。
6. 可选：抽取共享 confirm 组件（非阻塞）。
