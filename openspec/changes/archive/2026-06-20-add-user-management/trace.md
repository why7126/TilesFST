# add-user-management — Trace

## 变更摘要

- **REQ**: `REQ-0005-user-management`
- **Iteration**: `sprint-002`
- **Type**: add
- **Strategy**: CSS Port（路径 A，自 `user-management-list.html` + `user-management-modal.html`）
- **Depends**: `add-admin-home`（AdminLayout / AdminSidebar）
- **Status**: applied（待 archive；6.1 DS 预览可选跳过）

## 关联文档

| 文档 | 路径 |
|---|---|
| PRD | `issues/requirements/REQ-0005-user-management/requirement.md` |
| 验收 | `issues/requirements/REQ-0005-user-management/acceptance.md` |
| 列表 HTML | `issues/requirements/REQ-0005-user-management/prototype/web/user-management-list.html` |
| 列表 PNG | `issues/requirements/REQ-0005-user-management/prototype/web/user-management-list.png` |
| 弹窗 HTML | `issues/requirements/REQ-0005-user-management/prototype/web/user-management-modal.html` |
| 弹窗 PNG | `issues/requirements/REQ-0005-user-management/prototype/web/user-management-modal.png` |
| Design | `openspec/changes/add-user-management/design.md` |

## Conflict Resolution 记录

| 项 | 决议 |
|---|---|
| 角色 enum vs 中文 | 前端映射；API 保持 `store_owner`/`employee`/`admin` |
| 状态 deleted | 扩展 DB CHECK；登录拒绝 |
| employee 管理端 | 可进 dashboard；用户管理 admin-only |
| 用户名 4–32 | PRD / AC / 后端校验一致 |

## 视觉 Diff Checklist（1280×1024）

验收方式：2026-06-20 代码/CSS Port 结构对照 **HTML v1** + Docker 路由冒烟。

### 列表页（user-management-list.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | Shell 264px + 1fr | pass | `AdminLayout` + `admin-home.css` |
| 2 | Sidebar「用户管理」active | pass | `admin-nav.ts` `/admin/users` |
| 3 | 无首页欢迎区 | pass | 独立列表页 |
| 4 | 页面标题「用户管理」+ 品牌金「添加用户」 | pass | `page-hero` |
| 5 | 筛选卡片 6 列网格（桌面） | pass | `filter-grid` 1.5fr + 4 + auto auto |
| 6 | 输入/选择器高度 40px | pass | `.input/.select { height: 40px }` |
| 7 | 4 指标卡网格 | pass | summary API |
| 8 | 指标数值品牌金 | pass | `.metric-value` |
| 9 | 表格列：用户/角色/状态/最后登录/创建时间/操作 | pass | 6 列 |
| 10 | 角色/状态 badge 样式 | pass | `user-labels.ts` |
| 11 | 操作链接按钮组 | pass | 编辑/重置/冻结/删除 |
| 12 | 从未登录用户删除可点；已登录删除置灰 | pass | `canDelete = !last_login_at` |
| 13 | 分页区：每页条数 + 范围 + 页码 | pass | page-left + page-buttons |
| 14 | 表格 toolbar「当前显示 1-10 / N」 | pass | `table-toolbar` |
| 15 | 主内容 max-width 1080px | pass | `admin-home.css` `.content-inner` |

### 弹窗（user-management-modal.html）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 16 | 遮罩 rgba 暗色 | pass | `modal-backdrop` |
| 17 | 弹窗宽 520px | pass | `user-management.css` |
| 18 | 单列字段顺序 | pass | 用户名→头像→昵称→角色 |
| 19 | 无状态字段 | pass | status 仅列表操作 |
| 20 | 主按钮品牌金「创建用户」 | pass | `btn primary` |
| 21 | 输入框高度 ~42px | pass | 与 HTML 近似 |
| 22 | 背景列表仍可识别 | pass | 半透明遮罩 |

## Docker 冒烟（8.2）

| 检查 | 结果 |
|---|---|
| `./scripts/docker-up.sh` | pass（服务已运行） |
| `GET http://localhost:3000/admin/users` | 200 |
| `GET http://localhost:8000/api/v1/admin/users`（无 token） | 401（路由已挂载） |

## 验证命令

```bash
cd src/backend && uv run pytest tests/ -k user
cd src/web && npx vitest run src/features/admin src/pages/admin
cd src/web && npm run build
./scripts/generate-openapi-client.sh
./scripts/docker-up.sh
```

## 角色映射（实现参考）

| API `role` | UI 文案 |
|---|---|
| `store_owner` | 前台用户 |
| `employee` | 后台运营 |
| `admin` | 后台管理员 |

| API `status` | UI 文案 |
|---|---|
| `active` | 正常 |
| `disabled` | 已冻结 |
| `deleted` | 已删除 |
