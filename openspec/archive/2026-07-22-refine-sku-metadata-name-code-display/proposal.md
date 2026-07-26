## Why

瓷砖 SKU 主数据当前同时让运营和用户感知到“SKU 名称”和“SKU 编码”，在管理端录入、小程序详情、商品列表、搜索和分享中形成重复展示。REQ-0065 已评审通过，明确 SKU 编码应保留为系统自动生成的唯一内部识别字段，而商品名称才是用户填写与公开展示字段。

## What Changes

- 管理端 SKU 创建/编辑不再要求运营手工填写 SKU 编码；后端在保存草稿和正式创建时自动生成唯一、稳定的 SKU 编码。
- 管理端 SKU 列表与确认文案以商品名称为主展示，SKU 编码仅作为内部辅助信息和检索条件。
- 小程序/店主端商品卡片、SKU 详情、推荐、收藏、搜索结果和分享标题不展示 SKU 编码。
- 搜索仍可兼容 SKU 编码命中，但命中结果不得把编码渲染给公开端用户。
- 保留 `tiles.sku_code` 唯一字段和既有历史编码；若 API contract 调整，必须同步 OpenAPI、Orval、docs 和测试。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `tile-sku-management`: 调整 SKU 数据模型、创建/更新 API、管理端列表/弹窗展示和自动编码规则。
- `miniapp-sku-detail-page`: 调整 SKU 详情公开展示、参数和分享规则，隐藏 SKU 编码。
- `miniapp-product-list-page`: 调整商品卡片和公开列表响应展示契约，公开端不展示 SKU 编码。
- `miniapp-search`: 调整搜索结果与无结果建议中对 SKU 编码的公开展示口径。

## Impact

- 后端：SKU 创建/更新服务、唯一编码生成、公开商品/详情/search 响应组装、错误处理与测试。
- API：管理端 SKU 创建请求可能移除前端传入 `sku_code`；公开端响应可保留兼容字段但前端不得渲染。
- 数据库：默认保留 `tiles.sku_code UNIQUE NOT NULL`；可能需要历史缺失编码补齐或迁移兼容检查。
- Web 管理端：SKU 表单、列表、搜索 placeholder、确认文案、测试与 Orval 调用。
- 微信小程序/店主端：商品卡片、详情参数、推荐、收藏、搜索结果、分享标题和静态测试。
- 存储：不涉及对象存储策略变化。
