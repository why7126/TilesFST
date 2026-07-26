## MODIFIED Requirements

### Requirement: 小程序搜索入口组件
系统 SHALL 提供微信小程序搜索入口组件，用于首页、分类页、SKU 列表页、品牌相关页面和独立搜索页复用。

#### Scenario: 独立搜索页复用搜索入口组件
- **WHEN** 用户进入独立搜索页
- **THEN** 页面 SHALL 复用 `components/search-entry` 或实现与该组件一致的关键词、清空、提交、取消或返回、禁用态、`scope` 和 `sourcePage` 行为
- **AND** 顶部结构 SHALL 呈现返回按钮、搜索框、取消或搜索按钮
- **AND** 顶部结构 SHALL 位于顶部安全区下方并满足不小于 44px 或小程序等效触控尺寸。

### Requirement: 小程序完整搜索结果
系统 SHALL 提供微信小程序完整搜索结果页，用于展示综合、品牌、SKU 和证书结果。

#### Scenario: 综合结果按 sections 分区渲染
- **WHEN** 搜索结果响应包含 `sections` 或等价分区数据
- **THEN** 综合页 SHALL 展示最多 1 条最佳匹配
- **AND** 最佳匹配 SHALL 按 SKU 编码或名称直接命中、品牌名精确命中、证书名称或证书编号精确命中的顺序判定
- **AND** 综合页 SHALL 按品牌、SKU、证书顺序展示非 0 条分区
- **AND** 品牌、SKU 和证书单独 Tab SHALL 直接展示卡片内容，不展示分区标题和数量
- **AND** SKU 结果 SHALL 复用公开 SKU 卡片
- **AND** 品牌和证书结果 SHALL 使用与 SKU 卡片一致的一行卡片式视觉，但保留各自目标跳转行为
- **AND** 页面 SHALL NOT 展示类目 Tab 或仅以扁平 SKU 列表替代综合结果分区。

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
系统 SHALL 提供搜索无结果、加载和失败状态，帮助用户调整关键词并继续搜索。

#### Scenario: 无结果状态按原型呈现
- **WHEN** 用户提交关键词且无任何搜索结果
- **THEN** 无结果页 SHALL 展示当前关键词、搜索图标、调整建议列表和推荐搜索词
- **AND** 调整建议 SHALL 包含检查编码、缩短关键词或替换品牌、规格、名称等方向
- **AND** 页面 SHALL NOT 展示联系商家、提交找砖需求、购物车、询价、在线下单或客服找砖入口。

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
