## MODIFIED Requirements

### Requirement: 品牌列表页轮播

品牌列表页 SHALL 在顶部提供品牌轮播区域，并 SHALL 与小程序首页轮播保持一致的基础交互体验。品牌轮播区域 SHALL NOT 展示开发、原型、验收或能力说明类文案作为正式用户可见内容。品牌列表页存在有效 Banner 图片时，轮播 SHALL 以图片为主视觉，SHALL NOT 渲染 Banner `title` 作为前台主标题；与标题绑定的副标题、按钮或空文案容器 SHALL NOT 造成空白占位、遮挡、错位、高度异常或内容重叠。无轮播数据时，品牌列表页原有品牌化兜底 MAY 继续展示。

#### Scenario: 品牌轮播展示

- **WHEN** 品牌列表页存在有效轮播数据
- **THEN** 页面 SHALL 展示品牌轮播图片和指示点
- **AND** 页面 SHALL NOT 渲染 Banner `title` 作为轮播主标题
- **AND** 轮播 SHALL 支持自动播放和循环播放
- **AND** 页面 SHALL NOT 展示 `BRAND GALLERY`、`轮播图保持现有品牌页能力` 或等价开发/说明性文案。

#### Scenario: 品牌轮播文案清理后布局稳定

- **WHEN** 品牌列表页轮播图移除 Banner 标题和多余说明文案
- **THEN** 轮播图区域 SHALL NOT 留下空白占位、遮挡、错位、高度异常或内容重叠
- **AND** 品牌轮播图片加载、轮播切换、指示点和既有点击或跳转行为 SHALL 保持可用。

#### Scenario: 无轮播数据降级

- **WHEN** 品牌列表页没有有效轮播数据或轮播图片加载失败
- **THEN** 页面 SHALL 隐藏异常轮播项或展示品牌化兜底
- **AND** 本兜底文案 SHALL NOT 被视为 Banner `title` 遮罩回归。
