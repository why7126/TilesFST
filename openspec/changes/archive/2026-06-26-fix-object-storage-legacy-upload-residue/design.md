## Context

`BUG-0008-object-storage-legacy-upload-residue` 是 BUG-0006 修复后的 **post-migration cleanup** 技术债。

| 项目 | 内容 |
|---|---|
| 前置 Change | `fix-object-storage-upload-not-minio`（archived） |
| 关联 BUG | `BUG-0006-object-storage-upload-not-minio` |
| 运行环境 | local / Docker Compose |
| 有效存储 | MinIO `MINIO_BUCKET` + DB `object_key` |
| 遗留目录 | `data/uploads/`（BUG-0006 前本地写入） |
| 持久化卷 | `data/minio/`（MinIO 服务 `/data` 挂载） |

## Root Cause Summary

### RC-001：迁移 Change 未定义 cleanup 任务

BUG-0006 切换 `save_upload_file()` 与 `/media` 至 MinIO，但未清理历史 `data/uploads` 文件或退役无用挂载。

### RC-002：双目录同前缀结构造成认知混淆

`original/default/...` 同时出现在 `data/uploads` 与 `data/minio/tile-info-platform`，易被误判为重复存储。

### RC-003：UPLOAD_DIR 配置与挂载仍保留

`docker-compose.yml`、`.env.example`、`settings.upload_dir` 暗示本地上传仍可用，与当前 MinIO-only 实现不一致。

## Decisions

### D1：清理范围限定为 uploads 孤儿

清理目标为 `data/uploads/` 下 **无 DB 媒体字段引用** 的业务文件（如 `brands.logo_object_key`、用户头像 key、SKU 媒体 key 等）。不得删除 MinIO 对象或 DB 仍引用的 key 对应文件。

### D2：默认 dry-run + 显式确认

清理脚本 MUST 支持 dry-run 列出待删文件；实际删除需 `--apply` 或等价显式参数。

### D3：MinIO 卷为预期持久化

文档 MUST 明确：本地 `data/minio` 增长是 MinIO 正常工作方式，不是缺陷。

### D4：UPLOAD_DIR 收敛策略

实现阶段 grep/测试确认 `settings.upload_dir` 无上传/读取业务依赖后：

- 移除 `docker-compose.yml` 中 `./data/uploads` 挂载（若 backend 无其他用途）；
- 从 `config.py` 移除或标记 deprecated `upload_dir`；
- 更新 `.env.example` 注释或移除 `UPLOAD_DIR`。

若测试仍依赖 `UPLOAD_DIR`（如 `test_auth.py` monkeypatch），保留测试专用临时路径，不恢复生产上传写入。

### D5：无 API 变更

不修改上传响应、媒体 URL 或错误码；不触发 Orval。

## Test Strategy

| 层级 | 验证 |
|---|---|
| 清理脚本 | dry-run 列出孤儿；apply 后 uploads 无业务孤儿 |
| Backend pytest | 品牌 Logo 上传仍写 MinIO；`/media` 可读 |
| 回归 | `test_admin_brands.py` 媒体相关用例通过 |
| Docker | 上传后对象在 MinIO；`data/uploads` 无新增业务文件 |
| 文档 | `data/README.md` 职责说明可读且与实现一致 |

## Risks

| 风险 | 影响 | 缓解 |
|---|---|---|
| 误删仍被 DB 引用且仅存在于 uploads 的文件 | Logo 404 | 以 DB key 白名单保护；默认 dry-run |
| 移除 uploads 挂载破坏未知依赖 | 容器启动或测试失败 | grep 全代码路径；保留 processed/tmp 挂载 |
| 文档未同步 | 团队继续混淆双目录 | 纳入 tasks 强制更新 |

## Out of Scope

- 不改变 object key 前缀策略或路径深度。
- 不迁移 MinIO 对象到其他 Bucket。
- 不修改 Web 管理端 UI。
- 不清理 MinIO 桶内对象（仅 legacy uploads）。
