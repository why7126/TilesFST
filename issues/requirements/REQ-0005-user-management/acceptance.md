---
title: 需求验收标准
purpose: 定义管理后台用户管理的功能、接口、数据、UI 与异常场景验收标准
content: 基于 requirement.md 与 prototype/web/user-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005 管理后台用户管理
---

# 验收标准

## 1. 功能验收

### 1.1 访问与权限

- [ ] **AC-001** 已登录且 `role=admin` 的用户可访问 `/admin/users`，页面标题为「用户管理」。
- [ ] **AC-002** `role=employee` 用户 Sidebar 不展示「用户管理」菜单项。
- [ ] **AC-003** `role=employee` 直接访问 `/admin/users` 时展示无权限或重定向至 `/admin/dashboard`。
- [ ] **AC-004** 未登录访问 `/admin/users` 由路由守卫跳转 `/admin/login`。
- [ ] **AC-005** `role=store_owner` 不可访问管理端用户管理（前后端双重校验）。

### 1.2 列表与筛选

- [ ] **AC-006** 筛选区包含：关键词、角色、状态、登录情况、搜索、重置；控件高度统一 40px。
- [ ] **AC-007** 关键词搜索匹配用户名、昵称、邮箱、手机号（后两者字段有值时）。
- [ ] **AC-008** 回车触发搜索；重置清空所有筛选并重新加载。
- [ ] **AC-009** 展示 4 个指标卡：用户总数、当前筛选、正常用户、已冻结用户。
- [ ] **AC-010** 列表标题区显示「用户列表 · 共 N 个用户」。
- [ ] **AC-011** 表格列：用户（头像+用户名+昵称/邮箱）、角色、状态、最后登录、创建时间、操作。
- [ ] **AC-012** 无头像时显示用户名首字母或默认占位；从未登录显示「从未登录」。
- [ ] **AC-013** 分页默认每页 10 条，可切换 10/20/50；展示范围如 `1-10 / 126`。

### 1.3 添加 / 编辑用户

- [ ] **AC-014** 点击「添加用户」打开弹窗，字段单列顺序：用户名、头像、昵称、角色。
- [ ] **AC-015** 弹窗不展示状态字段；新用户默认状态为正常。
- [ ] **AC-016** 用户名必填，4–32 位；仅限小写字母、数字、`_`、`-`、`.`；须以字母开头；禁止连续两个及以上特殊符号；禁止保留关键字；创建后不可修改。
- [ ] **AC-017** 编辑弹窗中用户名为只读。
- [ ] **AC-018** 角色选项：前台用户、后台运营、后台管理员（无超级管理员）。
- [ ] **AC-019** 头像可选上传；无头像使用默认占位。
- [ ] **AC-020** 创建成功 Toast「用户已创建」；编辑成功 Toast「用户信息已更新」。

### 1.4 重置密码

- [ ] **AC-021** 重置前弹出确认；确认后生成随机密码（≥12 位，含大小写数字特殊字符）。
- [ ] **AC-022** 成功后在二次弹窗展示一次性密码，提供复制按钮。
- [ ] **AC-023** 关闭弹窗后不可再次查看同一密码，仅可再次重置。

### 1.5 冻结 / 解冻 / 删除

- [ ] **AC-024** 冻结后状态为已冻结，操作变为「解冻」；解冻后恢复正常。
- [ ] **AC-025** 已冻结用户无法登录前台或后台。
- [ ] **AC-026** 仅 `last_login_at` 为空的用户可删除；已登录用户删除按钮置灰并提示原因。
- [ ] **AC-027** 删除为软删除，状态为已删除；已删除用户不可登录。
- [ ] **AC-028** 冻结/解冻/删除成功分别 Toast：用户已冻结 / 已恢复正常 / 已删除。

### 1.6 布局与导航

- [ ] **AC-029** 继承 `AdminLayout`：Sidebar 264px、100vh sticky，右侧独立滚动，最大宽度 1080px。
- [ ] **AC-030** 当前激活菜单为 SYSTEM > 用户管理。
- [ ] **AC-031** 页面无首页顶部欢迎区；视觉与 `user-management-list.png` 并排验收。

## 2. 接口验收

| 接口（建议） | 说明 |
|---|---|
| `GET /api/v1/admin/users` | 分页列表 + 筛选 + summary |
| `POST /api/v1/admin/users` | 创建用户，返回 `initial_password`（一次性） |
| `GET /api/v1/admin/users/{id}` | 用户详情（编辑回填） |
| `PATCH /api/v1/admin/users/{id}` | 更新昵称、角色、头像 |
| `POST /api/v1/admin/users/{id}/reset-password` | 重置密码，返回一次性明文 |
| `PATCH /api/v1/admin/users/{id}/status` | 冻结/解冻/软删除 |
| `POST /api/v1/media/upload`（或专用头像接口） | 头像上传授权 |

- [ ] **AC-032** 上述管理端用户 API 仅 `admin` 可调用，否则 HTTP 403。
- [ ] **AC-033** API 变更后执行 Orval 生成前端客户端。
- [ ] **AC-034** 错误码覆盖：用户名冲突、非法状态流转、禁止删除已登录用户等。

## 3. 数据验收

- [ ] **AC-035** `users` 表扩展：`avatar_object_key`（或等价字段）、`status` 支持 `deleted`（软删除）。
- [ ] **AC-036** `display_name`（昵称）允许为空，展示层回退用户名。
- [ ] **AC-037** 角色枚举与产品文案映射文档化：`store_owner`↔前台用户、`employee`↔后台运营、`admin`↔后台管理员。
- [ ] **AC-038** 头像文件存 MinIO，经后端授权，禁止前端直连未授权存储。

## 4. 技术验收

- [ ] **AC-039** 实现策略建议 CSS Port（对齐 `add-admin-home`），样式引用 semantic token，TSX 无裸 Hex。
- [ ] **AC-040** 复用 `AdminLayout`、`AdminSidebar`、分页与表格视觉与首页一致。
- [ ] **AC-041** 单元/组件测试覆盖：权限菜单、列表渲染、弹窗字段顺序、删除按钮禁用逻辑。
- [ ] **AC-042** 集成测试覆盖：admin CRUD、employee 403、冻结后登录失败。

## 5. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/user-management-list.html
2. prototype/web/user-management-list.png
3. prototype/web/user-management-modal.html
4. prototype/web/user-management-modal.png
5. prototype/web/*-context.md
6. acceptance.md（本文件）
7. rules/ui-design.md
```

- [ ] **AC-043** 列表页与 PNG 并排：筛选卡片、指标卡、表格、分页。
- [ ] **AC-044** 弹窗宽 520px、单列字段、遮罩 `rgba(0,0,0,.62)`，主按钮品牌金实底。
- [ ] **AC-045** `/design-system` 管理端分区可预览用户管理相关组件（若新增）。
