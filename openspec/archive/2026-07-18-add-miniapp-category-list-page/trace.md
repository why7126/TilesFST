---
change_id: add-miniapp-category-list-page
type: add
status: proposed
created_at: 2026-07-18 22:07:26
updated_at: 2026-07-19 01:20:00
source_requirement: REQ-0045-category-list-page
iteration: sprint-008
related_requirements:
  - REQ-0045-category-list-page
related_sprint: sprint-008
affected_capabilities:
  new:
    - miniapp-category-list-page
  modified: []
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: conditional
  storage: conditional
  api: true
prototype_refs:
  - issues/requirements/archive/REQ-0045-category-list-page/prototype/miniapp/context.md
  - issues/requirements/archive/REQ-0045-category-list-page/prototype/miniapp/interaction.md
  - issues/requirements/archive/REQ-0045-category-list-page/prototype/miniapp/prototype.html
  - issues/requirements/archive/REQ-0045-category-list-page/prototype/miniapp/prototype.png
---

# add-miniapp-category-list-page Trace

## 来源

- REQ：`REQ-0045-category-list-page`
- Sprint：`sprint-008`
- 命令：`/req-opsx REQ-0045`

## PNG / Prototype Checklist

- [x] 390x844 原型截图与实现首屏布局一致（静态结构与样式断言覆盖；微信开发者工具截图需人工复核）。
- [x] 左侧一级分类导航约 98px，选中态含品牌金指示条。
- [x] 右侧二级分类为三列宫格，仅展示名称且单行省略。
- [x] 页面标题、左右双栏分类主体和底部 TabBar 与小程序首页风格一致。
- [x] 未出现店铺 Logo/Header 模块、搜索框、商品卡片、价格、收藏、筛选排序、热门分类或管理端维护入口。

## 实现证据

| 项 | 结论 |
|---|---|
| 分类树数据 | 新增 `GET /api/v1/miniapp/categories/tree?depth=2`，复用 `tile_categories`，仅返回 `status=ENABLED` 且 `level<=2` 的公开字段。 |
| 排序与版本 | 一级/二级均按 `sort_order ASC, created_at ASC, id ASC`；版本号由返回分类数量和最大更新时间生成。 |
| 分类图片 | 当前 DB 无独立分类封面字段；本 Change 不扩 DB/管理端，后端保留兼容 `coverUrl`，小程序分类列表页不渲染二级分类图片、不加载缩略图、不自动取商品主图。 |
| 小程序页面 | `pages/category/index` 已实现缓存优先、静默刷新、双栏滚动、状态恢复、二级分类跳转防抖和异常态；`pages/product-list/index` 已作为分类商品列表承接页注册，支持按二级类目名称过滤商品并跳转 SKU 详情；按最新反馈移除店铺 Logo/Header 模块、搜索框与二级分类图片。 |
| 埋点 | 新增 `category_page_view`、`primary_category_click`、`secondary_category_click`、`category_load_failed` 白名单，禁止 raw payload/object key/响应体等敏感字段。 |
| API/Orval/docs | 已更新 `docs/03-api-index.md`，并运行 `./scripts/generate-openapi-client.sh` 刷新 OpenAPI 与 Orval 生成物。 |
| DB/管理端 | 未修改 DB schema、migration 或管理端维护入口；分类封面维护能力如需真实素材，应拆分后续 REQ/Change。 |
| 验证 | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py` 通过；`openspec validate add-miniapp-category-list-page --strict` 通过；微信开发者工具截图预览待人工验收。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 01:20:00 | 归档前复核 | 修复二级类目点击未进入分类商品列表页：新增并注册 `pages/product-list/index` 承接页 |
| 2026-07-18 23:30:00 | 用户反馈 | 二级类目不需要显示图片，同步页面、规格、需求与测试 |
| 2026-07-18 23:05:00 | 用户反馈 | 分类列表页范围收窄：移除店铺 Logo/Header 模块和搜索框，同步规格、页面、事件与测试 |
| 2026-07-18 22:45:00 | /opsx-apply | 完成小程序分类页、公开分类树 API、埋点、文档、OpenAPI/Orval 和测试；微信开发者工具截图预览待人工验收 |
| 2026-07-18 22:07:26 | /req-opsx | 从 REQ-0045 创建 OpenSpec Change，状态 proposed |
