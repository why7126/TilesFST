## 1. Contract / Design

- [x] 1.1 确认分类树数据来源：复用现有 `tile_categories` 主数据，明确 `status=enabled`、排序、版本号和公开字段过滤策略。
- [x] 1.2 确认是否新增 `GET /api/miniapp/categories/tree?depth=2`；若复用现有接口，记录字段映射和缺口；若新增/调整 API，同步 OpenAPI、Orval、docs 和测试。
- [x] 1.3 明确分类列表页不展示二级分类图片；后端 `coverUrl` 仅兼容返回，真实分类封面维护能力拆分后续 REQ。
- [x] 1.4 明确分类商品列表页承接策略；目标页不可用时必须安全降级，不得白屏或路由错误。

## 2. Backend / API

- [x] 2.1 实现或复用小程序公开分类树查询 service/repository/schema。
- [x] 2.2 过滤停用分类、后台内部字段、内部备注、原始 object key 和未授权素材。
- [x] 2.3 返回两级分类树、排序字段、兼容 `coverUrl` 和数据版本号。
- [x] 2.4 补充 API 测试：成功、停用过滤、排序、空 children、兼容 URL 安全、网络/错误 envelope。

## 3. Miniapp Page

- [x] 3.1 新增或完善 `pages/category/index`，接入 TabBar「分类」入口。
- [x] 3.2 实现页面标题、左侧一级分类导航、右侧二级分类宫格和底部 TabBar；不展示店铺 Logo/Header 模块或搜索框。
- [x] 3.3 实现一级分类切换：选中态、右侧标题/宫格更新、右侧滚动到顶部、左侧滚动位置保持、不重复请求接口。
- [x] 3.4 实现二级分类卡片：仅展示单行省略名称、整卡点击热区、按压反馈，不渲染图片。
- [x] 3.5 实现二级分类跳转 `pages/product-list/index?categoryId=...&categoryName=...`、300ms 防抖、跳转失败提示。
- [x] 3.6 按最新范围移除分类页搜索入口，不在分类列表页提供搜索框或搜索跳转。

## 4. Cache / States / Analytics

- [x] 4.1 实现本地缓存优先渲染、24 小时建议缓存、版本号静默刷新和刷新失败保留缓存。
- [x] 4.2 实现页面返回恢复当前一级分类、左侧滚动位置和右侧滚动位置。
- [x] 4.3 实现骨架屏、一级无二级空状态、无缓存网络错误、有缓存网络降级和当前分类下架回退；二级分类不渲染图片，无图片占位状态。
- [x] 4.4 实现分类页埋点：`category_page_view`、`primary_category_click`、`secondary_category_click`、`category_load_failed`，并过滤敏感信息。

## 5. Visual / QA

- [x] 5.1 按 `prototype/miniapp/` 验收深色视觉、左侧 98px 导航、右侧三列宫格、底部 TabBar 和不做项。
- [x] 5.2 验证 375x812、390x844、320-430 pt 宽度范围无横向滚动、内容重叠、底部露白或 TabBar 遮挡。
- [x] 5.3 验证一级分类按钮 56-60px、主要触控区满足移动端可点击要求，二级分类卡片可访问名称完整。
- [x] 5.4 确认页面不展示商品卡片、价格、收藏按钮、筛选排序栏、热门分类模块、管理端维护入口。

## 6. Documentation / Validation

- [x] 6.1 若 API/DB/Orval 有变更，同步 `docs/03-api-index.md`、`docs/04-database-design.md`、OpenAPI/Orval 生成物和相关测试。
- [x] 6.2 更新 REQ-0045 trace、Sprint 008 双向追溯和验收证据。
- [x] 6.3 运行 `openspec validate add-miniapp-category-list-page --strict`。
- [x] 6.4 运行后端/小程序相关测试；若无法运行微信开发者工具，记录人工预览待验收项。
