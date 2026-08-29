# miniapp-search Specification

## Purpose
TBD - created by archiving change add-miniapp-search-component. Update Purpose after archive.
## Requirements
### Requirement: 小程序搜索入口组件
系统 SHALL 提供微信小程序搜索入口组件，用于首页、SKU 列表页、品牌列表页、证书列表页、收藏页和独立搜索页复用。组件 SHALL 支持入口模式和输入模式，并 SHALL 以统一契约输出关键词输入、提交、清空、取消或返回、禁用态、`scope`、`sourcePage` 和初始 `keyword` 行为。品牌列表页、证书列表页和收藏列表页 SHALL 复用输入模式在当前列表范围内过滤，不跳完整搜索结果页。底部 Tab「全部分类」页 SHALL NOT 复用该组件展示搜索入口。

#### Scenario: 独立搜索页复用搜索入口组件
- **WHEN** 用户进入独立搜索页
- **THEN** 页面 SHALL 复用 `components/search-entry` 或实现与该组件一致的关键词、清空、提交、取消或返回、禁用态、`scope` 和 `sourcePage` 行为
- **AND** 顶部结构 SHALL 呈现返回按钮、搜索框、取消或搜索按钮
- **AND** 顶部结构 SHALL 位于顶部安全区下方并满足不小于 44px 或小程序等效触控尺寸。

#### Scenario: 多页面入口模式
- **WHEN** 首页或商品列表页展示完整搜索入口
- **THEN** 页面 SHALL 复用 `components/search-entry` 的入口模式或等价封装
- **AND** 点击入口 SHALL 进入 `/pages/search/index`
- **AND** 跳转参数 SHALL 携带 `sourcePage`、`scope`、`keyword` 或当前上下文中的适用字段
- **AND** 入口文案 SHALL 让用户理解是全局搜索还是当前列表范围搜索。

#### Scenario: 列表内输入模式
- **WHEN** 页面选择在当前列表内直接输入关键词
- **THEN** 搜索入口 SHALL 使用输入模式或等价受控输入
- **AND** 提交、清空和取消 SHALL 保持稳定事件
- **AND** 列表内搜索 SHALL 只过滤当前列表上下文，不得被误表达为全站无结果。
- **AND** 品牌列表页 SHALL 在当前页按品牌名称、品牌简称和品牌英文名过滤，搜索态隐藏 Banner，清空后恢复完整品牌列表和 Banner。
- **AND** 证书列表页 SHALL 在当前页按证书名称、品牌名称、证书类型枚举或中文类型标签过滤，清空后恢复完整公开证书列表。
- **AND** 收藏列表页 SHALL 在当前收藏范围内过滤，清空后恢复完整收藏列表。

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

系统 SHALL 提供微信小程序完整搜索结果页，用于展示综合、品牌、SKU 和证书结果。搜索后端 MAY 继续使用 SKU 编码作为匹配信号，但小程序搜索结果 UI SHALL 以商品名称作为 SKU 结果主展示，且不得展示 SKU 编码。SKU 搜索结果复用公开 SKU 卡片时，SHALL 支持展示当前搜索结果中实际生效的召回置顶标识。完整搜索页 SHALL 作为多页面搜索入口的统一承接页，继续承接搜索首页、热门搜索、历史搜索、实时联想、结果分区、分页、加载、失败和无结果状态。

#### Scenario: 综合结果按 sections 分区渲染

- **WHEN** 搜索结果响应包含 `sections` 或等价分区数据
- **THEN** 综合页 SHALL 展示最多 1 条最佳匹配
- **AND** 最佳匹配 MAY 按 SKU 编码或商品名称直接命中、品牌名精确命中、证书名称或证书编号精确命中的顺序判定
- **AND** 综合页 SHALL 在最佳匹配后按品牌、证书、SKU 顺序展示非 0 条分区
- **AND** 顶部 Tab SHALL 保持综合、品牌、SKU、证书顺序
- **AND** 品牌、SKU 和证书单独 Tab SHALL 直接展示卡片内容，不展示分区标题和数量
- **AND** SKU 结果 SHALL 复用公开 SKU 卡片
- **AND** SKU 结果 SHALL 展示商品名称而不是 SKU 编码
- **AND** 品牌结果 SHALL 展示品牌图片或稳定占位、品牌名称和 SKU 数量，SKU 数量文案 SHALL NOT 包含“公开”
- **AND** 证书结果 SHALL 展示证书图片或稳定占位、证书名称、品牌和证书类型
- **AND** 品牌和证书结果 SHALL 使用与 SKU 卡片一致的一行卡片式视觉，但保留各自目标跳转行为
- **AND** 页面 SHALL NOT 展示类目 Tab 或仅以扁平 SKU 列表替代综合结果分区。

