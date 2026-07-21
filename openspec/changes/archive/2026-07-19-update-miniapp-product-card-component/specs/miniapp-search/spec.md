## MODIFIED Requirements

### Requirement: 小程序完整搜索结果
小程序搜索页 SHALL 以分区结构展示 SKU、品牌、类目、证书等搜索结果，并保证公开状态、结果为空和结果点击行为一致。

#### Scenario: 搜索结果类型
- **WHEN** 用户输入关键词并触发搜索
- **THEN** 搜索页 SHALL 展示 SKU、品牌、类目、证书或等价类型结果
- **AND** 类型 Tab SHALL 支持横向滚动并展示可用数量或等价反馈。

#### Scenario: 综合结果分区
- **WHEN** 搜索结果存在多个类型
- **THEN** 综合页 SHALL 展示最多 1 条最佳匹配
- **AND** 综合页 SHALL 按 SKU、品牌、类目、证书或等价结构分区展示结果
- **AND** 空分区 SHALL 隐藏或展示明确空状态。

#### Scenario: SKU 搜索卡片
- **WHEN** 搜索结果包含 SKU
- **THEN** SKU 卡片 SHALL 复用统一商品卡片核心结构
- **AND** SKU 卡片 SHALL 展示主图、SKU 名称、品牌、规格和参考价格
- **AND** SKU 卡片整卡点击 SHALL 进入 SKU 详情页并携带 `skuId`、`sourcePage=search`、可用 `keyword`、`listContext`、`index` 和 `requestId`
- **AND** SKU 卡片 SHALL NOT 放置收藏、分享、购物车、联系客服或询价快捷操作。

#### Scenario: 结果公开状态过滤
- **WHEN** 搜索、联想或结果聚合返回实体
- **THEN** 系统 SHALL 排除下架 SKU、停用品牌、停用类目、停用规格和不可公开证书
- **AND** 响应 SHALL NOT 暴露后台内部字段、内部备注、raw object key、未授权素材或敏感配置。
