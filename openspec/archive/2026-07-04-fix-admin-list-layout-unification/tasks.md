---
change_id: fix-admin-list-layout-unification
title: 管理端多列表页布局与筛选分页交互统一修复 - 任务
created_at: 2026-07-03 18:51:13
updated_at: 2026-07-04 07:48:50
source_bug: BUG-0055-admin-list-layout-unification
status: implemented
---

# Tasks

## 1. 公共结构与样式

- [x] 1.1 盘点 SKU、品牌、类目、规格、Banner、用户、日志审计、接口文档页面的模块顺序和 CSS class。
- [x] 1.2 沉淀或复用统一的管理端列表页结构约定：标题 → 指标卡 → 筛选/搜索 → 列表。
- [x] 1.3 沉淀统一筛选区按钮与控件样式，保留重置入口，移除显式查询/搜索入口。
- [x] 1.4 沉淀通用 sticky action column class 或 helper，基线对齐接口文档页操作列。
- [x] 1.5 沉淀最多 5 个可点击页码的分页窗口逻辑或组件。

## 2. 页面修复

- [x] 2.1 调整 `TileSkuManagementPage`：移除查询按钮、统一重置按钮、分页最多 5 页码、最后一列固定浮动。
- [x] 2.2 调整 `BrandManagementPage`：移除查询按钮、统一筛选区、分页最多 5 页码、最后一列固定浮动。
- [x] 2.3 调整 `TileCategoryManagementPage`：移除查询按钮、统一筛选区、分页最多 5 页码、最后一列固定浮动。
- [x] 2.4 调整 `TileSpecManagementPage`：移除查询按钮、统一筛选区、分页最多 5 页码、最后一列固定浮动。
- [x] 2.5 调整 `BannerManagementPage`：将指标卡移动到筛选区之前，移除搜索按钮、统一重置按钮、分页最多 5 页码、最后一列固定浮动。
- [x] 2.6 调整 `UserManagementPage`：确认模块顺序，统一分页最多 5 页码与最后一列固定浮动。
- [x] 2.7 调整 `LogAuditPage`：移除查询按钮、统一重置按钮、状态/结果筛选改为下拉并覆盖常见 HTTP 状态码、分页最多 5 页码、保持日志详情抽屉与查看操作不回退。
- [x] 2.8 调整 `ApiDocsPage`：保持接口文档页 sticky action column 基线，补齐最多 5 页码并作为公共基线校验。

## 3. 回归测试

- [x] 3.1 增加分页窗口计算单元测试，覆盖总页数 1、5、6、当前页靠前、居中、靠后。
- [x] 3.2 更新受影响页面测试，断言不再渲染【查询】或【搜索】按钮。
- [x] 3.3 更新受影响页面测试，断言保留统一【重置】按钮。
- [x] 3.4 更新页面结构测试，覆盖标题、指标卡、筛选/搜索、列表的 DOM 顺序。
- [x] 3.5 更新表格测试，断言最后一列表头/单元格具备 sticky action column 契约。
- [x] 3.6 更新分页测试，断言最多 5 个可点击页码、总页数为 1 时上一页/下一页禁用。
- [x] 3.7 保持新增、编辑、启停、删除、查看、重置密码等关键操作测试通过。
- [x] 3.8 更新日志审计页测试，覆盖状态/结果下拉、`result` 与 `status_code` 查询参数映射、`422 参数校验错误` 选项。

## 4. 视觉验收

- [x] 4.1 在 1366px、1440px、1920px desktop 视口验收全部 8 个页面。
- [x] 4.2 验收横向滚动时最后一列固定浮动，不出现表头/表体错位。
- [x] 4.3 验收筛选区和分页区在常见桌面宽度下无重叠、裁切或跳动。
- [x] 4.4 做 tablet / mobile smoke，确认页面不出现明显横向溢出或控件重叠。

## 5. 验证与追溯

- [x] 5.1 运行相关 Vitest / Testing Library 测试。
- [x] 5.2 运行 `openspec validate fix-admin-list-layout-unification --strict`。
- [x] 5.3 运行 `python scripts/validate-directory-structure.py`。
- [x] 5.4 确认不需要执行后端 pytest、Orval、数据库迁移或 Docker Compose 验证，并在 trace 中记录原因。
- [x] 5.5 更新 BUG trace 与 OpenSpec trace。
- [x] 5.6 若修复过程发现可复用故障经验，补充 `docs/knowledge-base/incidents/`；若无复用价值，在验收记录中说明不沉淀。