#### Scenario: 搜索结果自动加载更多

- **WHEN** 用户在搜索结果页向下滚动且仍有下一页
- **THEN** 页面 SHALL 自动加载下一页结果
- **AND** 自动加载 SHALL 避免在 loading 中重复请求
- **AND** 综合 Tab 后续页 SHALL 保留首屏最佳匹配、品牌和证书分区，并只向 SKU 分区追加新 SKU
- **AND** 后续页 SHALL NOT 用新响应覆盖已展示的综合分区结果
- **AND** 自动加载期间 SHALL 保留已展示结果，只在底部展示轻量加载状态
- **AND** 自动加载模式下 SHALL NOT 展示黄色“加载更多”主按钮
- **AND** 所有结果加载完毕后 SHALL 在底部展示轻量完成状态或不展示额外主按钮。

#### Scenario: 搜索翻页轻量响应

- **WHEN** 综合 Tab 或 SKU Tab 请求第 2 页及后续页
- **THEN** 后端 SHALL 返回继续展示所需的 SKU 结果、分页状态和必要计数
- **AND** 后端 SHOULD 跳过品牌、证书、facets、推荐词和最佳匹配等首屏摘要型查询
- **AND** 搜索 SKU 排序 SHALL NOT 依赖逐商品扫描行为事件 metadata 的热度计算。

#### Scenario: 多页面来源上下文
- **WHEN** 用户从首页或商品列表页进入搜索页
- **THEN** 搜索页 SHALL 解析 `sourcePage`、`scope`、`keyword` 和当前上下文参数
- **AND** 无初始关键词时 SHALL 展示搜索首页
- **AND** 有初始关键词时 MAY 直接展示搜索结果或保留可编辑关键词
- **AND** 有初始关键词时 SHALL NOT 额外请求搜索首页数据；用户清空关键词回到搜索首页时 SHALL 再加载热门词等搜索首页数据
- **AND** 搜索历史、热门搜索、联想和结果点击逻辑 SHALL NOT 因多页面入口接入而漂移。

#### Scenario: 搜索首屏轻量推荐词

- **WHEN** 完整搜索页请求第 1 页结果
- **THEN** 后端 SHALL 返回搜索结果、分页状态、分区、最佳匹配和必要推荐词字段
- **AND** `recommended_keywords` SHALL 使用轻量默认词或空数组
- **AND** 后端 SHALL NOT 为生成推荐词同步调用搜索首页或热门商品查询
- **AND** 搜索首屏 SHALL NOT 触发逐商品扫描行为事件 metadata 的 `hot_score` 计算分支。

#### Scenario: 搜索首屏按 Tab 最小查询

- **WHEN** 完整搜索页请求第 1 页结果
- **THEN** 后端 SHALL 只执行当前 Tab 展示所需的查询
- **AND** 综合 Tab SHALL 查询品牌、证书和 SKU，不查询未展示的 facets、类目 named 或规格 named
- **AND** 品牌 Tab SHALL 只查询品牌结果，不查询 SKU、证书或 facets
- **AND** 证书 Tab SHALL 只查询证书结果，不查询 SKU、品牌或 facets
- **AND** SKU Tab SHALL 只查询 SKU 结果，不查询品牌、证书或 facets
- **AND** 当前 UI 未展示 facets 时，搜索响应 SHALL 返回空 facets 结构。

#### Scenario: 品牌词搜索 SKU 快路径

