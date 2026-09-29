---
created_at: '2026-09-08 18:36:57'
updated_at: '2026-09-08 18:36:57'
---

## MODIFIED Requirements

### Requirement: 微信小程序品牌主页信息区
系统 SHALL 提供单品牌主页/详情页，并在页面上半部分展示可公开品牌图片和品牌基础信息。品牌主页顶部品牌图位 SHALL 作为首屏 Hero 大图展示位，普通展示 SHALL 优先使用后端受控 `display` 规格；品牌列表、品牌卡、商品详情品牌入口和证书详情品牌入口等小 Logo 场景 SHALL 继续优先使用后端受控真实缩略图。品牌主页信息区 SHALL 区分 Hero 展示 URL、小 Logo 展示 URL、高清预览或分享 URL，避免首屏直接加载原图。


品牌详情头图 SHALL 在既有稳定容器内等比完整适配并居中，允许上下或左右留白，SHALL NOT 裁切、拉伸或位移隐藏图片内容。展示图和缩略图回退 SHALL 使用相同适配规则；图片URL与变体消费、权限、加载和错误回退契约 SHALL 保持。
品牌头图 SHALL 在原总高内划分互不重叠的图片和文字区域，保留品牌名、英文名与描述及其原截断语义。

#### Scenario: 品牌详情顶部 Hero 展示使用 display 规格

- **WHEN** 用户进入品牌主页/详情页且品牌存在 Logo 或品牌图片
- **THEN** 页面上半部分顶部 Hero SHALL 优先请求 `brand_hero_display_url` 或等价 `display` 规格 URL
- **AND** `display` 规格缺失、为空或加载失败时 SHALL 降级请求 `brand_hero_thumbnail_url` 或等价轻量缩略图
- **AND** `display` 与 `thumbnail` 均不可用时 SHALL 展示安全视图占位、品牌名占位或可理解失败态
- **AND** 品牌主页顶部 Hero SHALL NOT 通过 `brand_logo_url`、`original_url`、`preview_url`、旧 `url`、语义不明 `image_url` 或不存在的本地静态资源冷加载原图或失败占位。

#### Scenario: 品牌详情头图不同比例完整显示

- **WHEN** 图片比例与容器不同，或展示图失败后切换到可用缩略图
- **THEN** 页面 SHALL 完整显示当前图片画面且保持等比与居中
- **AND** 页面 SHALL 保持容器高度，不因切换、加载或回退产生布局跳动
- **AND** 320、375、430pt等价逻辑宽度下 SHALL 无横向溢出或图片边缘裁切

#### Scenario: 品牌详情头图空态与既有交互兼容

- **WHEN** 图片为空、全部加载失败或用户触发现有点击与切换
- **THEN** 页面 SHALL 沿用既有占位、跳转、预览和轮播契约
- **AND** 页面 SHALL NOT 因完整适配新增原图冷加载或改变非Banner图片展示

#### Scenario: 品牌文字不遮挡头图

- **WHEN** 品牌名称或简介较长，或英文名与简介为空
- **THEN** 页面 SHALL 保持品牌头图总高度及独立图文区域
- **AND** 图片 SHALL 完整适配，品牌名一行、简介两行沿用既有截断语义且不覆盖图片
