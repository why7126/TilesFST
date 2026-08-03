## MODIFIED Requirements

### Requirement: 双列品牌卡片列表

品牌列表页 SHALL 在顶部轮播或品牌氛围 Hero 下方以每行一个品牌的信息卡片展示公开可见品牌，并 SHALL 为 Logo、长品牌名、商品数量、末级类目胶囊、不可用品牌和小屏视口提供稳定降级。品牌 Logo 或品牌图片小图 SHALL 优先使用后端受控真实缩略图；缩略图缺失或加载失败时 SHALL 安全回退原图、品牌首字或统一占位。

#### Scenario: 单行品牌列表展示
- **WHEN** 品牌列表页获取到公开品牌数据
- **THEN** 页面 SHALL 以每行一个品牌的信息卡片展示品牌
- **AND** 每个品牌卡片 SHALL 分为上行品牌信息区和下行类目汇总区
- **AND** 上行品牌信息区 SHALL 展示品牌 Logo 或首字母占位、品牌名称和该品牌公开商品数量
- **AND** 上行品牌信息区 SHALL 优先使用后端受控缩略图展示品牌 Logo
- **AND** 上行品牌信息区 SHOULD 展示轻量进入指示
- **AND** 下行类目汇总区 SHALL 展示该品牌所有上架/公开商品对应类目的最后一层级类目名称集合
- **AND** 下行类目 SHOULD 使用胶囊标签展示并自动换行
- **AND** 类目胶囊字号 SHOULD 比品牌名称字号小 2rpx
- **AND** 品牌列表页 SHALL NOT 继续以一行 2 个品牌卡片作为本需求目标形态。

#### Scenario: 品牌小图安全读取
- **WHEN** 品牌列表页展示品牌 Logo 或品牌图片
- **THEN** 图片 URL SHALL 是公开安全 URL 或后端授权 URL
- **AND** 小图场景 SHALL 优先使用缩略图 URL
- **AND** 品牌列表接口 SHOULD NOT 为每个列表 item 下发未被列表卡片渲染使用的原图 Logo URL
- **AND** 小程序页面 SHOULD NOT 在页面 data 中长期保存与接口缩略图 URL 等值的重复派生 URL 字段
- **AND** 缩略图缺失、为空或加载失败时 SHALL 安全回退原图、品牌首字或统一占位
- **AND** 大图预览或后续品牌详情查看 SHALL 使用原图或等价安全引用
- **AND** 响应 SHALL NOT 暴露 MinIO 原始 object key、内部路径、Authorization header 或 Cookie。
