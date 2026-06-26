---
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: pending_review
updated_at: 2026-06-26 23:55:19
root_cause_type: legacy-local-upload/post-migration-cleanup
---

# 根因分析

## 1. 直接原因

### 1.1 BUG-0006 修复未包含历史本地文件清理

BUG-0006（`fix-object-storage-upload-not-minio`）将 `save_upload_file()` 与 `/media/{object_key}` 从本地 `UPLOAD_DIR` 切换为 MinIO 读写，但未在修复 Change 中定义：

- 清理 `data/uploads/` 下 BUG-0006 之前写入的孤儿文件；
- 退役 Docker Compose 对 `./data/uploads` 的无用挂载；
- 更新 `data/README.md` 等文档，明确 `data/minio` 与 `data/uploads` 的职责边界。

因此修复后新上传只进 MinIO，旧本地文件仍留在宿主机。

### 1.2 双目录使用相同 object key 前缀结构

BUG-0006 前后均使用 `build_object_key()` 生成相同格式：

```text
original/default/brands/logos/2026/06/{uuid}.png
```

- 修复前：映射到 `UPLOAD_DIR` + object_key → `data/uploads/original/default/brands/logos/...`
- 修复后：写入 MinIO bucket → `data/minio/tile-info-platform/original/default/brands/logos/...`

两处目录结构高度相似，排查时易误判为「重复存储」或「MinIO 目录不应有业务数据」。

### 1.3 配置与挂载仍保留 UPLOAD_DIR

当前仍存在的遗留配置：

| 位置 | 内容 |
|---|---|
| `docker-compose.yml` | `./data/uploads:/app/data/uploads` |
| `.env.example` | `UPLOAD_DIR=/app/data/uploads` |
| `src/backend/app/core/config.py` | `settings.upload_dir` 字段仍存在 |

上传链路（`src/backend/app/modules/media/storage.py`）已不再调用 `upload_dir` 写入，但配置与挂载未同步收敛，暗示业务仍可能使用本地目录。

### 1.4 本地实测：有效引用与孤儿文件分离

2026-06-26 本地环境对比：

| 数据源 | 结果 |
|---|---|
| `brands.logo_object_key`（3 条） | 均在 `data/minio/tile-info-platform/`；均不在 `data/uploads/` |
| `data/uploads/.../brands/logos/2026/06/` | 6 个 PNG，UUID 均未出现在 `brands.logo_object_key` |
| 其他资源类型（avatars、tiles） | `data/uploads` 下暂无除 `.gitkeep` 外的业务文件 |

结论：当前残留主要为品牌 Logo 本地上传孤儿文件，无 DB 引用，删除不影响现网展示。

## 2. 根本原因

### 2.1 存储迁移缺少「收尾」门禁

对象存储接入属于基础设施变更，修复 Change 聚焦「新链路写 MinIO + 受控读取」，未将以下内容纳入验收：

- 历史本地文件清点与清理策略；
- 无用配置/挂载退役；
- 文档对 MinIO 持久化卷（`data/minio`）职责的澄清。

缺少 post-migration cleanup 任务，导致技术债在修复后显性化而非消除。

### 2.2 文档对 data 子目录职责表述不足

`data/README.md` 已说明 `data/uploads` 为「本地缓存/历史兼容」，但未强调：

- 本地 Docker 下 **`data/minio` 即 MinIO 桶物理存储**，增长是预期行为；
- BUG-0006 后业务上传**不应再**出现在 `data/uploads`；
- 如何安全识别并清理 uploads 孤儿文件。

团队易将 `data/minio` 增长误判为架构问题，而忽略真正应清理的 `data/uploads` 残留。

### 2.3 无自动化清理或一致性校验

项目未提供：

- 对比 DB `object_key` 与 `data/uploads` 的脚本；
- 开发环境初始化/重置时对 legacy uploads 的清理步骤；
- CI 或文档中的「双目录一致性」检查。

## 3. 触发条件

满足以下条件时可稳定观察到本缺陷：

1. 曾在 BUG-0006 修复前于本地/Docker 环境上传过品牌 Logo（或其他媒体）。
2. BUG-0006 修复后继续在本机使用同一 `data/` 卷（未 wipe）。
3. 查看 `data/uploads` 与 `data/minio/tile-info-platform`，可见同名前缀结构并存。
4. 对比 SQLite 中 `logo_object_key` 与两目录文件名，uploads 中存在无 DB 引用的 UUID 文件。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | legacy-local-upload / post-migration-cleanup / documentation |
| 直接原因 | BUG-0006 修复未清理历史 `data/uploads` 文件，且 UPLOAD_DIR 配置/挂载未收敛 |
| 根本原因 | 存储迁移缺少收尾门禁与文档澄清；无双目录一致性工具 |
| 是否功能回归 | 否；新上传与展示正常 |
| 是否数据库缺陷 | 否；有效 key 与 MinIO 一致 |
| 是否对象存储缺陷 | 否；`data/minio` 为正常持久化 |
| 主要修复面 | 清理脚本、data/部署文档、Docker 挂载收敛、可选 UPLOAD_DIR 退役 |

## 5. 后续修复建议

1. 提供安全清理脚本：删除 `data/uploads` 下 object key 不在 DB 且不在 MinIO 引用的孤儿文件（或整目录 wipe 后保留 `.gitkeep` 结构）。
2. 评估移除 `docker-compose.yml` 中 `./data/uploads` 挂载及 `settings.upload_dir`（若全代码路径确认无依赖）。
3. 更新 `data/README.md`、`docs/07-object-storage-strategy.md` 或 `docs/02-deployment.md`，澄清 `data/minio` vs `data/uploads`。
4. 在 OpenSpec fix Change 中定义 AC：清理后 uploads 无业务孤儿、新上传不写入 uploads。
5. 可选：在 `scripts/` 增加 `validate-media-storage-residue.py` 供本地/CI 检查。
