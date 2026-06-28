---
bug_id: BUG-0015-admin-list-status-tips-layout-shift
title: 管理端列表页状态变更 Tips 推挤页面导致上下布局波动
severity: medium
status: draft
owner: product
discovered_at: 2026-06-27 12:03:34
environment: local|docker
related_requirement: REQ-0005-brand-management
related_change: fix-brand-image-display-layout-shift
related_bugs:
  - BUG-0003-brand-image-display-layout-shift
suggested_fix_change: fix-admin-list-status-toast-layout
related_requirements:
  - REQ-0005-brand-management
  - REQ-0005-user-management
  - REQ-0005-tile-category-management
  - REQ-0006-tile-sku-management
---

# 缺陷说明

Web 管理端多个列表页在执行状态变更、CRUD 成功或 API 错误反馈时，会在 `page-hero` 前条件渲染 `.admin-notice` 提示条，约 3.2 秒后自动消失。该节点处于正常文档流，插入与移除会改变内容区纵向高度，导致 hero、指标卡、筛选区、表格等主体内容整页上下波动，影响连续操作体验。

**修复范围（用户确认一并处理）**：瓷砖品牌、用户管理、瓷砖类目、瓷砖 SKU 四个列表页 MUST 统一采用非占位文档流的固定位置 toast 反馈，且 MUST NOT 推挤页面主体内容。

品牌页在 `BUG-0003` / `fix-brand-image-display-layout-shift` 中已局部改为 `.admin-toast-region`，但样式仍散落在 `brand-management.css`，与用户/类目/SKU 未对齐；本缺陷负责四页统一落地与回归防护，而非仅补用户页遗漏。

# 复现步骤

1. 以 `admin` 或 `employee` 登录 Web 管理端（local 或 Docker 均可）。
2. 依次进入以下列表页，对任意一行执行会触发成功/失败 Tips 的操作（见下表）。
3. 观察 `page-hero` 上方是否临时出现一行 Tips。
4. 等待 Tips 自动消失（约 3.2 秒）。
5. 对比 Tips 出现前、出现后、消失后，hero / 指标卡 / 筛选区 / 表格的纵向位置是否发生位移。

| 页面 | 路由 | 可触发 Tips 的操作示例 |
|---|---|---|
| 瓷砖品牌 | `/admin/brands` | 启用、停用、删除、保存品牌、加载失败 |
| 用户管理 | `/admin/users` | 冻结、解冻、删除、重置密码、新建/编辑用户、加载失败 |
| 瓷砖类目 | `/admin/tile-categories` | 启用、停用、删除、保存类目、加载失败 |
| 瓷砖 SKU | `/admin/tile-skus` | 上架、下架、删除、保存 SKU、加载失败 |

**当前可稳定复现的页面**：用户管理、瓷砖类目、瓷砖 SKU（仍使用 `.admin-notice` 文档流模式）。

**品牌页**：源码已使用 `.admin-toast-region`（fixed）；若旧构建或未加载 `brand-management.css` 仍可能复现，纳入统一改造与回归验收。

# 期望结果

- 四页状态变更及操作成功/失败反馈 MUST 使用固定位置 toast（如右上角 overlay），MUST NOT 插入主体文档流占位。
- Tips 出现与消失 MUST NOT 改变 hero、指标卡、筛选区、表格、分页区的纵向布局位置。
- 四页 toast 视觉与行为 MUST 一致（位置、样式、自动消失时长、`aria-live` 可访问性）。
- 品牌页既有 toast 行为（`BUG-0003` 验收）MUST NOT 回归；`BrandManagementPage.test.tsx` 中「启用后展示 `.admin-toast-region`、无 `.admin-notice`」断言 MUST 保持通过。
- 共享 toast 样式 SHOULD 抽至管理端公共样式（如 `admin-home.css`），避免仅品牌页私有 CSS 承载。

# 实际结果

