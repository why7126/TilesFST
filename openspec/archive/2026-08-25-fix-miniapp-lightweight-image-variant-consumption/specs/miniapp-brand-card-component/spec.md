## MODIFIED Requirements

### Requirement: 品牌 Logo 与异常状态

品牌卡片组件 SHALL 使用稳定尺寸 Logo 容器，并在 Logo 缺失、加载失败、品牌名称缺失或入口不可用时提供统一可理解的降级状态。品牌卡片组件用于小图展示时 SHALL 优先使用后端受控缩略图或等价轻量 Logo URL；详情、预览或后续高清展示 SHALL 使用原图或等价安全引用。品牌卡片普通展示 SHALL NOT 以 `brand_logo_url` 原图作为默认 fallback；来自 SKU 详情页、证书详情页、品牌详情页或品牌列表页的品牌卡展示均 SHALL 遵守同一约束。

#### Scenario: Logo 缺失或加载失败

- **WHEN** 品牌 Logo 缩略图缺失、为空、不可访问或图片加载失败
- **THEN** 品牌卡片 SHALL 按安全占位、品牌首字或默认图片的顺序降级
- **AND** 小图展示场景 SHALL NOT 直接请求大体积 Logo 原图作为性能通过 fallback
- **AND** 卡片 SHALL NOT 展示破图
- **AND** 图片异常 SHALL NOT 影响品牌名称、入口提示和卡片点击能力。

#### Scenario: 品牌卡默认禁止原图 Logo fallback

- **WHEN** 页面未显式声明高清预览、下载或原图查看入口
- **THEN** 品牌卡片组件默认 SHALL 禁止使用 `brand_logo_url` 作为普通展示图片源
- **AND** 组件收到 `brand_logo_thumbnail_url` 为空时 SHALL 展示安全占位、品牌首字或默认图
- **AND** 静态测试 SHALL 覆盖默认配置不会产生 `brand_logo_thumbnail_url || brand_logo_url` 等原图 fallback 表达式。
