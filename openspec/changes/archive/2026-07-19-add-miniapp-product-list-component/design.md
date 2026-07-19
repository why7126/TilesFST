## Context

`REQ-0047` 已评审并纳入 `sprint-008`。现有小程序能力已经覆盖首页、分类列表页、SKU 详情页和搜索组件，但商品列表作为分类、搜索、品牌、推荐等入口的公共承接页尚未成为独立 OpenSpec capability。

现有边界：

- `miniapp-category-list-page` 已规定二级分类跳转 `pages/product-list/index?categoryId={secondaryCategoryId}&categoryName={encodedName}`，且分类页不展示商品卡片、价格、筛选或排序。
- `miniapp-sku-detail-page` 已规定 SKU 详情页可从分类列表、搜索结果、品牌页等入口进入，并要求公开字段过滤与安全媒体 URL。
- `miniapp-home` 已有推荐商品、全部产品瀑布流和入口承接要求。
- `add-miniapp-search-component` 进行中，搜索结果 SKU 列表需要可复用的商品列表容器和商品卡片。

## Goals / Non-Goals

**Goals:**

- 新增小程序商品列表页 capability，作为分类、搜索、品牌、推荐入口的统一承接页。
- 统一商品列表容器、商品卡片、筛选排序、分页加载、空/错/无更多状态和埋点。
- 明确公开商品列表接口契约边界：公开字段过滤、安全媒体 URL、分页、排序、筛选 facets 和敏感信息过滤。
- 与分类页、搜索组件、SKU 详情页保持职责清晰，避免重复实现分页状态机和商品卡片。

**Non-Goals:**

- 不新增 Web 管理端商品列表通用组件。
- 不新增店主 Web 商品列表。
- 不改造后台商品管理列表、批量操作、上下架、库存或价格编辑。
- 不新增商品数据模型、后台录入能力、购物车、询价、在线下单、客服找砖或收藏能力。
- 不实现 3D、AR、瀑布流增强、复杂推荐算法或后台运营插槽配置。

## Decisions

### D1. 新建 `miniapp-product-list-page` capability

商品列表页是多个小程序入口的公共承接能力，且现有 specs 没有独立商品列表页契约。因此本 Change 使用 `add` 类型新增 `miniapp-product-list-page`，并以 delta spec 轻量补充分类、SKU 详情和 usage event 的连接点。

备选方案是把商品列表写入 `miniapp-category-list-page` 或 `miniapp-search`，但会让分类页和搜索页同时承担列表容器、分页和商品卡片规则，后续复用成本更高。

### D2. 列表容器负责状态机，入口页面只传上下文

商品列表页统一处理 `categoryId`、`keyword`、`brandId`、`source`、筛选、排序、分页和刷新。分类页、搜索页、品牌页或首页推荐只负责传入上下文，不重复维护分页游标、加载更多和错误状态。

这可以减少分类列表、搜索结果、品牌商品列表之间的行为差异，也让后续验收能集中验证列表状态机。

### D3. 商品卡片只承担浏览和详情跳转

商品卡片展示公开选砖信息，并整卡进入 SKU 详情页。v1 不放收藏、询价、购物车、在线下单或联系商家快捷按钮，避免把商品列表做成交易型页面。

### D4. API 优先复用现有公开 SKU 查询能力

实现阶段先梳理现有 SKU/首页/搜索接口。如果现有接口已能提供公开字段、分页、排序、筛选条件和安全媒体 URL，应复用或薄封装；若无法满足商品列表契约，再新增小程序公开商品列表 API，并同步 OpenAPI、Orval、docs 和测试。

### D5. 原型冲突处理

本 REQ 只有 `prototype/miniapp/`，没有 `prototype/web/`，因此不触发 Web UI Explore Gate。

验收优先级：

```text
prototype/miniapp/prototype.html
> prototype/miniapp/context.md
> prototype/miniapp/interaction.md
> acceptance.md
> rules/ui-design.md
> openspec/specs
```

当前未发现冲突：

- 原型强调商品卡片、筛选排序和加载状态。
- acceptance 强调同一能力的可测试 AC。
- 既有分类页 spec 明确分类页不展示商品列表，商品列表页作为跳转目标承接。

## Risks / Trade-offs

- 商品列表范围外溢到后台商品管理、店主 Web 或交易能力 → design 和 spec 明确 Non-Goals，tasks 加验收项确认范围外能力未出现。
- API 合约与搜索/首页已有接口重复 → 实现阶段先梳理复用策略，只有必要时新增小程序公开商品列表 API。
- Sprint 容量已超载 → 本 Change 估算 M=3.0 人天，必须复用现有分类、搜索和 SKU 详情链路，避免扩展到复杂推荐或新后台配置。
- 图片比例和真实媒体加载导致列表跳动 → spec 要求稳定图片比例、失败占位和加载前后一致布局。
- 埋点误写敏感字段 → 复用 product-usage-logging 的敏感信息过滤边界，新增商品列表事件只保留必要业务字段。

## Migration Plan

1. 创建或确认小程序商品列表页面与组件结构。
2. 确认公开商品列表 API 复用或新增策略。
3. 接入分类二级分类、搜索 SKU 列表、首页推荐和品牌入口上下文。
4. 补齐商品列表埋点和敏感信息过滤测试。
5. 按 `prototype/miniapp/`、acceptance 和 spec 完成验收。

无数据迁移是默认路径；若新增接口字段或 usage event 字典，需同步 OpenAPI、Orval、docs、SQLite/MySQL schema 或事件字典测试。

## Open Questions

- 商品列表 v1 最终采用单列大卡还是双列卡片，apply 阶段应以 `prototype/miniapp/prototype.html` 和实际小程序视口验收决定。
- 品牌页是否已有可用入口；若品牌页尚未实现，品牌上下文可先作为接口和组件参数预留，页面入口安全降级。
