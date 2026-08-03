## MODIFIED Requirements

### Requirement: 品牌列表页轮播
品牌列表页 SHALL 在顶部提供品牌轮播区域，并 SHALL 与小程序首页轮播保持一致的基础交互体验。品牌轮播区域 SHALL NOT 展示开发、原型、验收或能力说明类文案作为正式用户可见内容。

#### Scenario: 品牌轮播展示
- **WHEN** 品牌列表页存在有效轮播数据
- **THEN** 页面 SHALL 展示品牌轮播图片、标题、副标题和指示点
- **AND** 轮播 SHALL 支持自动播放和循环播放
- **AND** 指示点激活态 SHALL 使用品牌金或等价品牌强调语义。
- **AND** 页面 SHALL NOT 展示 `BRAND GALLERY`、`轮播图保持现有品牌页能力` 或等价开发/说明性文案。

#### Scenario: 品牌轮播跳转
- **WHEN** 用户点击有效品牌轮播项
- **THEN** 小程序 SHALL 按配置跳转到品牌详情、品牌商品列表、商品详情、搜索或门店信息等可达目标
- **AND** 当目标不可达时，小程序 SHALL 安全降级并提示
- **AND** 小程序 SHALL NOT 打开空白页或无效路由。

#### Scenario: 品牌轮播图片安全
- **WHEN** 品牌轮播展示图片
- **THEN** 图片 URL SHALL 是公开安全 URL 或后端授权 URL
- **AND** 响应 SHALL NOT 暴露 MinIO 原始 object key、内部路径、Authorization header 或 Cookie。

#### Scenario: 无轮播数据降级
- **WHEN** 品牌列表页没有有效轮播数据或轮播图片加载失败
- **THEN** 页面 SHALL 隐藏异常轮播项或展示品牌化兜底
- **AND** 页面 SHALL NOT 展示破图。

#### Scenario: 品牌轮播文案清理后布局稳定
- **WHEN** 品牌列表页轮播图移除多余说明文案
- **THEN** 轮播图区域 SHALL NOT 留下空白占位、遮挡、错位、高度异常或内容重叠
- **AND** 品牌轮播图片加载、轮播切换、指示点和既有点击或跳转行为 SHALL 保持可用。
