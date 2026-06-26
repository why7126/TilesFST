---
bug_id: BUG-0005-login-fails-after-service-restart
status: in_sprint
updated_at: 2026-06-26 20:49:27
---

# 回归验收标准

## AC-001 首次启动空数据库时默认管理员可登录

**Given** 本地或 Docker 环境使用空的 SQLite 数据库  
**And** 已在实际启动环境中配置 `ADMIN_INITIAL_PASSWORD`  
**When** 启动后端服务并访问 `/admin/login`  
**Then** 使用 `admin` 与配置的初始密码 MUST 登录成功。  
**And** 登录成功后 MUST 进入管理端首页或受保护管理端页面。

## AC-002 服务重启后已有管理员账号仍可按既有密码登录

**Given** `users` 表中已存在 `username = 'admin'` 的启用账号  
**And** 该账号已有可用密码  
**When** 重启本地或 Docker 服务  
**Then** 使用该账号的既有正确密码 MUST 仍可登录。  
**And** 重启流程 MUST NOT 生成无法匹配的 admin 密码状态。

## AC-003 已存在 admin 且初始密码变化时必须有明确策略

**Given** 持久化数据库中已存在 `admin` 用户  
**And** 环境变量中的 `ADMIN_INITIAL_PASSWORD` 与该用户当前密码不一致  
**When** 服务启动  
**Then** 系统 MUST 采用明确、可审计的策略处理。  
**And** 不得静默让用户误以为新的初始密码已生效。  
**And** 若不自动重置密码，系统 SHOULD 输出明确启动日志或文档提示。

## AC-004 密码恢复不得绕过安全边界

**Given** 需要恢复默认管理员访问能力  
**When** 执行修复方案提供的重置或恢复流程  
**Then** 密码 MUST 以哈希形式存储。  
**And** 不得在代码、日志或响应中泄露真实密钥、明文密码或数据库绝对路径。  
**And** 不得放宽管理端鉴权或允许未授权用户重置管理员密码。

## AC-005 Docker Compose 环境变量说明必须一致

**Given** 使用 Docker Compose 本地开发或演示部署  
**When** 查看根目录 `.env.example` 与部署文档  
**Then** MUST 能看到 `ADMIN_USERNAME` 与 `ADMIN_INITIAL_PASSWORD` 的用途说明。  
**And** 示例环境变量 MUST 与 `docker-compose.yml` 实际读取的根目录 `.env` 保持一致。  
**And** 文档 MUST 明确持久化 SQLite 数据库重启后不会自动覆盖已有 admin 密码，除非启用显式恢复策略。

## AC-006 错误提示保持一致但排障信息可定位

**Given** 用户输入错误账号或密码  
**When** 调用 `POST /api/v1/auth/login`  
**Then** 接口仍 MUST 返回统一凭证错误，避免暴露账号存在性。  
**And** 管理端仍 MUST 展示「账号或密码错误」。  
**And** 服务端排障日志或文档 SHOULD 能区分“凭证错误”和“默认管理员初始化/恢复未生效”的运维场景。

## AC-007 必须补充回归测试

**Given** 缺陷进入修复阶段  
**When** 完成 `fix-*` OpenSpec Change  
**Then** 后端测试 MUST 覆盖首次启动空数据库创建默认 admin 并可登录。  
**And** 后端测试 MUST 覆盖已有 admin 时重启不破坏既有密码。  
**And** 若新增显式密码恢复策略，测试 MUST 覆盖恢复触发条件、未触发时不覆盖密码、恢复后可登录。

## AC-008 不得破坏既有认证能力

**Given** 修复完成  
**When** 执行认证回归  
**Then** `POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`POST /api/v1/auth/logout` MUST 保持既有响应结构和错误码。  
**And** `admin`、`employee`、`store_owner` 的管理端权限边界 MUST 保持不变。  
**And** 已禁用用户仍 MUST 被拒绝登录。
