---
bug_id: BUG-0014-tile-sku-publish-action-missing
status: pending_review
created_at: 2026-06-27 12:18:20
updated_at: 2026-06-27 12:18:20
---

# 临时规避方案

## 1. API 直接上架（推荐规避）

在修复发布前，对已下架 SKU 可通过 Admin API 恢复上架：

```http
POST /api/v1/admin/tile-skus/{id}/publish
Authorization: Bearer <admin_or_employee_token>
```

**前置条件**（与正常上架一致）：

- SKU 已设置主图（`has_main_image === true`）
- 必填字段完整（名称、编码、规格尺寸等）
- 编码非 `DRAFT-` 前缀

成功返回 HTTP 200 且 `data.status === 'PUBLISHED'` 后，刷新列表页即可看到「已上架」状态。

Swagger 入口：`http://localhost:8000/docs` → `POST /api/v1/admin/tile-skus/{tile_id}/publish`。

## 2. 不可用路径（排除）

| 路径 | 说明 |
|---|---|
| 编辑弹窗改状态 | 弹窗无 status 字段；PUT 不允许直接改 status（设计如此） |
| 先删除再新建 | 丢失原 id 与素材关联，非等价恢复 |
| SQL 直接改 `tiles.status` | 绕过业务校验，禁止 |

## 3. 规避有效期

- **有效期**：自 2026-06-27 起至 `fix-tile-sku-publish-action-missing` 发布并验收通过。
- **修复后**：正常流程 MUST 使用列表「恢复/上架」按钮；API 路径仅作应急保留。

## 4. 风险说明

- 运营人员若无 API 访问能力，**下架后无法恢复上架**，阻断 SKU 上下架闭环。
- 阻塞 REQ-0006 AC-018、AC-037 及 `add-tile-sku-management` 产品验收。
- severity **high**，建议优先于 medium 级 UI 一致性缺陷排期修复。
