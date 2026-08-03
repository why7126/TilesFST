---
requirement_id: REQ-0093-standardize-deployment-environment-matrix
title: 标准化部署环境矩阵与 deploy 目录治理
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-03 13:39:30
updated_at: 2026-08-03 20:47:04
---

# REQ-0093 标准化部署环境矩阵与 deploy 目录治理

## 1. 需求背景

项目当前已通过根目录 `docker-compose.yml`、`docker-compose.prod.yml`、`docker-compose.prod.external.yml`、`.env.example` 以及 `scripts/docker-up.sh` / `scripts/docker-down.sh` 支持本地开发、演示与生产部署。随着部署组合增加，SQLite / MySQL、自建 MinIO / 外部 MinIO / 腾讯云 COS、本地 / 生产之间的配置差异已经超出单一 `.env.example` 与一段部署文档可清晰表达的范围。

当前主要问题不是缺少 Docker Compose，而是缺少稳定的部署环境矩阵：每种环境没有统一 ID、env 示例、Compose 入口、前置条件、校验规则和安全边界说明。继续把所有组合挤在根目录 `.env.example` 与 `docs/02-deployment.md` 中，会增加误用生产配置、误启本地 MinIO、生产回退 SQLite、云对象存储自动建桶或脚本参数漂移的风险。

本需求用于定义一个可治理的 `deploy/` 部署目录：按本地与生产分层管理 env 示例、环境化 Compose 和部署脚本，同时保留必要的根目录兼容入口，避免破坏现有开发习惯、发布镜像治理和 Docker Compose 默认工作流。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 本地开发者 | 能快速选择 SQLite/MySQL 与 MinIO/COS 组合，并用稳定命令启动或停止环境。 |
| 测试 / 验收 | 能按环境 ID 复现指定部署组合，确认接口、数据库和对象存储配置一致。 |
| 实施 / 运维 | 能区分本地示例、生产示例和真实私有配置，避免把示例密钥或 SQLite 配置带入生产。 |
| 发布负责人 | 能知道部署相关文件是否影响镜像构建计划、manifest 和发布门禁。 |
| AI Agent | 能按目录规范创建、校验和引用部署资产，不再随意新增顶层目录或复制多套脚本。 |
| 评审者 | 能通过需求、OpenSpec、目录规范和部署文档审查 `deploy/` 的边界与兼容策略。 |

## 3. 范围

### 3.1 本期包含

- 正式定义一级 `deploy/` 目录的职责与目录结构。
- 定义 `deploy/local/` 与 `deploy/prod/` 两个二级目录，分别承载本地和生产部署资产。
- 定义部署环境 ID 与环境矩阵，覆盖 SQLite/MySQL、自建 MinIO、外部 MinIO、腾讯云 COS 等组合。
- 定义“一拓扑一 Compose + 一环境一 env 示例”的原则。
- 定义 `deploy/local/compose.yml` 与生产 Compose 文件的放置策略。
- 定义 `deploy/scripts/up.sh`、`deploy/scripts/down.sh`、`deploy/scripts/validate-env.py` 的职责。
- 保留 `scripts/docker-up.sh` 与 `scripts/docker-down.sh` 作为兼容 wrapper，内部转调新部署脚本。
- 明确根目录 Compose 的兼容策略，避免破坏默认 `docker compose up` 或既有文档入口。
- 更新目录结构规范、AGENTS、部署文档、环境变量说明和相关校验脚本。
- 定义部署校验门禁，阻止生产 SQLite、示例密钥、COS 自动建桶、本地 MinIO profile 误启等高风险配置。

### 3.2 本期不包含

- 不在 PRD 阶段直接创建 `deploy/` 或迁移文件。
- 不实现 CI/CD 自动部署流水线。
- 不引入 Kubernetes、Helm、Terraform、Ansible 或云平台托管部署。
- 不自动创建、管理或销毁生产 MySQL、腾讯云 COS bucket、云密钥或安全组。
- 不把真实 `.env`、生产私有域名、数据库连接串、对象存储密钥或客户数据写入仓库。
- 不改变后端对象存储单 Bucket + 前缀策略。
- 不要求每个环境复制一份完整 Docker Compose。
- 不直接修改后端、Web、小程序业务代码。

