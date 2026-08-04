---
requirement_id: REQ-0097-prod-compose-media-maintenance-job
title: 生产 Docker Compose 环境支持媒体历史数据维护任务安全执行
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-04 10:33:55
updated_at: 2026-08-04 22:59:32
---

# REQ-0097 生产 Docker Compose 环境支持媒体历史数据维护任务安全执行

## 1. 需求背景

线上生产环境已经演进为部署矩阵治理模式，当前推荐生产入口为 `deploy/prod/compose.tencent-cos.yml`，结构化数据使用外部 MySQL，媒体对象使用腾讯云 COS 或等价 S3 兼容对象存储。根目录 `docker-compose.prod.external.yml` 仍可作为 VPS、离线交付或历史兼容入口维护，但不应再作为唯一生产事实源。

媒体历史治理已经出现多类维护场景，包括对象 Key 迁移、公开 SKU 暂存主图正式化、品牌与证书图片缩略图回填、证书图片从 `files/` 到 `images/` 的分类治理，以及媒体五联或四联验收后的二次审计。这些任务通常需要同时访问生产数据库和对象存储，且具备写操作风险。

当前已有若干脚本可用于本地或受控环境审计，但后端生产镜像构建上下文为 `src/backend`，镜像默认只复制 `app/`，根目录 `scripts/` 不一定在生产容器内可用。部分脚本仍偏 SQLite 或本地路径假设，不能直接在外部 MySQL + COS 的生产环境中执行 apply。

本需求用于定义一种可审计、可回滚、可分批执行的生产维护任务入口，使运维和交付团队能在生产服务器上通过 Docker Compose 一次性容器安全执行媒体历史维护任务，而不需要将生产 `.env`、数据库连接串或对象存储密钥下载到开发机。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 实施 / 运维 | 能在生产服务器上复用现有 Compose env 与网络执行受控维护任务，避免密钥外泄和误连环境。 |
| 发布负责人 | 能确认维护任务使用的镜像、脚本、Compose、env 示例和发布镜像治理证据一致。 |
| 后端开发 | 能把媒体历史处理脚本改造成支持 MySQL、对象存储 provider、dry-run/apply 和批处理的可维护入口。 |
| 测试 / 验收 | 能基于 dry-run、apply、二次审计和媒体四联/五联摘要确认生产维护任务结果。 |
| 产品 / 业务负责人 | 能知道历史媒体治理的影响范围、回滚方式和用户可见收益，不被一次性脚本黑箱化。 |

## 3. 范围

### 3.1 本期包含

- 定义生产媒体维护任务的 Compose 执行入口和安全边界。
- 明确 `deploy/prod/compose.tencent-cos.yml` 为当前推荐生产矩阵入口，根目录生产 Compose 仅作为兼容入口。
- 明确维护任务应使用生产服务器本地 env 注入，不要求下载生产 `.env` 到开发机。
- 确认维护脚本进入生产镜像或专用 maintenance 镜像的发布策略。
- 将媒体历史脚本改造为支持外部 MySQL、腾讯云 COS / S3 兼容对象存储 provider 和生产路径假设。
- 为写操作提供 dry-run / apply 两阶段、limit / batch 分批、幂等、失败原因统计和二次审计能力。
- 明确执行前必须完成 MySQL 快照和对象存储 bucket / prefix 快照。
- 明确执行后必须输出 key、object、URL、thumbnail benefit、render 或等价媒体四联/五联验收摘要。
- 明确日志与报告不得输出真实密钥、数据库连接串、Authorization header、Cookie、生产 `.env` 内容或真实客户敏感数据。

### 3.2 本期不包含

- 不在 PRD 阶段直接修改 Dockerfile、Compose、脚本、源码、测试或 OpenSpec Change。
- 不直接执行任何生产维护任务或生产数据写操作。
- 不引入 Kubernetes、定时任务平台、CI/CD 自动生产作业或云资源编排。
- 不新增视频转码、视频压缩、多清晰度、PDF 首页渲染缩略图或 OCR 能力。
- 不改变对象存储单 Bucket + 标准前缀策略。
- 不允许前端、管理端或小程序绕过后端鉴权直接访问对象存储。
- 不把真实 `.env`、数据库备份、对象存储导出、运行时数据库或客户媒体对象提交到仓库。
- 不自动清理历史媒体对象；清理类高风险动作需要后续单独确认。