- **用户管理、瓷砖类目、瓷砖 SKU**：在 `page-hero` 前渲染 `<p className="admin-notice">`，属于文档流节点；3.2s 定时清除后高度收回，整页上下跳动。
- **瓷砖品牌**：已改为 `.admin-toast-region` + `.admin-toast`（`position: fixed`），单页行为正确，但未与其他三页共享实现，样式耦合在 `brand-management.css`。
- `.admin-notice` 样式（`admin-home.css`）仅定义 margin/padding/border，无 fixed/overlay，不适合「几秒后自动消失」的操作反馈。

涉及源码：

| 页面 | 文件 | 当前 notice 模式 |
|---|---|---|
| 瓷砖品牌 | `BrandManagementPage.tsx` | `.admin-toast-region`（已 fixed） |
| 用户管理 | `UserManagementPage.tsx` | `.admin-notice`（文档流） |
| 瓷砖类目 | `TileCategoryManagementPage.tsx` | `.admin-notice`（文档流） |
| 瓷砖 SKU | `TileSkuManagementPage.tsx` | `.admin-notice`（文档流） |

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖品牌列表 | 局部已修；需纳入统一 toast 与回归验收 |
| Web 管理端 / 用户管理列表 | 状态变更、密码重置、CRUD 反馈导致布局抖动 |
| Web 管理端 / 瓷砖类目列表 | 启停、删除、CRUD 反馈导致布局抖动 |
| Web 管理端 / 瓷砖 SKU 列表 | 上下架、删除、CRUD 反馈导致布局抖动 |
| 角色 | `admin`、`employee` |
| 后端 / API / 数据库 | 无变更需求 |
| 店主端 / 小程序 | 无直接影响 |
| 关联需求 | REQ-0005-brand-management、REQ-0005-user-management、REQ-0005-tile-category-management、REQ-0006-tile-sku-management |
| 关联缺陷 / Change | BUG-0003、`fix-brand-image-display-layout-shift`（品牌 toast 先例） |

**不在本缺陷范围**：`AdminLayout.tsx` 侧栏占位「功能建设中」提示（`.admin-notice`）；若后续需统一可另开优化项。

# 严重等级说明

严重程度为 **medium**。

理由：

- 问题在四页均可感知，影响管理端连续维护主数据的操作体验，但不阻断 API 调用或数据写入。
- 品牌页已有局部修复，用户/类目/SKU 为同类遗漏，修复面集中在前端 notice/toast 模式统一。
- 无安全、权限、数据一致性风险，不属于 hotfix 或 blocker 场景。
- 与 `BUG-0003` 中 Tips 子问题同类；图片显示部分已在 archived change 中闭环，本缺陷聚焦四页 toast 布局统一。

# 修复建议（供 bug-complete / bug-opsx）

1. 将 `.admin-toast-region` / `.admin-toast` 从 `brand-management.css` 提升至管理端共享样式。
2. 用户、类目、SKU 三页 notice 渲染改为与品牌页一致的 toast 结构；可选抽 `AdminToast` 小组件减少重复。
3. 品牌页改用共享样式/组件，保留现有 fixed 行为与单测。
4. 为用户/类目/SKU 页补充 vitest：操作成功后 MUST 存在 `.admin-toast-region`，MUST NOT 存在文档流 `.admin-notice`（成功反馈路径）。
5. OpenSpec change 建议命名：`fix-admin-list-status-toast-layout`；参考 `fix-brand-image-display-layout-shift` delta 与验收写法。

# 备注

- 经 `/bug-explore` 确认：品牌页当前源码不应复现文档流推挤；capture 中「品牌仍复现」更可能为修复前记录或未覆盖页遗漏，本 bug 按用户要求四页一并统一处理。
- 与 `BUG-0016`（二次确认缺失）、`BUG-0017`（重置密码确认 UI）可同 Sprint 编排，但职责独立。
