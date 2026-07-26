## ADDED Requirements

### Requirement: 小程序搜索入口组件
系统 SHALL 提供微信小程序搜索入口组件，用于首页、分类页、SKU 列表页、品牌相关页面和独立搜索页复用。

#### Scenario: 搜索入口支持基础交互
- **WHEN** 用户在小程序页面使用搜索入口组件
- **THEN** 组件 SHALL 支持关键词输入、清空、提交、取消或返回和禁用态
- **AND** 组件 SHALL 支持外部传入初始关键词、占位文案、搜索范围和来源页面
- **AND** 组件 SHALL 支持键盘搜索和搜索按钮触发。

#### Scenario: 搜索入口满足触控规范
- **WHEN** 团队验收搜索入口组件
- **THEN** 搜索框、返回按钮和清空按钮可点击区域 SHALL 不小于 44px 或小程序等效尺寸
- **AND** 搜索框 SHALL 固定在顶部安全区下方或页面设计指定位置
- **AND** 组件 SHALL 避免与小程序原生导航栏、TabBar 或安全区重叠。

#### Scenario: 分类上下文进入搜索
- **WHEN** 用户从分类页或 SKU 列表页进入搜索
- **THEN** 搜索入口 SHALL 传递当前页面的搜索范围和来源页面
- **AND** 分类页进入搜索时 SHOULD 保留当前类目上下文
- **AND** 返回或取消 SHALL 回到原页面且不重置原页面浏览状态。

### Requirement: 小程序搜索首页
系统 SHALL 提供微信小程序搜索首页，用于展示最近搜索、热门搜索和最近浏览。

#### Scenario: 搜索首页展示历史与热门内容
- **WHEN** 用户进入独立搜索页且尚未提交新关键词
- **THEN** 页面 SHALL 展示最近搜索、热门搜索和最近浏览
- **AND** 最近搜索 SHALL 本机保存最多 20 条，重复关键词去重后置顶
- **AND** 最近浏览 SHALL 最多展示 10 条并按最近访问倒序排列。

#### Scenario: 最近搜索可维护
- **WHEN** 用户管理最近搜索
- **THEN** 小程序 SHALL 支持单条删除和全部清空
- **AND** 删除或清空后 SHALL 立即刷新搜索首页对应区域
- **AND** 最近搜索 SHALL NOT 上传为管理端配置事实。

#### Scenario: 热门词仅小程序展示
- **WHEN** 小程序展示热门搜索词
- **THEN** 热门词 SHALL 仅作为小程序端搜索入口展示内容
- **AND** 本 Change SHALL NOT 新增后台热门词维护、同义词维护、自然语言词典维护或搜索统计管理页。

### Requirement: 小程序实时联想
系统 SHALL 在用户输入关键词时提供实时联想，并控制请求频率和过期响应。

#### Scenario: 输入阈值触发联想
- **WHEN** 用户输入中文 1 字或英文/数字 2 字及以上
- **THEN** 小程序 SHALL 触发实时联想
- **AND** 联想请求 SHALL 使用 300ms 防抖
- **AND** 未达到阈值时 SHALL 保持输入态且不得请求远程联想。

#### Scenario: 旧请求不得覆盖新结果
- **WHEN** 用户连续输入导致多个联想请求并发或乱序返回
- **THEN** 小程序 SHALL 使用 requestId、序列号或等价机制忽略旧关键词响应
- **AND** 页面 SHALL 只展示当前关键词对应的联想结果。

#### Scenario: 联想结果构成
- **WHEN** 联想结果返回
- **THEN** 页面 SHALL 展示 6 到 10 条建议
- **AND** 建议 MAY 包含最近搜索、SKU、品牌、类目、规格和普通关键词建议
- **AND** 证书 SHALL NOT 出现在实时联想中。

#### Scenario: 联想点击跳转
- **WHEN** 用户点击可直达实体建议
- **THEN** 小程序 SHALL 进入对应详情页、品牌页、类目页或列表页
- **AND** 当目标页面不存在或不可达时 SHALL 安全降级到搜索结果页
- **AND** 用户点击不可直达关键词建议 SHALL 进入搜索结果页。

### Requirement: 小程序完整搜索结果
系统 SHALL 提供微信小程序完整搜索结果页，用于展示综合、SKU、品牌、类目和证书结果。

#### Scenario: 搜索结果类型切换
- **WHEN** 用户提交搜索关键词
- **THEN** 搜索结果页 SHALL 展示综合、SKU、品牌、类目和证书类型 Tab
- **AND** 综合 Tab SHALL 默认激活
- **AND** 类型 Tab SHALL 支持横向滚动并展示可用数量或等价反馈。

