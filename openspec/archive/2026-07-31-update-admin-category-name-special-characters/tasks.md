## 1. Backend / API

- [x] 1.1 定位类目创建与更新 Schema、Service 校验、错误码映射中所有“仅中文、英文和数字”字符集假设。
- [x] 1.2 将类目名称业务规则调整为最多 15 个用户可见字符，允许中文、英文、数字和常见可见特殊字符。
- [x] 1.3 保持空名称、16 字符、换行、制表符、不可见控制字符、同层级唯一、层级和排序权重校验不回归。
- [x] 1.4 确认 `tile_categories.name`、SQLite schema、MySQL migration、CHECK 约束和触发器支持特殊字符；如无需迁移，在实现说明中记录原因。
- [x] 1.5 若新增或调整错误码 / message，同步 `docs/standards/error-codes.md` 与 API 文档。

## 2. Web Admin

- [x] 2.1 更新 `CategoryFormModal` 或等价表单的类目名称字符集校验与字段级错误提示。
- [x] 2.2 回归新增 / 编辑弹窗中特殊字符名称可保存、16 字符保存前被拦截、控制字符显示字段级错误。
- [x] 2.3 回归类目列表名称列、左侧类目树、SKU 类目选择器和筛选控件展示特殊字符名称时不重叠、不撑破。
- [x] 2.4 执行 admin-list 横切 AC：分页 DOM、fixed toast、DS confirm modal、无 `window.confirm` 不回归。
- [x] 2.5 执行 admin-modal 横切 AC：无 `modal-card` 与专属类双挂载、computed width 正确、矮视口 body 可滚动。

## 3. Miniapp / Web Catalog

- [x] 3.1 使用特殊字符类目名称样例回归小程序分类页或分类入口布局。
- [x] 3.2 使用特殊字符类目名称样例回归 Web 展示端分类筛选入口或商品列表入口布局。
- [x] 3.3 如展示空间有限，沿用合理截断 / tooltip / 换行策略，但不得在数据层拒绝合法特殊字符名称。

## 4. OpenAPI / Orval / Docs

- [x] 4.1 导出 OpenAPI，确认类目名称字段 `maxLength`、`pattern` 或描述与新规则一致。
- [x] 4.2 运行 Orval 生成客户端并提交生成物，前端不得手写重复接口类型。
- [x] 4.3 同步 `docs/03-api-index.md`、`docs/04-database-design.md` 相关类目字段或接口说明。

## 5. Tests / Validation

- [x] 5.1 后端 pytest 覆盖创建特殊字符名称成功、16 字符失败、控制字符失败。
- [x] 5.2 后端 pytest 覆盖更新特殊字符名称成功、16 字符失败、控制字符失败。
- [x] 5.3 后端 pytest 覆盖空名称、同层级重复名称不因本变更放松。
- [x] 5.4 前端 Vitest / Testing Library 覆盖特殊字符名称不报错、16 字符和控制字符显示字段级错误。
- [x] 5.5 更新测试 helper、fixture 和最小合法 payload，移除旧字符集有效约束假设。
- [x] 5.6 运行 OpenSpec strict 校验、相关后端测试、前端测试，并记录小程序 / Web 展示端回归证据。

## Validation Evidence

- `./scripts/generate-openapi-client.sh`：OpenAPI 导出与 Orval 生成成功。
- `uv run pytest src/backend/tests/test_admin_tile_categories.py`：16 passed。
- `pnpm --dir src/web test -- CategoryFormModal`：56 files / 300 tests passed。
- `pnpm --dir src/web test -- TileCategoryManagementPage TileSkuFormModal tile-categories-api`：56 files / 300 tests passed。
- `uv run pytest tests/test_miniapp_static.py`：30 passed。
- `rg -n "只能包含中文、英文和数字|仅允许中文、英文和数字" src docs src/web/openapi.json src/web/src/shared/api/generated.ts -g '!node_modules'`：无匹配。

## 验收返修记录

| 时间 | 反馈 | 调整 | 验证 |
|---|---|---|---|
| 2026-07-30 23:19:57 | 类目树前面的勾选框需要改成 `+/-`，支持展开 / 收起；默认只显示一级类目，其他级别默认收起。 | `CategoryTree` 从扁平列表改为递归树行；有子级的节点显示独立 `+/-` 展开按钮，类目名称按钮保留筛选能力；默认 `expandedIds` 为空，仅显示一级类目。 | `pnpm --dir src/web test -- CategoryTree CategoryFormModal TileCategoryManagementPage`：57 files / 302 tests passed。 |
