## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0012-tile-sku-modal-form-field-rules` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 对照当前 `TileSkuFormModal.tsx`、`tile_sku_admin_service.py`、`tile_sku_admin.py`
- [x] 1.3 确认不回退 BUG-0011 弹窗滚动与 BUG-0009 列表 UI

## 2. 前端表单修复

- [x] 2.1 表面工艺：移除 Label `*` 与 `validateCreateFields` 必填校验
- [x] 2.2 参考价格：Label 加 `*`；新建默认 `0`；空值前端拦截（AC-027 风格）
- [x] 2.3 `buildPayload`：禁止 `reference_price: null`；默认/合法值含 `0`
- [x] 2.4 编辑模式：`reference_price==null` 回填 `0`

## 3. 后端 API 修复

- [x] 3.1 移除 create/update 对 surface_finish 的必填校验；空值 persist 为 `"-"`
- [x] 3.2 create/update 增加 reference_price 必填校验（含 `0.0`）
- [x] 3.3 `publish_sku` 移除 surface_finish 完整性拦截
- [x] 3.4 更新 Pydantic schemas 与 OpenAPI；运行 `./scripts/generate-openapi-client.sh`

## 4. 测试

- [x] 4.1 更新 `TileSkuFormModal.test.tsx`（默认值、必填、校验）
- [x] 4.2 更新 `test_admin_tile_skus.py`（create/update/publish 矩阵）
- [x] 4.3 运行 `cd src/backend && uv run pytest tests/ -k tile_sku`
- [x] 4.4 运行 `cd src/web && npx vitest run src/features/admin/components/TileSkuFormModal`

## 5. REQ 文档与验收

- [x] 5.1 更新 `issues/requirements/archive/REQ-0006-tile-sku-management/requirement.md` 字段定义
- [x] 5.2 更新 `acceptance.md` AC-024、AC-015
- [x] 5.3 按 BUG-0012 acceptance AC-001～AC-012 验收，记录于本 change `trace.md`
- [x] 5.4 更新 `BUG-0012-tile-sku-modal-form-field-rules/trace.md` 中 `openspec_changes` 状态

## 6. 收尾

- [x] 6.1 评估是否需 `docs/knowledge-base/incidents/` 沉淀（本缺陷为业务规则对齐，通常不需要）
- [ ] 6.2 `/opsx-archive fix-tile-sku-modal-form-field-rules`（Sprint 内与 add-tile-sku-management 协调顺序）