## 4. 功能要求

### FR-001 生产维护任务入口

系统 MUST 提供生产 Docker Compose 环境下的媒体维护任务执行入口。该入口 SHOULD 以 `deploy/prod/compose.tencent-cos.yml` 和对应生产 env 为当前主路径，并说明 `docker-compose.prod.external.yml` 仅作为兼容入口时的适用边界。

维护任务 SHOULD 通过一次性容器执行，例如 `docker compose ... run --rm <maintenance-service> ...` 或等价命令。命令必须在生产服务器或受控堡垒环境执行，并复用生产环境注入方式和 Compose 网络。

### FR-002 镜像与服务策略

系统 MUST 明确维护任务使用的镜像策略。

优先方案 SHOULD 是新增或定义专用 `tilesfst-maintenance` 服务或镜像，使维护命令与在线后端服务隔离。若选择复用 `tilesfst-backend` 镜像，系统 MUST 确认镜像内包含受控维护入口，且不会改变后端在线服务启动命令、端口和健康检查语义。

无论采用哪种策略，维护入口 MUST 经过发布镜像治理，避免生产临时 bind mount 未评审脚本后直接 apply。只读审计临时挂载可以作为应急方案，但必须在文档中明确限制、审批和禁止写操作边界。

### FR-003 环境变量与密钥安全

维护任务 MUST 复用生产 env / secret 注入，不要求也不鼓励将生产 `.env` 下载到开发机。

维护命令、日志、审计报告和失败摘要 MUST 只输出变量名、脱敏对象标识、统计结果和错误码，不得输出真实数据库连接串、对象存储 access key / secret key、Authorization header、Cookie、生产 `.env` 原文、本机绝对路径或真实客户敏感数据。

生产环境 MUST 显式使用 MySQL `DATABASE_URL`，不得回退 SQLite。腾讯云 COS 或 S3 兼容对象存储生产环境 MUST 禁止自动建桶，并依赖运维提前创建的 bucket、region、endpoint 和最小权限策略。

### FR-004 脚本生产适配

媒体历史维护脚本 MUST 支持生产 MySQL 与对象存储 provider，不得只依赖 SQLite 文件路径或本地 MinIO 默认值。

脚本 SHOULD 统一通过后端配置、数据库 session、对象存储适配层和媒体模块能力执行，避免在脚本内重复拼接不一致的对象存储客户端、路径或数据库连接逻辑。涉及对象 copy、remove、put、stat 的动作 MUST 适配腾讯云 COS、MinIO 和 S3 兼容 provider 的差异。

### FR-005 dry-run / apply 两阶段

所有可能写数据库或对象存储的维护任务 MUST 支持 dry-run / apply 两阶段。

dry-run MUST 输出受影响记录数量、对象数量、跳过原因、缺失对象、目标 key 冲突、预计写入动作、风险提示和执行前置条件。dry-run 不得写数据库、不得写对象存储、不得删除对象。

apply MUST 要求显式参数触发，并在执行前确认已完成备份。apply 输出 MUST 包含成功、失败、跳过、重试候选、失败原因统计和可用于二次审计的摘要。

### FR-006 分批、幂等与失败恢复

维护任务 MUST 支持分批执行，至少提供 limit、batch size、范围过滤或等价控制方式，避免一次性扫描或写入过大数据集。

维护任务 MUST 尽量幂等。重复执行同一任务时，已完成记录应被识别为 skipped 或 already_done，不得重复生成冲突对象或重复破坏数据库引用。

任务失败时 MUST 保留可定位的失败原因、失败对象标识和建议恢复动作。系统 SHOULD 支持失败后重跑剩余项或按失败原因重试。

### FR-007 备份、回滚与审计

维护任务文档 MUST 在 apply 前要求：

- 完成 MySQL 快照或可恢复备份。
- 完成对象存储 bucket、prefix 或受影响对象集合快照。
- 记录执行镜像 tag、Compose 文件、env 文件位置、命令参数、执行人、执行时间和 dry-run 摘要。

