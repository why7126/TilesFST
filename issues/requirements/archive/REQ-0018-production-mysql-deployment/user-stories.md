---
title: 用户故事
purpose: REQ-0018 生产环境部署与 MySQL 数据库支持
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 20:24:46
updated_at: 2026-06-28 20:24:46
note: REQ-0018-production-mysql-deployment
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---|---|
| US-001 | 运维 / 部署人员 | P0 | 是 |
| US-002 | 平台后端开发 | P0 | 是 |
| US-003 | 管理端管理员 | P0 | 是（间接受益） |
| US-004 | 发布负责人 | P1 | 是 |

---

## US-001 在 VPS 上用 Compose 部署生产环境

**作为** 运维人员，  
**我希望** 在 VPS 上通过 Docker Compose 启动 backend、web、MinIO，并连接客户已有的 MySQL 8.0+ 实例，  
**以便** 在不内嵌数据库服务的情况下完成生产上线。

### 验收要点

- 存在生产 Compose 文件与分步部署文档（含外部 MySQL 连接、防火墙、密钥注入）。
- Compose **不含** mysql 服务；backend 通过 `DATABASE_URL` 连接客户实例。
- 生产 env 不使用 `.env.example` 默认密钥。
- 重启容器后 MySQL 与 MinIO 数据持久。

### 关联功能

- FR-001、FR-006、FR-007、FR-008

---

## US-002 本地开发继续使用 SQLite

**作为** 平台后端开发，  
**我希望** 本地与 Docker 演示环境默认仍使用 SQLite，无需安装 MySQL，  
**以便** 日常开发与现有 pytest 流程不被生产化改造阻断。

### 验收要点

- `./scripts/docker-up.sh` 行为与变更前一致（SQLite 文件卷 + MinIO）。
- `APP_ENV` 非 production 时默认 SQLite；`cd src/backend && pytest` 全绿。
- MySQL 路径有独立集成测试或 CI job，与 SQLite 测试分离。

### 关联功能

- FR-001、FR-003、FR-009

---

## US-003 生产空库首次启动可登录管理端

**作为** 管理端管理员，  
**我希望** 生产环境首次部署后能用配置的默认管理员账号登录并维护业务，  
**以便** 平台可立即投入使用（无需手工导入 SQLite 数据）。

### 验收要点

- 空 MySQL 库首次启动：自动建表 + 创建 `ADMIN_USERNAME` 账号（bcrypt）。
- 登录 API 与管理端 Web 登录页可用。
- 至少完成一次品牌 Logo 或 Banner 图片上传并在页面回显。

### 关联功能

- FR-004、FR-005、FR-008

---

## US-004 生产数据库配置可审计、可 fail-fast

**作为** 发布负责人，  
**我希望** 生产环境在数据库配置错误或不可达时快速失败并给出清晰日志，且文档说明 MySQL 前置条件，  
**以便** 减少上线当晚的隐性故障与回滚成本。

### 验收要点

- `APP_ENV=production` 且缺少/无效 `DATABASE_URL` 时 backend 启动失败，日志可定位。
- 文档含 MySQL 8.0+、`utf8mb4_unicode_ci`、DDL/DML 权限、网络可达检查清单。
- 日志不输出 MySQL 密码或 `ADMIN_INITIAL_PASSWORD` 明文。

### 关联功能

- FR-002、FR-007、FR-010
