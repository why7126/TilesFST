## 1. Backend / API

- [x] 1.1 定位类目创建与更新 Schema、Service 校验、错误码映射中所有 10 字符长度假设。
- [x] 1.2 将类目名称业务上限调整为 15 个用户可见字符，保持空名称、非法字符、同层级唯一、层级和排序权重规则不变。
- [x] 1.3 确认 `tile_categories.name`、SQLite schema、MySQL migration 支持至少 15 字符；如无需迁移，在实现说明中记录原因。
- [x] 1.4 若新增或调整错误码 / message，同步 `docs/standards/error-codes.md` 与 API 文档。

## 2. Web Admin

- [x] 2.1 更新 `CategoryFormModal` 或等价表单的类目名称长度校验与字段级错误提示为「类目名称最多 15 个字符」。
- [x] 2.2 回归新增 / 编辑弹窗中 15 字符可保存、16 字符保存前被拦截。
- [x] 2.3 回归类目列表名称列与左侧类目树展示 15 字符名称时不重叠、不撑破。
- [x] 2.4 执行 admin-list 横切 AC：分页 DOM、fixed toast、DS confirm modal、指标卡 DOM 不回归。
- [x] 2.5 执行 admin-modal 横切 AC：无 `modal-card` 与专属类双挂载、computed width 正确、矮视口 body 可滚动。

## 3. Miniapp / Web Catalog

- [x] 3.1 使用 15 字符类目名称样例回归小程序分类页或分类入口布局。
- [x] 3.2 使用 15 字符类目名称样例回归 Web 展示端分类筛选入口或商品列表入口布局。
- [x] 3.3 如展示空间有限，沿用合理截断 / tooltip / 换行策略，但不得在数据层拒绝合法 15 字符名称。

## 4. OpenAPI / Orval / Docs

- [x] 4.1 导出 OpenAPI，确认类目名称字段 `maxLength` 或等价约束为 15。
- [x] 4.2 运行 Orval 生成客户端并提交生成物，前端不得手写重复接口类型。
- [x] 4.3 同步 `docs/03-api-index.md`、`docs/04-database-design.md` 相关类目字段或接口说明。

## 5. Tests / Validation

- [x] 5.1 后端 pytest 覆盖创建 15 字符成功、16 字符失败。
- [x] 5.2 后端 pytest 覆盖更新 15 字符成功、16 字符失败。
- [x] 5.3 后端 pytest 覆盖空名称、非法字符、同层级重复名称不因本变更放松。
- [x] 5.4 前端 Vitest / Testing Library 覆盖 15 字符不报错、16 字符显示字段级错误。
- [x] 5.5 更新测试 helper、fixture 和最小合法 payload，移除 10 字符有效约束假设。
- [x] 5.6 运行相关后端、前端、OpenSpec 校验，并记录小程序 / Web 展示端手工或自动化回归证据。

## Validation Evidence

- Backend: `uv run pytest src/backend/tests/test_admin_tile_categories.py`，14 passed，覆盖创建 / 更新 15 字符成功、16 字符失败、空名称、非法字符、同层级重复名称。
- Web Admin: `pnpm --dir src/web test -- CategoryFormModal TileCategoryManagementPage`，56 files / 293 tests passed；覆盖表单 15/16 字符边界、列表分页 DOM、fixed toast、confirm modal、指标卡 DOM、弹窗 CSS contract。
- OpenSpec: `openspec validate update-category-name-max-length-15 --strict` pass。
- OpenAPI / Orval: `./scripts/generate-openapi-client.sh` pass；`TileCategoryCreateRequest.name` 与 `TileCategoryUpdateRequest.name` 均导出 `maxLength: 15`，Orval 生成类型包含 `@maxLength 15`。
- DB: SQLite `tile_categories.name` 为 `TEXT`，MySQL 为 `VARCHAR(128)`，均支持至少 15 字符，本变更无需 schema / migration。
- Miniapp layout: `src/miniapp/pages/category/index.wxss` 中一级分类标题单行 ellipsis，二级分类卡片两行 clamp + `word-break: break-all`，15 字符样例不会被数据层拒绝。
- Web Catalog layout: `src/web/src/shared/ui/sidebar.tsx` 为分类筛选 label 增加 `min-w-0 flex-1 truncate` 与 `title`，沿用截断展示且不改变数据层合法性。
