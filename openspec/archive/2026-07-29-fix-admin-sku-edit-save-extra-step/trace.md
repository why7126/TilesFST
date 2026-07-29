---
change_id: fix-admin-sku-edit-save-extra-step
status: applied
type: fix
created_at: 2026-07-28 23:23:36
updated_at: 2026-07-28 23:34:32
source_bug: BUG-0088-admin-sku-edit-save-extra-step
source_bug_path: issues/bugs/archive/BUG-0088-admin-sku-edit-save-extra-step/
sprint: sprint-013
capabilities:
  modified:
    - tile-sku-management
impact:
  backend: false
  web: true
  miniapp: false
  admin: true
  database: false
  storage: false
  api: false
---

# Change Trace

## 来源

- BUG：`BUG-0088-admin-sku-edit-save-extra-step`
- 评审状态：`approved`
- 父需求：`REQ-0006-tile-sku-management`
- Change 类型：`fix`

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-28 23:29:42 | `/opsx-apply` | 已修复管理端 SKU 编辑弹窗保存成功后多余任务追踪反馈；编辑成功直接关闭弹窗。 |
| 2026-07-28 23:34:32 | scope-adjust | 按反馈扩展范围：创建 SKU 成功后也不保留弹窗内任务追踪反馈，统一直接关闭弹窗。 |
| 2026-07-28 23:23:36 | `/sprint-propose` | 纳入 sprint-013 正式范围。 |
| 2026-07-28 23:23:36 | `/bug-opsx` | 创建 OpenSpec Change，并生成 proposal、design、delta spec、tasks 与 trace。 |

## Implementation Evidence

| 项 | 结论 |
|---|---|
| Web Admin | `TileSkuFormModal` 创建、保存草稿、编辑成功后调用对应 `onSuccess(...)` 并立即 `onClose()`。 |
| Tips | 成功响应即使包含 `task_trace_id`，也不渲染弹窗内 task trace feedback、任务类型或复制追踪 ID 按钮。 |
| Create Flow | 新增 SKU 成功后不再保留弹窗内 task trace feedback，直接关闭弹窗。 |
| Admin Modal Gate | 继续使用单一 `sku-modal-card`，未引入 `modal-card` 双类或 CSS 宽度层叠变更。 |

## Validation Evidence

| 命令 | 结果 |
|---|---|
| `pnpm --dir src/web test -- TileSkuFormModal.test.tsx` | Pass：Vitest run 完成，56 files / 298 tests passed。 |
| `openspec validate fix-admin-sku-edit-save-extra-step --strict` | Pass。 |

## Impact Conclusion

- API/DB/Orval：无影响。
- Web/Admin：仅影响 SKU 编辑弹窗成功态。
- 小程序/存储/Docker：无影响，本次无需 Docker Compose 验证。
