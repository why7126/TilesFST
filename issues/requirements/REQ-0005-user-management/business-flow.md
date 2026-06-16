---
title: 业务流程
purpose: 描述管理后台用户管理的访问控制、列表操作与弹窗主流程
content: 基于 requirement.md 与 prototype/web/user-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005 管理后台用户管理
---

# 业务流程

## 1. 流程总览

```text
后台管理员登录（role=admin）
  ↓
进入 /admin/users
  ↓
浏览 / 搜索 / 筛选用户列表
  ↓
可选操作：
  ├─ 添加用户 → 弹窗 → 创建 → Toast + 展示初始密码（若后端返回）
  ├─ 编辑用户 → 弹窗 → 保存 → Toast
  ├─ 重置密码 → 确认 → 展示一次性随机密码
  ├─ 冻结 / 解冻 → 确认 → Toast
  └─ 删除（仅从未登录）→ 确认 → 软删除 → Toast
```

## 2. 访问与权限流程

```text
用户携带 JWT 访问 /admin/users
  ↓
ProtectedRoute：已登录？
  ├─ 否 → /admin/login
  └─ 是 → role === admin？
        ├─ 否 → 403 或重定向 /admin/dashboard
        └─ 是 → 渲染 UserManagementPage
```

### 2.1 角色与菜单

| 产品角色 | 后端 role（建议映射） | 后台入口 | 用户管理菜单 |
|---|---|---|---|
| 后台管理员 | `admin` | 允许 | 可见 |
| 后台运营 | `employee` | 允许 | 不可见 |
| 前台用户 | `store_owner` | 拒绝 | 不可见 |

## 3. 列表查询流程

```text
页面加载
  ↓
GET /api/v1/admin/users?page=1&page_size=10&...
  ↓
并行或内嵌返回 summary（总数、筛选数、正常、已冻结）
  ↓
渲染筛选区 + 指标卡 + 表格 + 分页
```

### 3.1 搜索与重置

```text
用户输入关键词 / 选择筛选项
  ↓
点击「搜索」或回车
  ↓
page 重置为 1，带 query 重新请求
  ↓
点击「重置」→ 清空条件 → 重新请求默认列表
```

## 4. 添加用户流程

```text
点击「添加用户」
  ↓
打开弹窗（字段顺序：用户名 → 头像 → 昵称 → 角色）
  ↓
填写并提交 POST /api/v1/admin/users（用户名须满足 4–32 位及格式规则，见 requirement.md §7.2）
  ↓
成功：
  ├─ Toast「用户已创建」
  ├─ 关闭弹窗，刷新列表
  └─ 若响应含 initial_password → 展示一次性密码弹窗
失败：表单/接口错误提示（用户名重复、格式不合法等）
```

## 5. 编辑用户流程

```text
列表点击「编辑」
  ↓
打开弹窗，用户名只读
  ↓
PATCH /api/v1/admin/users/{id}
  ↓
成功 → Toast「用户信息已更新」→ 刷新列表
```

## 6. 重置密码流程

```text
点击「重置密码」
  ↓
确认对话框
  ↓
POST /api/v1/admin/users/{id}/reset-password
  ↓
成功 → 二次弹窗展示随机密码 + 复制按钮
  ↓
关闭后不可再次查看同一密码
```

## 7. 冻结 / 解冻流程

```text
点击「冻结」或「解冻」
  ↓
（可选）确认
  ↓
PATCH status: disabled | active
  ↓
成功 → Toast → 刷新列表
  ↓
已冻结用户登录前台/后台 → 403 AUTH_USER_DISABLED
```

## 8. 删除流程

```text
点击「删除」
  ↓
若 last_login_at 非空 → 按钮置灰，不可操作
  ↓
若从未登录 → 确认 → DELETE（软删除，status=deleted）
  ↓
成功 → Toast → 列表可按「已删除」筛选查看
```

## 9. 与现有能力的衔接

| 依赖 | 说明 |
|---|---|
| REQ-0001 / REQ-0004 | 管理端登录、`AdminLayout`、Sidebar 264px、CSS Port 风格 |
| `openspec/specs/auth/spec.md` | JWT、`/auth/me`、角色校验需扩展为「仅 admin 可管用户」 |
| MinIO | 头像上传走后端授权，object_key 存 `users` 表 |

## 10. 异常流程

| 场景 | 期望行为 |
|---|---|
| 非 admin 访问 API | HTTP 403 |
| 创建重复用户名 | HTTP 409，前端提示 |
| 删除已登录用户 | 前端禁用 + 后端拒绝 |
| 上传头像失败 | 保留原头像，提示错误 |
| 网络错误 | Toast 或内联错误，不丢筛选条件 |
