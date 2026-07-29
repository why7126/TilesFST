## Why

小程序证书列表页当前只提供聚合浏览和文件预览，缺少单张证书的完整详情承接，用户无法在一个页面内查看证书图片组、品牌信息、有效信息并分享给客户。REQ-0080 已评审通过，需要通过 OpenSpec Change 固化小程序证书详情页、公开详情接口和证书列表点击行为的契约。

## What Changes

- 新增小程序证书详情页能力，建议路由为 `pages/certificate-detail/index`，支持从证书列表、品牌详情证书区域和微信分享路径进入。
- 调整证书列表页卡片主点击行为：从直接文件预览改为进入详情页；详情页内保留图片预览和 PDF 受控打开。
- 新增或扩展公开证书详情 API，返回证书公开字段、图片组/主图、旧单文件兼容信息、品牌入口和分享信息。
- 详情页复用商品详情页的大媒体区、信息分区、品牌入口、分享和异常状态体验，但不引入收藏、推荐、价格、购物、购买、库存或询价能力。
- 将小程序自定义导航 best-practice 纳入详情页验收，覆盖分享直达、返回兜底、胶囊 reserve、页面 offset 和 DevTools/真机 evidence 边界。

## Capabilities

### New Capabilities

- 无。该变更扩展既有小程序证书展示能力，不新增独立 capability。

### Modified Capabilities

- `miniapp-certificate-list-page`: 从“证书 Tab 列表 + 文件预览”扩展为“证书列表进入详情页，详情页承载证书媒体、公开字段、品牌入口、分享、异常状态与详情 API”。

## Impact

- 后端/API：可能新增 `GET /api/v1/miniapp/certificates/{certificateId}` 或等价详情接口；需保持统一响应 envelope、公开过滤、错误码和安全 URL 边界。
- 数据库：若详情所需字段或证书图片组字段不足，需同步 SQLite/MySQL schema、migration 和数据库文档；若现有字段足够则仅消费既有证书与图片数据。
- 对象存储：详情页只消费后端受控 URL 或签名 URL，不允许小程序直连未授权对象存储或暴露 object key。
- 小程序：新增证书详情页、路由注册、证书列表卡片点击跳转、详情页媒体预览/PDF 打开、品牌入口、分享和埋点。
- Web/管理端：不改管理端维护能力；仅依赖管理端已有证书主数据、多图与主图规则。
- 测试：需补充后端公开详情接口测试、小程序静态/页面测试、DevTools 320/375/430 pt evidence；真机不可用时标记 blocked/follow_up。
- Orval：若 OpenAPI 暴露或调整小程序证书详情接口，需同步 OpenAPI/Orval 或小程序服务层调用契约。
