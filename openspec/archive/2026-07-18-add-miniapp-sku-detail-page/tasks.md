## 1. API 与数据边界

- [x] 1.1 盘点现有 SKU、品牌、类目、规格、图片和视频数据是否满足 SKU 详情页公开字段。
- [x] 1.2 设计小程序 SKU 详情响应 schema，覆盖 SKU 主体、媒体、品牌、收藏状态、同系列推荐和同品牌推荐。
- [x] 1.3 实现或调整 `GET /api/v1/miniapp/skus/{skuId}` 或等价详情接口，确保只返回公开字段和安全媒体 URL。
- [x] 1.4 实现 SKU 不存在、已下架、不可公开、缺少媒体和网络异常对应错误码或降级响应。
- [x] 1.5 如需新增收藏、公开状态、推荐或媒体关系字段，同步 SQLite/MySQL schema、迁移、数据库文档和测试。

## 2. 收藏、分享与推荐

- [x] 2.1 实现 SKU 粒度收藏与取消收藏接口，保证幂等、失败可回滚、授权失败不误写收藏事实。
- [x] 2.2 实现详情页分享数据生成，优先后台分享图，缺失时安全降级到主图或默认品牌图。
- [x] 2.3 实现品牌入口数据和跳转参数，目标不可用时安全降级。
- [x] 2.4 实现同系列推荐和同品牌推荐查询，排除当前 SKU 并对同品牌推荐去除同系列已出现项。
- [x] 2.5 确认购物车、立即购买、在线下单、支付、库存、优惠券、促销倒计时和询价承诺未进入接口或页面。

## 3. 小程序页面与媒体交互

- [x] 3.1 新增或完善小程序 SKU 详情页路由，承接首页、分类、搜索、品牌页、收藏页和分享卡片入口。
- [x] 3.2 实现详情页骨架屏、正常态、SKU 不存在/已下架、网络失败、图片失败、视频失败和推荐为空状态。
- [x] 3.3 实现顶部图片/视频混合轮播，主图固定第一项，媒体计数准确展示。
- [x] 3.4 实现图片全屏预览、缩放/拖动/切换或小程序平台等价能力，并支持原图加载失败重试。
- [x] 3.5 实现视频用户主动播放、播放期间停止轮播、页面隐藏或跳转暂停视频。
- [x] 3.6 实现品牌卡、SKU 摘要、商品参数、备注卡、同系列、同品牌和底部操作栏布局。
- [x] 3.7 实现收藏/取消收藏、品牌按钮、分享按钮和推荐卡点击反馈，失败时不阻断主浏览流程。

## 4. 埋点与安全

- [x] 4.1 扩展 usage event 字典，支持 `sku_detail_view`、`sku_media_swipe`、`sku_image_preview`、`sku_video_play`、`sku_favorite`、`sku_unfavorite`、`sku_share_click`、`sku_brand_click`、`sku_recommend_click` 和 `sku_load_error`。
- [x] 4.2 确保 SKU 详情页事件只携带必要 SKU ID、入口、目标 SKU、推荐类型、client type 和时间上下文。
- [x] 4.3 增加服务端校验，拒绝或移除 token、password、Authorization、Cookie、raw object key、raw payload 和内部路径等禁止属性。
- [x] 4.4 确保埋点失败不阻断详情展示、媒体浏览、收藏、分享或推荐跳转。

## 5. 文档、生成物与测试

- [x] 5.1 若 API contract 变化，更新 OpenAPI、Orval、`docs/03-api-index.md` 和错误码说明。
- [x] 5.2 若 DB schema 变化，更新 `docs/04-database-design.md`、迁移脚本和 SQLite/MySQL 兼容测试。
- [x] 5.3 补充后端测试，覆盖公开字段过滤、详情成功、不可公开状态、收藏幂等、推荐排除、安全媒体 URL 和 usage event 脱敏。
- [x] 5.4 补充小程序静态或行为测试，覆盖入口路由、媒体状态、收藏分享交互、异常状态和范围外能力未出现。
- [x] 5.5 记录原型/截图验收证据，覆盖 320 到 430px 逻辑宽度、底部安全区、44x44px 点击目标和深色视觉对齐。
- [x] 5.6 运行 OpenSpec validate、相关后端测试、小程序静态测试，并在 Change trace 中记录结果。
## 6. Sprint 与追溯

- [x] 6.1 确认 `REQ-0044` trace 指向 `add-miniapp-sku-detail-page`，且 `iteration: sprint-008`。
- [x] 6.2 将 `add-miniapp-sku-detail-page` 加入 `iterations/archive/sprint-008/sprint.yaml` 的 `changes[]` 并运行 Workflow Sync。
- [x] 6.3 在 `/opsx-apply` 前确认 sprint-008 同时包含 `REQ-0044` 与 `add-miniapp-sku-detail-page`，避免迭代纳入门禁失败。
