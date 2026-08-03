## MODIFIED Requirements

### Requirement: 双列品牌卡片列表

品牌列表页 SHALL 在顶部轮播或品牌氛围 Hero 下方以每行一个品牌的信息卡片展示公开可见品牌，并 SHALL 为 Logo、长品牌名、商品数量、末级类目胶囊、不可用品牌和小屏视口提供稳定降级。品牌 Logo 或品牌图片小图 SHOULD 优先使用后端受控真实缩略图；缩略图缺失或加载失败时 SHALL 安全回退原图、品牌首字或统一占位。

#### Scenario: 单行品牌列表展示

- **WHEN** 品牌列表页获取到公开品牌数据
- **THEN** 页面 SHALL 以每行一个品牌的信息卡片展示品牌
- **AND** 每个品牌卡片 SHALL 分为上行品牌信息区和下行类目汇总区
- **AND** 上行品牌信息区 SHALL 展示品牌 Logo 或首字母占位、品牌名称和该品牌公开商品数量
- **AND** 上行品牌信息区 SHOULD 优先使用后端受控缩略图展示品牌 Logo
- **AND** 上行品牌信息区 SHOULD 展示轻量进入指示
- **AND** 下行类目汇总区 SHALL 展示该品牌所有上架/公开商品对应类目的最后一层级类目名称集合
- **AND** 下行类目 SHOULD 使用胶囊标签展示并自动换行
- **AND** 类目胶囊字号 SHOULD 比品牌名称字号小 2rpx
- **AND** 品牌列表页 SHALL NOT 继续以一行 2 个品牌卡片作为本需求目标形态。

#### Scenario: 品牌公开过滤

- **WHEN** 小程序请求品牌列表数据
- **THEN** 系统 SHALL 仅返回或仅展示启用且公开可见的品牌
- **AND** 系统 SHALL NOT 展示未公开品牌、已停用品牌、内部备注或管理端专用字段。

#### Scenario: 品牌 Logo、长文案和类目多行展示

- **WHEN** 品牌 Logo 缩略图缺失、原图缺失、图片加载失败、品牌名称较长、类目名称较长或类目数量较多
- **THEN** 品牌卡片 SHALL 展示品牌名称首字、品牌占位或统一占位图
- **AND** 品牌名称 SHALL 按设计策略截断或换行
- **AND** 类目汇总 SHALL 全部折行展示，不使用“等 N 类”折叠或隐藏后续类目
- **AND** 品牌卡片 SHALL NOT 出现破图、文字重叠、横向滚动、布局跳动或类目标签覆盖品牌信息。

#### Scenario: 品牌小图安全读取
- **WHEN** 品牌列表页展示品牌 Logo 或品牌图片
- **THEN** 图片 URL SHALL 是公开安全 URL 或后端授权 URL
- **AND** 小图场景 SHOULD 使用缩略图 URL
- **AND** 大图预览或后续品牌详情查看 SHALL 使用原图或等价安全引用
- **AND** 响应 SHALL NOT 暴露 MinIO 原始 object key、内部路径、Authorization header 或 Cookie。
