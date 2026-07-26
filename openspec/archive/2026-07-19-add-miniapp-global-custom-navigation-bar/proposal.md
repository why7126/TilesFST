## Why

微信小程序已有首页品牌自定义导航栏，但搜索、详情、分类、列表、收藏、证书和门店信息等非首页还缺少统一顶部导航契约。REQ-0048 要求将导航能力扩展为全局模块，确保非首页可稳定返回、右侧避让微信原生胶囊，并避免 fixed header 遮挡页面内容。

## What Changes

- 新增小程序全局自定义导航栏能力，区分首页形态与非首页形态。
- 首页继续保留当前品牌 `brand-header`，不显示左侧返回按钮。
- 非首页复用同一导航模块，在左侧显示返回按钮，并提供无页面栈时的首页兜底。
- 所有覆盖页面右侧避让微信原生分享 / 关闭胶囊，不手绘模拟系统胶囊。
- 页面主体、加载态、空态、错误态、骨架屏和下拉刷新区域统一避让 fixed header。
- 覆盖 search、tile-detail、category、product-list、favorites、certificates、store-info 等页面。

## Capabilities

### New Capabilities

- `miniapp-global-custom-navigation-bar`: 小程序首页与非首页统一自定义导航栏契约，覆盖返回、原生胶囊避让、状态栏安全区和内容不遮挡。

### Modified Capabilities

- 无。本 Change 新增独立全局导航能力；与既有 `miniapp-home` 首页品牌导航能力保持兼容，不修改其已归档需求。

## Impact

- **Miniapp:** 预计影响 `src/miniapp` 的导航组件、全局配置、首页和主要非首页页面 WXML/WXSS/TS。
- **API:** 默认不新增或调整 API。
- **Database:** 默认不新增表或字段。
- **Storage:** 默认不新增对象存储能力；Logo 或图片继续使用已有安全 URL 或本地安全资源。
- **Web/Admin:** 不涉及 Web 展示端或管理端。
- **Orval:** 默认不需要；若后续实现新增 API contract，必须另行同步 OpenAPI、Orval、docs 和测试。
