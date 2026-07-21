## Why

微信小程序分类页当前规格只明确二级分类进入商品列表，用户在只确定一级大类时缺少稳定的“查看全部商品”入口。REQ-0051 已纳入 sprint-009，需要把一级分类聚合入口、分类层级参数和商品列表承接语义补入 OpenSpec，避免实现阶段把一级分类错误当成二级分类查询。

## What Changes

- 分类页新增当前一级分类的商品列表入口，且不改变左侧一级分类点击只用于切换的既有语义。
- 二级分类跳转继续保留，并统一携带 `categoryId`、`categoryName`、`categoryLevel` 和 `sourcePage`。
- 商品列表页支持 `categoryLevel=primary|secondary`：一级分类聚合其启用二级分类下商品，二级分类精确查询当前分类商品。
- 商品列表页标题、筛选范围、空状态、错误状态、分页刷新和返回恢复都必须保留分类层级上下文。
- 分类入口与商品列表浏览埋点补充一级/二级分类语义，并禁止记录与浏览无关的个人敏感信息。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `miniapp-category-list-page`: 分类页增加一级分类商品列表入口，二级分类跳转参数补充分类层级与来源页面。
- `miniapp-product-list-page`: 商品列表页分类入口支持一级聚合和二级精确查询，并保持筛选、分页、空状态和异常状态上下文。
- `product-usage-logging`: 使用行为事件字典补充分类页一级/二级入口和商品列表分类浏览事件。

## Impact

- **Miniapp:** 修改分类页交互、跳转参数、防重复点击、商品列表上下文解析、标题/空状态/错误状态和返回恢复。
- **Backend/API:** 商品列表公开查询需要显式支持 `categoryLevel=primary|secondary`；若已有接口无法承接一级聚合，需要在实现中补齐并同步 OpenAPI。
- **Database:** 不新增表；一级聚合查询依赖现有一级/二级分类关系和公开 SKU 过滤。
- **Storage:** 不影响 MinIO 或媒体策略。
- **Web/Admin:** 不影响 Web 管理端和店主 Web 展示端。
- **Docs/OpenSpec/Tests:** 更新 OpenSpec delta；实现阶段需补充小程序交互测试、商品列表查询测试和埋点校验测试。
- **Orval:** 若后端 OpenAPI 新增或调整商品列表查询参数，需要重新生成 Orval；若仅小程序内部服务层消费既有兼容参数，可不生成。
