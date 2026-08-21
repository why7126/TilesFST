## MODIFIED Requirements

### Requirement: 首页聚合数据

系统 SHALL 为小程序首页提供公开数据聚合能力，复用现有品牌、门店、SKU、规格、类目、Banner 和媒体数据源，不新增重复业务数据源。首页聚合数据中的 Banner SHALL 仅来自小程序首页轮播位置。首页公开 Banner 数据 SHALL 对后台内部标题进行净化；`internal-*`、内部枚举、时间戳或等价后台识别字段 MUST NOT 作为公开标题、搜索兜底、分享文案或埋点展示摘要下发。

#### Scenario: 首页聚合接口净化内部 Banner 标题

- **GIVEN** 后台存在标题为 `internal-*` 或包含内部枚举/时间戳的首页 Banner
- **WHEN** 小程序请求首页聚合数据
- **THEN** 响应 SHALL 返回可展示 Banner 的公开安全字段
- **AND** 响应 SHALL NOT 暴露该 Banner 的后台内部标题
- **AND** `jump_type=none` 的 Banner SHALL NOT 通过 `title`、`search_keyword` 或等价字段携带内部标题。

### Requirement: Banner 与快捷入口

小程序首页 SHALL 复用已有后台 Banner 配置能力，并展示固定默认快捷业务入口。首页 Banner SHALL 只读取小程序首页轮播位置；品牌入口 SHALL 进入品牌列表页，品牌列表页轮播 SHALL 使用独立位置。Banner 图片 SHALL 使用后端授权、公开安全且符合性能策略的展示图 URL；若存在缩略图、展示图或压缩图字段，首页 Banner SHALL 优先使用该字段。首页存在有效 Banner 图片时，页面 SHALL NOT 渲染 Banner `title` 作为前台主标题；页面 SHALL NOT 在首页 Banner 图片上叠加从左深到右浅的渐变遮罩，且 SHALL NOT 通过透明度降低 Banner 图片本身不透明度；与标题绑定的副标题、按钮或空文案容器 SHALL NOT 造成空白占位、遮挡、错位、高度异常或内容重叠。无 Banner 数据时，首页原有品牌兜底 Hero 文案 MAY 继续展示。首页 Banner 点击、搜索兜底、分享和埋点展示链路 SHALL 对内部标题做防御，MUST NOT 让 `internal-*` 标识进入用户可见文案；`jump_type=none` 的首页 Banner 点击 SHALL 保持静默，不显示“内容建设中”或其他占位提示。

#### Scenario: 无跳转首页 Banner 不显示内部标题

- **GIVEN** 小程序首页存在 `jump_type=none` 且后台内部标题为 `internal-*` 的有效 Banner
- **WHEN** 页面渲染首页轮播并点击该 Banner
- **THEN** 页面 SHALL 只展示 Banner 图片、轮播指示点和安全点击区域
- **AND** 页面 SHALL NOT 显示 `internal-*`、内部枚举或时间戳
- **AND** 页面 SHALL NOT 在 Banner 图片上叠加从左深到右浅的渐变遮罩或透明化 Banner 图片
- **AND** 点击该无跳转 Banner SHALL 保持静默，不显示“内容建设中”或其他占位提示
- **AND** 搜索兜底、分享文案和埋点展示摘要 SHALL NOT 包含内部标题。
