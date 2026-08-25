## MODIFIED Requirements

### Requirement: 品牌 Logo 与异常状态

品牌卡片组件 SHALL 使用稳定尺寸 Logo 容器，并在 Logo 缺失、加载失败、品牌名称缺失或入口不可用时提供统一可理解的降级状态。品牌卡片组件用于小图展示时 SHALL 优先使用后端受控缩略图或等价轻量 Logo URL；详情、预览或后续高清展示 SHALL 使用原图或等价安全引用。来自 SKU 详情页的品牌卡普通展示 SHALL NOT 在存在可用缩略图时请求 Logo 原图。

#### Scenario: Logo 容器稳定

- **WHEN** 品牌 Logo 正在加载、加载完成或加载失败
- **THEN** Logo 区域 SHALL 保持稳定尺寸
- **AND** 卡片高度 SHALL NOT 因图片加载状态变化发生明显跳动
- **AND** Logo 可用缩略图存在时 SHALL 优先使用缩略图或等价轻量 URL。

#### Scenario: Logo 缺失或加载失败

- **WHEN** 品牌 Logo 缩略图缺失、为空、不可访问或图片加载失败
- **THEN** 品牌卡片 SHALL 按安全占位、品牌首字或默认图片的顺序降级
- **AND** 小图展示场景 SHALL NOT 直接请求大体积 Logo 原图作为性能通过 fallback
- **AND** 卡片 SHALL NOT 展示破图
- **AND** 图片异常 SHALL NOT 影响品牌名称、入口提示和卡片点击能力。

#### Scenario: SKU 详情页品牌 Logo 请求证据

- **WHEN** 品牌卡片在 SKU 详情页内渲染
- **THEN** 验收 SHALL 确认品牌卡收到 `brand_logo_thumbnail_url`
- **AND** Network evidence SHALL 显示普通展示请求命中受控缩略图 URL 或安全占位资源
- **AND** Network evidence SHALL NOT 将直接请求 Logo 原图视为轻量展示验收通过。
