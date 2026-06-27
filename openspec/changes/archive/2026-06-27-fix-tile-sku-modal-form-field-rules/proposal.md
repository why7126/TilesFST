## Why

[BUG-0012-tile-sku-modal-form-field-rules](issues/bugs/BUG-0012-tile-sku-modal-form-field-rules/) 已评审通过并纳入 `sprint-002`。UAT 阶段产品规则调整要求：SKU 新增/编辑弹窗「表面工艺」改**非必填**、「参考价格（元）」改**必填**且新建默认 **0 元**。当前实现仍按 REQ-0006 v4 旧 spec（工艺必填、价格选填）在前后端双重校验，且 `publish_sku` 拒绝空工艺，导致运营录入与验收预期不符。

`add-tile-sku-management` 尚未归档；本缺陷 MUST 通过新的 `fix-*` change 修正校验规则并同步 REQ-0006 acceptance delta。

## What Changes

- 前端 `TileSkuFormModal`：去掉表面工艺 `*` 与必填校验；参考价格加 `*`、新建默认 `0`、空值拦截。
- 后端 `TileSkuAdminService`：create/update 移除 surface_finish 必填；reference_price 必填（含 `0.0`）；`publish_sku` 移除表面工艺完整性拦截。
- OpenAPI / Pydantic 更新后运行 Orval。
- 更新 `issues/requirements/REQ-0006-tile-sku-management/requirement.md` 字段定义与 `acceptance.md` AC-024、AC-015。
- 补充前后端回归测试；记录 change `trace.md` 验收结论。

## Impact

| 影响面 | 说明 |
|---|---|
| Web 管理端 | SKU 弹窗表单校验、默认值、Label 必填标记 |
| 后端 API | create/update/publish 校验规则；OpenAPI schema |
| REQ-0006 | acceptance / requirement 字段规则 delta |
| 数据库 | 不变（`surface_finish NOT NULL` 仍可用 `"-"` 表示空；`reference_price` 可空列存 0） |
| Orval | **需要**（`reference_price` 语义变更） |
| MinIO | 不变 |

## Rollback Plan

若修复引起 SKU 保存/上架回归，可回滚本 change 的前后端校验改动：

1. 恢复 `TileSkuFormModal.tsx` 校验与默认值。
2. 恢复 `tile_sku_admin_service.py` create/update/publish 校验。
3. 恢复 OpenAPI 并重新 Orval。
4. 保留 BUG 与 OpenSpec 记录，重新评估产品规则。

回滚不涉及数据库 migration。
