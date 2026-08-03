---
change_id: update-miniapp-brand-list-category-summary
source_requirement: REQ-0083-miniapp-brand-list-category-summary
change_type: update
status: applied
created_at: 2026-07-30 22:58:51
updated_at: 2026-07-31 00:30:54
owner: product
iteration: sprint-014
---

# Change Trace

## 来源

- REQ: `issues/requirements/archive/REQ-0083-miniapp-brand-list-category-summary/`
- 父需求：`REQ-0060-brand-list-page`
- 相关能力：`miniapp-brand-list-page`
- 预期 Change：`update-miniapp-brand-list-category-summary`

## 影响分析

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - miniapp-brand-list-page
change_type: update
readiness: Ready
```

## 知识库引用

- `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`
- `docs/knowledge-base/retrospectives/sprint-013-retrospective.md`

## 原型与验收优先级

```text
prototype/miniapp/prototype.html > prototype/miniapp/context.md > acceptance.md > rules/ui-design.md > openspec/specs
```

PNG checklist：

- [ ] `prototype/miniapp/prototype.png` 可在后续从 HTML 导出，缺 PNG 不阻塞当前 proposal。
- [ ] `/opsx-apply` 后需要记录 DevTools 320、375、430 pt evidence。
- [ ] 真机不可用时必须标记 blocked 或 follow_up。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-31 00:30:54 | `/opsx-modify` | 验收返修：品牌无公开商品时右侧类目区留空，不重复展示左侧已有的“暂无商品”空态文案 |
| 2026-07-31 00:23:26 | `/opsx-modify` | 验收返修：品牌 Logo / 名称点击进入品牌详情页；右侧类目点击进入该品牌该类目商品列表；公开品牌接口新增 `leaf_categories` 类目 ID / 名称集合 |
| 2026-07-31 00:09:46 | `/opsx-modify` | 验收返修：取消小程序端前 3 个类目和 `+N` 折叠策略，右侧类目区折行展示品牌下所有上架/公开商品关联的去重末级类目名称 |
| 2026-07-30 23:54:39 | `/opsx-modify` | 验收返修：移除“品牌有商品但无类目”的正常兜底语义；明确右侧类目完全根据品牌下公开商品关联类目计算，只有无公开商品时展示无商品空态 |
| 2026-07-30 23:23:41 | `/opsx-apply` | 已实现公开品牌列表 `leaf_category_names` 契约、小程序品牌单行列表布局、OpenAPI/Orval/文档和自动化测试；DevTools 320/375/430 与真机验收在 Sprint 验收报告标记 follow_up |
| 2026-07-30 23:04:59 | `/sprint-propose sprint-014` | 纳入 Sprint 014 正式范围 |
| 2026-07-30 22:58:51 | `/req-opsx` | 从 REQ-0083 创建 OpenSpec Change，生成 proposal、design、delta spec、tasks 与 trace |

## 实现记录

| 范围 | 文件 | 说明 |
|---|---|---|
| 后端 API | `src/backend/app/schemas/miniapp_home.py`、`src/backend/app/repositories/miniapp_home_repository.py`、`src/backend/app/services/miniapp_home_service.py` | `MiniappBrandCard` 增加 `leaf_category_names`；列表和详情复用同一公开商品过滤口径聚合去重末级类目名称 |
| 小程序 | `src/miniapp/pages/brand-list/index.*` | 保留顶部轮播结构与行为；下半部改为一行一个品牌，左侧 Logo/名称/商品数，右侧折行展示所有上架/公开商品关联末级类目标签 |
| API 契约 | `src/web/openapi.json`、`src/web/src/shared/api/generated.ts` | 运行 `bash scripts/generate-openapi-client.sh` 同步 OpenAPI 与 Orval |
| 文档 | `docs/03-api-index.md`、`src/miniapp/README.md` | 更新品牌列表公开字段、过滤口径和小程序布局说明 |
| 测试 | `tests/test_miniapp_home.py`、`tests/test_miniapp_static.py` | 覆盖商品数量、类目提取/去重/排序、空商品、单行布局、Logo fallback、类目溢出和点击跳转 |

## 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-30 23:21:10 | `uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking` | 3 passed；3 warnings（既有 Pydantic/FastAPI deprecation） |
| 2026-07-30 23:21:10 | `python scripts/validate-api-standard.py` | API 标准校验通过 |
| 2026-07-30 23:21:10 | `openspec validate update-miniapp-brand-list-category-summary --strict` | valid |
| 2026-07-30 23:22:02 | `python scripts/validate-directory-structure.py` | 目录结构校验通过 |
| 2026-07-30 23:54:39 | `uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking` | 返修后 3 passed；3 warnings（既有 Pydantic/FastAPI deprecation） |
| 2026-07-30 23:54:39 | `openspec validate update-miniapp-brand-list-category-summary --strict` | valid |
| 2026-07-31 00:09:46 | `uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking` | 返修后 3 passed |
| 2026-07-31 00:09:46 | `openspec validate update-miniapp-brand-list-category-summary --strict` | valid |
| 2026-07-31 00:23:26 | `uv run pytest tests/test_miniapp_home.py::test_miniapp_brand_list_returns_public_brands_and_brand_list_carousel tests/test_miniapp_home.py::test_miniapp_brand_home_endpoints_return_public_detail_and_certificates tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking` | 返修后 3 passed |
| 2026-07-31 00:23:26 | `bash scripts/generate-openapi-client.sh` | OpenAPI / Orval 已同步 `leaf_categories` |
| 2026-07-31 00:30:54 | `uv run pytest tests/test_miniapp_static.py::test_miniapp_brand_list_page_covers_carousel_grid_entry_and_tracking` | 返修后 1 passed，覆盖无公开商品品牌右侧不渲染重复空态文案 |
| 2026-07-31 00:30:54 | `openspec validate update-miniapp-brand-list-category-summary --strict` | valid |

## 设备 Evidence

| 项 | 状态 | 说明 |
|---|---|---|
| DevTools 320/375/430 pt | follow_up | 本次完成代码、静态与接口自动化验证；未伪造微信开发者工具截图通过，需要人工在 IDE 中补录首屏轮播、品牌单行列表、胶囊避让和底部 TabBar evidence |
| 真机验收 | follow_up | 当前未执行真机验收；按 `miniapp-custom-navigation` best practice 保留人工确认项，不将 DevTools 或静态检查写作真机通过 |
