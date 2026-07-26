## MODIFIED Requirements

### Requirement: SKU 详情页入口与公开数据

系统 SHALL 提供微信小程序 SKU 详情页，用于从首页、分类、搜索、品牌页、收藏页和微信分享卡片进入单个瓷砖 SKU 的公开详情。

#### Scenario: 多入口进入 SKU 详情

- **WHEN** 用户从首页商品卡片、分类列表、搜索结果、品牌页、收藏页或微信分享卡片点击 SKU
- **THEN** 小程序 SHALL 携带 `skuId` 进入 SKU 详情页
- **AND** 页面 SHALL 记录可用的来源参数
- **AND** 缺少或非法 `skuId` 时 SHALL 展示可恢复错误状态，而不是白屏或路由错误。

#### Scenario: 详情接口返回公开数据

- **WHEN** 小程序请求 SKU 详情数据
- **THEN** 后端 SHALL 返回 SKU 主体、媒体、品牌、收藏状态、同系列推荐和同品牌推荐所需公开字段
- **AND** 响应 SHALL NOT 暴露后台内部字段、库存管理、内部备注、未授权素材、原始 object key、Authorization header、Cookie 或敏感配置
- **AND** 响应 MAY 保留 `sku_code` 作为兼容字段，但小程序 SHALL NOT 直接渲染该字段。

#### Scenario: SKU 不存在或不可公开

- **WHEN** SKU 不存在、已下架或不允许公开展示
- **THEN** 小程序 SHALL 展示“商品暂不可查看”或等价空状态
- **AND** 页面 SHALL 提供返回首页或返回上一页入口。

### Requirement: SKU 详情信息展示

SKU 详情页 SHALL 完整展示用户选砖所需的品牌、商品名称、价格、参数、类目和备注信息。SKU 编码 SHALL 作为系统内部识别字段，不在小程序/店主端详情页标题、参数区或推荐卡中展示。

#### Scenario: 展示 SKU 核心字段

- **WHEN** SKU 详情加载成功
- **THEN** 页面 SHALL 展示品牌名称、商品名称、参考价格、计价单位、规格、表面工艺、主色系、完整类目路径和备注说明
- **AND** 品牌信息 SHALL 位于商品名称上方并提供品牌入口
- **AND** 页面 SHALL NOT 展示 SKU 编码、`sku_code` 字段名或“SKU 编码：xxx”参数行。

#### Scenario: 空字段安全展示

- **WHEN** 表面工艺、主色系、备注或可选媒体字段为空
- **THEN** 页面 SHALL 按字段规则展示 “—”、隐藏对应模块或展示安全占位
- **AND** 页面 SHALL NOT 展示 `null`、`undefined`、接口字段名或空白异常卡片
- **AND** 商品名称缺失 SHALL 作为异常数据处理，不得用 SKU 编码作为正常公开兜底。

#### Scenario: 价格展示为参考价

- **WHEN** 详情页展示价格
- **THEN** 页面 SHALL 使用“参考价格”文案和计价单位
- **AND** 价格为 0 或空值时 SHALL 展示“暂无参考价”或等价状态
- **AND** 页面 SHALL 提示实际价格以门店最终确认为准。

### Requirement: SKU 收藏与分享

SKU 详情页 SHALL 支持 SKU 粒度收藏、取消收藏和微信原生分享。公开分享文案 SHALL 使用品牌名称与商品名称，不展示 SKU 编码。

#### Scenario: 收藏和取消收藏成功

- **WHEN** 用户点击收藏或取消收藏当前 SKU 且请求成功
- **THEN** 页面 SHALL 更新按钮状态
- **AND** 页面 SHALL 展示成功 Toast
- **AND** 收藏页或等价收藏数据 SHALL 与当前 SKU 收藏事实保持一致。

#### Scenario: 收藏失败回滚

- **WHEN** 收藏或取消收藏请求失败、超时或授权失败
- **THEN** 页面 SHALL 回滚到请求前状态
- **AND** 页面 SHALL 展示可理解失败提示
- **AND** 失败 SHALL NOT 阻断用户继续浏览详情。

#### Scenario: 收藏接口幂等

- **WHEN** 客户端重复提交收藏或取消收藏请求
- **THEN** 后端 SHALL 返回与目标状态一致的结果
- **AND** 不得产生重复收藏记录或错误取消状态。

#### Scenario: 分享 SKU

- **WHEN** 用户点击 SKU 详情页分享入口
- **THEN** 小程序 SHALL 调起微信原生分享或等价分享能力
- **AND** 分享标题 SHALL 包含商品名称和品牌名称
- **AND** 分享卡片 SHALL 包含主图、商品名称、品牌和参考价格
- **AND** 分享路径 SHALL 携带 `skuId` 和来源参数
- **AND** 分享标题、摘要和卡片展示 SHALL NOT 拼接 SKU 编码。
