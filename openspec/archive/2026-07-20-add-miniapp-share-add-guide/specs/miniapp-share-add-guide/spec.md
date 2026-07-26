## ADDED Requirements

### Requirement: 小程序添加引导语展示
系统 SHALL 在微信小程序进入场景提供“添加到我的小程序”引导语，使用户知道可以通过右上角微信原生入口添加小程序，方便下次找回。

#### Scenario: 未关闭时进入小程序展示引导语
- **WHEN** 用户以普通启动方式进入小程序且添加引导未处于关闭记忆有效期
- **THEN** 小程序 SHALL 展示表达“添加到我的小程序，方便下次找回”含义的引导语
- **AND** 引导语 SHALL 以轻提示、气泡或等价形式呈现
- **AND** 引导语 SHALL NOT 阻塞首页搜索、分类、Banner、商品卡片或其他主内容。

#### Scenario: 扫码或分享进入时安全展示
- **WHEN** 用户从扫码、分享卡片或外部入口进入小程序且引导语需要展示
- **THEN** 引导语 SHALL NOT 遮挡当前页面核心内容、返回入口、错误提示或重试入口
- **AND** 若当前页面状态不适合展示引导语，小程序 SHALL 安全降级为不展示或延后展示
- **AND** 页面 SHALL NOT 因引导语失败而白屏、报错或阻断浏览。

### Requirement: 微信原生胶囊与导航避让
系统 SHALL 使添加引导语避让微信原生胶囊、状态栏、自定义导航栏和页面首屏内容，并 SHALL 禁止模拟微信系统控件。

#### Scenario: 引导语避让原生胶囊
- **WHEN** 小程序展示添加引导语
- **THEN** 引导语容器、箭头和关闭入口 SHALL NOT 进入微信原生分享 / 更多 / 关闭胶囊区域
- **AND** 引导语位置 SHALL 基于微信菜单按钮信息、状态栏高度或项目统一 fallback 计算
- **AND** 页面 SHALL NOT 使用 WXML、WXSS、自定义图片或文本模拟微信分享按钮、更多按钮、关闭按钮或系统胶囊。

#### Scenario: 引导语不遮挡自定义导航
- **WHEN** 首页或非首页存在自定义导航栏
- **THEN** 引导语 SHALL NOT 遮挡首页品牌 Logo、门店名称、品牌副文案、搜索入口、非首页返回按钮或页面标题
- **AND** 在 320、375、430 pt 视口下，引导语、胶囊 reserve、导航文字和页面首屏内容 SHALL 无明显重叠
- **AND** 页面 SHALL NOT 产生横向滚动。

### Requirement: 手工关闭与展示频率
系统 SHALL 允许用户手工关闭添加引导语，并 SHALL 在关闭记忆有效期内避免重复展示。

#### Scenario: 用户关闭引导语
- **WHEN** 用户点击添加引导语的关闭入口
- **THEN** 小程序 SHALL 立即隐藏引导语
- **AND** 关闭入口有效点击区域 SHALL 不小于 32x32 pt
- **AND** 关闭入口 SHALL NOT 与微信原生胶囊重叠。

#### Scenario: 关闭后当前会话不再展示
- **WHEN** 用户已关闭添加引导语且当前会话仍有效
- **THEN** 小程序 SHALL NOT 再次展示添加引导语
- **AND** 若实现采用当天或长期关闭记忆，验收材料 SHALL 记录具体记忆周期和再次进入行为
- **AND** 本地关闭状态写入失败 SHALL NOT 影响页面主功能。

### Requirement: API 数据与安全边界
系统 SHALL 默认以小程序本地状态实现添加引导能力，不新增 API、数据库、Web 管理端配置或 Orval 变更。

#### Scenario: 默认不新增服务端能力
- **WHEN** 实现添加引导语
- **THEN** 系统 SHALL NOT 默认新增后端接口、数据库表、数据库字段、迁移、Web 管理端配置页或 Orval 生成物
- **AND** 关闭状态 SHALL 优先使用小程序本地状态或本地存储
- **AND** 若后续实现必须新增服务端配置或埋点接口，Change SHALL 同步 OpenAPI、Orval、docs、数据库文档和测试。

#### Scenario: 引导或埋点不记录敏感信息
- **WHEN** 系统记录引导展示、关闭或相关入口点击意向事件
- **THEN** 事件 SHALL NOT 记录手机号、地址、微信身份标识、Authorization header、Cookie、`.env` 内容、真实客户数据或其他不必要敏感信息
- **AND** 事件 SHOULD 仅包含匿名事件类型、页面、时间和必要上下文。

### Requirement: 设备验收 evidence
系统 SHALL 为添加引导语实现保留可复核的小程序设备验收 evidence，并 SHALL 区分静态测试、DevTools 预览和真机验收结论。

#### Scenario: DevTools 视口 evidence
- **WHEN** 团队验收添加引导语实现
- **THEN** 验收材料 SHALL 记录 DevTools 320、375、430 pt 视口下的引导位置、胶囊 reserve、关闭按钮和首屏遮挡结论
- **AND** evidence SHALL 使用仓库相对路径、稳定 artifact 引用或人工摘要
- **AND** evidence SHALL NOT 记录本机绝对路径、token、Cookie、Authorization header、`.env` 内容、真实密钥或真实客户隐私。

#### Scenario: 真机 evidence 边界
- **WHEN** 团队执行真机验收
- **THEN** evidence SHALL 记录设备型号、系统类型、微信版本、页面路径、状态栏、胶囊避让、关闭行为和剩余风险
- **AND** 若无法执行真机验收，验收材料 SHALL 标记 `blocked` 或 `follow_up` 并说明原因
- **AND** 静态测试或 DevTools 通过 SHALL NOT 被表述为真机通过。
