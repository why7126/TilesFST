## 1. Implementation

- [x] 1.1 确认当前 SKU 发布时间事实字段为 `published_at`；历史空值使用 `created_at` 作为排序兜底。
- [x] 1.2 调整 `/api/v1/miniapp/products` 品牌过滤场景排序，使 `brandId` 默认按发布时间升序、ID 升序返回。
- [x] 1.3 确认微信小程序品牌详情页商品 Tab 保持接口返回顺序展示，不新增前端跨页重排。
- [x] 1.4 保持搜索页相关性排序、新品榜近 90 天召回、热销榜 `hot_score DESC` 排序不变。
- [x] 1.5 如实现阶段引入新的请求参数、响应字段或数据库字段，补充 API、DB、docs、OpenAPI/Orval 同步任务后再继续。

## 2. Tests

- [x] 2.1 补充后端测试：同一品牌多 SKU 按发布时间升序、ID 升序返回。
- [x] 2.2 补充或扩展分页测试：品牌过滤场景跨页顺序稳定且无重复遗漏。
- [x] 2.3 补充回归断言：搜索页相关性排序、新品榜、热销榜不受影响。
- [x] 2.4 按需执行小程序静态检查或相关 smoke，确认品牌详情页商品 Tab 请求路径和展示顺序无回归。

## 3. Documentation & Trace

- [x] 3.1 实现说明中记录“发布时间”字段映射，以及是否影响 API、数据库、Orval、Web、小程序。
- [x] 3.2 若本修复没有改变 API 结构，明确记录“不需要 OpenAPI / Orval”。
- [x] 3.3 完成修复后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，记录不沉淀原因。

## Implementation Notes

- “发布时间”字段映射：当前 `tiles` 表已有独立 `published_at`，本修复使用 `tiles.published_at` 作为发布时间；历史空值使用 `tiles.created_at` 兜底以保证排序稳定。
- 后端影响：`MiniappHomeRepository.list_products()` 在 `brandId` + `sort=default` + 非新品/热销场景下使用 `COALESCE(t.published_at, t.created_at) ASC, t.id ASC`；`section=new`、`section=hot`、价格排序和搜索相关性排序保持原有分支。
- 小程序影响：品牌详情页商品 Tab 已确认仅按接口返回顺序首屏加载和追加分页数据，不新增端侧排序。
- API / DB / Orval：请求参数、响应结构和数据库结构均未改变，不需要 OpenAPI / Orval。
- Web / 管理端：不影响。
- 知识库：本修复为局部排序契约修正，已有 OpenSpec、BUG trace 和测试覆盖即可，不新增 `docs/knowledge-base/incidents/`。

## 归档验证摘要

- validation：`python scripts/validate-sprint-archive-readiness.py --sprint sprint-013` 于 2026-07-29 09:24:09 前置检查发现本归档 Change 缺少 `trace.md`，其余任务完成度为 12/12；本摘要作为历史归档证据兜底，供 Sprint 关闭门禁复核。
- acceptance：`tasks.md` 全部任务已完成，修复限定为 `/api/v1/miniapp/products?brandId=...` 品牌过滤场景默认排序；使用 `tiles.published_at` 升序、`id` 升序，历史空值使用 `created_at` 兜底，不改变 API 响应结构、数据库结构、OpenAPI / Orval、小程序端侧排序或管理端行为。
- issue_or_sprint_status：关联 `BUG-0087-miniapp-brand-detail-product-tab-sort-order` 已由 Workflow Sync 同步为 `status: done`、`lifecycle_stage: archive`、`iteration: sprint-013`，并记录 Change `fix-miniapp-brand-detail-product-sort-order` 为 `archived`；`iterations/archive/sprint-013/sprint.md` Scope 中该 BUG 与 Change 均显示 done / archived。
- archive_evidence：归档目录为 `openspec/archive/2026-07-28-fix-miniapp-brand-detail-product-sort-order/`；BUG trace 记录 `2026-07-29 07:53:54 | /opsx-archive | Change ... 已归档，状态同步完成`，并记录 `2026-07-29 07:54:14 | lifecycle-stage-migrate | review -> archive`。
