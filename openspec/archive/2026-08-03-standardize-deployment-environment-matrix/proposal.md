---
change_id: standardize-deployment-environment-matrix
type: update
status: proposed
created_at: 2026-08-03 18:43:20
updated_at: 2026-08-03 18:43:20
source_requirement: REQ-0093-standardize-deployment-environment-matrix
---

# 标准化部署环境矩阵与 deploy 目录治理

## 背景

项目当前通过根目录 `docker-compose.yml`、`docker-compose.prod.yml`、`docker-compose.prod.external.yml`、`.env.example` 以及 `scripts/docker-up.sh` / `scripts/docker-down.sh` 支持本地开发、演示与生产部署。随着 SQLite / MySQL、自建 MinIO / 外部 MinIO / 腾讯云 COS、本地 / 生产等组合增加，单一 `.env.example` 与部署文档已经难以清晰表达每个环境的前置条件、启动命令和安全边界。

REQ-0093 已评审通过，要求建立部署环境矩阵，并通过 OpenSpec Change 正式引入一级 `deploy/` 目录，承载本地和生产部署资产、环境化 env 示例、Compose 入口、部署脚本和配置校验。

## 变更范围

本 Change 将扩展部署治理能力：

- 新增 `deploy/` 顶层目录职责与目录结构。
- 定义 `deploy/local/`、`deploy/prod/`、`deploy/scripts/` 的边界。
- 定义本地 6 种部署环境和生产腾讯云 COS 环境。
- 确立“一拓扑一 Compose + 一环境一 env 示例”原则。
- 将核心部署 up/down/validate 逻辑迁移到 `deploy/scripts/`，保留 `scripts/docker-up.sh` 与 `scripts/docker-down.sh` 作为兼容 wrapper。
- 更新部署文档、环境变量规则、目录校验和发布镜像治理输入。

## 不包含

- 不实现 CI/CD、Kubernetes、Helm、Terraform、Ansible 或云平台托管部署。
- 不自动创建、管理或销毁生产 MySQL、腾讯云 COS bucket、云密钥或安全组。
- 不提交真实 `.env`、密钥、生产私有域名、数据库连接串、对象存储凭据或客户数据。
- 不修改后端、Web、小程序业务功能。
- 不为每个环境复制一份完整 Compose。

## 影响分析

```yaml
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: config-only
  api: false
  docker: true
  docs: true
  release_image_inputs: true
capabilities:
  new:
    - deploy-directory-governance
    - deployment-environment-matrix
  modified:
    - deployment
    - deployment-image-build
```

## 预期收益

- 开发者和测试人员可以按环境 ID 启动可复现部署组合。
- 运维和发布负责人可以区分本地、生产与真实私有配置边界。
- 部署文件变化可进入镜像构建计划和 manifest 输入 hash。
- 目录结构和脚本边界明确，降低后续新增环境时复制脚本和泄露配置的风险。
