---
change_id: standardize-deployment-environment-matrix
status: proposed
created_at: 2026-08-03 18:43:20
updated_at: 2026-08-03 18:43:20
source_requirement: REQ-0093-standardize-deployment-environment-matrix
---

# 任务清单

## 1. 目录与文档治理

- [x] 1.1 更新 `rules/directory-structure.md`，正式允许 `deploy/`，定义 `deploy/local/`、`deploy/prod/`、`deploy/scripts/` 边界和禁止事项。
- [x] 1.2 更新 `AGENTS.md`，在部署任务读取路由和目录边界摘要中加入 `deploy/`。
- [x] 1.3 更新 `rules/environment.md`，补充 `deploy/**/*.env.example` 注释、安全边界和真实 env 禁止提交规则。
- [x] 1.4 更新 `docs/02-deployment.md`，新增部署环境矩阵、环境 ID、启动命令、Compose 选择规则和生产安全边界。

## 2. deploy 目录与环境矩阵

- [x] 2.1 新建 `deploy/README.md`，说明总矩阵和“一拓扑一 Compose + 一环境一 env 示例”原则。
- [x] 2.2 新建 `deploy/local/README.md`，描述 6 种本地环境与使用方式。
- [x] 2.3 新建 `deploy/prod/README.md`，描述 `prod-mysql-tencent-cos` 前置条件、启动方式和安全边界。
- [x] 2.4 新建本地 6 个 `deploy/local/*.env.example`。
- [x] 2.5 新建生产 `deploy/prod/mysql-tencent-cos.env.example`。

## 3. Compose 与脚本

- [x] 3.1 新建或迁移 `deploy/local/compose.yml`，让本地环境按 env 和 profile 区分数据库与对象存储组合。
- [x] 3.2 新建 `deploy/prod/compose.tencent-cos.yml`，表达外部 MySQL + 腾讯云 COS 生产拓扑。
- [x] 3.3 新建 `deploy/scripts/validate-env.py`，实现生产 SQLite、示例密钥、COS 自动建桶、本地 MinIO profile 错配等校验。
- [x] 3.4 新建 `deploy/scripts/up.sh`，按 `<domain> <environment>` 解析 env、Compose、profile 并启动。
- [x] 3.5 新建 `deploy/scripts/down.sh`，按部署域停止并输出数据保留说明。
- [x] 3.6 将 `scripts/docker-up.sh` 与 `scripts/docker-down.sh` 改为兼容 wrapper，默认转调本地默认环境。

## 4. 发布与校验

- [x] 4.1 更新 `/image-prepare` 相关脚本或规则，使 `deploy/**/*.yml`、`deploy/**/*.env.example`、`deploy/scripts/*` 纳入发布镜像输入追踪。
- [x] 4.2 更新发布镜像文档或规则，说明 deploy 输入漂移会使 manifest 过期。
- [x] 4.3 更新 `scripts/validate-directory-structure.py`，允许合法 `deploy/` 并阻断真实 env、运行时数据和镜像包。
- [x] 4.4 补充部署校验相关测试，覆盖环境矩阵解析、危险配置阻断和目录结构校验。

## 5. 验证

- [x] 5.1 运行 `python scripts/validate-directory-structure.py`。
- [x] 5.2 运行 `python scripts/validate-openspec-language.py`。
- [x] 5.3 对至少一个本地默认环境运行 Compose config 校验。
- [x] 5.4 对 `prod-mysql-tencent-cos` 运行生产等价 Compose config 校验，不启动本地 MinIO。
- [x] 5.5 运行与部署脚本和目录校验相关的测试。

## 验收返修记录

- [x] 2026-08-03 20:35:23：按验收反馈完善 `deploy/**/*.env.example` 的变量分组与候选值说明；同步 `rules/environment.md`、`docs/02-deployment.md`、Change design/spec、REQ acceptance，并补充 env 示例结构测试。
