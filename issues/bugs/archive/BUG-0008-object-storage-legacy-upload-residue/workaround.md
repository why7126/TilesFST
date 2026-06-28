---
bug_id: BUG-0008-object-storage-legacy-upload-residue
status: pending_review
updated_at: 2026-06-26 23:55:19
---

# 临时规避方案

## 1. 认知规避（排查媒体问题时）

在正式修复前，开发/运维应遵循以下原则，避免误判：

| 目录 | 正确理解 |
|---|---|
| `data/minio/tile-info-platform/` | 本地 MinIO 桶物理存储；**当前有效业务对象应在此**；随上传增长属预期 |
| `data/uploads/` | BUG-0006 前的历史本地上传残留；**新上传不应再出现**；可清理孤儿文件 |

判断 Logo 是否有效：

1. 查 SQLite `brands.logo_object_key`。
2. 在 MinIO Console 或 `data/minio/tile-info-platform/{object_key}` 确认对象存在。
3. **不要**以 `data/uploads` 是否有同名文件作为上传成功与否的依据。

## 2. 手动清理规避（本地开发）

若仅需释放磁盘、消除混淆，可在确认无 DB 引用后手动删除 legacy uploads：

```bash
# 1. 确认当前 brands 引用的 key（示例）
sqlite3 data/sqlite/tile-info-platform.db \
  "SELECT logo_object_key FROM brands WHERE logo_object_key IS NOT NULL;"

# 2. 删除 BUG-0006 前写入的 brands/logos 孤儿目录（保留 .gitkeep 结构）
rm -rf data/uploads/original/

# 3. 验证新上传仍只出现在 MinIO
# 管理端上传 Logo → 检查 data/minio/tile-info-platform/... 有对象
# 且 data/uploads/original/ 不应再新增文件
```

**风险**：若误删仍被 DB 引用且**仅**存在于 uploads（未迁移到 MinIO）的文件，会导致该 Logo 404。当前环境实测有效 key 均在 MinIO，uploads 下 6 个 PNG 均为孤儿，可安全删除。

## 3. 验收规避

在正式修复前，对象存储相关验收应区分：

| 检查项 | 当前状态 |
|---|---|
| 新上传写入 MinIO | ✅ 已通过（BUG-0006） |
| 品牌 Logo 展示 | ✅ 已通过（BUG-0007） |
| `data/uploads` 无业务孤儿 | ❌ 本 BUG 未通过 |
| 文档澄清双目录职责 | ❌ 本 BUG 未通过 |
| UPLOAD_DIR 挂载/配置收敛 | ❌ 本 BUG 未通过 |

## 4. 无产品内规避

Web 管理端与 API 无开关可「隐藏」双目录问题；需通过运维清理与文档/配置收敛解决。不建议在应用层增加对 `data/uploads` 的读取回退，以免重新引入双轨存储。

## 5. 建议

进入 `/bug-review` 评审通过后，通过 `fix-*` OpenSpec Change 实施清理脚本、文档更新与 Docker 配置收敛。
