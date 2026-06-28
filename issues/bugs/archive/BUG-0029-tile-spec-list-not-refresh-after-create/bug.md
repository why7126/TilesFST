---
bug_id: BUG-0029-tile-spec-list-not-refresh-after-create
title: 瓷砖规格新增/编辑保存后列表未自动刷新
severity: high
status: draft
owner: product
discovered_at: 2026-06-28 13:13:16
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_change: add-tile-spec-management
---

# 缺陷说明

Web 管理端「瓷砖规格」列表页（`/admin/tile-specs`）在新增或编辑弹窗点击「保存」后，后端 API 调用成功、Toast 提示出现且弹窗关闭，但页面列表与顶部统计卡片仍展示保存前的旧数据，须手动刷新浏览器（F5）才能看到最新记录。

同页「启用 / 停用 / 删除」操作在成功后能正确刷新列表，仅表单弹窗保存路径缺失刷新逻辑。

# 复现步骤

1. 以 admin 用户登录 Web 管理端（local `5173` 或 Docker `3000` 均可）。
2. 进入「瓷砖规格」列表页（侧栏 OPERATIONS → 瓷砖规格，或 `/admin/tile-specs`）。
3. 记录当前列表条数或清空筛选条件（关键词、状态均为「全部」）。
4. 点击「＋ 新增瓷砖规格」，填写必填项（宽度、长度、排序等）后点击「保存」。
5. 观察弹窗关闭后：Toast 显示「规格已创建」，但列表未出现新记录，统计卡片（规格总数等）未更新。
6. 手动刷新页面（F5）后，新记录出现且统计数字同步。

**编辑路径（同类问题）**：对已有规格点击「编辑」，修改排序或备注后保存，列表行数据不更新，须 F5 后才可见变更。

# 期望结果

- 新增或编辑保存成功后，列表 MUST 自动重新加载（或等价乐观更新），立即展示最新规格记录。
- 顶部 4 个统计卡片（规格总数 / 启用规格 / 停用规格 / 未关联 SKU）MUST 与列表数据同步更新。
- 行为 MUST 与同项目品牌管理、类目管理、SKU 管理页一致：`onSuccess` 回调中除 Toast 外调用列表加载函数。

# 实际结果

- `TileSpecFormModal` 保存成功后调用 `onSuccess(message)` 并关闭弹窗，数据已写入后端。
- `TileSpecManagementPage` 将 `onSuccess` 直接绑定为 `setNotice`，仅展示 Toast，未调用 `loadSpecs()`。
- 列表表格、`共 {total} 条` 分页摘要及指标卡均保持 stale 状态，直至整页刷新。

# 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端 / 瓷砖规格列表 | 新增、编辑保存后 UI 不刷新 |
| Web 管理端 / 规格统计卡片 | 保存后 summary 数据 stale |
| 关联需求 | REQ-0009-tile-spec-management（`add-tile-spec-management` 实现范围） |
| 后端 API / SQLite | 无影响（数据已正确持久化） |
| 小程序 / 店主端 | 无影响 |

不影响启停、删除、筛选、分页等已正确调用 `loadSpecs()` 的操作路径。

# 严重等级说明

严重程度为 `high`。

理由：

- 阻断规格主数据的日常维护闭环：运营人员保存后无法确认结果，误以为创建失败或需反复 F5，显著降低操作效率。
- 属于 REQ-0009 核心 CRUD 流程的功能性缺陷，非纯视觉问题。
- 修复成本低（前端单处回调补 `loadSpecs()`），但若不修复将直接影响 Sprint 验收与管理端可用性。

# 代码线索

| 线索 | 路径 |
|---|---|
| 规格列表页（`onSuccess` 未刷新） | `src/web/src/pages/admin/TileSpecManagementPage.tsx` |
| 规格表单弹窗（保存成功回调） | `src/web/src/features/admin/components/TileSpecFormModal.tsx` |
| 品牌管理页参考（正确模式） | `src/web/src/pages/admin/BrandManagementPage.tsx` |
| 类目管理页参考 | `src/web/src/pages/admin/TileCategoryManagementPage.tsx` |
| SKU 管理页参考 | `src/web/src/pages/admin/TileSkuManagementPage.tsx` |
| 截图 | `screenshots/tile-spec-add-save-no-list-refresh.png` |
