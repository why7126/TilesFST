---
bug_id: BUG-0006-object-storage-upload-not-minio
title: 业务上传未写入 MinIO 对象存储
severity: high
status: in_sprint
owner: product
discovered_at: 2026-06-26 10:09:12
environment: local|docker
related_requirement: null
related_change: fix-object-storage-upload-not-minio
---

# 缺陷说明

## 1. 现象

Docker Compose 环境中 MinIO 服务已启动，`minio-init` 可以创建项目桶 `tile-info-platform`，但业务上传链路没有把图片或视频对象写入 MinIO。用户在 MinIO Console 中无法看到上传后的品牌 Logo、SKU 图片、SKU 视频或其他业务媒体对象。

当前观察到：

- Docker Compose 中存在 `minio` 与 `minio-init` 服务。
- `minio-init` 日志显示桶 `tile-info-platform` 已创建并设置为 private。
- 本地目录存在 `data/minio/tile-info-platform`。
- 后端上传实现当前写入 `UPLOAD_DIR` 对应的本地文件系统路径，而不是通过 MinIO client 写入对象存储。
- `data/minio/tile-info-platform` 下未看到业务上传对象。

## 2. 复现步骤

1. 启动 Docker Compose 环境。
2. 打开 MinIO Console，确认项目桶 `tile-info-platform` 已存在。
3. 在管理端执行任意媒体上传，例如品牌 Logo、SKU 图片或 SKU 视频上传。
4. 回到 MinIO Console 查看 `tile-info-platform` 桶内对象。

## 3. 期望结果

- 上传成功后，文件应写入 MinIO 的 `tile-info-platform` 桶。
- 对象 Key 应使用项目标准对象前缀区分资源类型，例如 `original/`、`videos/`、`videos/covers/`。
- 上传链路应通过后端授权与校验后写入对象存储，不应绕过后端，也不应仅保存在本地 `UPLOAD_DIR`。
- MinIO Console 中应能看到上传后的业务对象。

## 4. 实际结果

- 上传链路使用本地 `UPLOAD_DIR` 文件系统保存文件。
- MinIO 桶内没有对应业务上传对象。
- 对象存储服务虽然已初始化，但未被业务上传链路实际使用。

## 5. 影响范围

| 维度 | 影响 |
|---|---|
| Web 管理端 | 影响品牌 Logo、SKU 图片、SKU 视频、头像等上传后存储一致性 |
| 后端媒体上传 | 影响上传保存路径、对象 Key、访问 URL 或受控读取策略 |
| MinIO 对象存储 | 桶已创建但未承载业务对象，违背项目对象存储规范 |
| Docker 演示环境 | 影响本地开发与演示部署中对 MinIO 集成能力的验证 |
| 数据库 | 待分析；若媒体元数据记录本地路径，后续修复可能涉及字段含义或数据迁移确认 |
| 小程序 | 潜在影响；若小程序复用媒体访问 URL，则会受后端媒体读取策略影响 |

## 6. 严重等级说明

严重等级建议为 `high`。

理由：

- 项目规范要求文件上传通过后端授权写入 MinIO，并采用单桶加标准前缀策略。
- 当前缺陷会导致 Docker 环境中对象存储能力形同未接入，影响图片、视频和附件上传的核心基础能力。
- 问题覆盖品牌、SKU、视频等多个媒体使用场景，属于跨业务上传链路的基础设施缺陷。
- 当前尚未确认是否造成上传接口完全失败或数据丢失，因此暂不定为 `critical` 或 `blocker`。
