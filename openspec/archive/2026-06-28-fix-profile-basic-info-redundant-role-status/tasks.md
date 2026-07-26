## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0022-profile-basic-info-redundant-role-status` 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `ProfilePage.tsx` 表单 grid 是否仍含 `profile-role` / `profile-status`
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO、Docker compose 变更

## 2. 前端修复

- [x] 2.1 移除 `profile-form-grid` 内「所属角色」「账号状态」只读 field（若已移除则 verify）
- [x] 2.2 确认「账号安全」卡片 info-list 仍展示 role/status badge
- [x] 2.3 确认 identity-strip / card-head 不在本 change scope 内改动
- [x] 2.4 确认 TSX/CSS 无裸 Hex；表单 grid 布局无错位

## 3. 文档 delta

- [x] 3.1 确认 REQ-0014 `acceptance.md` AC-011、`requirement.md` FR-004 已 MODIFIED
- [x] 3.2 确认 `profile-page.html`、`profile-page-context.md` 已移除表单内 role/status
- [x] 3.3 归档前 OpenSpec delta 与 `openspec/specs/admin-profile-page/spec.md` 一致

## 4. 测试

- [x] 4.1 运行 `cd src/web && pnpm vitest run src/pages/admin/ProfilePage`
- [x] 4.2 可选：断言 `queryByLabelText('所属角色')` / `queryByLabelText('账号状态')` 在表单区为 null
- [x] 4.3 运行 `cd src/web && pnpm build`

## 5. 验收与追溯

- [x] 5.1 1440×1024 查看 `/admin/profile`：表单无 role/status input；账号安全卡片完整（vitest 结构 gate）
- [x] 5.2 对照 BUG-0022 acceptance AC-001～AC-009 勾选
- [x] 5.3 填写本 change `trace.md` 表单字段验收结论
- [x] 5.4 更新 `BUG-0022-profile-basic-info-redundant-role-status/trace.md` 中 `openspec_changes` 状态（apply 后 → applied）
- [x] 5.5 评估 `docs/knowledge-base/incidents/`（本缺陷为 UI UX，通常不需要）

## 6. 归档准备

- [x] 6.1 本文件全部 `[x]` 后执行 `/opsx-archive fix-profile-basic-info-redundant-role-status`
