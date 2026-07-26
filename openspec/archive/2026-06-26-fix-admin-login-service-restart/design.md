## Context

`BUG-0005-login-fails-after-service-restart` 描述了管理端登录恢复路径缺陷：服务重启后，使用正确管理员账号密码仍提示「账号或密码错误」。

| 项目 | 内容 |
|---|---|
| 父需求 | `REQ-0001-user-login` |
| 目标接口 | `POST /api/v1/auth/login` |
| 目标数据 | `users.username = admin`、`users.password_hash` |
| 关键配置 | `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD` |
| 运行环境 | local / Docker Compose |
| 主要风险 | 持久化 SQLite 中已有 admin 与当前环境初始密码不一致 |

## Root Cause Summary

### RC-001：默认管理员 seed 是 create-only

启动流程执行 `seed_admin_user(session)`，但当数据库中已存在 `admin` 时直接返回，不校验当前环境密码，也不提供恢复路径。

### RC-002：持久化 SQLite 保留历史密码哈希

Docker Compose 将 `./data/sqlite` 挂载为持久化数据。重启服务不会清空 `users` 表，也不会重新创建默认管理员。

### RC-003：环境变量事实源不一致

根目录 `.env.example` 是 Docker Compose 运行入口的示例文件，但当前未明确 `ADMIN_INITIAL_PASSWORD`；`src/backend/.env.example` 则存在该变量，容易造成操作者认知偏差。

## Decisions

### D1：默认策略为不静默覆盖

系统 MUST NOT 在每次启动时静默覆盖已有 `admin` 的密码哈希。该规则保护真实管理员账号，避免部署重启导致密码被意外重置。

### D2：恢复策略必须显式触发

若实现默认管理员密码恢复，MUST 使用显式环境变量或一次性管理流程触发。建议实现阶段采用类似以下语义：

```text
ADMIN_RESET_PASSWORD_ON_STARTUP=true
```

该触发只用于本地开发/演示或受控运维场景，且必须在文档中标注风险。

### D3：登录接口错误语义不变

`POST /api/v1/auth/login` 对错误账号或密码仍返回统一凭证错误，不得暴露账号存在性。修复只改善初始化/恢复路径和排障信息，不改变登录 API schema。

### D4：文档与环境变量同步

根目录 `.env.example`、部署文档和数据库说明 MUST 明确：

- `ADMIN_INITIAL_PASSWORD` 仅用于首次创建或显式恢复策略。
- 持久化 SQLite 下，已有 `admin` 不会因重启自动使用新的初始密码。
- 若需恢复密码，应使用受控流程而非直接删除运行时数据库。

## Test Strategy

| 层级 | 验证 |
|---|---|
| Backend pytest | 空数据库 + `ADMIN_INITIAL_PASSWORD` 创建 admin 后可登录 |
| Backend pytest | 已存在 admin 时重启/重复 seed 不破坏既有密码 |
| Backend pytest | 显式恢复触发后 admin 可用新密码登录，旧密码失效 |
| Backend pytest | 未触发恢复时，改变 `ADMIN_INITIAL_PASSWORD` 不覆盖已有密码 |
| API regression | 账号或密码错误仍返回统一错误码与消息 |
| Docs check | `.env.example`、部署和 DB 文档说明一致 |

## Risks

| 风险 | 影响 | 缓解 |
|---|---|---|
| 恢复策略误覆盖真实密码 | 管理员无法使用原密码登录 | 默认不覆盖；必须显式触发 |
| 日志泄露恢复密码 | 安全事故 | 禁止日志/API 响应输出明文密码 |
| 测试依赖全局 settings 缓存 | pytest 不稳定 | 测试中重置 settings 与 DB engine |
| 文档未同步 | 操作者继续误判默认密码 | 将 `.env.example`、部署和 DB 文档纳入 tasks |

## Out of Scope

- 不新增忘记密码页面。
- 不新增自助密码重置 API。
- 不改变 JWT 签发、`remember_me` 或前端登录表单行为。
- 不改变 `users` 表结构，除非实现阶段发现现有字段无法承载审计要求并另行说明。
