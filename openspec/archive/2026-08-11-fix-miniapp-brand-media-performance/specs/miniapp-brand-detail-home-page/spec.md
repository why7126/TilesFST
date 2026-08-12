# miniapp-brand-detail-home-page Delta

## MODIFIED Requirements

### Requirement: 微信小程序品牌主页信息区
系统 SHALL 提供单品牌主页/详情页，并在页面上半部分展示可公开品牌图片和品牌基础信息。品牌主页信息区的小图展示 SHOULD 优先使用后端受控真实缩略图；大图预览、分享图或需要高清资源的入口 MAY 使用原图或等价安全引用。品牌主页信息区 SHALL 区分小图展示 URL 与高清预览或分享 URL，避免首屏直接加载大图。

#### Scenario: 品牌详情 Logo 展示使用轻量缩略图

- **WHEN** 用户进入品牌主页/详情页且品牌存在 Logo 或品牌图片
- **THEN** 页面上半部分展示的小图 SHALL 优先使用后端受控真实轻量缩略图
- **AND** 分享图、预览图或高清查看入口 MAY 使用原图或等价安全高清 URL
- **AND** 缩略图缺失、为空、0 字节、体积无收益或加载失败时 SHALL 安全回退并记录性能风险
- **AND** 响应和页面 SHALL NOT 暴露原始 object key、对象存储 endpoint、bucket 名称、Authorization header、Cookie 或未授权素材路径。

### Requirement: 品牌主页商品 Tab

商品 Tab SHALL 展示当前品牌下的公开 SKU 列表，并复用或对齐既有商品列表双列卡片、分页和状态机。商品 Tab SHALL 按 SKU 发布时间 `published_at` 升序、ID 升序展示当前品牌公开 SKU；历史数据 `published_at` 为空时，系统 SHALL 使用 SKU 创建时间 `created_at` 作为排序兜底。商品 Tab 的商品卡片图片 SHALL 复用商品列表缩略图优先策略，且非首屏商品图片 SHALL 启用懒加载或等价延迟加载。

#### Scenario: 品牌详情商品 Tab 使用商品卡片缩略图策略

- **WHEN** 用户查看品牌详情页商品 Tab
- **THEN** 商品卡片图片 SHALL 优先使用列表缩略图或等价轻量优化图片 URL
- **AND** 非首屏商品卡片图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** 商品详情、图片预览或分享场景 SHALL NOT 被强制降级为列表缩略图
- **AND** 缩略图缺失回退原图时 SHALL 记录为性能风险。

### Requirement: 品牌主页证书 Tab
证书 Tab SHALL 展示当前品牌关联且可公开的证书列表，并过滤不可展示证书和内部字段。证书 Tab 图片小图 SHOULD 优先使用后端受控真实缩略图；图片预览或证书详情 SHALL 使用原图、原文件或等价安全引用。证书 Tab SHALL 对非首屏图片类证书启用懒加载或等价延迟加载策略。

#### Scenario: 证书图片使用缩略图且预览保留原图

- **WHEN** 用户查看品牌详情页证书 Tab 且证书为图片类资源
- **THEN** 证书列表小图 SHALL 优先使用同目录 `.thumb` 缩略图或等价轻量图片 URL
- **AND** 图片预览或证书详情 SHALL 使用原图、原文件或等价受控高清 URL
- **AND** 非首屏证书图片 SHALL 启用小程序 `lazy-load` 或等价延迟加载策略
- **AND** `.thumb` 缺失、体积无收益或实际回退原图时 SHALL 在媒体四联验收中记录。