回滚说明 MUST 以恢复 MySQL 快照和对象存储快照为主。若某些动作可提供反向迁移或对象恢复脚本，应明确其适用条件；不得把未验证的反向脚本描述为默认可靠回滚。

### FR-008 媒体维护任务类型

系统 SHOULD 至少覆盖以下维护任务类型的接入规则：

| 任务类型 | 示例 | 关键验收 |
|---|---|---|
| Object Key 迁移 | 历史 `original/`、`files/` 图片类对象迁入标准 `images/` 前缀 | key、object、URL、render 不断链。 |
| 缩略图回填 | 品牌 Logo、证书图片、SKU 图片缩略图补齐或重生成 | thumbnail benefit 可解释，原图读取不受影响。 |
| SKU 暂存主图正式化 | 公开商品主图从 暂存目录迁入 SKU 正式目录 | 公开接口与端侧展示继续可用。 |
| 二次审计 | 对已执行任务验证对象存在、数据库引用和端侧 URL | 输出可脱敏追溯摘要。 |

新增维护任务类型 MAY 在后续 OpenSpec Change 中扩展，但必须遵守本需求的安全、审计、dry-run/apply 和备份边界。

### FR-009 验收摘要

维护任务执行后 MUST 输出媒体四联或五联验收摘要。

对于媒体对象迁移、缩略图回填和历史审计，摘要 SHOULD 覆盖：

- `key`：数据库记录中的对象 key 是否符合标准前缀和脱敏要求。
- `object`：对象存储中真实 object 是否存在，MIME、大小、权限和缩略图关系是否符合预期。
- `URL`：后端受控 `/media/{object_key}` 或等价 URL 是否可追溯，不直连未授权对象存储。
- `thumbnail benefit`：缩略图是否真实生成、体积或展示收益是否可解释。
- `render`：管理端、店主 Web 或小程序受影响场景是否有验证或明确 blocked 补证说明。

## 5. UI 约束

本需求以生产维护与运维执行为主，默认不新增用户可见 UI。

如后续实现需要在管理端增加维护任务状态页、审计报告页或下载入口，MUST 单独在 OpenSpec Change 中明确权限、页面范围、Design System 复用策略和敏感信息脱敏规则。任何管理端 UI 变更 MUST 使用 semantic token，复用既有暗色旗舰风组件，并仅面向已授权企业内部管理员或运维角色开放。

命令行输出和文档表格 SHOULD 保持可读、可复制和便于审计，但不得为了展示完整性输出密钥、生产连接串、真实客户标识或对象存储私有 URL。

## 6. 关联需求

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0012-object-storage-key-layout | 前置规则 | 定义单 Bucket、标准前缀和 Object Key 迁移方向。 |
| REQ-0018-production-mysql-deployment | 前置部署 | 定义生产 MySQL 部署约束，维护任务不得回退 SQLite。 |
| REQ-0092-brand-certificate-image-thumbnails | 相关媒体能力 | 品牌与证书缩略图存在存量回填和重生成需求。 |
| REQ-0093-standardize-deployment-environment-matrix | 前置部署治理 | 当前生产入口以 `deploy/prod/compose.tencent-cos.yml` 为主。 |
| REQ-0090-media-five-point-acceptance-template | 验收模板 | 媒体维护任务应输出五联验收摘要。 |
| REQ-0091-media-bug-four-point-acceptance-template | 验收模板 | 媒体缺陷或修复类维护任务应输出四联验收摘要。 |

## 7. 状态块

```yaml
status: done
lifecycle_stage: plan
next_command: /req-opsx REQ-0097
open_questions:
  - 生产维护任务优先采用专用 tilesfst-maintenance 镜像/服务，还是复用 tilesfst-backend 镜像内的受控命令入口。
  - 生产对象存储是否固定为腾讯云 COS，还是需要同时保留外部 MinIO 和通用 S3 兼容 provider 的 apply 验收。
  - 是否允许在生产服务器上临时只读 bind mount scripts/ 进行审计；若允许，哪些命令必须禁止 apply。
  - 首批纳入维护入口的脚本清单是否包含 object key 迁移、品牌证书缩略图回填、SKU 暂存主图正式化和二次审计。
  - 维护任务执行报告是否需要进入 release 或 docs 事实源，还是仅作为生产运维外部证据保存。
```
