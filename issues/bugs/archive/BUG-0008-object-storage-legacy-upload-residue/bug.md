---
bug_id: BUG-0008-object-storage-legacy-upload-residue
title: 对象存储修复后本地 uploads 双目录残留与历史数据清理缺失
severity: medium
status: draft
owner: product
discovered_at: 2026-06-26 23:49:23
environment: local|docker
related_requirement: null
related_change: null
related_bug: BUG-0006-object-storage-upload-not-minio
---

# 缺陷说明

## 1. 现象

BUG-0006 修复后，业务上传已正式写入 MinIO 单桶 `tile-info-platform`，品牌 Logo 等媒体的读写链路正常。但本地 Docker 开发环境仍存在 **双目录并存**，且缺少明确的历史数据清理策略与文档澄清：

1. **`data/minio/tile-info-platform/`** — MinIO 持久化卷，当前有效业务对象的物理落盘位置（预期行为）。
2. **`data/uploads/original/default/brands/logos/...`** — BUG-0006 修复前本地上传链路残留，存在与数据库 `logo_object_key` **无关联的孤儿文件**。

当前观察到（2026-06-26 本地环境）：

- `brands` 表中 3 条有效 `logo_object_key` 均可在 `data/minio/tile-info-platform/` 找到对应对象。
- 同一批 key **不在** `data/uploads/` 下。
- `data/uploads/original/default/brands/logos/2026/06/` 仍有 6 个 PNG 孤儿文件（UUID 未出现在 `brands.logo_object_key`）。
- Docker Compose 仍挂载 `./data/uploads:/app/data/uploads`，`.env.example` 仍保留 `UPLOAD_DIR`，但当前上传实现已不再写入该目录。
- 运维/开发易误解为「业务数据不应出现在 `data/minio/`，否则目录无限扩大」；实际 `data/minio` 即本地 MinIO 桶物理存储，真正需清理的是 **`data/uploads` 历史残留**。

## 2. 复现步骤

1. 启动 Docker Compose 本地环境（backend + minio）。
2. 在管理端 `/admin/brands` 上传品牌 Logo 并保存（修复后行为）。
3. 分别查看：
   - MinIO Console → `tile-info-platform` → `original/default/brands/logos/...`
   - 宿主机 `data/minio/tile-info-platform/original/default/brands/logos/...`
   - 宿主机 `data/uploads/original/default/brands/logos/...`
4. 对比 SQLite `brands.logo_object_key` 与两处目录文件名。
5. 可观察到：有效引用仅在 MinIO；`data/uploads` 可能仍有更早的孤儿 PNG。

## 3. 期望结果

- 业务上传唯一落点为 MinIO `MINIO_BUCKET`；数据库仅存 `object_key` 引用。
- 本地开发环境中，`data/minio` 作为 MinIO 卷的职责在文档中说明清晰，不与 `data/uploads` 混淆。
- BUG-0006 修复后，应有明确的历史数据清理策略（脚本、运维说明或一次性迁移），移除 `data/uploads` 中与 DB/MinIO 无关联的孤儿文件。
- Docker Compose 与 `.env.example` 中不再保留无实际用途的 `UPLOAD_DIR` 挂载或配置（或明确标注为历史兼容且不参与业务上传）。
- 排查媒体存储问题时，开发/运维路径单一、无误导。

## 4. 实际结果

- 新上传已满足「仅写 MinIO + DB 存 key」。
- `data/minio` 增长属预期，但文档未充分澄清，易与 `data/uploads` 混淆。
- `data/uploads` 孤儿文件仍在；`UPLOAD_DIR` 挂载与配置未收敛。
- 双目录下存在相同前缀结构（如 `original/default/brands/logos/...`），增加排查成本。

## 5. 影响范围

| 维度 | 影响 |
|---|---|
| Web 管理端 | 无功能回归；当前品牌 Logo 展示正常 |
| 后端上传链路 | 无功能回归；已写入 MinIO |
| 本地 Docker 环境 | `data/uploads` 占用磁盘；双目录误导排查 |
| MinIO 对象存储 | 无缺陷；`data/minio` 为正常持久化卷 |
| 数据库 | 无数据不一致；有效 `logo_object_key` 均指向 MinIO 对象 |
| 文档与运维 | `data/README.md`、部署说明对两目录职责澄清不足 |
| 其他媒体类型 | 头像、SKU 图片/视频可能存在同类 `data/uploads` 残留，待排查 |

## 6. 严重等级说明

严重等级建议为 `medium`。

理由：

- 本缺陷为 BUG-0006 修复后的 **技术债 / 运维清理**，不影响当前上传与展示功能。
- 孤儿文件会持续占用本地磁盘，并在团队内造成「数据到底存在哪」的认知混乱。
- 若长期不清理，`data/uploads` 可能与 MinIO 残留并存，放大后续媒体问题排查成本。
- 不涉及生产数据丢失或线上功能阻断，因此不定为 `high`；但应在下一迭代或维护窗口内收敛。
