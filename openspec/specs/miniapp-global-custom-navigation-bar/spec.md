# miniapp-global-custom-navigation-bar Specification

## Purpose
TBD - created by archiving change add-miniapp-global-custom-navigation-bar. Update Purpose after archive.
## Requirements
### Requirement: 小程序全局自定义导航栏
系统 SHALL 提供小程序全局自定义导航栏能力，使首页和主要非首页页面共享一致的顶部导航契约，并按页面类型收束 `brand-header` 标题规则。

#### Scenario: 首页固定品牌双行文案

- **WHEN** 用户打开微信小程序首页
- **THEN** 页面 SHALL 使用首页品牌 `brand-header` 或等价品牌导航形态
- **AND** 第一行 SHALL 固定展示 `菲尚特瓷砖馆`
- **AND** 第二行 SHALL 固定展示 `质感空间，由砖而生`
- **AND** 首页 SHALL NOT 显示左侧返回按钮
- **AND** 首页品牌文案 SHALL NOT 被接口门店描述、页面标题、SKU 信息或其他上下文覆盖
- **AND** 首页右侧 SHALL 避让微信原生分享 / 关闭胶囊
- **AND** 首页搜索框、Banner 和入口区 SHALL 从导航栏下方开始展示且不被遮挡。

#### Scenario: 非首页仅展示单行页面标题

- **WHEN** 用户打开 search、tile-detail、category、product-list、favorites、certificates 或 store-info 页面
- **THEN** 页面 SHALL 使用同一导航模块的非首页形态
- **AND** 左侧 SHALL 显示返回按钮
- **AND** 标题区域 SHALL 只展示一行页面标题
- **AND** 页面 SHALL NOT 展示 `subtitle`、品牌副文案、SKU 编号第二行或其他辅助第二行
- **AND** 首页形态和非首页形态 SHALL 由页面类型区分，不得在首页误显示返回按钮。

#### Scenario: 覆盖页面标题映射稳定

- **WHEN** 覆盖页面渲染非首页 `brand-header`
- **THEN** search 页面标题 SHALL 为 `搜索`
- **AND** category 页面标题 SHALL 为 `全部分类` 或等价分类页标题
- **AND** product-list 页面 SHALL 展示一行列表标题
- **AND** tile-detail 页面标题 SHALL 固定为 `商品详情`
- **AND** favorites 页面标题 SHALL 为 `收藏`
- **AND** certificates 页面标题 SHALL 为 `证书`
- **AND** store-info 页面标题 SHALL 为 `门店信息`
- **AND** SKU 编号、商品名、品牌信息、分类上下文或关键词上下文 SHALL 保留在页面内容区或列表区，不得作为第二行标题展示。

#### Scenario: 非首页长标题单行截断

- **WHEN** 非首页标题超过可用宽度
- **THEN** 标题 SHALL 单行截断
- **AND** 标题 SHALL NOT 换行、横向滚动或挤压右侧微信原生胶囊避让区
- **AND** 在 320、375、430 pt 宽度下，返回按钮、标题和右侧胶囊避让区 SHALL 无重叠。

#### Scenario: 后续页面默认遵守非首页规则

- **WHEN** find、profile 或后续新增页面接入自定义导航栏
- **THEN** 页面 SHOULD 默认使用非首页单行标题规则
- **AND** 若页面需要豁免，SHALL 通过后续需求或 OpenSpec Change 明确说明。

### Requirement: 非首页返回行为
系统 SHALL 为小程序非首页导航栏提供稳定返回能力。

#### Scenario: 有页面栈时返回上一页

- **WHEN** 非首页页面栈存在上一页且用户点击返回按钮
- **THEN** 小程序 SHALL 返回上一页
- **AND** 返回过程 SHALL NOT 破坏当前页面的分享、刷新或错误重试能力。

#### Scenario: 无页面栈时兜底返回首页

