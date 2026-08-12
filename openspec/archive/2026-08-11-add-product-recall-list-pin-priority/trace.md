---
change_id: add-product-recall-list-pin-priority
source_requirement: REQ-0103-product-recall-list-pin-priority
related_sprint: sprint-022
status: applied
created_at: 2026-08-07 23:12:00
updated_at: 2026-08-08 07:17:00
---

# 变更追踪

## 基本信息

```yaml
change_id: add-product-recall-list-pin-priority
source_requirement: REQ-0103-product-recall-list-pin-priority
related_sprint: sprint-022
status: applied
change_type: add
capabilities:
  modified:
    - tile-sku-management
    - miniapp-product-list-page
    - miniapp-search
    - database
impact:
  backend: true
  web_admin: true
  web_catalog: false
  miniapp: true
  database: true
  api: true
  storage: false
readiness: ready
```

## 实施记录

| 范围 | 证据 |
|---|---|
| 数据库 | SQLite / MySQL `tiles` 新增召回排序值与有效期字段，SQLite rebuild / extended migration 与 MySQL 兼容迁移同步维护，新增 `idx_tiles_recall_pin`。 |
| 后端 API | 管理端 SKU create/update/detail/list schema 支持召回字段；小程序品牌、分类、普通关键词列表与完整搜索 SKU 结果在分页前应用最多 4 个生效置顶 SKU；新品榜、热销榜、价格排序、实时联想和首页无筛选全部产品保持原排序。 |
| 管理端 Web | SKU 新建 / 编辑弹窗新增“运营配置”字段组，提交时归一化时间和默认值，校验正整数与开始/结束时间顺序。 |
| OpenAPI / Orval | 已运行 `./scripts/generate-openapi-client.sh`，同步 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`。 |
| 文档 | 已同步 API 索引和数据库设计文档。 |

## 验收返修记录

| 时间 | 验收反馈 | 调整 |
|---|---|---|
| 2026-08-08 07:00:00 | SKU 编辑弹窗排序字段需放在参考价格后，标签改为“排序”，标记必填并增加问号 hover 说明。 | 已调整 `TileSkuFormModal` 字段位置、标签、必填标识和 `CircleHelp` 帮助图标。 |
| 2026-08-08 07:00:00 | SKU 列表状态字段前需新增排序字段。 | 已在 `TileSkuManagementPage` 状态列前新增“排序”列，展示 `recall_pin_sort_order`。 |
| 2026-08-08 07:00:00 | SKU 列表“已上架”“已下架”状态不允许换行。 | 已为 `.sku-status` 增加单行显示样式，并更新列表测试断言。 |
| 2026-08-08 07:17:00 | SKU 编辑弹窗排序值非法时，错误提示需放在排序字段下方，文案为“排序值必须为正整数”，红色显示。 | 已将排序校验改为字段级错误，不再展示到弹窗顶部 `admin-notice`，并补充红色字段错误样式与测试。 |

## 需求映射

| 来源 | 覆盖方式 |
|---|---|
| FR-001 适用范围 | `miniapp-product-list-page` 与 `miniapp-search` delta 明确普通列表和搜索 SKU 结果生效，榜单 / 价格 / 联想等分支不生效。 |
| FR-002 后端统一排序 | delta 与 design 明确后端分页前排序事实源。 |
| FR-003 筛选与公开条件 | delta 明确公开过滤和请求筛选先于置顶资格计算。 |
| FR-004 数量与同级排序 | delta 明确默认最多 4 个生效置顶 SKU、排序值升序和稳定兜底。 |
| FR-005 运营配置与有效期 | `tile-sku-management` 与 `database` delta 明确字段、默认值、有效期空值语义和校验。 |
| FR-006 榜单例外 | `miniapp-product-list-page` delta 明确新品榜、热销榜和价格排序例外。 |
| FR-007 小程序展示约束 | `miniapp-product-list-page` 与 `miniapp-search` delta 明确无 UI 标识。 |
| FR-008 API 与数据模型 | proposal、design、tasks 和 `database` delta 明确同步范围。 |
| FR-009 可观测与测试 | tasks 与 test-plan 覆盖测试矩阵。 |

## 原型检查

| 项目 | 结论 |
|---|---|
| HTML 原型 | 无，非阻塞。 |
| PNG Golden Reference | 无，非阻塞。 |
| context.md | 已采纳：管理端 SKU 弹窗增加运营配置字段；小程序不新增 UI 标识。 |
| UI 策略 | 采用 Design System / 现有 SKU 弹窗复用策略。 |

## 校验记录

| 时间 | 命令 | 结果 | 说明 |
|---|---|---|---|
| 2026-08-07 23:28:00 | `./scripts/generate-openapi-client.sh` | passed | 已同步 OpenAPI 与 Orval 客户端。 |
| 2026-08-07 23:32:00 | `uv run pytest tests/test_miniapp_home.py` | passed | 40 passed；覆盖商品列表、搜索 SKU 结果、筛选、有效期、分页前排序和公开响应无召回字段。 |
| 2026-08-07 23:46:00 | `uv run pytest tests/test_miniapp_home.py tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py` | passed | 47 passed；覆盖小程序回归与 MySQL migration / schema drift。 |
| 2026-08-07 23:46:00 | `openspec validate add-product-recall-list-pin-priority --strict` | passed | Change strict 校验通过。 |
| 2026-08-07 23:46:00 | `python scripts/validate-openspec-language.py` | passed | OpenSpec 文档语言校验通过。 |
| 2026-08-07 23:46:00 | `python scripts/validate-directory-structure.py` | passed | 目录结构校验通过。 |
| 2026-08-07 23:46:00 | `python scripts/validate-sprint-scope.py sprint-022 --item REQ-0103-product-recall-list-pin-priority` | passed | Sprint scope 校验通过。 |
| 2026-08-07 23:48:00 | `python scripts/sync-workflow-status.py --event opsx.apply --change add-product-recall-list-pin-priority --sprint auto` | passed | Workflow Sync 更新 3 项、0 错误，REQ acceptance 保持 pending。 |
| 2026-08-07 23:48:00 | `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change add-product-recall-list-pin-priority --sprint sprint-022 --json` | passed | AI Usage 记录完成，sprint-022 snapshot refreshed。 |
| 2026-08-07 23:38:00 | `pnpm --dir src/web test -- TileSkuFormModal TileSkuManagementPage tile-skus-api` | passed | 59 files passed，337 tests passed；覆盖管理端 SKU 弹窗字段渲染与提交。 |
| 2026-08-07 23:39:00 | `uv run pytest src/backend/tests/test_admin_tile_skus.py ...` | blocked | 当前环境缺少 `PIL`，测试收集失败；已补充管理端 SKU 后端用例，待环境补齐 Pillow 后重跑。 |
| 2026-08-08 07:00:00 | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx src/pages/admin/TileSkuManagementPage.test.tsx -t "recall pin\|headers on one line\|renders pagination"` | passed | 2 files passed，3 passed / 38 skipped；覆盖本次返修字段位置、必填、帮助图标、列表排序列与状态单行样式。 |
| 2026-08-08 06:58:57 | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx src/pages/admin/TileSkuManagementPage.test.tsx src/features/admin/api/tile-skus-api.test.ts` | partial | SKU 相关 42 passed，1 个既有图片 fallback 用例失败；失败与本次排序/状态列返修无关，未改旁支契约。 |
| 2026-08-08 07:00:00 | `python scripts/sync-workflow-status.py --event opsx.modify --change add-product-recall-list-pin-priority --sprint auto` | passed | Workflow Sync 更新 2 项、0 错误，REQ acceptance 保持 pending。 |
| 2026-08-08 07:00:00 | `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change add-product-recall-list-pin-priority --sprint sprint-022 --json` | passed | AI Usage 记录完成，sprint-022 snapshot refreshed，warning_count=0。 |
| 2026-08-08 07:18:00 | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx -t "recall pin sort validation\|recall pin operation fields"` | passed | 1 file passed，2 passed / 23 skipped；覆盖排序字段级错误位置、红色错误 class、文案和全局错误区不展示。 |
| 2026-08-08 07:18:00 | `openspec validate add-product-recall-list-pin-priority --strict` | passed | Change strict 校验通过。 |
| 2026-08-08 07:18:00 | `python scripts/validate-openspec-language.py` | passed | OpenSpec 文档语言校验通过。 |
| 2026-08-08 07:18:00 | `python scripts/sync-workflow-status.py --event opsx.modify --change add-product-recall-list-pin-priority --sprint auto` | passed | Workflow Sync 更新 1 项、0 错误，REQ acceptance 保持 pending。 |
| 2026-08-08 07:18:00 | `python scripts/validate-directory-structure.py` | passed | 目录结构校验通过。 |
| 2026-08-08 07:18:00 | `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.modify --change add-product-recall-list-pin-priority --sprint sprint-022 --json` | passed | AI Usage 记录完成，sprint-022 snapshot refreshed，warning_count=0。 |
