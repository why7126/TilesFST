## Context

REQ-0051-category-list-product-list-entry-by-level 是 REQ-0045 分类列表页的 refinement，并已纳入 `sprint-009`。现有正式规格中，分类页左侧一级分类点击负责切换，右侧二级分类卡片进入商品列表；商品列表页只表达“分类入口”但未区分一级分类聚合和二级分类精确查询。

原型来源为 `issues/requirements/archive/REQ-0051-category-list-product-list-entry-by-level/prototype/miniapp/prototype.html` 与 `prototype/miniapp/context.md`。本 Change 不修改 `src/`，只为后续 `/opsx-apply` 明确实现合同。

## Goals / Non-Goals

**Goals:**

- 分类页在右侧当前一级分类标题区或等价区域提供“查看全部商品”入口。
- 左侧一级分类点击继续只切换当前一级分类，避免把切换和进入列表合并成一个易误触手势。
- 商品列表页通过 `categoryLevel` 明确一级聚合与二级精确查询语义。
- 查询、筛选、排序、分页、刷新、空状态、错误状态和埋点都保留分类上下文。
- 埋点覆盖一级入口、二级入口和商品列表浏览，同时不采集与浏览无关的个人敏感信息。

**Non-Goals:**

- 不新增三级及以上分类模型。
- 不在分类页直接渲染商品卡片、价格、筛选、排序或分页。
- 不改 Web 管理端、店主 Web 展示端、后台分类管理或商品管理。
- 不新增购物车、询价、收藏、下单、客服找砖或推荐排序能力。
- 不变更 MinIO、媒体上传或对象存储策略。

## Decisions

- **D1. UI strategy: Miniapp DS continuation.** 使用现有小程序“工业石材 · 暗色旗舰风”和分类页左右双栏布局；新增入口放在右侧一级分类标题区或等价区域，使用品牌金/激活语义但不大面积铺色。没有 `prototype/web/`，因此不触发 Web CSS Port / Tailwind DS explore gate；小程序原型优先级为 HTML > context > acceptance > ui-design.md > specs。
- **D2. Navigation parameters.** 分类页跳转统一携带 `categoryId`、URL 编码后的 `categoryName`、`categoryLevel=primary|secondary`、`sourcePage=category`。二级分类兼容既有 `categoryId/categoryName`，但实现必须补充层级和来源，不依赖“是否有 children”推断层级。
- **D3. Primary aggregate query.** `categoryLevel=primary` 表示查询该一级分类下所有启用二级分类的公开 SKU 聚合结果；不得只查询直接挂载在一级分类上的 SKU。若后端公开商品列表接口暂不支持该参数，apply 阶段必须补齐接口/服务层并同步 OpenAPI、Orval、API 文档和测试。
- **D4. Secondary exact query.** `categoryLevel=secondary` 表示仅查询当前二级分类下公开 SKU，继续复用商品列表容器、筛选、排序、分页、刷新和详情跳转。
- **D5. State preservation.** 从商品列表或 SKU 详情返回分类页时，分类页恢复当前一级分类、左侧滚动位置、右侧滚动位置和有效缓存；商品列表内的筛选、排序、分页、刷新和加载更多请求必须持续携带 `categoryId` 与 `categoryLevel`。
- **D6. Tracking boundary.** 分类页入口点击可以使用独立事件或在既有事件中添加 `action=product_list_entry`。商品列表浏览事件必须包含分类层级上下文、结果数量和 `requestId`，但不得包含手机号、Authorization、Cookie、raw payload 或无关个人敏感信息。

## Conflict Resolution

- **Prototype vs existing category spec:** 现有 spec 说左侧一级点击切换、二级卡片跳转；REQ-0051 原型新增右侧标题区一级入口。处理：保留左侧切换语义，修改“分类跳转与埋点”和“分类商品列表承接”，新增一级入口场景。
- **Acceptance vs existing product-list spec:** 现有商品列表只要求 `categoryId`，未区分层级。处理：修改“微信小程序商品列表页入口”“商品列表公开数据接口”“商品列表空状态与异常状态”，新增 `categoryLevel` 查询语义。
- **Usage logging spec vs acceptance:** 现有 usage event 字典未显式登记分类入口事件。处理：修改产品使用行为事件采集要求，补入分类页和商品列表分类上下文事件，并沿用安全脱敏规则。

## Risks / Trade-offs

- 一级分类聚合可能扩大查询范围并影响分页性能 -> 后端查询应先展开启用二级分类 ID 集合，再复用公开 SKU 过滤和分页索引，避免内存聚合全量商品。
- 小程序入口增加可能挤压标题区空间 -> 实现需在 320 到 430px 宽度验收，入口点击热区不小于 44px，长分类名单行省略或合理换行。
- 埋点事件字典若未同步会被服务端拒绝 -> apply 阶段需要同步事件字典和测试，埋点失败仍不得阻断主流程。
- 若接口参数变更需要 Orval，但小程序不使用 Orval -> 后端 OpenAPI 仍必须准确；Web Orval 只在相关生成客户端受影响时执行。

## Migration Plan

- 无数据库迁移。
- 后端接口若新增 `categoryLevel`，保持缺省行为兼容既有二级分类入口；推荐缺省按 `secondary` 或既有语义处理，并在文档中明确。
- 发布后可通过 usage events 区分一级聚合入口与二级精确入口转化。