#### Scenario: 综合结果分区
- **WHEN** 搜索结果存在多个类型
- **THEN** 综合页 SHALL 展示最多 1 条最佳匹配
- **AND** 综合页 SHALL 按 SKU、品牌、类目、证书或等价结构分区展示结果
- **AND** 空分区 SHALL 隐藏或展示明确空状态。

#### Scenario: SKU 搜索卡片
- **WHEN** 搜索结果包含 SKU
- **THEN** SKU 卡片 SHALL 展示主图、产品名称、SKU 编码、品牌、规格和参考价格
- **AND** SKU 卡片整卡点击 SHALL 进入 SKU 详情页
- **AND** SKU 卡片 SHALL NOT 放置收藏、分享、购物车或询价快捷操作。

#### Scenario: 结果公开状态过滤
- **WHEN** 搜索、联想或结果聚合返回实体
- **THEN** 系统 SHALL 排除下架 SKU、停用品牌、停用类目、停用规格和不可公开证书
- **AND** 响应 SHALL NOT 暴露后台内部字段、内部备注、raw object key、未授权素材或敏感配置。

### Requirement: 小程序搜索筛选与排序
系统 SHALL 提供小程序搜索筛选和排序能力，用于缩小搜索结果范围。

#### Scenario: 快捷筛选和完整筛选
- **WHEN** 用户查看搜索结果页
- **THEN** 页面 SHALL 支持品牌、类目、规格快捷筛选
- **AND** 完整筛选 SHALL 使用底部抽屉展示品牌、类目、规格和价格区间
- **AND** 筛选抽屉 SHALL 支持重置和确认。

#### Scenario: 筛选聚合与确认反馈
- **WHEN** 用户调整筛选条件
- **THEN** 筛选选项和数量 SHALL 基于当前搜索结果动态聚合
- **AND** 确认按钮 SHALL 展示应用筛选后的结果数量
- **AND** 用户重置筛选 SHALL 保留当前关键词并清空筛选条件。

#### Scenario: 搜索排序优先级
- **WHEN** 系统排序搜索结果
- **THEN** 结果 SHALL 按完整 SKU 精确匹配、SKU 前缀匹配、产品名称精确匹配、品牌精确匹配、品牌拼音或首字母匹配、标签组合匹配、普通模糊匹配的优先级排序
- **AND** 同等级结果 SHALL 按有图优先、热度优先、最近更新优先排序
- **AND** v1 SHALL NOT 支持人工置顶或个性化浏览权重。

### Requirement: 小程序搜索无结果与异常状态
系统 SHALL 提供搜索无结果、加载和失败状态，帮助用户调整关键词并继续搜索。

#### Scenario: 无结果状态
- **WHEN** 用户提交关键词且无任何搜索结果
- **THEN** 无结果页 SHALL 展示当前关键词
- **AND** 页面 SHALL 提示用户检查编码、缩短关键词或替换品牌、规格、名称
- **AND** 页面 SHALL 展示推荐搜索词。

#### Scenario: 搜索范围外能力不展示
- **WHEN** 用户处于搜索无结果或搜索结果页
- **THEN** 页面 SHALL NOT 展示联系商家、提交找砖需求、购物车、询价、在线下单或客服找砖入口
- **AND** 页面 SHALL NOT 引导进入管理端配置流程。

#### Scenario: 状态切换稳定
- **WHEN** 搜索空状态、加载态、联想态、结果态或失败态切换
- **THEN** 页面 SHALL 避免明显布局跳动、内容重叠或底部操作遮挡
- **AND** 用户 SHALL 能继续修改关键词、重试或返回。

### Requirement: 小程序搜索原型验收
小程序搜索实现 SHALL 参考 `issues/requirements/archive/REQ-0046-search-component-application/prototype/` 下的 HTML、PNG 和 context。

#### Scenario: 原型优先级
- **WHEN** 原型、验收标准、UI 规则和既有 spec 存在冲突
- **THEN** 验收优先级 SHALL 为 HTML、PNG、context、acceptance、UI 设计规则、既有 spec
- **AND** 390px 画布、44px 搜索框、顶部安全区、横向 Tab、72% 筛选抽屉和 62% 遮罩 SHALL 作为本期视觉验收基准。

#### Scenario: 小程序深色品牌视觉
- **WHEN** 团队验收搜索首页、联想页、结果页、筛选页和无结果页
- **THEN** 页面 SHALL 与菲尚特小程序首页深色企业轻奢风保持一致
- **AND** 筛选选中态 SHALL 使用品牌金边框与浅金背景
- **AND** 主要点击区域 SHALL 满足小程序触控尺寸。
