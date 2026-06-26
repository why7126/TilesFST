---
bug_id: BUG-0006-object-storage-upload-not-minio
status: captured
recorded_at: 2026-06-26 10:09:12
severity_hint: high
environment: local|docker
related_requirement: null
---

# 现象

对象存储 MinIO 服务已启动，`minio-init` 能创建 `tile-info-platform` 存储桶，但业务上传链路没有把图片/视频对象写入 MinIO。用户在对象存储控制台无法看到上传后的业务对象。

当前观察到：

- Docker Compose 中存在 `minio` 与 `minio-init` 服务。
- `minio-init` 日志显示桶 `tile-info-platform` 已创建并设置为 private。
- 本地目录存在 `data/minio/tile-info-platform`。
- 后端上传实现当前写入 `UPLOAD_DIR` 对应的本地文件系统路径，而不是通过 MinIO client 写入对象存储。
- `data/minio/tile-info-platform` 下未看到业务上传对象。

# 复现步骤

1. 启动 Docker Compose 环境。
2. 打开 MinIO Console，确认项目桶 `tile-info-platform`。
3. 在管理端执行任意媒体上传，例如品牌 Logo、SKU 图片或 SKU 视频上传。
4. 回到 MinIO Console 查看桶内对象。

# 期望 vs 实际

| 项目 | 内容 |
|---|---|
| 期望 | 上传成功后，文件应写入 MinIO 的 `tile-info-platform` 桶，并使用标准对象前缀（如 `original/`、`videos/`）区分资源类型。 |
| 实际 | 上传链路使用本地 `UPLOAD_DIR` 文件系统保存；MinIO 桶内没有对应业务对象。 |

# 附件

- 暂无截图。
- 初步分析证据来自当前 Docker Compose 配置、MinIO init 日志与后端上传代码观察。

# 初步备注

- 该问题影响品牌 Logo、SKU 图片、SKU 视频、头像等上传能力的一致性。
- 可能需要在后续阶段将 `save_upload_file()` 改为 MinIO put object，并同步 `/media/{object_key}` 的受控读取策略。
- 本阶段仅 capture，不修改源码、不创建 OpenSpec Change。
