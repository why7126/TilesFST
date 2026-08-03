---
requirement_id: REQ-0093-standardize-deployment-environment-matrix
title: 标准化部署环境矩阵与 deploy 目录治理 - 业务流程
created_at: 2026-08-03 18:31:16
updated_at: 2026-08-03 18:31:16
owner: product
---

# 业务流程

## 1. 环境选择流程

```text
选择部署域
    |
    +-- local
    |     |
    |     +-- sqlite-minio-managed
    |     +-- sqlite-minio-external
    |     +-- sqlite-tencent-cos
    |     +-- mysql-minio-managed
    |     +-- mysql-minio-external
    |     +-- mysql-tencent-cos
    |
    +-- prod
          |
          +-- mysql-tencent-cos
```

## 2. 启动流程

```text
用户执行 deploy/scripts/up.sh <domain> <environment>
        |
        v
解析环境 ID
        |
        +-- 定位 env.example
        +-- 定位 compose.yml
        +-- 判断是否需要 self-hosted-storage profile
        |
        v
校验真实 env 或生成配置提示
        |
        +-- pass
        |     |
        |     v
        |   docker compose --env-file <env> -f <compose> up -d --build
        |
        +-- blocked
              |
              v
            输出 blocker 与修复建议
```

## 3. 停止流程

```text
用户执行 deploy/scripts/down.sh <domain>
        |
        v
定位当前域使用的 Compose
        |
        v
docker compose -f <compose> down
        |
        v
输出已停止服务与保留的数据卷说明
```

## 4. Compose 与 env 分工

| 变化类型 | 承载位置 | 示例 |
|---|---|---|
| 环境变量值不同 | `.env.example` | SQLite vs MySQL、MinIO endpoint、COS region、secure/path-style |
| 服务拓扑不同 | Compose / profile | 是否启动项目内 MinIO、是否包含 minio-init |
| 命令入口不同 | `deploy/scripts/` | local/prod 环境 ID 解析、校验和启动 |
| 人类说明不同 | README / docs | 本地运行、生产部署、前置条件、安全边界 |

## 5. 与现状差异

| 现状 | 新流程 |
|---|---|
| 根目录 `.env.example` 同时承载本地与生产示例 | `deploy/local/`、`deploy/prod/` 分别维护环境化 env 示例 |
| `scripts/docker-up.sh` 根据 provider 简单判断是否启 MinIO | `deploy/scripts/up.sh` 按环境 ID 选择 env、Compose 和 profile |
| Compose 与 env 示例缺少一一映射 | 每个环境 ID 显式声明 env 示例、Compose 文件和 profile |
| 生产安全边界依赖人工阅读文档 | validate-env 在启动前阻断 SQLite、示例密钥、COS 自动建桶等风险 |
| 部署文件迁移对镜像发布影响不够显式 | image plan / manifest 记录 `deploy/` 下 Compose、脚本与 env 示例 hash |

## 6. 异常流程

| 异常 | 处理 |
|---|---|
| 环境 ID 不存在 | 启动脚本阻断，列出可用环境 ID。 |
| 真实 env 缺失 | 提示从对应 `.env.example` 复制，禁止自动写入密钥。 |
| 生产 env 使用 SQLite | validate-env 阻断。 |
| 生产 env 使用示例密钥 | validate-env 阻断。 |
| 腾讯云 COS 生产环境允许自动建桶 | validate-env 阻断。 |
| 外部对象存储场景启用本地 MinIO profile | validate-env 阻断或要求明确修正。 |
| Compose 文件迁移后旧引用残留 | 目录结构校验、部署文档校验或 image prepare 输入校验报告 blocker。 |