- **WHEN** 完整搜索页关键词精确匹配启用品牌的名称、简称或英文名
- **THEN** 后端 SHALL 先识别该品牌命中
- **AND** SKU 结果查询和 SKU 总数查询 SHALL 使用命中品牌的 `brand_id` 过滤
- **AND** SKU 结果查询 SHALL NOT 使用 SKU 名称、SKU 编码、品牌、规格、表面、色系和类目等多字段 `OR LIKE` 主路径
- **AND** 未命中品牌快路径时 SHALL 保留通用关键词召回逻辑。

#### Scenario: 搜索接口服务端分段耗时

- **WHEN** 完整搜索页请求搜索结果
- **THEN** 后端 SHALL 返回 `Server-Timing` 响应头或等价服务端分段耗时观测信号
- **AND** 观测信号 SHALL 至少能定位品牌识别、SKU list、SKU count、SKU 卡片构建、品牌 named、证书查询和搜索构建总耗时中的已执行阶段
- **AND** 观测信号 SHALL 只包含阶段名和耗时
- **AND** 观测信号 SHALL NOT 包含关键词原文、SQL、内部对象 key、请求体或结果明细。

#### Scenario: 列表型 SKU 卡片构建避免同步媒体探测

- **WHEN** 小程序首页新品/热销、商品列表、搜索首页最近浏览/热门商品、完整搜索结果或 SKU 详情推荐构建列表型 SKU 卡片
- **THEN** 后端 SHALL 使用约定的缩略图和展示图 URL 生成列表图片字段
- **AND** 后端 SHALL NOT 为每张 SKU 卡片同步调用对象存储存在性探测
- **AND** 缺失图片 SHALL 由小程序图片 fallback 或详情页媒体加载策略兜底
- **AND** 详情主媒体、Banner、证书详情和品牌 Hero MAY 保留对象存储存在性探测。

### Requirement: 小程序搜索筛选与排序
系统 SHALL 避免在小程序搜索结果页展示筛选 UI，保持结果页聚焦浏览与跳转。

#### Scenario: 搜索结果页不展示筛选入口
- **WHEN** 用户查看搜索结果页
- **THEN** 页面 SHALL NOT 展示快捷筛选、筛选按钮或筛选抽屉
- **AND** 页面 SHALL NOT 展示价格区间筛选、重置或确认筛选操作。

#### Scenario: API 保留筛选兼容
- **WHEN** 外部调用搜索 API 传入既有筛选参数
- **THEN** 后端 MAY 继续按参数过滤结果，以保持接口兼容。

### Requirement: 小程序搜索无结果与异常状态

系统 SHALL 提供搜索无结果、加载和失败状态，帮助用户调整关键词并继续搜索。公开文案 SHALL 引导用户调整品牌、规格或商品名称，不把 SKU 编码作为普通用户可见检索概念。

#### Scenario: 无结果状态按原型呈现

- **WHEN** 用户提交关键词且无任何搜索结果
- **THEN** 无结果页 SHALL 展示当前关键词、搜索图标、调整建议列表和推荐搜索词
- **AND** 调整建议 SHALL 包含缩短关键词或替换品牌、规格、商品名称等方向
- **AND** 页面 SHALL NOT 展示检查 SKU 编码、内部编码、联系商家、提交找砖需求、购物车、询价、在线下单或客服找砖入口。

### Requirement: 小程序搜索原型验收
小程序搜索实现 SHALL 参考 `issues/requirements/archive/REQ-0046-search-component-application/prototype/` 下的 HTML、PNG 和 context。

#### Scenario: 五个原型状态必须逐项验收
- **WHEN** 团队验收小程序搜索修复
- **THEN** 团队 SHALL 逐项对照搜索首页、联想态、结果态和无结果态
- **AND** 验收记录 SHALL 覆盖搜索首页、联想态、结果态无筛选 UI 和无结果态
- **AND** 未完成原型对照和回归测试前，修复任务 SHALL NOT 标记为完成。

#### Scenario: 原型关键结构纳入测试
- **WHEN** 团队为小程序搜索修复补充测试
- **THEN** 测试 SHALL 覆盖搜索通用组件应用或等价行为、综合分区渲染、联想类型限制、最佳匹配优先级、结果页无筛选和无结果结构
- **AND** 测试 SHALL 覆盖联系商家、提交找砖需求、购物车、询价、在线下单和客服找砖入口在无结果状态不展示
- **AND** 测试 SHALL 作为 BUG-0066 回归验收证据。

