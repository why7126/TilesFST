## 根因摘要

BUG-0137 的根因状态为 `confirmed`。小程序端已经有 `thumbnail / display / original` 多规格媒体能力，但 Banner、品牌 Logo 和分享图仍在不同入口沿用历史字段或原图 fallback：

- Banner schema 和模板以 `image_url` 为主，无法表达当前 URL 是 thumbnail、display 还是 original。
- 品牌 Logo 组件和页面仍允许 `brand_logo_thumbnail_url || brand_logo_url`，导致缺缩略图时普通展示可冷加载原图。
- SKU 详情分享图仍可从 `preview_url`、`url` 或原图字段派生，用户补证样本已复现 `share.image_url` 为 `.jpg` 原图且同对象存在 `.thumb.webp`。

## 修复方案

### Banner 轻量字段

后端小程序首页和品牌列表 Banner 响应 SHALL 暴露明确轻量字段，例如 `display_url`、`thumbnail_url` 或等价字段。小程序 Banner 轮播图属于首屏大图展示位，目标规格为 `display`。端侧普通展示优先级应为：

```text
display_url -> thumbnail_url -> 安全占位
```

`image_url` 可作为兼容字段保留，并优先与 `display_url` 对齐，但不能作为端侧唯一展示契约；若 `image_url` 指向原图或语义不明，普通展示不得直接冷加载。安全占位优先使用本地视图占位或已存在且可服务的稳定资源，不得把失败图改写为不存在的静态资源路径导致二次 500。

### 品牌 Logo fallback

品牌主页顶部品牌图位已经承担首屏 Hero 大图职责，应与小 Logo 语义拆开。品牌详情接口应暴露独立 Hero 字段：

```text
brand_hero_display_url -> brand_hero_thumbnail_url -> 安全视图占位 / 品牌名占位
```

该策略仅适用于 `pages/brand-detail/index` 顶部品牌 Hero 展示位，不扩散到品牌列表、品牌卡、商品详情品牌入口或证书详情品牌入口。Hero 字段可由品牌 Logo 同源对象派生，但端侧不得以 `brand_logo_url` 原图、preview、旧 `url`、语义不明 `image_url` 或不存在静态资源作为 fallback。

品牌 Logo 小图展示入口统一使用：

```text
brand_logo_thumbnail_url -> 安全占位 / 品牌首字 / 默认图
```

`brand_logo_url` 只保留为兼容字段、高清预览语义或后台数据引用，不作为列表、卡片、Header 小 Logo 的普通展示 fallback。若实现需要保留组件参数，默认值必须是不允许原图 fallback，只有显式高清入口才能打开。

### 分享图语义

分享图与普通展示不是同一个入口，但仍必须遵守媒体矩阵：

- 商品详情分享图优先使用明确分享轻量字段、`display_url` 或 `thumbnail_url`。
- 证书详情图片分享图优先使用 `display_url`，缺失时使用 `thumbnail_url` 或安全占位。
- 若微信分享平台或业务确需高清图，必须在代码和验收中标为分享入口例外，并证明不会影响普通展示冷加载。
- 分享对象不得暴露原始 object key、未授权对象存储地址、Authorization header、Cookie 或真实客户隐私。

### 证据与测试

实现阶段必须补齐以下证据：

- 后端测试：Banner schema、多规格 URL 字段、Banner `image_url` 兼容字段 display 优先级、品牌详情 Hero 字段、品牌 Logo 缩略图字段、SKU/证书分享图优先级、缺轻量图不合成坏 URL。
- 小程序静态测试：Banner、品牌主页 Hero、品牌 Logo、品牌卡片、SKU 分享、证书分享不再使用原图作为普通展示默认 fallback。
- 小程序静态测试：缺轻量图或加载失败时不得引用不存在的本地占位资源，例如 `/assets/tile-placeholder.png`。
- 小程序 DevTools、真机或体验版证据：记录 `source`、`page_path`、`media_kind`、`media_url_type`、`request_domain`、`http_status`、`business_status`、`resource_bytes`、`duration_ms`、`render_result`。
- 媒体 BUG 四联：key、object、URL、render 不得以 helper 或静态断言替代真实 render evidence。

## 兼容与边界

- 不新增媒体上传能力，不改变对象存储单 Bucket + 前缀策略。
- 不强制重建全部历史对象；发现历史轻量图缺失时，记录 dry-run/apply 或说明 n/a。
- 不修改店主 Web 或管理端展示行为，除非 API 类型变更要求同步 Orval 和文档。
- 不将证书 PDF/文档分享伪装为图片 display 图；PDF/文档仍走文件打开或占位策略。

## 风险

- 小程序分享图平台尺寸要求可能与轻量图目标冲突，需要用“分享入口例外”明确记录。
- 历史 Banner 或品牌 Logo 数据可能缺少派生图，修复后会显示占位而不是原图，需业务接受该降级。
- 当前 `sprint-025` 容量已到 103.33%，实现阶段应优先控制范围，避免夹带新的媒体治理能力。