- **WHEN** 用户从分享卡片或外部入口直达非首页且页面栈无上一页
- **AND** 用户点击返回按钮
- **THEN** 小程序 SHALL 进入明确兜底路径
- **AND** 兜底路径 SHOULD 为首页
- **AND** 页面 SHALL NOT 报错、白屏或停留在无反馈状态。

#### Scenario: 返回按钮触控区域可用

- **WHEN** 用户在 320 到 430 pt 宽度范围操作非首页导航栏
- **THEN** 返回按钮有效点击区域 SHALL 不小于 44x44 pt
- **AND** 返回按钮 SHALL NOT 与品牌 Logo、页面标题、微信原生胶囊或页面内容重叠。

#### Scenario: 状态页返回按钮可用

- **WHEN** 非首页处于加载态、空态、错误态或骨架屏
- **THEN** 返回按钮 SHALL 保持可见且可点击
- **AND** 点击返回 SHALL 遵守有页面栈返回上一页、无页面栈兜底回首页的规则。

### Requirement: 微信原生胶囊与状态栏避让
系统 SHALL 在所有覆盖页面避让微信原生分享 / 关闭胶囊和状态栏安全区，并 SHALL 在小程序首页设备验收中补齐可复核 evidence。

#### Scenario: 右侧避让微信原生胶囊
- **WHEN** 页面渲染自定义导航栏
- **THEN** 导航栏右侧 SHALL 为微信原生分享 / 关闭胶囊预留不可占用区域
- **AND** 品牌信息、页面标题、返回按钮、搜索入口或其他自定义元素 SHALL NOT 进入该区域。

#### Scenario: 禁止手绘系统胶囊
- **WHEN** 团队实现或验收自定义导航栏
- **THEN** 页面 SHALL NOT 在 WXML / WXSS 中自绘模拟微信分享按钮、关闭按钮或系统胶囊
- **AND** 支持分享的页面 SHALL 保留微信小程序原生分享能力。

#### Scenario: 状态栏高度动态适配
- **WHEN** 页面在不同机型、不同状态栏高度或 320 到 430 pt 宽度范围渲染
- **THEN** 导航栏 SHALL 使用微信小程序可获得的系统信息、菜单按钮信息或等价安全区信息计算布局
- **AND** 页面 SHALL NOT 依赖单一机型硬编码高度完成验收。

#### Scenario: BUG-0068 首页胶囊与状态栏 evidence 闭环
- **WHEN** 团队验收首页品牌自定义导航栏
- **THEN** evidence SHALL 覆盖 320、375、390、430 pt 及 320-430 pt 常见宽度下的微信原生胶囊、状态栏和品牌导航布局
- **AND** 品牌 Logo、门店名称、品牌副文案、返回区域、搜索入口或其他自定义元素 SHALL NOT 进入原生胶囊区域
- **AND** 胶囊区域 SHOULD 在截图中可辨认且未被页面内容覆盖
- **AND** 若真机无法验收，材料 SHALL 标记 `blocked` 或 `follow_up`，不得写作真机通过。

### Requirement: fixed header 内容避让
系统 SHALL 确保所有覆盖页面的主体内容、状态页和滚动区域不被 fixed header 遮挡。

#### Scenario: 首屏内容避让导航栏
- **WHEN** search、tile-detail、category、product-list、favorites、certificates 或 store-info 页面加载
- **THEN** 页面主体内容 SHALL 从导航栏下方开始展示
- **AND** 搜索框、媒体轮播、分类列表、商品列表、收藏列表、证书列表和门店信息首屏内容 SHALL NOT 被 fixed header 遮挡。

#### Scenario: 状态页与下拉刷新避让导航栏
- **WHEN** 页面处于加载态、空状态、错误态、骨架屏或下拉刷新状态
- **THEN** 对应内容 SHALL 使用同一导航栏 offset
- **AND** SHALL NOT 被 fixed header 遮挡或与导航栏重叠。

