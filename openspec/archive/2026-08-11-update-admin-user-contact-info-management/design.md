# 设计：用户管理联系信息维护

## 决策摘要

- Change 类型：`update`，修改既有 `user-management` 能力。
- 联系邮箱、手机号码是普通联系信息，不唯一，不参与认证和权限。
- 列表展示采用独立列：`用户 | 角色 | 状态 | 联系邮箱 | 手机号码 | 最后登录 | 创建时间 | 操作`。
- 空值统一显示 `-`。
- 创建时间按 `yyyy-mm-dd hh:MM` 分钟级格式展示。
- 管理端弹窗字段顺序：用户名、头像、昵称、联系邮箱、手机号码、角色。

## 需求与知识库引用

- REQ：`issues/requirements/archive/REQ-0110-admin-user-contact-info-management/`
- Sprint：`iterations/archive/sprint-022/`
- 原型：`issues/requirements/archive/REQ-0110-admin-user-contact-info-management/prototype/web/admin-user-contact-info.html`
- Knowledge-base：
  - `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
  - `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- UI 验收标准：`docs/standards/prototype-ui-acceptance.md`

## Conflict Resolution

事实源优先级：

```text
1. prototype/web/admin-user-contact-info.html
2. prototype/web/context.md
3. acceptance.md
4. requirement.md
5. rules/ui-design.md
6. openspec/specs/user-management/spec.md
```

已知冲突与处理：

| 来源 | 冲突 | 决策 |
|---|---|---|
| 既有 `user-management` spec | 表单字段顺序只有用户名、头像、昵称、角色 | 本 Change MODIFIED 为用户名、头像、昵称、联系邮箱、手机号码、角色 |
| 既有列表 spec | 用户列可展示昵称/邮箱，未要求独立列 | 本 Change MODIFIED 为状态列后新增两个独立列 |
| 历史列表优化需求 | 搜索范围曾收窄到用户名/昵称 | 本 Change 重新扩展到用户名、昵称、邮箱、手机号 |

## UI Contract

| 项 | 合同 |
|---|---|
| 事实源优先级 | 以 `admin-user-contact-info.html` 与 `context.md` 为增量事实源；与旧 spec 冲突时以本 Change delta 为准 |
| 页面与入口 | `/admin/users`，仅 `role=admin` 可见和可操作；Sidebar SYSTEM「用户管理」active |
| 信息架构 | 保留页面标题、指标卡、筛选区、用户表格、分页和行操作；表格新增联系邮箱、手机号码独立列 |
| 列顺序 | 用户、角色、状态、联系邮箱、手机号码、最后登录、创建时间、操作 |
| 时间格式 | 创建时间按 `yyyy-mm-dd hh:MM` 展示；最后登录沿用既有分钟级展示或从未登录文案 |
| 空值 | 联系邮箱、手机号码为空时显示 `-` |
| 弹窗 | 添加/编辑用户弹窗单列字段：用户名、头像、昵称、联系邮箱、手机号码、角色；状态字段仍不展示；用户表单弹窗专属 backdrop 采用顶部对齐并收紧标题区留白 |
| 视觉 token | 沿用 `user-management.css` 与管理端 semantic token；禁止新增裸 Hex |
| 交互状态 | 字段校验错误显示在对应字段或字段组附近；保存成功使用 fixed toast；上传状态机不回退 |
| 图标与文案 | 搜索 placeholder 表达用户名/昵称/邮箱/手机；联系信息文案不暗示可登录 |
| Mock/API 边界 | 使用真实管理端用户 API；本 Change 不引入 Mock 数据；OpenAPI/Orval 是前端类型事实源 |
| 权限规则 | 仅 admin 可调用；employee/store_owner 仍 403；受保护账号不可编辑 |
| 一致性参照 | 列表分页、toast、confirm 对齐 admin-list best-practice；弹窗宽度和矮视口滚动对齐 admin-modal best-practice |

## API 设计

### 创建用户

`POST /api/v1/admin/users` 请求体新增可选字段：

```yaml
email: string | null
phone: string | null
```

保存规则：

- 前后空白裁剪。
- 空字符串保存为 `null`。
- 邮箱非空时按邮箱格式校验。
- 手机号非空时只允许数字、空格、`+`、`-`。
- 不做唯一性校验。

### 更新用户

`PATCH /api/v1/admin/users/{id}` 请求体新增可选字段：

```yaml
email: string | null
phone: string | null
```

字段存在时更新或清空；字段缺省时保持原值。

### 查询用户

`GET /api/v1/admin/users` 与 `GET /api/v1/admin/users/{id}` 继续返回 `email`、`phone`。列表关键词匹配范围为 `username`、`display_name`、`email`、`phone`。

## 数据设计

`users.email`、`users.phone` 已存在，不新增字段。实现时需确认：

- SQLite schema / migration 包含 `email`、`phone`。
- MySQL schema / migration 包含 `email`、`phone`。
- 历史环境缺列时只通过既有 migration 机制补齐，不做业务代码旁路。

## 测试策略

- 后端：`tests/test_admin_users.py` 或等价集成测试覆盖创建、更新、清空、非法格式、搜索、权限。
- 前端：`UserFormModal.test.tsx`、`UserManagementPage.test.tsx` 覆盖字段、payload、列顺序、空值显示和 placeholder。
- 生成物：同步 OpenAPI / Orval 后执行相关类型或组件测试。
- UI：1440px 验收表格列顺序、空值 `-`、弹窗字段顺序；必要时记录弹窗 computed width。

## 后续实现顺序

1. 更新后端 Schema、校验、Repository、Service 和 API 测试。
2. 生成 OpenAPI / Orval。
3. 更新 Web 表单、列表列、搜索文案和前端测试。
4. 执行后端、前端和 UI 相关验证。
