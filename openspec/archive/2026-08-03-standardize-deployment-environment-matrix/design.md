---
change_id: standardize-deployment-environment-matrix
status: proposed
created_at: 2026-08-03 18:43:20
updated_at: 2026-08-03 18:43:20
source_requirement: REQ-0093-standardize-deployment-environment-matrix
---

# 设计说明

## 1. 设计目标

本 Change 采用“部署资产集中、默认入口兼容”的设计：

- `deploy/` 作为部署环境矩阵和环境化部署资产的主目录。
- 根目录保留默认 `docker compose up` 兼容入口，降低本地开发破坏面。
- Compose 按服务拓扑拆分，env 示例按具体环境拆分。
- 部署脚本集中在 `deploy/scripts/`，旧 `scripts/docker-up.sh` / `scripts/docker-down.sh` 仅作为 wrapper。

## 2. 目录结构

目标结构：

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

如需保留生产自建 MinIO，`deploy/prod/` 可增加 `compose.self-hosted-minio.yml` 与 `mysql-minio-managed.env.example`。该项不是当前生产目标的必选项。

## 3. Compose 与 env 分工

设计原则：

```text
环境变量不同 → 新增或调整 .env.example
服务拓扑不同 → 新增或调整 Compose / profile
命令入口不同 → 调整 deploy/scripts
人类说明不同 → 更新 README / docs
```

本地 6 种部署环境复用 `deploy/local/compose.yml`，通过 `DATABASE_URL`、`OBJECT_STORAGE_PROVIDER`、`OBJECT_STORAGE_ENDPOINT`、`OBJECT_STORAGE_*` 和 `self-hosted-storage` profile 区分。生产腾讯云 COS 使用 `deploy/prod/compose.tencent-cos.yml`，因为生产拓扑、镜像 tag、安全边界和外部服务前置条件均不同于本地。

env 示例采用统一分组结构：环境标识、应用安全、数据库、镜像、对象存储、端口。没有某类变量的环境可省略该组。布尔、枚举、provider、region、端口和连接串变量的上一行注释必须包含候选值或候选格式，避免验收和运维阶段只能从默认值反推配置范围。

## 4. 命令入口

新入口：

```bash
./deploy/scripts/up.sh local sqlite-minio-managed
./deploy/scripts/up.sh local mysql-tencent-cos
./deploy/scripts/up.sh prod mysql-tencent-cos
./deploy/scripts/down.sh local
./deploy/scripts/down.sh prod
```

兼容入口：

```bash
./scripts/docker-up.sh
./scripts/docker-down.sh
```

兼容 wrapper 默认转调 `local sqlite-minio-managed`，避免重复维护 provider 判断、profile 判断和安全校验逻辑。

## 5. 环境校验

`deploy/scripts/validate-env.py` 负责启动前校验：

- 生产不得使用 SQLite。
- 生产不得开启 `APP_DEBUG=true`。
- 生产不得使用示例密钥、示例对象存储凭据或示例管理员初始密码。
- 腾讯云 COS / 外部对象存储生产必须 `OBJECT_STORAGE_AUTO_CREATE_BUCKET=false`。
- 外部对象存储场景不得启用本地 MinIO profile。
- 项目自建 MinIO 场景必须启用对应 profile 或 Compose 服务。
- env 示例变量和 Compose 引用变量必须同步。
- env 示例必须按主题分组，并为关键变量补充候选值或候选格式。

校验输出只展示变量名、环境 ID、blocker 和修复建议，不输出真实变量值。

## 6. 发布镜像治理兼容

REQ-0081 已要求镜像构建计划和 manifest 记录 Dockerfile、Compose、脚本和 env 示例输入 hash。本 Change 迁移或新增部署 Compose 后，`/image-prepare` 与 `/image-build` 必须记录新的 `deploy/` 路径，`/release-publish` 必须识别 Compose、脚本或 env 示例漂移。

## 7. 冲突报告

本 Change 不涉及 UI prototype。冲突优先级为 N/A。

目录策略上，当前 `rules/directory-structure.md` 只允许根目录存在项目级 Compose。REQ-0093 明确要求通过本 Change 更新该规则，因此新增 `deploy/` 和环境化 Compose 是有授权的目录治理变更。

## 8. 风险与缓解

| 风险 | 缓解 |
|---|---|
| 完全迁移 Compose 破坏 `docker compose up` 默认体验 | 保留根目录默认入口或 wrapper。 |
| 多环境复制 Compose 导致漂移 | 明确“一拓扑一 Compose + 一环境一 env 示例”。 |
| 生产误用本地 SQLite 或示例密钥 | 启动前 validate-env 阻断。 |
| 迁移后发布镜像输入遗漏新路径 | 更新 image prepare / manifest 输入清单与 release 文档。 |
| 真实 env 被误提交 | 更新 `.gitignore`、目录校验和环境变量规则。 |
