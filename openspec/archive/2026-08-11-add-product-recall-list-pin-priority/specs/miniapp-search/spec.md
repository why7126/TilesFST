## ADDED Requirements

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

#### Scenario: 搜索结果无置顶标识

- **WHEN** 小程序展示参与召回置顶的 SKU 搜索结果
- **THEN** SKU 卡片 MUST NOT 展示“置顶”“推荐”“召回”等新增 UI 标识
- **AND** 搜索结果页结构 MUST 保持既有综合、品牌、SKU 和证书分区语义。
