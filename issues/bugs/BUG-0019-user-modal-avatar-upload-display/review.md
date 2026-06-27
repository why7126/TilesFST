---
bug_id: BUG-0019-user-modal-avatar-upload-display
review_id: REV-BUG-0019-001
status: approved
reviewed_at: 2026-06-27 13:12:26
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0019-user-modal-avatar-upload-display` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0019-user-modal-avatar-upload-display
```

建议修复 Change：

```text
fix-user-modal-avatar-upload-display
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 代码层 100% 可复现；运行时验证上传 Network 200 且 `avatar_object_key` 已入库，排除存储层；`root-cause.md` 已定位 `UserFormModal`、`UserManagementPage`、`UserAdminItem` 缺 `avatar_url`。 |
| 严重等级合理 | 通过 | 弹窗与列表头像均不可见，上传无 UI 反馈，管理员无法确认操作结果；与 REQ-0005 AC-019 及品牌 Logo 已修复体验不一致，`high` 合理。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-012 覆盖 API `avatar_url`、弹窗回显、Logo 对齐状态机、列表展示、测试/Orval、DS 约束。 |
| 是否需 hotfix 路径 | 不需要 | 非 blocker，不影响登录/核心业务；可走常规 `fix-*` Change，参照 BUG-0004/0007 模式。 |

## 3. 批准理由

1. **交付缺口明确**：上传与持久化链路已通，缺陷集中在 UI 预览/回显与 API 字段，非误报。
2. **修复路径清晰**：可直接复用 `BrandFormModal` + `brand_admin_service._logo_url` 已验证模式，scope 已确认含列表回显与完整上传状态机。
3. **规范对齐**：修复后满足 `openspec/specs/user-management/spec.md` 对 `avatar_url` 的要求。
4. **workaround 不可接受为长期方案**：仅能 Network/DB 验证，无法满足产品验收。

## 4. 后续要求

1. `/bug-opsx` 创建 `fix-user-modal-avatar-upload-display`，对齐 acceptance AC-001～AC-012。
2. 后端补充 `UserAdminItem.avatar_url`；前端弹窗对齐 `BrandFormModal` 状态机；列表页有 `avatar_url` 时渲染 `<img>`。
3. `uploadAvatar` 增加 `onUploadProgress`；OpenAPI 变更后同步 Orval。
4. 补充后端 avatar_url 可访问性测试与前端弹窗/列表 Vitest。
5. 建议纳入 Sprint 正式范围，优先级高于 medium 级 UI 一致性缺陷。
