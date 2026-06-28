---
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: captured
recorded_at: 2026-06-26 23:49:23
severity_hint: medium
environment: local|docker
related_requirement: null
related_bug: BUG-0006-object-storage-upload-not-minio
---

# 现象

BUG-0006 修复后，业务上传已正式写入 MinIO 单桶 `tile-info-platform`，但本地开发环境仍存在 **双目录并存** 现象，缺少明确的历史数据清理与文档澄清策略：

1. **`data/minio/tile-info-platform/`** — MinIO 持久化卷，当前有效业务对象落盘位置（预期行为）。
2. **`data/uploads/original/default/brands/logos/...`** — BUG-0006 修复前本地上传链路残留，存在与数据库 `logo_object_key` **无关联的孤儿文件**。

当前观察到（2026-06-26 本地环境）：

- `brands` 表中 3 条有效 `logo_object_key` 均可在 `data/minio/tile-info-platform/` 找到对应对象。
- 同一批 key **不在** `data/uploads/` 下。
- `data/uploads/original/default/brands/logos/2026/06/` 仍有 6 个 PNG 孤儿文件（UUID 未出现在 `brands.logo_object_key`）。
- Docker Compose 仍挂载 `./data/uploads:/app/data/uploads`，`.env.example` 仍保留 `UPLOAD_DIR`，但当前上传实现已不再写入该目录。
- 运维/开发易误解为「业务数据不应出现在 `data/minio/`，否则目录无限扩大」，实际 `data/minio` 即本地 MinIO 桶物理存储；真正需清理的是 **`data/uploads` 历史残留**。

# 复现步骤

1. 启动 Docker Compose 本地环境（backend + minio）。
2. 在管理端 `/admin/brands` 上传品牌 Logo 并保存（修复后行为）。
3. 分别查看：
   - MinIO Console → `tile-info-platform` → `original/default/brands/logos/...`
   - 宿主机 `data/minio/tile-info-platform/original/default/brands/logos/...`
   - 宿主机 `data/uploads/original/default/brands/logos/...`
4. 对比 SQLite `brands.logo_object_key` 与两处目录文件名。
5. 可观察到：有效引用仅在 MinIO；`data/uploads` 可能仍有更早的孤儿 PNG。

# 期望 vs 实际

| 项目 | 期望 | 实际 |
|---|---|---|
| 业务上传唯一落点 | 仅 MinIO `MINIO_BUCKET`；DB 存 `object_key` | ✅ 新上传已满足 |
| 本地持久化 | `data/minio` 作为 MinIO 卷增长属预期；文档说明清晰 | ⚠️ 易与 `data/uploads` 混淆 |
| 历史残留 | BUG-0006 修复后有明确清理策略（脚本/文档/移除无用挂载） | ❌ `data/uploads` 孤儿文件仍在；`UPLOAD_DIR` 挂载未收敛 |
| 开发体验 | 排查媒体问题时路径单一、无误导 | ❌ 双目录同名前缀增加排查成本 |

# 附件

- 暂无截图。
- 探索依据：本地 `data/` 目录对比、`brands.logo_object_key` 查询、BUG-0006 root-cause 与 `data/README.md`。

# 初步备注

- 本缺陷为 **技术债 / 运维清理**，非上传或展示功能回归；当前品牌 Logo 读写链路正常。
- 修复面可能包括：清理脚本、更新 `data/README.md` / 部署文档、评估移除 backend 对 `UPLOAD_DIR` 的无用挂载、确认 `settings.upload_dir` 是否仍被非上传代码引用。
- 若存在其他资源类型（头像、SKU 图片/视频）在 `data/uploads` 的同类残留，应一并纳入清理范围。
- 本阶段仅 capture，不修改源码、不创建 OpenSpec Change。