## 4. 功能要求

### FR-001 新增 `deploy/` 目录治理

系统 MUST 通过 OpenSpec Change 正式引入一级 `deploy/` 目录。

`deploy/` SHOULD 采用以下结构：

```text
deploy/
├── README.md
├── local/
│   ├── README.md
│   ├── compose.yml
│   ├── sqlite-minio-managed.env.example
│   ├── sqlite-minio-external.env.example
│   ├── sqlite-tencent-cos.env.example
│   ├── mysql-minio-managed.env.example
│   ├── mysql-minio-external.env.example
│   └── mysql-tencent-cos.env.example
├── prod/
│   ├── README.md
│   ├── compose.tencent-cos.yml
│   └── mysql-tencent-cos.env.example
└── scripts/
    ├── up.sh
    ├── down.sh
    └── validate-env.py
```

如需保留生产自建 MinIO 部署，`deploy/prod/` MAY 增加：

```text
compose.self-hosted-minio.yml
mysql-minio-managed.env.example
```

### FR-002 部署环境矩阵

系统 MUST 定义稳定的部署环境 ID。

本地环境 SHOULD 至少包含：

| 环境 ID | 数据库 | 对象存储 | 说明 |
|---|---|---|---|
| `local-sqlite-minio-managed` | SQLite | 项目 Compose 自建 MinIO | 默认本地开发与 demo。 |
| `local-sqlite-minio-external` | SQLite | 本机已有 Docker MinIO / 外部 MinIO | 不启动项目内 MinIO。 |
| `local-sqlite-tencent-cos` | SQLite | 腾讯云 COS | 本地后端直连云对象存储。 |
| `local-mysql-minio-managed` | 外部 MySQL | 项目 Compose 自建 MinIO | 本地验证 MySQL 兼容性。 |
| `local-mysql-minio-external` | 外部 MySQL | 本机已有 Docker MinIO / 外部 MinIO | 使用项目外部数据库和对象存储。 |
| `local-mysql-tencent-cos` | 外部 MySQL | 腾讯云 COS | 本地近生产链路验证。 |

生产环境 SHOULD 至少包含：

| 环境 ID | 数据库 | 对象存储 | 说明 |
|---|---|---|---|
| `prod-mysql-tencent-cos` | 外部 MySQL | 腾讯云 COS | 当前目标生产环境。 |

每个环境 ID MUST 对应一个 `.env.example`，并声明 Compose 文件、是否启用 profile、必填变量、安全边界和启动命令。

### FR-003 Compose 拆分原则

系统 MUST 遵守“一拓扑一 Compose + 一环境一 env 示例”原则。

环境变量差异 SHOULD 通过不同 `.env.example` 表达；服务拓扑差异 SHOULD 通过不同 Compose 或 profile 表达。不得为每个部署环境复制一份几乎相同的 Compose。

本地 6 种环境 SHOULD 复用 `deploy/local/compose.yml`，通过 `DATABASE_URL`、`OBJECT_STORAGE_PROVIDER`、`OBJECT_STORAGE_ENDPOINT`、`OBJECT_STORAGE_*` 和 `self-hosted-storage` profile 区分组合。

生产 `prod-mysql-tencent-cos` SHOULD 使用 `deploy/prod/compose.tencent-cos.yml`。若保留生产自建 MinIO，则 SHOULD 使用独立 `deploy/prod/compose.self-hosted-minio.yml`，因为该拓扑包含 MinIO 与初始化服务。

### FR-004 根目录 Compose 兼容策略

系统 SHOULD 保留根目录默认 Compose 入口，避免破坏 `docker compose up` 的开箱即用体验。

