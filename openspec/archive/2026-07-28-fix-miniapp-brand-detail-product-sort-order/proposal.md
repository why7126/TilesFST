## Why

BUG-0087 指出微信小程序品牌详情页商品 Tab 的展示顺序未按发布时间升序、ID 升序稳定返回。当前品牌详情页商品 Tab 请求 `/api/v1/miniapp/products?brandId=...`，后端复用公开商品列表通用默认排序 `updated_at DESC, id DESC`，导致品牌主页内商品陈列顺序与验收预期不一致，并存在分页顺序漂移风险。

## What Changes

- 将品牌详情页商品 Tab 的排序契约固化为发布时间升序、ID 升序。
- 将 `/api/v1/miniapp/products?brandId=<brandId>` 品牌过滤场景的默认排序固化为发布时间升序、ID 升序。
- 明确“发布时间”使用现有 SKU 发布时间事实字段 `tiles.published_at`；历史空值使用 `tiles.created_at` 兜底以保证排序稳定，不新增数据库字段。
- 补充后端回归测试，覆盖同一品牌多 SKU 的品牌过滤排序与分页稳定性。
- 保持搜索页相关性排序、新品榜、热销榜和普通商品列表排序不变。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `miniapp-brand-detail-home-page`: 品牌主页商品 Tab 必须按发布时间升序、ID 升序展示当前品牌公开 SKU。
- `miniapp-product-list-page`: 商品列表公开数据接口在 `brandId` 过滤场景下必须按发布时间升序、ID 升序返回公开 SKU。

## Rollback Plan

如修复导致品牌详情页商品 Tab 展示异常或分页异常：

1. 回滚后端品牌过滤排序逻辑到当前通用默认排序。
2. 保留新增测试中的问题数据作为回归分析样本，确认是否为发布时间字段映射或分页参数问题。
3. 若发现历史 SKU 缺少 `published_at`，保留新增测试中的问题数据作为回归分析样本，确认兜底排序和分页是否稳定。

## Impact

- 影响范围：后端小程序公开商品列表查询逻辑、微信小程序品牌详情页商品 Tab 展示顺序、后端测试。
- API 路径与响应结构不变；仅调整 `brandId` 过滤场景的默认排序语义，预计不需要 OpenAPI / Orval。
- 数据库结构不变；当前 `tiles.published_at` 已存在并由 SKU 发布流程维护，本修复仅调整品牌过滤排序语义。
- 不影响搜索页相关性排序、新品榜、热销榜、普通商品列表、管理端 SKU 列表或媒体上传。
