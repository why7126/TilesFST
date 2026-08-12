---
change_id: update-admin-user-contact-info-management
status: applied
source_requirement: REQ-0110-admin-user-contact-info-management
source_sprint: sprint-022
created_at: 2026-08-11 22:31:00
updated_at: 2026-08-12 00:12:00
ui_change: true
prototype_refs:
  - issues/requirements/archive/REQ-0110-admin-user-contact-info-management/prototype/web/admin-user-contact-info.html
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
---

# Trace

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-08-11 22:31:00 | req.opsx | 由 REQ-0110 创建 OpenSpec Change，状态为 proposed。 |
| 2026-08-11 23:36:00 | opsx.apply | 已实现管理端用户联系邮箱、手机号码维护；同步 OpenAPI/Orval/API 文档并完成后端、前端测试。 |
| 2026-08-11 23:47:00 | opsx.modify | 验收反馈：用户管理列表「创建时间」需按 `yyyy-mm-dd hh:MM` 展示；已调整前端展示、测试与 Change/REQ 文档。 |
| 2026-08-12 00:02:00 | opsx.modify | 验收反馈：用户新增/编辑弹窗标题上方空隙过大；已用专属 backdrop 作用域收紧标题区高度与上下 padding，并补充测试证据。 |
| 2026-08-12 00:12:00 | opsx.modify | 验收反馈：用户新增/编辑弹窗整体顶部空隙仍过大；已将用户表单弹窗 backdrop 改为顶部对齐并减小顶部 padding。 |

## 实现证据

- 后端：`src/backend/app/schemas/user_admin.py` 新增创建/更新联系字段；`src/backend/app/services/user_admin_service.py` 实现邮箱与宽松手机号校验、裁剪和清空语义；`src/backend/app/repositories/user_repository.py` 实现保存、更新、清空和关键词搜索。
- Web：`src/web/src/features/admin/components/UserFormModal.tsx` 新增联系邮箱、手机号码字段并提交 `null` 清空；`src/web/src/pages/admin/UserManagementPage.tsx` 在状态列后新增「联系邮箱」「手机号码」独立列，空值显示 `-`，搜索 placeholder 覆盖邮箱和手机。
- API：已运行 `./scripts/generate-openapi-client.sh`，同步 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`；`docs/03-api-index.md` 已补充字段、搜索、清空和校验说明。
- 验收返修：`src/web/src/pages/admin/UserManagementPage.tsx` 创建时间改为分钟级格式；`UserManagementPage.test.tsx` 补充 `2026-06-01 00:00` 展示断言。本次不改变 API、DB、权限或 Orval 类型。
- 验收返修：`src/web/src/features/admin/components/UserFormModal.tsx` 为用户表单弹窗 backdrop 增加 `user-form-modal-backdrop` 作用域；`user-management.css` 仅在该作用域下将 `.modal-head` 调整为 `min-height: 52px`、上下 padding `10px`，通用确认弹窗仍沿用默认 header。本次不改变 API、DB、权限或 Orval 类型。
- 验收返修：`user-management.css` 仅在 `.user-form-modal-backdrop` 作用域下将弹窗外层从默认垂直居中覆盖为 `align-items: flex-start`，并将顶部 padding 收为 `8px`，通用确认弹窗仍保持默认居中。本次不改变 API、DB、权限或 Orval 类型。

## UI 验收清单

- [x] UI Contract 已写入 `design.md`。
- [x] Skeleton 阶段引用 `prototype/web/admin-user-contact-info.html`，实现沿用既有 `user-management.css` 表格横向滚动策略。
- [x] 实现完成证据：`UserManagementPage.test.tsx` 覆盖状态列后新增联系邮箱、手机号码独立列、空值 `-` 和搜索 placeholder。
- [x] 实现完成证据：`UserFormModal.test.tsx` 覆盖字段展示、编辑回填、提交 payload 和清空提交。
- [x] 未新增裸 Hex；弹窗宽度沿用既有 modal 样式，未引入新的 card 宽度层叠覆盖。

## 验证记录

- `./scripts/generate-openapi-client.sh`：通过。
- `pnpm --dir src/web test UserFormModal.test.tsx UserManagementPage.test.tsx`：2 个文件、15 个用例通过。
- `uv run pytest src/backend/tests/test_admin_users.py`：22 个用例通过。
- `pnpm --dir src/web test UserManagementPage.test.tsx`：验收返修后通过。
- `pnpm --dir src/web test UserFormModal.test.tsx`：验收返修后通过；测试覆盖专属 backdrop 作用域，且确认 `modal-card` 未双挂专属 card 类。
- `sed -n '586,626p' src/web/src/features/admin/styles/user-management.css`：确认用户表单 backdrop 顶部对齐与 header 紧凑规则。