#### Scenario: 统一顶部 offset 策略
- **WHEN** 团队验收页面布局实现
- **THEN** 覆盖页面 SHOULD 使用统一变量、工具函数或 layout class 承接导航栏高度
- **AND** 页面 SHALL NOT 散落互相冲突的顶部 padding 硬编码。

#### Scenario: BUG-0068 首页 fixed header 与底部 TabBar evidence 闭环
- **WHEN** 团队检查首页首屏、滚动中段和页面底部
- **THEN** fixed header SHALL 通过 spacer、offset 或等价方式为内容让位
- **AND** 底部 TabBar 与安全区 SHALL 不遮挡商品卡片、加载状态、空状态或主要点击目标
- **AND** 主要点击目标 SHOULD 不小于 44x44 pt
- **AND** evidence SHALL 明确记录结论、截图/录屏/人工摘要和剩余风险。

### Requirement: 范围与数据边界
系统 SHALL 保持本 Change 为小程序导航 UI refinement，不扩展后台配置、API、数据库或业务页面范围。

#### Scenario: 不新增业务页面

- **WHEN** 实现本 Change
- **THEN** 系统 SHALL NOT 因导航栏新增 search、tile-detail、category、product-list、favorites、certificates 或 store-info 之外的新业务页面
- **AND** 底部 TabBar 文案、图标和路由 SHALL NOT 因本 Change 调整。

#### Scenario: 默认不新增接口与数据库

- **WHEN** 实现本 Change
- **THEN** 系统 SHALL NOT 默认新增 API、数据库表或字段
- **AND** 若实现阶段发现必须调整接口 contract，SHALL 同步 OpenAPI、Orval、docs 和测试
- **AND** 若实现阶段新增字段，SHALL 同步 SQLite/MySQL schema、数据库文档和测试。

#### Scenario: 媒体与 Logo 安全边界

- **WHEN** 导航栏展示 Logo 或图片资源
- **THEN** 小程序 SHALL 使用后端返回的安全 URL 或本地安全资源
- **AND** SHALL NOT 直连未授权对象存储或暴露 raw object key。

#### Scenario: 不提供标题后台配置

- **WHEN** 实现首页品牌文案或非首页页面标题规则
- **THEN** 系统 SHALL NOT 新增后台标题配置、品牌副文案配置或详情标题配置
- **AND** 首页品牌文案和覆盖页面短标题 SHALL 由小程序端导航契约或本地安全常量承接。

### Requirement: 小程序自定义导航 best-practice

系统 SHALL 为小程序自定义导航栏维护可复用 best-practice，用于后续小程序页面、OpenSpec Change、Sprint 验收报告和 release note 统一引用状态栏、微信原生胶囊、返回兜底、页面 offset 和截图验收矩阵规则。

#### Scenario: best-practice 文档存在且结构完整

- **WHEN** 本能力实现完成
- **THEN** 仓库 SHALL 存在小程序自定义导航 best-practice 长期文档
- **AND** 文档 SHOULD 位于 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
- **AND** 文档 SHALL 包含适用范围、导航结构、状态栏与胶囊、返回兜底、页面 offset、截图验收矩阵、页面接入 checklist 和引用示例。

#### Scenario: 页面接入 checklist 可复用

- **WHEN** 后续新增或改造小程序页面并涉及自定义导航栏
- **THEN** 团队 SHALL 使用 best-practice checklist 判断页面属于首页形态、TabBar 页面形态、普通非首页形态或详情 / 分享直达形态
- **AND** checklist SHALL 覆盖标题截断、胶囊 reserve、返回兜底、原生分享、首屏内容遮挡和 N/A reason
- **AND** 若页面豁免自定义导航，验收材料 SHALL 记录豁免原因。

#### Scenario: 状态栏与胶囊规则集中说明