允许以下任一兼容方式：

- 保留根目录 `docker-compose.yml` 作为本地默认开发入口。
- 或新增 / 保留根目录 `compose.yaml` 作为薄入口，明确引用或等价于默认本地部署。

若将生产 Compose 从根目录迁移到 `deploy/prod/`，系统 MUST 同步更新所有引用，包括部署文档、发布镜像构建计划、image manifest 输入 hash、脚本、规则和 README。

### FR-005 环境化 env 示例

系统 MUST 为每个环境提供独立 `.env.example`。

每个 env 示例 MUST：

- 使用示例值，不包含真实密钥、真实生产域名、真实数据库连接串或客户数据。
- 在每个变量上一行保留用途、取值范围或安全边界注释。
- 明确是否允许 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=true`。
- 明确 `APP_ENV`、`APP_DEBUG`、`DATABASE_URL` 和对象存储 provider。
- 明确该文件是否只用于本地、生产或受控验证。
- 说明复制为真实本地 env 的目标路径和命令入口。

生产 env 示例 MUST 要求：

- `APP_ENV=production`。
- `APP_DEBUG=false`。
- `DATABASE_URL` 为 MySQL 8.0+。
- `OBJECT_STORAGE_PROVIDER=tencent-cos`。
- `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。
- 密钥与管理员初始密码不得使用示例默认值。

### FR-006 部署脚本迁移与兼容

系统 SHOULD 将核心部署逻辑迁移到 `deploy/scripts/`。

`deploy/scripts/up.sh` SHOULD 支持：

```bash
./deploy/scripts/up.sh local sqlite-minio-managed
./deploy/scripts/up.sh local mysql-tencent-cos
./deploy/scripts/up.sh prod mysql-tencent-cos
```

`deploy/scripts/down.sh` SHOULD 支持：

```bash
./deploy/scripts/down.sh local
./deploy/scripts/down.sh prod
```

`scripts/docker-up.sh` 与 `scripts/docker-down.sh` SHOULD 保留为兼容 wrapper，默认转调本地默认环境，例如 `local sqlite-minio-managed`。兼容 wrapper MUST 避免重复维护复杂部署逻辑。

### FR-007 部署配置校验

系统 SHOULD 提供 `deploy/scripts/validate-env.py` 或等价校验入口。

校验 MUST 覆盖：

- 生产环境不得使用 SQLite。
- 生产环境不得开启 `APP_DEBUG=true`。
- 生产环境不得使用示例 `APP_SECRET_KEY`、对象存储密钥或管理员初始密码。
- 腾讯云 COS / 外部对象存储生产环境必须 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。
- 外部对象存储场景不得启用本地 MinIO profile。
- 项目自建 MinIO 场景必须启用对应 profile 或 Compose 服务。
- `OBJECT_STORAGE_BUCKET`、region、endpoint、path-style、secure 等 provider 关键字段必须满足环境要求。
- `.env.example` 与 Compose 引用变量必须保持同步。

校验输出 MUST 保持摘要化，不输出真实 `.env` 内容、密钥、数据库连接串、Authorization header 或 Cookie。

### FR-008 文档与规则同步

引入 `deploy/` 时 MUST 同步更新：

- `rules/directory-structure.md`：新增 `deploy/` 顶层目录职责与边界。
- `AGENTS.md`：新增部署任务读取和目录边界摘要。
- `docs/02-deployment.md`：新增部署矩阵、命令入口、env 示例路径、Compose 选择规则。
- `rules/environment.md`：补充 `deploy/**/*.env.example` 注释与真实 env 禁止提交边界。
- `rules/release.md` 与镜像构建相关文档：说明部署 Compose 迁移对 image plan / manifest 输入 hash 的影响。
- `scripts/validate-directory-structure.py`：允许并校验 `deploy/` 的合法子目录。

### FR-009 发布镜像治理兼容

部署目录调整 MUST 与 REQ-0081 发布镜像准备与构建治理兼容。

