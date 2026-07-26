## Why

微信小程序已有首页与 SKU 详情页，但缺少 TabBar「分类」一级频道，用户无法通过清晰的一级/二级类目结构快速进入分类商品浏览路径。REQ-0045 已完成评审并纳入 sprint-008，需要先建立 OpenSpec Change，明确分类页、公开分类树、缓存、跳转、异常态与验收边界后再实现。

## What Changes

- 新增微信小程序 `pages/category/index` 分类列表页，作为底部 TabBar「分类」频道。
- 展示一级分类左侧纵向导航与二级分类右侧三列宫格，二级分类仅展示名称。
- 提供或复用小程序公开分类树接口，一次返回两级启用分类、排序、兼容 `coverUrl` 与数据版本号。
- 支持本地缓存优先渲染、版本号静默刷新、切换一级分类不重复请求、返回页面恢复当前分类与滚动位置。
- 支持二级分类跳转分类商品列表页、点击防抖、跳转失败提示。
- 覆盖骨架屏、空状态、网络失败、分类下架后的安全降级。
- 覆盖分类页埋点、移动视口、触控可访问性与小程序深色视觉验收。
- 不新增管理端分类维护能力，不在分类页展示店铺 Logo/Header、搜索框、商品卡片、价格、收藏、筛选排序或热门分类模块。

## Capabilities

### New Capabilities

- `miniapp-category-list-page`: 定义微信小程序分类列表页、公开分类树数据、分类导航交互、缓存恢复、异常状态、埋点、视觉与测试同步要求。

### Modified Capabilities

- 无。管理端 `tile-category-management` 仍作为后台类目主数据能力，本 Change 只消费或扩展公开小程序读取契约，不改变管理端类目维护需求；如实现阶段发现需修改既有 capability，应先更新 design 与 delta spec。

## Impact

- **Miniapp:** 新增或完善 `pages/category/index`、TabBar 分类入口、双栏滚动、二级分类跳转、缓存恢复、异常态和埋点。
- **API:** 可能新增 `GET /api/miniapp/categories/tree?depth=2`，或在已有公开接口上补足两级分类树、版本号与兼容 `coverUrl` 字段；若新增/调整 contract，必须同步 OpenAPI、Orval、docs 与测试。
- **Backend:** 可能新增小程序公开分类查询 service/repository/schema，必须过滤停用分类和后台内部字段。
- **Database:** 默认复用既有 `tile_categories` 主数据；若需要版本号事实源，必须同步 schema、迁移、数据库文档和测试。
- **Storage:** 分类列表页不渲染二级分类图片；若后端兼容返回 `coverUrl`，不得暴露原始 object key。
- **Web/Admin:** 不新增管理端页面；真实分类封面维护入口如需上线，应拆分独立 REQ/Change。
