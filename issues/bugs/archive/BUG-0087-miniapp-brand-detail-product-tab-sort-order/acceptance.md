---
bug_id: BUG-0087-miniapp-brand-detail-product-tab-sort-order
status: done
created_at: 2026-07-28 22:36:46
updated_at: 2026-07-29 07:54:10
related_requirement: REQ-0058-brand-detail-home-page
related_change:
---

# Acceptance - BUG-0087 品牌详情页商品 Tab 排序未按发布时间升序和 ID 升序

## 回归验收标准

- [ ] AC-BUG-001 `GET /api/v1/miniapp/products?brandId=<brandId>` 在品牌过滤场景下 MUST 仅召回当前品牌下可公开 SKU。
- [ ] AC-BUG-002 品牌过滤场景的默认排序 MUST 为发布时间升序、ID 升序。
- [ ] AC-BUG-003 当多条 SKU 发布时间相同时，接口 MUST 使用 `id ASC` 保证稳定排序。
- [ ] AC-BUG-004 品牌详情页商品 Tab 首屏展示顺序 MUST 与接口返回顺序一致。
- [ ] AC-BUG-005 品牌详情页商品 Tab 加载更多后，追加结果 MUST 继续保持发布时间升序、ID 升序，不得跨页重复、遗漏或顺序漂移。
- [ ] AC-BUG-006 修复 MUST 明确“发布时间”对应字段为 `tiles.published_at`；历史空值可使用 `tiles.created_at` 兜底排序，不得使用 `updated_at` 冒充发布时间。
- [ ] AC-BUG-007 修复 MUST 不改变搜索页相关性排序。
- [ ] AC-BUG-008 修复 MUST 不改变新品榜近 90 天召回规则和热销榜 `hot_score DESC` 排序。
- [ ] AC-BUG-009 修复 MUST 补充或更新后端测试，覆盖同一品牌多 SKU 的品牌过滤排序。
- [ ] AC-BUG-010 若仅调整后端排序逻辑且不改变响应结构，MUST 明确说明不需要 OpenAPI / Orval；若实际新增请求参数、响应字段或 schema，MUST 同步 OpenAPI、Orval、接口文档和测试。

## 验收证据要求

| 类型 | 要求 |
|---|---|
| API 证据 | 构造同品牌多 SKU，证明 `/miniapp/products?brandId=...` 返回顺序为发布时间升序、ID 升序 |
| 小程序证据 | 微信开发者工具或真机截图/录屏证明品牌详情页商品 Tab 顺序与接口一致 |
| 分页证据 | 至少覆盖两页数据或模拟分页，证明跨页顺序稳定 |
| 回归证据 | 搜索页、新品榜、热销榜排序未被品牌场景修复误改 |
| 影响说明 | 明确是否影响 API 字段结构、数据库、小程序页面、Web 管理端和 Orval |

## 非目标

- 本 BUG 不要求新增品牌详情页能力。
- 本 BUG 不要求重做品牌详情页视觉布局。
- 本 BUG 不要求调整搜索页、普通商品列表、新品榜或热销榜排序。
- 本 BUG 不要求新增购物车、下单、库存、促销或询价能力。
- 本 BUG 不要求直接修改数据库字段，除非后续评审确认缺少发布时间事实字段。
