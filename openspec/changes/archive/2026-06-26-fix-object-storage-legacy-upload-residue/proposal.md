## Why

`BUG-0008-object-storage-legacy-upload-residue` 已评审通过并纳入 `sprint-002`。BUG-0006（`fix-object-storage-upload-not-minio`）修复后，业务上传已写入 MinIO 单桶，但本地 Docker 环境仍存在 **双目录并存**：

- `data/minio/tile-info-platform/` — MinIO 持久化卷（预期、有效对象落盘）
- `data/uploads/original/...` — BUG-0006 修复前本地上传孤儿文件（无 DB 引用）

根因见 `issues/bugs/BUG-0008-object-storage-legacy-upload-residue/root-cause.md`：存储迁移缺少 post-migration cleanup；`UPLOAD_DIR` Docker 挂载与配置未收敛；`data/README.md` 对两目录职责说明不足。

## What Changes

- 提供 legacy `data/uploads` 业务孤儿文件的安全清理策略：
  - 脚本或文档化步骤 MUST 能识别并删除无 DB `object_key` 引用的 uploads 残留。
  - 清理 MUST NOT 删除 MinIO 中仍被 DB 引用的有效对象。
- 收敛无用 `UPLOAD_DIR` 配置与 Docker 挂载（在确认无业务代码依赖后）：
  - 评估移除 `docker-compose.yml` 中 `./data/uploads` 挂载。
  - 评估从 `settings` / `.env.example` 退役或标注 `UPLOAD_DIR` 为历史兼容且不参与上传。
- 更新数据与部署文档，澄清：
  - `data/minio` 为本地 MinIO 桶物理存储，增长属预期；
  - `data/uploads` 不为 BUG-0006 后业务上传正式存储；
  - 媒体排查以 DB `object_key` + MinIO 为准。
- 可选：提供 `scripts/` 一致性检查工具，列出 uploads 孤儿或报告无残留。
- 回归验证：新上传仅写 MinIO；品牌 Logo 展示无回归（BUG-0006/BUG-0007 能力保持）。

## Impact

| 影响面 | 说明 |
|---|---|
| 后端上传链路 | 默认无逻辑变更；确认不恢复 `UPLOAD_DIR` 写入 |
| Web 管理端 | 无 UI 变更；Logo 展示 MUST 无回归 |
| API / Orval | 无 schema 变更，不需要 Orval |
| 数据库 | 无 schema 变更 |
| Docker Compose | 可能移除 `./data/uploads` 挂载；应用内部端口不变 |
| 文档 | `data/README.md`、`docs/07-object-storage-strategy.md`、`docs/02-deployment.md`、`.env.example` |
| 脚本 | 新增清理/校验脚本（若 tasks 要求） |
| 本地数据 | 删除 legacy uploads 孤儿文件；不影响 MinIO 有效对象 |

## Rollback Plan

如清理或配置收敛导致媒体不可用：

1. 回滚 Docker Compose 挂载与文档变更；恢复 `./data/uploads` 挂载（若已移除）。
2. 清理脚本 MUST 默认 dry-run；误删场景可从 MinIO 重新读取有效对象（DB key 仍在）。
3. 不得回滚 BUG-0006 MinIO 写入与受控读取逻辑。
4. 将 `BUG-0008` 状态回退为 `in_sprint` 未修复，并保留验收失败记录。