- **WHEN** 团队实现或验收自定义导航栏
- **THEN** best-practice SHALL 要求优先使用微信小程序窗口、状态栏和菜单按钮信息或项目确认的兼容封装
- **AND** SHALL 说明状态栏高度、导航内容高度、总导航高度和右侧胶囊 reserve 的记录或验收方式
- **AND** SHALL 定义获取状态栏或胶囊信息失败时的统一 fallback
- **AND** fallback SHALL NOT 散落在多个页面中各自定义义。

#### Scenario: 返回兜底规则集中说明

- **WHEN** 后续 Change 涉及小程序自定义导航返回按钮
- **THEN** best-practice SHALL 要求有上一页页面栈时优先返回上一页
- **AND** 无上一页页面栈时 SHALL 进入明确兜底路径
- **AND** 兜底路径失败时 SHALL 存在二级安全入口
- **AND** 分享卡片、扫码、收藏入口或外部入口直达详情页时返回按钮 SHALL NOT 失效、报错或无反馈。

#### Scenario: 页面 offset 规则集中说明

- **WHEN** 后续 Change 涉及 fixed 或 sticky 自定义导航
- **THEN** best-practice SHALL 要求页面主体通过统一 spacer、CSS 变量、style 片段、class 或等价布局 token 避让导航高度
- **AND** 首页首屏、搜索框、分类列表、商品列表、SKU 媒体区、收藏列表、证书列表、门店信息、加载态、骨架屏、空状态、错误态和网络失败提示 SHALL 纳入内容不遮挡验收
- **AND** 不同页面 SHALL NOT 各自硬编码互相冲突的顶部 padding；若确需特殊 offset，验收材料 SHALL 记录原因。

### Requirement: 自定义导航截图验收矩阵

系统 SHALL 为小程序自定义导航 best-practice 定义截图验收矩阵，并复用小程序设备验收 evidence 模板区分 DevTools 预览、真机验收、blocked、not_applicable 和 follow_up 结论。

#### Scenario: 矩阵维度完整

- **WHEN** 团队为小程序自定义导航相关 Change 制定验收计划
- **THEN** 截图验收矩阵 SHALL 覆盖页面、入口、DevTools 视口、真机类型、页面状态和结论字段
- **AND** 页面维度 SHOULD 包含首页、搜索、分类、商品列表、商品详情、收藏、证书和门店信息
- **AND** DevTools 视口维度 SHOULD 包含 320 pt、375 pt 和 430 pt
- **AND** 页面状态维度 SHOULD 包含正常、加载、空状态、错误态、网络失败和长标题。

#### Scenario: DevTools 与真机结论分层

- **WHEN** 团队记录自定义导航截图验收结果
- **THEN** DevTools evidence 与真机 evidence SHALL 分层记录
- **AND** 没有真机记录时 SHALL NOT 写作真机通过
- **AND** 无法执行真机验证时 SHALL 标记 `blocked` 或 `follow_up` 并说明原因。

#### Scenario: 矩阵结论可复核且安全

- **WHEN** 团队记录自定义导航截图、录屏、报告或人工摘要
- **THEN** evidence SHALL 能记录状态栏不遮挡、胶囊不重叠、返回可用、首屏内容不被遮挡和无横向滚动结论
- **AND** 证据路径 SHALL 使用仓库相对路径或稳定 artifact 引用
- **AND** SHALL NOT 记录本机绝对路径、token、Cookie、Authorization header、`.env` 内容、真实密钥、数据库 DSN、MinIO 凭据或真实客户隐私。

#### Scenario: 后续流程引用 best-practice

- **WHEN** 后续小程序 REQ、OpenSpec Change、Sprint 验收报告或 release note 涉及自定义导航、fixed header、分享、返回或页面顶部布局
- **THEN** 相关材料 SHOULD 引用小程序自定义导航 best-practice
- **AND** 若 best-practice 不适用，相关材料 SHALL 记录不适用原因
- **AND** Sprint 验收报告 SHOULD 汇总矩阵摘要、通过项、blocked 和 follow_up，不复制完整 evidence。

