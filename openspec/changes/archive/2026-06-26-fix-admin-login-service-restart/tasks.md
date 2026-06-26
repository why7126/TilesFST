## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0005-login-fails-after-service-restart` 的 `bug.md`、`root-cause.md`、`acceptance.md`、`review.md`
- [x] 1.2 确认 BUG 状态为 `in_sprint` 或 `approved`
- [x] 1.3 确认本 change 默认不改变登录 API 响应 schema
- [x] 1.4 梳理现有 `seed_admin_user`、`AuthService.login`、SQLite 路径与 Docker Compose 数据卷行为

## 2. 后端初始化与恢复策略

- [x] 2.1 保持空数据库首次启动时通过 `ADMIN_INITIAL_PASSWORD` 创建默认 admin
- [x] 2.2 已存在 admin 时，重复启动或重复 seed MUST NOT 静默覆盖既有密码
- [x] 2.3 增加显式、可审计的默认管理员密码恢复策略
- [x] 2.4 恢复策略触发后，必须使用 bcrypt 哈希更新密码，不写入明文
- [x] 2.5 恢复策略不得放宽管理端权限，不得绕过登录鉴权
- [x] 2.6 排障日志可说明恢复策略是否触发，但 MUST NOT 输出明文密码、密钥或数据库绝对路径

## 3. 环境变量与文档

- [x] 3.1 根目录 `.env.example` 增加 `ADMIN_USERNAME`、`ADMIN_INITIAL_PASSWORD` 和恢复策略变量说明
- [x] 3.2 `docs/02-deployment.md` 说明 Docker Compose 持久化 SQLite 下的默认管理员密码行为
- [x] 3.3 `docs/04-database-design.md` 说明 `users.password_hash` 与默认管理员 seed / 恢复规则
- [x] 3.4 如涉及后端环境示例，保持 `src/backend/.env.example` 与根目录 `.env.example` 语义一致
- [x] 3.5 若未改变 API schema，明确记录不需要 Orval

## 4. 测试

- [x] 4.1 pytest：空数据库 + `ADMIN_INITIAL_PASSWORD` 创建 admin 后可登录
- [x] 4.2 pytest：已有 admin 时重复 seed / 模拟重启不破坏既有密码
- [x] 4.3 pytest：改变 `ADMIN_INITIAL_PASSWORD` 但未触发恢复时，不覆盖已有 admin 密码
- [x] 4.4 pytest：显式恢复触发后，新密码可登录，旧密码不可登录
- [x] 4.5 pytest：错误账号或密码仍返回统一凭证错误，不暴露账号存在性
- [x] 4.6 回归 `tests/test_auth.py` 及必要的管理端权限测试

## 5. 验收与追溯

- [x] 5.1 更新本 change `trace.md` checklist
- [x] 5.2 更新 `BUG-0005-login-fails-after-service-restart/trace.md` 中 change 状态
- [x] 5.3 同步 `iterations/sprint-002` 中 BUG-0005 对应 Change 状态
- [x] 5.4 评估是否需要更新 `docs/knowledge-base/incidents/`；如不需要，在 trace 中说明原因