### Requirement: 搜索 SKU 结果召回置顶排序

小程序完整搜索结果中的 SKU 商品结果 MUST 支持召回置顶排序。后端 MUST 在 SKU 结果匹配、公开过滤和兼容筛选之后计算召回置顶资格，并在分页或分区截断前将最多 4 个生效召回 SKU 排在 SKU 结果前部。搜索实时联想、热门搜索、最近搜索、品牌结果和证书结果 MUST NOT 因本能力改变排序或展示结构。

#### Scenario: SKU 搜索结果置顶

- **GIVEN** 用户提交关键词并命中多个可公开 SKU
- **AND** 其中部分命中 SKU 配置了生效召回置顶
- **WHEN** 小程序请求 `/api/v1/miniapp/search`
- **THEN** SKU 结果中的生效召回 SKU MUST 排在非召回 SKU 之前
- **AND** 生效召回 SKU MUST 按 `recall_pin_sort_order` 升序排列
- **AND** 非召回 SKU MUST 保持既有搜索排序或稳定兜底排序。

#### Scenario: 搜索召回不越过匹配条件

- **GIVEN** 某 SKU 配置了生效召回置顶
- **WHEN** 该 SKU 不匹配当前搜索关键词或不满足公开条件
- **THEN** 搜索 SKU 结果 MUST NOT 返回该 SKU
- **AND** MUST NOT 因置顶配置绕过搜索匹配。

#### Scenario: 搜索置顶上限

- **GIVEN** 当前搜索命中 5 个或更多生效召回 SKU
- **WHEN** 后端计算 SKU 搜索结果
- **THEN** 仅排序值最靠前的 4 个 SKU MUST 进入置顶区
- **AND** 其余 SKU MUST 按普通搜索排序参与结果。

#### Scenario: 搜索实时联想不受影响

- **WHEN** 用户输入关键词触发实时联想
- **THEN** 联想结果 MUST 保持既有类型、数量和排序策略
- **AND** MUST NOT 因 SKU 召回置顶配置展示额外联想、角标或说明。

#### Scenario: 搜索非置顶结果无置顶标识

- **WHEN** 小程序展示搜索实时联想、搜索建议或后端未标记为当前搜索结果实际生效置顶的 SKU 搜索结果
- **THEN** SKU 卡片 MUST NOT 展示“置顶”“推荐”“召回”等置顶 UI 标识
- **AND** 搜索结果页结构 MUST 保持既有综合、品牌、SKU 和证书分区语义。

### Requirement: 小程序搜索行为与请求链路观测
系统 SHALL 为小程序搜索入口、搜索提交、联想、结果展示和列表搜索路径提供稳定行为事件与请求链路观测，且 SHALL 对关键词和筛选摘要进行脱敏或截断。

#### Scenario: 搜索事件名稳定
- **WHEN** 用户点击搜索入口、输入关键词、提交搜索、查看联想、点击联想、查看结果、点击结果、遇到无结果或使用列表内搜索
- **THEN** 小程序 SHALL 使用已登记或等价预留的稳定事件名
- **AND** 事件名 SHALL NOT 由用户输入、页面文案或临时按钮标题拼接生成。

#### Scenario: 搜索事件属性脱敏
- **WHEN** 小程序上报搜索相关事件
- **THEN** 事件属性 SHALL 包含来源页面、搜索范围、关键词脱敏摘要、结果数量、选中 Tab、筛选条件摘要和请求 ID 中的可用字段
- **AND** 事件 SHALL NOT 保存 Authorization、Cookie、Token、密码、完整请求体、完整响应体、本机绝对路径、完整对象 key 或未脱敏关键词原文。

#### Scenario: 搜索请求链路透传
- **WHEN** 搜索行为触发小程序业务 API 请求
- **THEN** 请求 SHALL 通过小程序请求封装透传 `behavior_trace_id`、`behavior_event_id`、`client_request_id` 或等价字段
- **AND** 行为采集失败 SHALL NOT 阻断搜索、联想、跳转或结果点击。

