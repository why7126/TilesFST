---
bug_id: BUG-0005-login-fails-after-service-restart
status: in_sprint
updated_at: 2026-06-26 20:49:27
root_cause_type: seed-data/runtime-db/environment
---

# 根因分析

## 1. 直接原因

服务启动时会执行 `seed_admin_user(session)` 初始化默认管理员，但该逻辑只在 `users` 表中不存在 `username = 'admin'` 时创建用户。

如果本地或 Docker 持久化 SQLite 数据库中已经存在 `admin` 用户，启动流程会直接返回，不会校验、修复或重置该用户的 `password_hash`。因此，当用户按当前环境认为“正确”的默认密码登录，而数据库中保留的是另一份历史密码哈希时，登录接口会按普通凭证错误返回 `账号或密码错误`。

## 2. 根本原因

### 2.1 默认管理员初始化是 create-only，不具备重启一致性校验

当前初始化策略可以保证“首次启动时创建 admin”，但不能保证“服务重启后 admin 与当前环境声明的初始密码仍一致”。

关键代码路径：

| 层级 | 证据 |
|---|---|
| 启动流程 | `src/backend/app/main.py` 的 startup 中执行 `init_database()` 与 `seed_admin_user(session)` |
| 种子逻辑 | `src/backend/app/db/seed.py` 检测到 `admin` 已存在后直接 `return False` |
| 登录校验 | `src/backend/app/services/auth_service.py` 通过 `verify_password(password, user.password_hash)` 校验数据库哈希 |
| 密码哈希 | `src/backend/app/core/security.py` 使用 bcrypt，每次哈希带盐，不应通过字符串比对推断明文 |

### 2.2 运行时数据库是持久化的，重启不会清空历史用户数据

Docker Compose 将宿主机 `./data/sqlite` 挂载到容器内 `/app/data/sqlite`。这意味着容器或服务重启后，SQLite 数据库会继续保留已有 `users` 表数据，包括历史 `admin.password_hash`。

因此，“重启服务”不是“重新初始化默认账号密码”。如果用户曾经使用不同的 `ADMIN_INITIAL_PASSWORD` 首次启动，或数据库来自旧环境，后续重启即使调整环境变量，也不会自动更新已有 admin 密码。

### 2.3 环境变量说明存在不一致，增加误判概率

根目录 `.env.example` 当前未展示 `ADMIN_INITIAL_PASSWORD`，而 `src/backend/.env.example` 展示了该变量。Docker Compose 实际读取根目录 `.env`，不是 `src/backend/.env.example`。

这会让操作者容易误以为默认管理员密码由文档或代码内默认值稳定提供，但实际是否创建默认 admin、创建时使用哪个密码，取决于首次启动时根目录 `.env` 中是否配置 `ADMIN_INITIAL_PASSWORD`。

## 3. 触发条件

满足以下条件时容易触发：

1. 本地或 Docker 环境使用持久化 SQLite 数据库。
2. `users` 表中已经存在 `username = 'admin'`。
3. 该用户的 `password_hash` 与当前操作者输入的默认密码不匹配。
4. 服务重启后，启动流程跳过已有 admin 的密码更新。
5. 用户在 `/admin/login` 输入 `admin` 和当前认为正确的密码。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | seed-data / runtime-db / environment |
| 是否接口缺陷 | 否；登录接口按现有哈希校验返回 401 符合当前实现 |
| 是否数据库缺陷 | 是；运行时数据与环境声明的初始密码之间缺少一致性治理 |
| 是否 Docker 缺陷 | 部分相关；Docker 持久化数据卷保留旧密码哈希，符合配置但缺少运维提示 |
| 是否权限缺陷 | 否；未发现绕过鉴权或权限放宽 |
| 是否前端缺陷 | 否；前端展示后端返回的统一凭证错误提示 |
| 主要修复面 | 默认管理员初始化策略、环境变量说明、重启/持久化数据库下的账号恢复流程 |

## 5. 后续修复建议

1. 明确默认管理员初始化策略：仅首次创建、允许显式重置，或在开发环境按配置同步重置。
2. 若支持重置，必须通过显式环境变量或一次性管理脚本触发，避免每次启动覆盖真实管理员密码。
3. 根目录 `.env.example` MUST 补充 `ADMIN_USERNAME` 与 `ADMIN_INITIAL_PASSWORD` 说明，并与 Docker Compose 实际读取路径一致。
4. 为服务重启场景补充测试：已有 admin 且哈希不匹配时，应有可预期的恢复路径或明确日志提示。
5. 文档中明确：Docker/本地 SQLite 持久化后，重启不会自动把已有 admin 密码恢复成新的初始密码。
