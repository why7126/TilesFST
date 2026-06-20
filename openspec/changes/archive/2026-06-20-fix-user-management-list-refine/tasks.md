## 1. 后端 keyword 收窄

- [x] 1.1 修改 `user_repository.py`：keyword WHERE 仅保留 `username`、`display_name` LIKE，移除 `email`、`phone`
- [x] 1.2 补充 `test_admin_users.py`：keyword 命中 username/display_name 正向用例；email/phone 不被 keyword 误命中负向用例

## 2. 前端列表页 UI（CSS Port 增量）

- [x] 2.1 更新 `user-management.css`：筛选网格 5 列（`1.5fr 1fr 1fr 1.1fr auto`）；`.user-meta` 纵向两行；`.pagination` 左 summary + 右 page-right 结构；移除/废弃 section-head、table-toolbar 样式引用
- [x] 2.2 更新 `UserManagementPage.tsx`：删除「搜索」按钮与 `section-head`、`table-toolbar` DOM
- [x] 2.3 placeholder 改为「搜索用户名/昵称」；移除邮箱相关文案
- [x] 2.4 实现关键词防抖（~300ms）+ Enter + 筛选项 onChange 自动查询；重置清空全部条件 page=1
- [x] 2.5 用户列：`.user-meta` 包裹 `.user-main`（username）与 `.user-sub`（display_name 或「未设置昵称」）；禁止 email 回退
- [x] 2.6 分页：左侧「共 {total} 个用户」；右侧页码 +「每页显示」select；移除「1-10 / N」等旧文案

## 3. 测试

- [x] 3.1 更新/新增 vitest：`UserManagementPage` 或相关组件测试（无搜索按钮、自动查询、用户列两行、分页文案）
- [x] 3.2 运行 `cd src/backend && uv run pytest tests/test_admin_users.py -q`
- [x] 3.3 运行 `cd src/web && pnpm exec vitest run`（用户管理相关用例）

## 4. 构建与部署验证

- [x] 4.1 `cd src/web && pnpm run build`
- [x] 4.2 （可选）`./scripts/docker-up.sh` 本地验证 `/admin/users`

## 5. 视觉验收（PNG Golden Reference）

- [x] 5.1 1280×1024 并排对比实现页与 v2 `user-management-list.html` / 导出 PNG
- [x] 5.2 填写 `openspec/changes/fix-user-management-list-refine/trace.md` checklist（≥15 项）
- [ ] 5.3 更新 `issues/requirements/REQ-0005-user-management-list-refine/prototype/web/user-management-list.png`（重新导出）
- [x] 5.4 回归：modal 行为与 `user-management-modal.png` 无变化

## 6. 文档与追溯

- [x] 6.1 更新 `issues/requirements/REQ-0005-user-management-list-refine/trace.md`：`openspec_changes` status
- [x] 6.2 （可选）同步 `docs/03-api-index.md` keyword 参数说明
- [x] 6.3 完成后执行 `/opsx-archive fix-user-management-list-refine`（建议 `add-user-management` 已 archive 或同批处理）
