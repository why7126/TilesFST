---
bug_id: BUG-0029-tile-spec-list-not-refresh-after-create
status: pending_review
created_at: 2026-06-28 13:25:00
updated_at: 2026-06-28 13:25:00
related_requirement: REQ-0009-tile-spec-management
---

# 回归验收标准

> 修复本缺陷 MUST 使规格列表页新增/编辑保存后与品牌、类目、SKU 管理页行为一致：Toast + 自动重载列表与 summary；不得回归启停、删除、筛选、分页及弹窗 CRUD 本身。

## AC-001 新增保存后列表 MUST 自动刷新

**Given** 管理员已登录 `/admin/tile-specs`，筛选条件为默认（无关键词、全部状态），当前列表共 N 条  
**When** 点击「＋ 新增瓷砖规格」，填写合法宽/长/排序并点击「保存」  
**Then** MUST 展示 Toast「规格已创建」  
**And** 弹窗 MUST 关闭  
**And** **无需 F5**，列表 MUST 出现新记录，`共 {total} 条` MUST 变为 N+1（或符合当前页分页逻辑的最新 total）  
**And** 新记录字段（display_name、宽长、排序等）MUST 与提交一致

## AC-002 编辑保存后列表行 MUST 自动更新

**Given** 列表中存在规格 S，当前排序为 A  
**When** 点击 S 的「编辑」，将排序改为 B 并保存  
**Then** MUST 展示 Toast「规格已更新」  
**And** **无需 F5**，S 所在行排序 MUST 显示 B  
**And** 其他未改字段 MUST 保持正确

## AC-003 统计卡片 MUST 与列表同步更新

**Given** 保存前指标卡「规格总数」为 T  
**When** 成功新增一条规格  
**Then** **无需 F5**，「规格总数」MUST 更新为 T+1  
**And** 「启用规格」计数 MUST 同步（新建默认 ENABLED）  
**And** 编辑不改变总数时，总数 MUST 不变

## AC-004 onSuccess 实现 MUST 对齐管理端标准模式

**Given** 检查 `TileSpecManagementPage.tsx`  
**When** 表单弹窗 `onSuccess` 被调用  
**Then** MUST 同时：`setNotice(message)` **与** `void loadSpecs()`（或等价列表重载）  
**And** MUST 与 `BrandManagementPage` / `TileSkuManagementPage` 回调结构一致

## AC-005 启停与删除刷新 MUST 保持可用（回归）

**Given** 修复已部署  
**When** 用户对规格执行启用、停用或删除并确认  
**Then** 行为 MUST 与修复前一致：Toast + 列表刷新 + 状态 badge 更新  
**And** MUST NOT 因本次修改导致重复请求或 loading 异常

## AC-006 筛选场景下刷新 MUST 尊重当前筛选

**Given** 当前 `status=DISABLED` 筛选  
**When** 新增一条默认 ENABLED 的规格并保存  
**Then** 列表 MUST 自动重载  
**And** 新记录 MAY 不在当前筛选结果中（符合筛选语义）  
**And** `共 {total} 条` 与 summary  MUST 反映**当前筛选条件**下的 API 返回值

## AC-007 修复范围 MUST 为纯前端

**Given** 缺陷修复已合并  
**When** 检查变更范围  
**Then** MUST NOT 变更 API 路径、请求/响应结构、SQLite schema  
**And** MUST NOT 需要 Orval 重新生成  
**And** 预期变更文件：`TileSpecManagementPage.tsx`（± 可选 vitest）

## AC-008 测试 SHOULD 补齐

**Given** 进入 `fix-tile-spec-list-refresh-after-create`（或等价 fix-* Change）  
**When** 完成 `/opsx-apply`  
**Then** SHOULD 补充 Vitest：mock `fetchTileSpecs`，模拟 `TileSpecFormModal` success 后断言列表加载函数被调用  
**And** MAY 在 Change `trace.md` 记录手工验收步骤与截图对比

## AC-009 与 BUG-0027 / BUG-0028 修复 MUST 可独立合并

**Given** 本 BUG 与 UI 类 BUG-0027、BUG-0028 可能同 Sprint  
**When** 分别或合并提交 fix Change  
**Then** 本 AC 集合 MUST 可独立验收，不依赖分页样式或弹窗字段顺序修复  
**And** 合并 Change 时 MUST 仍满足 AC-001～AC-006
