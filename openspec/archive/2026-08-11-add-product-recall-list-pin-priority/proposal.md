---
change_id: add-product-recall-list-pin-priority
source_requirement: REQ-0103-product-recall-list-pin-priority
related_sprint: sprint-022
status: applied
created_at: 2026-08-07 23:12:00
updated_at: 2026-08-07 23:45:00
---

# 商品召回列表排序置顶

## 背景

小程序普通商品列表和搜索 SKU 结果缺少统一的召回优先排序层。运营配置了少量重点 SKU 后，当前公开列表仍可能按发布时间、相关性或既有默认排序把这些商品排在后部，影响搜索 / 推荐召回商品的首屏曝光。

本 Change 将召回置顶配置纳入 SKU 主数据维护，并在后端公开查询排序层统一生效，确保小程序只按接口返回顺序展示。

## 变更内容

- 管理端 SKU 新增召回置顶运营配置：召回排序值、生效开始时间、生效结束时间。
- 召回排序值只允许正整数，默认值为 `9999`；低于默认值且处于有效期内时才参与置顶，数值越低排序越前。
- 小程序品牌、分类、普通关键词商品列表和搜索 SKU 结果在分页前应用召回置顶排序，默认同一请求少于 5 个生效置顶商品。
- 召回置顶商品必须先满足公开条件和当前请求筛选条件，不允许越过关键词、品牌、类目、规格、价格等条件强插。
- 新品榜 `section=new`、热销榜 `section=hot` 以及价格排序分支不应用召回置顶，保留原排序语义。
- 小程序商品卡片、列表和搜索结果不展示“置顶”“推荐”“召回”等 UI 标识。
- 同步 SQLite / MySQL schema、migration、数据库文档、Pydantic Schema、OpenAPI、Orval 和自动化测试。

## 能力范围

### 新增能力

- 无。本 Change 在既有 SKU 管理、小程序商品列表、小程序搜索和数据库能力上追加行为约束。

### 修改能力

- `tile-sku-management`：新增 SKU 召回置顶配置字段、校验、保存回显和管理端弹窗验收要求。
- `miniapp-product-list-page`：新增普通商品列表召回置顶排序、榜单 / 价格排序例外、分页前排序和无 UI 标识约束。
- `miniapp-search`：新增搜索 SKU 结果召回置顶排序，明确不影响实时联想和搜索页可见结构。
- `database`：新增 SQLite / MySQL 对 SKU 召回置顶字段、默认值、索引和迁移一致性的要求。

## 影响范围

| 范围 | 影响 |
|---|---|
| 后端 API | 影响 `/api/v1/miniapp/products` 品牌、分类、普通关键词入口与 `/api/v1/miniapp/search` 商品结果排序；管理端 SKU create/update/detail/list schema 需按字段实际暴露同步。 |
| 数据库 | `tiles` 表新增召回排序值与有效期字段，需同步 SQLite schema、SQLite migration、MySQL baseline / migration 和数据库文档。 |
| 管理端 Web | SKU 新建 / 编辑弹窗增加运营配置字段，复用现有表单和 Design System 控件；不改变管理端 SKU 列表排序。 |
| 微信小程序 | 只消费接口排序结果，不新增 UI 标识、不做本地跨页重排。 |
| OpenAPI / Orval | 管理端 SKU 请求 / 响应字段变化后必须重新生成并复核。 |
| 测试 | 覆盖字段校验、有效期、上限、筛选、榜单例外、分页前排序和小程序无 UI 标识。 |

## 不包含

- 不新增独立算法服务、个性化推荐引擎或召回策略后台。
- 不改变新品榜、热销榜、价格升降序、收藏列表、店主 Web 商品列表和管理端 SKU 列表排序。
- 不在小程序公开 UI 展示召回状态或排序解释字段。
