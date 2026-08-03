---
bug_id: BUG-0094-miniapp-list-images-not-loading-after-speed-fix
title: 小程序商品列表图片加载优化后全部显示暂无图片
severity: high
status: done
owner: product
discovered_at: 2026-07-31 12:05:44
environment: miniapp
related_requirement: REQ-0049-miniapp-product-card-component
related_change:
created_at: 2026-07-31 21:32:14
updated_at: 2026-07-31 21:32:14
---

# 现象

微信小程序商品列表类页面中，商品卡片图片区域没有展示真实商品图，统一显示“暂无图片”。从用户截图看，“新品推荐”“热销推荐”和“全部产品”多个列表区域均受影响，而商品文字、SKU 编号、规格、品牌和参考价格仍能正常显示。

该问题发生在此前为解决 `BUG-0092-miniapp-card-images-slow-load` 做过图片加载优化之后。优化目标本应是提升加载速度，但当前效果退化为已有列表图片整体不可见。

# 复现

1. 打开微信小程序。
2. 进入首页。
3. 查看“新品推荐”“热销推荐”“全部产品”中的商品卡片。
4. 进入其他复用商品卡片的列表入口，例如分类商品列表、品牌商品列表、搜索结果页或品牌详情商品区域。
5. 观察商品卡片图片是否展示真实商品图，或是否统一显示“暂无图片”。

# 期望

- 有真实主图的商品卡片应展示真实商品图片。
- 图片加载速度优化应保留，例如懒加载、缩略图、缓存、请求节流或后端媒体链路优化。
- 缩略图不存在、对象存储响应慢或单张图片加载失败时，应具备可靠回退策略，不应导致所有有图商品都显示“暂无图片”。
- 确实没有主图或对象引用已失效的商品，才允许显示“暂无图片”。

# 实际

- 多个列表区域商品卡片均显示“暂无图片”。
- 商品基础信息可见，说明列表接口主体数据加载成功。
- 页面顶部品牌 Logo 可展示，说明不是所有媒体资源完全不可用；问题更集中在商品列表 `cover_image`、列表图片 URL 策略或商品卡片失败兜底链路。

# 影响范围

- 微信小程序首页：新品推荐、热销推荐、全部产品。
- 微信小程序商品列表页。
- 微信小程序搜索结果页。
- 微信小程序品牌详情商品列表。
- 其他复用 `components/product-card/` 且依赖商品 `cover_image` 的列表入口。
- 后端公开商品列表接口返回的 `cover_image` 字段。
- `/media/{object_key}` 受控媒体读取、缩略图路径回退和对象存储 provider 异常处理。

# 严重等级说明

严重等级：`high`。

商品图片是小程序选砖和浏览商品的核心信息。该问题影响多个商品列表入口，且表现为整片列表图片不可见，会显著降低用户识别商品、比较商品和进入详情的效率。问题还属于 `BUG-0092` 修复后的体验回归：为解决“加载慢”引入的新策略不能以“图片不展示”为代价。

# 初步分析

- 历史修复中，列表商品 `cover_image` 倾向返回 `/media/thumbnails/...` 缩略图 URL，而详情页仍保留原图 URL。
- 生产环境已确认首页和商品列表接口返回的 `cover_image` 均为 `/media/thumbnails/...`。
- 用户补充确认：此前怀疑的其他生产环境问题均正常，不作为当前主因继续展开。
- 真机异常请求显示，失败 URL 集中在 `https://tilesfst.wjoyhappy.site/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
- `tiles/pending` 是商品图片未绑定 tile_id 上传时的对象 key 形态；列表缩略图策略会把 `images/default/tiles/pending/<uuid>.jpg` 转成 `/media/thumbnails/default/tiles/pending/<uuid>.jpg`。
- 当前问题焦点进一步收敛到公开 SKU 主图 object key 生命周期和缩略图 URL 生成：公开列表不应返回不可访问的 pending 缩略图。
- 生产已确认：公开 SKU 主图存在 `images/default/tiles/pending/<uuid>.jpg`；原图对象存在，但 thumbnail 对象不存在。
- 修复策略已确认：补齐缩略图；缩略图与原图同路径存储，仅通过文件名差异区分；同时补全历史缩略图。
- 商品卡片组件在图片加载失败或未正确渲染时会切换到“暂无图片”，因此 pending 缩略图请求异常会直接转化为大面积无图。

# 真机证据

- 请求样本记录：`logs/true-device-thumbnail-requests.md`
- 异常路径模式：`/media/thumbnails/default/tiles/pending/<uuid>.jpg`

# 关联

- 相关需求：`REQ-0049-miniapp-product-card-component`
- 相关历史缺陷：`BUG-0092-miniapp-card-images-slow-load`
- 相关历史 Change：`fix-miniapp-card-image-loading`

# 附件

- 用户截图：`screenshots/miniapp-list-images-placeholder.png`
