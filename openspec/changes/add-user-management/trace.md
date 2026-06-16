# add-user-management — Trace

## 变更摘要

- **REQ**: `REQ-0005-user-management`
- **Iteration**: `sprint-002`
- **Type**: add
- **Strategy**: CSS Port（路径 A，自 `user-management-list.html` + `user-management-modal.html`）
- **Depends**: `add-admin-home`（AdminLayout / AdminSidebar）
- **Status**: applied（待 PNG 人工验收与 archive）

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

## PNG 视觉 Diff Checklist（1280×1024）

### 列表页（user-management-list.png）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | Shell 264px + 1fr | | |
| 2 | Sidebar「用户管理」active | | |
| 3 | 无首页欢迎区 | | |
| 4 | 页面标题「用户管理」+ 品牌金「添加用户」 | | |
| 5 | 筛选卡片 6 列网格（桌面） | | |
| 6 | 输入/选择器高度 40px | | |
| 7 | 4 指标卡网格 | | |
| 8 | 指标数值品牌金 | | |
| 9 | 表格列：用户/角色/状态/最后登录/创建时间/操作 | | |
| 10 | 角色/状态 badge 样式 | | |
| 11 | 操作链接按钮组 | | |
| 12 | 从未登录用户删除可点；已登录删除置灰 | | |
| 13 | 分页区：每页条数 + 范围 + 页码 | | |
| 14 | 表格 toolbar「当前显示 1-10 / N」 | | |
| 15 | 主内容 max-width 1080px | | |

### 弹窗（user-management-modal.png）

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 16 | 遮罩 rgba 暗色 | | |
| 17 | 弹窗宽 520px | | |
| 18 | 单列字段顺序 | | |
| 19 | 无状态字段 | | |
| 20 | 主按钮品牌金「创建用户」 | | |
| 21 | 输入框高度 ~42px | | |
| 22 | 背景列表仍可识别 | | |

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