当 Compose 文件从根目录迁移或新增到 `deploy/` 后：

- `/image-prepare` MUST 将新的 Compose 路径纳入输入文件清单。
- `/image-build` manifest MUST 记录实际使用的 Compose 文件和 hash。
- `/release-publish` MUST 能识别 Compose 输入漂移。
- 旧路径引用必须更新或保留兼容说明。

### FR-010 安全与数据边界

`deploy/` MUST NOT 存放：

- 真实 `.env`。
- 真实密钥、数据库连接串、对象存储凭据、Authorization header、Cookie。
- 真实客户数据。
- 运行时数据库文件、MinIO 对象数据或镜像 tar 包。
- 不可公开的生产私有域名或内部运维凭据。

如需记录生产私有配置，MUST 只记录占位符、变量名、注释和安全边界，不记录真实值。

## 5. UI / UE 约束

本需求不新增 Web 管理端、店主 Web 或微信小程序 UI。

命令行体验 SHOULD 清晰可预期：

- 用户能通过环境 ID 选择部署组合。
- 命令输出展示 Web、Backend、MinIO Console 或对象存储类型。
- 校验失败时展示 blocker、涉及变量名和修复建议。
- 成功输出不展示真实配置值。

文档体验 SHOULD 支持两种阅读路径：

- “我要本地跑起来”：进入 `deploy/local/README.md`。
- “我要生产部署”：进入 `deploy/prod/README.md`。

## 6. 非功能约束

| 项 | 要求 |
|---|---|
| 安全 | env 示例、校验输出、部署文档不得泄露密钥、真实连接串、真实客户数据或私有运维地址。 |
| 可维护 | Compose 按拓扑拆分，env 按环境拆分，避免一环境一 Compose 的重复维护。 |
| 兼容性 | 保留根目录默认入口或 wrapper，降低现有开发命令、文档和发布脚本的迁移风险。 |
| 可验证 | 提供环境校验脚本，能在启动前发现生产 SQLite、示例密钥、对象存储 profile 错配等问题。 |
| 可追踪 | 部署文件变化必须进入发布镜像计划和 manifest 的输入 hash。 |
| 可扩展 | 后续新增 staging、测试 COS、生产自建 MinIO 或外部 S3 兼容存储时，应扩展 env 示例和矩阵，而非复制全套脚本。 |

## 7. 关联需求与规范

| 关联项 | 关系 |
|---|---|
| REQ-0081-release-image-build-governance | 部署 Compose 路径、脚本和 env 示例变化会影响镜像构建计划与 manifest 输入。 |
| `standardize-deployment-environment-matrix` | 本需求对应的 OpenSpec Change，用于实现部署环境矩阵与 deploy 目录治理。 |
| `rules/directory-structure.md` | 新增一级 `deploy/` 必须先更新目录结构规范。 |
| `rules/environment.md` | env 示例、真实 env 禁止提交、变量注释和安全边界需遵守。 |
| `rules/release.md` | 部署变更可能触发镜像准备、构建和发布门禁。 |
| `docs/02-deployment.md` | 需要同步部署矩阵、命令入口和 Compose 选择方式。 |
| `docs/07-object-storage-strategy.md` | 对象存储仍遵守单 Bucket + 前缀策略。 |
| `docker-compose.yml` | 当前本地默认 Compose，需决定保留、包装或迁移策略。 |
| `docker-compose.prod.yml` / `docker-compose.prod.external.yml` | 当前生产 Compose，迁移时需更新所有引用和发布输入。 |
| `scripts/docker-up.sh` / `scripts/docker-down.sh` | 当前启停入口，后续应作为 wrapper 或迁移到 `deploy/scripts/`。 |

## 8. 状态块

```yaml
requirement_id: REQ-0093-standardize-deployment-environment-matrix
priority: P1
status: done
readiness: Ready
next: /req-opsx REQ-0093-standardize-deployment-environment-matrix
```
