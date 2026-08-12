---
change_id: update-miniapp-recall-pinned-product-badge
status: applied
created_at: 2026-08-08 09:36:33
updated_at: 2026-08-08 10:25:00
---

# 设计：小程序召回置顶商品展示“置顶”标识

## 1. 需求来源与门禁

- 来源需求：`REQ-0104-miniapp-recall-pinned-product-badge`
- 父需求：`REQ-0103-product-recall-list-pin-priority`
- Sprint：`sprint-022`
- Readiness：Ready
- 评审状态：已 approved，并已纳入 Sprint 正式范围

## 2. 影响分析

| 范围 | 结论 |
|---|---|
| 后端 | 需要在公开商品卡片构造时暴露置顶展示状态。 |
| API | 需要同步 `MiniappProductCard` 响应字段、OpenAPI 和 Orval。 |
| 小程序 | 需要调整商品卡片 badge 归一化逻辑与模板展示。 |
| 管理端 | 不涉及，继续复用 `REQ-0103` 的召回置顶配置。 |
| 数据库 | 不新增字段，复用 `recall_pin_sort_order`、有效期和排序 rank 判断。 |
| 测试 | 需要补后端接口测试、小程序静态测试和字段兼容测试。 |

## 3. 字段策略

后端响应字段建议命名为 `is_recall_pinned`，类型为 boolean，默认 `false`。字段语义必须限定为“当前列表中实际生效的召回置顶展示状态”，不是后台是否配置了召回排序值。

生成规则：

```text
当前请求应用召回置顶逻辑
AND SKU 满足召回置顶有效期和排序值条件
AND SKU 位于置顶数量上限内
AND SKU 满足当前筛选与公开展示条件
=> is_recall_pinned = true
```

新品商品列表、热销商品列表、搜索实时联想、收藏列表和不应用置顶逻辑的入口必须返回 `false` 或不触发前端展示。小程序遇到旧接口缺少该字段时默认按 `false` 处理。

## 4. 小程序展示策略

商品卡片继续复用现有角标区域。普通列表和搜索 SKU 结果中，当 `is_recall_pinned === true` 时展示固定文案“置顶”。

优先级：

```text
置顶 > 新品 > 热销 > 下架
```

该优先级只适用于会应用召回置顶逻辑的普通商品列表和搜索 SKU 结果。新品商品列表与热销商品列表本身没有置顶逻辑，因此不会进入“置顶”分支。

## 5. 原型与验收冲突处理

本需求只有 `prototype/miniapp/context.md`，没有 `prototype/web/`、HTML 或 PNG。原型策略与 acceptance 一致：复用商品图左上角角标、文案固定“置顶”、不新增页面、弹窗、教学文案或排序控件。

冲突结论：

- `REQ-0103` 曾约束“小程序不展示置顶 UI 标识”，本 Change 以 `REQ-0104` 的已评审需求为准，修改小程序商品卡片展示策略。
- 新品榜和热销榜继续遵守 `REQ-0103` 的“不应用置顶逻辑”边界。

## 6. 知识库承接

- `docs/knowledge-base/best-practices/miniapp-product-list-sorting.md`：后端公开 SKU 查询仍是分页排序事实源，小程序不得在分页追加后做跨页重排。
- `docs/knowledge-base/retrospectives/sprint-021-retrospective.md`：继续用 Scope 校验保证新增 REQ、Change 与 Sprint 目标一致。

## 7. 测试策略

- 后端测试覆盖 `/api/v1/miniapp/products` 普通列表中置顶商品返回 `is_recall_pinned: true`。
- 后端测试覆盖新品榜、热销榜返回 `is_recall_pinned: false`。
- 后端测试覆盖搜索 SKU 结果中置顶商品返回 `is_recall_pinned: true`。
- 小程序静态测试覆盖商品卡片优先展示“置顶”，缺省字段不展示。
- 回归测试确认小程序端不做本地重排，加载更多后不重复、不遗留错误标识。
