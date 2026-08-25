## 背景

`BUG-0137-miniapp-lightweight-image-variant-consumption` 已确认：小程序仍有 Banner、品牌 Logo、分享图三类图片消费未完全符合 `thumbnail / display / original` 多规格规范。当前证据显示首页 Banner schema 仍只有 `image_url`，品牌 Logo 普通展示仍允许 `brand_logo_url` 原图 fallback，商品详情分享图在 `thumbnail_url` 同时存在时仍下发 `.jpg` 原图 `share.image_url`。

该问题会让普通展示链路继续依赖历史单字段或原图兜底，削弱 `REQ-0115-media-multi-variant-images` 已交付能力的验收可信度，并影响小程序弱网首屏、媒体缓存和对象存储流量。

## 变更内容

- 补齐小程序首页 Banner 与品牌列表 Banner 的轻量图字段语义，后端 schema/API 返回 `display_url`、`thumbnail_url` 或等价轻量展示字段；Banner 轮播图作为首屏大图展示位，端侧普通展示优先使用 `display_url`，缺失或不可读时降级到 `thumbnail_url`，不再只依赖 `image_url`。
- 将品牌主页顶部品牌图位定义为独立 Hero 大图展示位，后端品牌详情响应提供 `brand_hero_display_url` 与 `brand_hero_thumbnail_url`，端侧普通展示优先消费 display 规格并降级到 thumbnail 或安全占位；品牌列表、品牌卡和详情页品牌入口等小 Logo 场景仍只消费 `brand_logo_thumbnail_url`。
- 收紧品牌 Logo 普通展示策略：品牌列表、品牌详情、商品详情品牌卡、证书详情品牌卡等小图展示入口优先消费 `brand_logo_thumbnail_url`，缺失或加载失败时使用安全占位、品牌首字或默认图，不以 `brand_logo_url` 原图作为普通展示兜底。
- 收敛商品详情、品牌详情、证书详情分享图字段优先级，普通展示与分享入口分离记录；分享图默认使用 `display_url`、`thumbnail_url` 或明确的分享轻量字段，只有平台明确要求高清且不会影响普通展示冷加载时才允许受控例外。
- 更新小程序静态测试、后端响应测试和媒体四联验收，补齐修复后的 DevTools、真机或体验版 Network/render evidence。
- 回填 BUG-0137 acceptance 与 trace，确保 key、object、URL、render 四联闭环。

## 能力影响

### 新增能力

- 无。该 Change 是 BUG 修复，不新增独立产品能力。

### 修改能力

- `media-multi-variant-images`：补充 Banner、品牌 Logo、分享图在小程序端的强约束消费矩阵。
- `miniapp-home`：首页 Banner 聚合数据和渲染优先消费轻量图字段。
- `miniapp-brand-list-page`：品牌列表 Banner 和品牌 Logo 禁止普通展示原图 fallback。
- `miniapp-brand-detail-home-page`：品牌主页顶部 Hero 图优先消费 display 规格、thumbnail 兜底，并与小 Logo 场景分离。
- `miniapp-brand-card-component`：品牌卡片默认不允许原图 Logo fallback，只有显式高清入口可使用原图。
- `miniapp-sku-detail-page`：SKU 详情分享图字段优先级与普通展示媒体字段解耦。
- `miniapp-certificate-list-page`：证书详情分享图沿用 display 或安全占位语义，并作为分享图矩阵的一部分验收。

## 影响范围

- 后端：小程序首页、品牌列表、品牌详情、SKU 详情、证书详情相关 schema/service 响应字段与分享图构造逻辑。
- API：若新增或改名响应字段，必须同步 OpenAPI、Orval、API 文档和后端测试。
- 小程序：首页 Banner、品牌列表 Banner、品牌主页顶部 Hero、品牌 Logo、品牌卡片、SKU 分享、证书分享的字段优先级和 fallback。
- 存储：不新增 Bucket 或 key 模型；继续使用受控 `/media/` 或等价公开安全 URL。
- 数据库：默认不新增字段；若实现选择持久化新派生字段或状态，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试。
- 验收：必须补媒体 BUG 四联、小程序 Network/render evidence、缺轻量图降级态和静态测试。

## 回滚计划

- 保留后端旧字段兼容读取，但普通展示端侧不得自动恢复原图 fallback。
- 若新增字段导致老客户端异常，可先保留 `image_url` / `brand_logo_url` 兼容字段，同时将新轻量字段作为优先消费字段。
- 若某类历史数据缺少派生图，回滚时只回退到安全占位或暂停相关 Banner/Logo 展示，不恢复普通展示加载原图。
- 如 API schema 变更出现兼容风险，回滚相关 schema/service 和 Orval 生成物，并保留 BUG-0137 trace 中的阻塞证据。
