---
bug_id: BUG-0016-admin-list-status-action-confirm-missing
title: 管理端用户/SKU 列表状态变更操作缺少二次确认弹窗
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 12:03:34
environment: local|docker
related_requirement: REQ-0008-brand-status-confirm
related_change: fix-brand-status-confirm
related_bugs:
  - BUG-0017-user-reset-password-confirm-ui-inconsistency
suggested_fix_change: fix-admin-list-status-action-confirm
related_requirements:
  - REQ-0008-brand-status-confirm
  - REQ-0005-user-management
  - REQ-0006-tile-sku-management
  - REQ-0007-tile-category-management-refine
---

# 缺陷说明

管理端部分列表页在执行**状态变更类行内操作**（冻结/解冻、上架/下架/恢复等）时，点击后直接调用 API，缺少与「瓷砖类目」「瓷砖品牌」已对齐的二次确认 modal（`modal-backdrop` + `modal-card` + head/body/footer）。存在误触导致账号冻结或 SKU 上下架的风险。

经 `/bug-explore` 核对源码：**品牌列表启停/删除已在 REQ-0008 / `fix-brand-status-confirm` 中交付 modal 确认**；capture 中「品牌缺少确认」为记录过时，**不纳入本缺陷修复范围**。本缺陷聚焦尚未落地的用户冻结/解冻、SKU 上下架/恢复，以及用户删除确认形态与 DS modal 的不一致。

**不在本缺陷范围**：

- 品牌列表启用/停用/删除（已满足 REQ-0008 与 `openspec/specs/web-client/spec.md`）
- 瓷砖类目启停/删除（REQ-0007 参考实现）
- 用户「重置密码」确认 UI 统一（→ **BUG-0017**，虽有 `window.confirm` 但职责独立）

# 复现步骤

1. 以 `admin` 登录 Web 管理端（local 或 Docker）。
2. **用户管理**（`/admin/users`）：对正常用户点击「冻结」，观察是否在 API 调用前弹出确认 Dialog。
3. 对已冻结用户点击「解冻」，同样观察。
4. 对从未登录用户点击「删除」，观察是否为浏览器原生 `window.confirm` 而非管理端 modal。
5. **瓷砖 SKU**（`/admin/tile-skus`）：对已上架行点击「下架」；对草稿/已停用行点击「上架」或「恢复」，观察是否直接生效。
6. **对照（不应复现本缺陷）**：进入「瓷砖类目」或「瓷砖品牌」，点击「启用/停用」，应出现 DS modal 确认框。

| 页面 | 路由 | 可稳定复现的操作 | 当前行为 |
|---|---|---|---|
| 用户管理 | `/admin/users` | 冻结、解冻 | 直接 `updateUserStatus`，无确认 |
| 用户管理 | `/admin/users` | 删除 | `window.confirm`，非 modal |
| 瓷砖 SKU | `/admin/tile-skus` | 上架、下架、恢复 | 直接 `publishTileSku` / `unpublishTileSku` |
| 瓷砖品牌 | `/admin/brands` | 启用、停用、删除 | modal 确认（**已修复，非本 BUG**） |
| 瓷砖类目 | `/admin/tile-categories` | 启用、停用、删除 | modal 确认（参考实现） |

# 期望结果

- 用户列表「冻结」「解冻」MUST 在执行前展示二次确认 modal，文案含用户名与操作类型（如「确认冻结用户「{username}」？」）。
- 用户列表「删除」MUST 使用与同页/类目页一致的 modal 结构，MUST NOT 使用 `window.confirm`（重置密码 UI 归 BUG-0017）。
- SKU 列表「上架」「下架」「恢复」MUST 在执行前展示二次确认 modal，文案含 SKU 名称与操作类型。
- 确认 modal MUST 复用既有 `modal-backdrop` / `modal-card` 结构，视觉对齐 `TileCategoryManagementPage` / `BrandManagementPage`（semantic token，无裸 Hex）。
- 取消、点击遮罩、× 或等效关闭 MUST NOT 调用 API；仅主按钮确认后调用 API 并 Toast + 刷新列表。
- 品牌/类目既有确认流程 MUST NOT 回归；`BrandManagementPage.test.tsx` 启停确认用例 MUST 保持通过。

# 实际结果

