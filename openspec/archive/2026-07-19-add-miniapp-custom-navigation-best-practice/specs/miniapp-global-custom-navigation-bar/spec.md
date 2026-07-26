## ADDED Requirements

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
