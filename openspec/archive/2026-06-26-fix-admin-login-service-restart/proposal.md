## Why

`BUG-0005-login-fails-after-service-restart` 已评审通过并纳入 `sprint-002`。当前本地或 Docker 服务重启后，用户进入 `/admin/login` 并使用其认为正确的管理员账号密码，仍可能收到「账号或密码错误」。

根因是默认管理员初始化逻辑只在 `admin` 不存在时创建用户。若持久化 SQLite 数据库中已存在 `admin`，服务重启不会校验或恢复该用户的密码哈希；同时根目录 `.env.example` 未明确 `ADMIN_INITIAL_PASSWORD`，容易让操作者误以为当前环境中的默认密码会在重启后自动生效。

## What Changes

- 明确并修复默认管理员初始化/恢复策略：
  - 空数据库首次启动时，配置 `ADMIN_INITIAL_PASSWORD` 后默认 `admin` MUST 可登录。
  - 已存在 `admin` 时，服务重启 MUST NOT 破坏既有密码。
  - 若需要恢复默认管理员密码，MUST 使用显式、可审计的触发策略，避免每次启动覆盖真实管理员密码。
- 补齐环境变量与部署/数据库说明：
  - 根目录 `.env.example` MUST 说明 `ADMIN_USERNAME` 与 `ADMIN_INITIAL_PASSWORD`。
  - 部署文档 MUST 说明持久化 SQLite 下重启不会自动覆盖已有 admin 密码，除非启用显式恢复策略。
- 补充后端认证回归测试，覆盖首次创建、重启保持、显式恢复和未触发恢复场景。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端 | 默认管理员 seed / 恢复策略 |
| API | 登录接口响应结构与错误码不应变化 |
| 数据库 | 不新增表；可能更新已有 `admin.password_hash`，但仅在显式恢复策略触发时 |
| 环境变量 | 需补齐根目录 `.env.example` 的管理员初始化变量说明 |
| Docker Compose | 文档需说明持久化 SQLite 与管理员密码恢复行为；应用内部端口不变 |
| Web 管理端 | 登录链路恢复；页面交互不变 |
| 小程序 / 店主端 | 不涉及 |
| Orval | 不需要，除非实现阶段意外改变 API schema |
| 测试 | 需补充后端 pytest 认证/seed 回归 |

## Rollback Plan

如修复导致启动初始化异常或误覆盖管理员密码：

1. 回滚本 change 涉及的默认管理员 seed / 恢复逻辑。
2. 保留 `users` 表和认证接口现有结构，不回滚已存在业务数据。
3. 移除或禁用新增的显式恢复触发环境变量。
4. 恢复文档中对应的恢复策略说明。
5. 将 `BUG-0005` 标记为未修复，并保留回归失败记录。