- **用户冻结/解冻**：`handleFreeze` 内直接 `await updateUserStatus(...)`，无前置确认；`UserManagementPage.test.tsx` 甚至断言点击「冻结」后立即调用 mock API。
- **用户删除**：使用 `window.confirm(\`确认删除用户 ${user.username}？\`)`，交互形态与类目/品牌 modal 不一致。
- **SKU 上下架/恢复**：`handlePublish` / `handleUnpublish` 直接调用 API；`TileSkuManagementPage.test.tsx` 断言点击「恢复」后立即 `publishTileSku`。
- **品牌启停/删除、类目启停/删除、SKU 删除**：已实现 modal 确认，行为正确。

涉及源码：

| 页面 | 文件 | 缺口操作 | 当前确认方式 |
|---|---|---|---|
| 用户管理 | `UserManagementPage.tsx` | 冻结、解冻 | 无 |
| 用户管理 | `UserManagementPage.tsx` | 删除 | `window.confirm` |
| 瓷砖 SKU | `TileSkuManagementPage.tsx` | 上架、下架、恢复 | 无 |
| 瓷砖品牌 | `BrandManagementPage.tsx` | 启用、停用、删除 | modal（已满足） |
| 瓷砖类目 | `TileCategoryManagementPage.tsx` | 启用、停用、删除 | modal（参考） |

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 用户管理 | 误触冻结/解冻导致账号无法登录；删除确认 UX 不统一 |
| Web 管理端 / 瓷砖 SKU | 误触上下架影响前台商品可见性 |
| Web 管理端 / 瓷砖品牌、瓷砖类目 | 无缺口；作为 Golden Reference，修复时 MUST NOT 回归 |
| 角色 | `admin`（用户管理写操作）；SKU 上下架含 `employee` |
| 后端 / API / 数据库 | 无变更需求 |
| Orval | 不需要 |
| 店主端 / 小程序 | 间接：SKU 误下架影响 catalog 可见 SKU |
| 关联需求 | REQ-0008（交互模式先例）、REQ-0005-user-management、REQ-0006-tile-sku-management、REQ-0007（类目参考） |
| 关联 Change | `fix-brand-status-confirm`、`fix-tile-category-management-refine`（已归档，交互参考） |
| 关联缺陷 | BUG-0017（重置密码 confirm UI，独立 fix 面） |

# 严重等级说明

严重程度为 **medium**。

理由：

- 问题可 100% 稳定复现（用户冻结、SKU 上下架），存在真实误操作风险，但不造成不可逆数据丢失（冻结/上下架可逆；删除仍有 `window.confirm` 或 modal 门槛）。
- 非回归：`fix-brand-status-confirm` 已闭环品牌启停；缺口为交互规范未横向推广至用户/SKU 页。
- 无安全漏洞、权限绕过或 API 契约问题，不属于 hotfix 或 blocker。
- 与 BUG-0015（toast 布局）、BUG-0017（重置密码 modal UI）可同 Sprint 编排，但 fix change 职责 MUST 独立。

# 修复建议（供 bug-complete / bug-opsx）

1. 在 `UserManagementPage` 增加 `statusConfirmTarget`（及可选 `deleteTarget` modal，替换 `window.confirm`）。
2. 在 `TileSkuManagementPage` 增加 `publishConfirmTarget` / `unpublishConfirmTarget`（或统一 `statusConfirmTarget` + action 枚举）。
3. 文案与按钮结构对齐 `TileCategoryManagementPage` 启停确认及同页删除 modal。
4. 更新/新增 vitest：确认前 mock API MUST NOT 被调用；取消/关闭后不调用；确认后调用并 Toast。
5. OpenSpec change 建议命名：`fix-admin-list-status-action-confirm`；delta 扩展 `web-client` 中用户冻结/解冻与 SKU 上下架确认 requirement（参考品牌/类目既有条目）。
6. 可选后续优化：抽取共享 `AdminConfirmDialog` 组件（非本 BUG 阻塞项）。

# 备注

- capture.md 中「品牌列表缺少确认」经 explore 证伪；`/bug-complete` 时可同步收窄 capture 描述或于 trace 注明。
- REQ-0005 `business-flow.md` 已描述冻结/删除「→ 确认」，但 AC 未像 REQ-0008 那样细化 modal 结构；修复以四页已交付的 modal 模式为准。
- REQ-0006 上下架流程未强制二次确认，本缺陷按产品一致性（对齐类目/品牌）补全，非 API 缺陷。
