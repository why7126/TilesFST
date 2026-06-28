---
bug_id: BUG-0029-tile-spec-list-not-refresh-after-create
status: pending_review
created_at: 2026-06-28 13:25:00
updated_at: 2026-06-28 13:25:00
root_cause_type: code
---

# 根因分析

## 1. 直接原因

`TileSpecManagementPage.tsx` 将表单弹窗的成功回调直接绑定为 `setNotice`，保存成功后仅展示 Toast，**未调用** `loadSpecs()` 重新拉取列表与 summary：

```tsx
<TileSpecFormModal
  ...
  onSuccess={setNotice}
/>
```

同页其他写操作路径已正确刷新：

| 操作 | 成功后行为 |
|---|---|
| 启用 / 停用 | `handleStatusConfirm` → `void loadSpecs()` |
| 删除 | `handleDeleteConfirm` → `void loadSpecs()` |
| 新增 / 编辑保存 | `onSuccess` → 仅 `setNotice(message)` |

`TileSpecFormModal` 在 API 成功后调用 `onSuccess('规格已创建' | '规格已更新')` 并 `onClose()`，后端数据已持久化；前端 React state（`data`）未更新，导致表格、分页 `共 {total} 条` 与 4 个指标卡均 stale。

## 2. 根本原因

### 2.1 实现时未复用已验收的管理端列表页 `onSuccess` 模式

同项目 `BrandManagementPage`、`TileCategoryManagementPage`、`TileSkuManagementPage` 均在表单 `onSuccess` 中同时执行 Toast + 列表重载：

```tsx
onSuccess={(message) => {
  setNotice(message);
  void loadBrands(); // 或 refreshAll / loadSkus
}}
```

`TileSpecManagementPage` 在 `add-tile-spec-management` 交付时复制了弹窗与 `loadSpecs` 基础设施，但遗漏上述回调组合，属于**复制粘贴不完整**。

### 2.2 启停/删除路径单独实现刷新，未形成统一「写操作后 invalidate 列表」约定

规格页在后续补齐启停二次确认（任务 6.4）与删除确认（6.5）时，各自 handler 内显式调用 `loadSpecs()`；表单弹窗作为较早实现的 CRUD 路径，未在同一 PR 或 checklist 中强制对齐，导致同一页面内行为不一致。

### 2.3 验收与测试未覆盖「保存后 UI 即时反映」

- REQ-0009 `acceptance.md` 对启停写了「刷新列表」类 AC，对规格新增/编辑保存后的列表刷新**未显式编号**，OpenSpec `web-client/spec.md` 亦仅对启停场景写明 MUST 刷新。
- `add-tile-spec-management` tasks 8.3 Docker 验收 pending；缺少 E2E 或组件级断言：`onSuccess` 后 `fetchTileSpecs` 被再次调用。
- 后端 pytest 覆盖 spec CRUD，前端 vitest 仅覆盖删除按钮 disabled 矩阵，未测保存后列表同步。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 admin 或 employee 登录 Web 管理端（local 或 Docker）。
2. 访问 `/admin/tile-specs`。
3. 通过「＋ 新增瓷砖规格」或行内「编辑」打开弹窗，填写合法数据并点击「保存」。
4. 观察 Toast 出现、弹窗关闭，列表与统计卡未变化。
5. F5 整页刷新后数据出现。

**编辑与新增均受影响**（共用同一 `onSuccess` 绑定）。

**非缺陷路径：**

- 启停、删除、筛选查询、翻页——均已调用 `loadSpecs()` 或等价 fetch。
- 保存失败（校验/API 错误）——弹窗不关闭，列表本不应变化。

**筛选边界（修复后预期行为）：**

- 若当前 `status=DISABLED` 筛选，新建默认 `ENABLED` 的规格刷新后仍不显示——符合筛选逻辑，非 bug。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | **code** / frontend-logic |
| 是否接口缺陷 | 否（`POST/PUT /api/v1/admin/tile-specs` 正常） |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（`add-tile-spec-management` 交付即存在） |
| 主要修复面 | `TileSpecManagementPage.tsx` — `TileSpecFormModal` 的 `onSuccess` 回调 |
| 关联需求 | REQ-0009-tile-spec-management |
| 建议 Change | `fix-tile-spec-list-refresh-after-create`（或与 BUG-0027/0028 合并为 `fix-tile-spec-admin-ui`） |

## 5. 后续修复建议

1. 将 `onSuccess` 改为与品牌页一致：

   ```tsx
   onSuccess={(message) => {
     setNotice(message);
     void loadSpecs();
   }}
   ```

2. **不要**修改 API、schema 或 `TileSpecFormModal` 内部保存逻辑（除非需抽取共享 hook——本 BUG 范围外）。
3. 可选：新增 vitest，mock `fetchTileSpecs`，断言保存 success 后调用次数增加。
4. 修复后验证：新增后列表 + summary 即时更新；编辑排序/备注后行内数据同步；当前页码保持不变（与 Brand 页一致）。
