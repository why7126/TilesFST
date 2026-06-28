## 1. 准备与定位

- [x] 1.1 阅读 `BUG-0023-profile-duplicate-save-buttons` 的 bug.md、root-cause.md、acceptance.md
- [x] 1.2 对照 `ProfilePage.tsx` 页头与表单底双按钮、`ProfilePage.test.tsx`
- [x] 1.3 确认不涉及 API、数据库、Orval、MinIO、Docker compose 变更

## 2. 前端修复

- [x] 2.1 移除 `profile-page-head` 内「保存修改」按钮（保留眉标/标题/说明）
- [x] 2.2 确认表单底 `profile-form-actions` 保留「重置 + 保存修改」与 `handleSave()` / disabled 逻辑不变
- [x] 2.3 确认 TSX/CSS 无裸 Hex；页头 layout 无错位

## 3. 测试

- [x] 3.1 更新 `ProfilePage.test.tsx`：`getAllByRole` → `getByRole('button', { name: '保存修改' })`
- [x] 3.2 校验失败、重置、save-tip 用例仍通过
- [x] 3.3 运行 `cd src/web && pnpm vitest run src/pages/admin/ProfilePage`

## 4. 验收与追溯

- [x] 4.1 1440×1024 查看 `/admin/profile`：页头无重复金色主按钮；表单 actions 与 save-tip 对齐（vitest 单 CTA）
- [x] 4.2 对照 BUG-0023 acceptance AC-001～AC-011 勾选
- [x] 4.3 填写本 change `trace.md` 单 CTA 验收结论
- [x] 4.4 更新 `BUG-0023-profile-duplicate-save-buttons/trace.md` 中 `openspec_changes` 状态（apply 后 → applied）
- [x] 4.5 评估 `docs/knowledge-base/incidents/`（本缺陷为 UI UX，通常不需要）

## 5. 归档准备

- [x] 5.1 本文件全部 `[x]` 后执行 `/opsx-archive fix-profile-duplicate-save-buttons`
