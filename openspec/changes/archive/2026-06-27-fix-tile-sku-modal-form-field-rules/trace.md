---
created_at: 2026-06-27 11:47:09
updated_at: 2026-06-27 11:50:30
title: fix-tile-sku-modal-form-field-rules 追溯
purpose: BUG-0012 SKU 弹窗表面工艺/参考价格字段规则 fix change
content: 表面工艺非必填、参考价格必填默认0；前后端校验与 REQ-0006 delta
owner: product
status: applied
bug_id: BUG-0012-tile-sku-modal-form-field-rules
related_requirement: REQ-0006-tile-sku-management
sprint: sprint-002
---

# Change 追溯

## 关联

| 项 | 值 |
|---|---|
| BUG | BUG-0012-tile-sku-modal-form-field-rules |
| REQ | REQ-0006-tile-sku-management |
| Sprint | sprint-002 |
| 父 change | add-tile-sku-management |

## 验收 checklist（apply 后）

| AC | 描述 | 结果 |
|---|---|---|
| AC-001 | 表面工艺非必填 | pass |
| AC-003 | 参考价格必填默认 0 | pass |
| AC-004 | 参考价格空值拦截 | pass |
| AC-005 | 0 元展示 ¥ 0.00 | pass |
| AC-007 | 上架不拦空工艺 | pass |
| AC-009 | Orval 同步 | pass |
| AC-010 | REQ-0006 文档 delta | pass |
| AC-012 | 不回退 BUG-0011/0009 | pass |

## 测试记录

| 套件 | 命令 | 结果 |
|---|---|---|
| 后端 | `uv run pytest tests/ -k tile_sku` | 14 passed |
| 前端 | `npx vitest run TileSkuFormModal.test.tsx` | 3 passed |
| Orval | `./scripts/generate-openapi-client.sh` | ok |

## 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-27 11:47:09 | `/bug-opsx` | 创建 fix-tile-sku-modal-form-field-rules |
| 2026-06-27 11:50:30 | `/opsx-apply` | 前后端校验、测试、REQ delta；20/21 tasks |
