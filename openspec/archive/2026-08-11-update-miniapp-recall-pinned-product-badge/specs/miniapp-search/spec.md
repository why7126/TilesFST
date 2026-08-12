## MODIFIED Requirements

### Requirement: 小程序完整搜索结果

系统 SHALL 提供微信小程序完整搜索结果页，用于展示综合、品牌、SKU 和证书结果。搜索后端 MAY 继续使用 SKU 编码作为匹配信号，但小程序搜索结果 UI SHALL 以商品名称作为 SKU 结果主展示，且不得展示 SKU 编码。SKU 搜索结果复用公开 SKU 卡片时，SHALL 支持展示当前搜索结果中实际生效的召回置顶标识。

#### Scenario: 综合结果按 sections 分区渲染

- **WHEN** 搜索结果响应包含 `sections` 或等价分区数据
- **THEN** 综合页 SHALL 展示最多 1 条最佳匹配
- **AND** 最佳匹配 MAY 按 SKU 编码或商品名称直接命中、品牌名精确命中、证书名称或证书编号精确命中的顺序判定
- **AND** 综合页 SHALL 按品牌、SKU、证书顺序展示非 0 条分区
- **AND** 品牌、SKU 和证书单独 Tab SHALL 直接展示卡片内容，不展示分区标题和数量
- **AND** SKU 结果 SHALL 复用公开 SKU 卡片
- **AND** SKU 结果 SHALL 展示商品名称而不是 SKU 编码
- **AND** 品牌和证书结果 SHALL 使用与 SKU 卡片一致的一行卡片式视觉，但保留各自目标跳转行为
- **AND** 页面 SHALL NOT 展示类目 Tab 或仅以扁平 SKU 列表替代综合结果分区。

#### Scenario: 搜索 SKU 结果展示置顶标识
- **WHEN** 搜索 SKU 结果中的商品被后端标记为当前搜索结果中实际生效的召回置顶商品
- **THEN** 搜索 SKU 商品卡片 SHALL 展示固定文案“置顶”
- **AND** 搜索页 SHALL 复用商品卡片的置顶标识展示规则
- **AND** 搜索页 SHALL NOT 根据排序位置自行推断置顶状态。

#### Scenario: 搜索实时联想不展示置顶标识
- **WHEN** 用户查看搜索实时联想、搜索建议或 suggestion 结果
- **THEN** 小程序 SHALL NOT 展示“置顶”标识
- **AND** 本 Change SHALL NOT 改变搜索实时联想排序或跳转规则。
