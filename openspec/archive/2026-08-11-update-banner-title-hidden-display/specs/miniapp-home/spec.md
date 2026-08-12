## MODIFIED Requirements

### Requirement: Banner 与快捷入口

小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。首页 Banner SHALL 只读取小程序首页轮播位置；品牌入口 SHALL 进入品牌列表页，品牌列表页轮播 SHALL 使用独立位置。Banner 图片 SHALL 使用后端授权、公开安全且符合性能策略的展示图 URL；若存在缩略图、展示图或压缩图字段，首页 Banner SHALL 优先使用该字段。首页存在有效 Banner 图片时，页面 SHALL NOT 渲染 Banner `title` 作为前台主标题；与标题绑定的副标题、按钮或空文案容器 SHALL NOT 造成空白占位、遮挡、错位、高度异常或内容重叠。无 Banner 数据时，首页原有品牌兜底 Hero 文案 MAY 继续展示。

#### Scenario: 首页轮播与品牌列表页轮播隔离

- **WHEN** 小程序首页加载 Banner
- **THEN** 首页 SHALL 只展示小程序首页轮播位置中已上线且有效期内的 Banner
- **AND** 首页 SHALL NOT 展示品牌列表页轮播位置 Banner
- **WHEN** 品牌列表页无轮播数据
- **THEN** 首页轮播 SHALL NOT 被用作品牌列表页兜底。

#### Scenario: 首页 Banner 标题遮罩移除

- **GIVEN** 小程序首页存在有效 Banner 图片
- **WHEN** 页面渲染首页轮播
- **THEN** 页面 SHALL 展示 Banner 图片、轮播指示点和点击区域
- **AND** 页面 SHALL NOT 渲染 `item.title` 或等价 Banner 标题作为主标题
- **AND** Banner 点击跳转、轮播切换和快捷入口展示 SHALL 保持可用。

#### Scenario: 首页 Banner 无数据兜底

- **GIVEN** 小程序首页没有可用 Banner 数据
- **WHEN** 页面渲染首页首屏
- **THEN** 首页 MAY 展示原有品牌兜底 Hero 文案
- **AND** 本兜底文案 SHALL NOT 被视为 Banner `title` 遮罩回归。
