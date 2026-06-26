---
purpose: 数据目录说明
content: 说明本地开发数据、样例数据、上传文件、SQLite文件、视频处理产物的存放规则
source: AI自动生成初稿，项目团队确认
update_method: 新增数据类型、上传目录、视频处理流程、数据库持久化方式时由AI辅助更新，人工Review
note: data目录用于本地开发、演示、测试样例和运行时数据；生产环境应使用正式对象存储和持久化卷
---

# data 目录规范

`data/` 用于承载本地开发、演示、测试样例和运行时数据。该目录不是业务源码目录，也不是正式文档目录。

**业务媒体正式存储**：MinIO 单桶 `MINIO_BUCKET`（本地 Docker 物理落盘为 `data/minio/tile-info-platform/`）。

**`data/uploads`**：BUG-0006 之前本地上传链路的历史兼容目录；对象存储迁移后 **新上传不得再写入此处**。若存在迁移前残留，使用清理脚本处理（见下文）。

## 目录说明

```text
data/
├── sqlite/                  # SQLite本地数据库文件，运行时生成，不提交真实db
├── uploads/                 # 历史本地上传兼容目录（非正式业务存储；迁移后不应新增业务文件）
│   ├── images/              # 占位目录（.gitkeep）
│   ├── videos/              # 占位目录（.gitkeep）
│   └── documents/           # 占位目录（.gitkeep）
├── minio/                   # Docker Compose 本地 MinIO 持久化卷（桶内对象增长属预期）
│   └── tile-info-platform/  # 默认 MINIO_BUCKET 物理存储
├── processed/               # 处理后产物
│   ├── videos/              # 视频转码、压缩、格式化产物
│   └── thumbnails/          # 图片/视频封面图
├── samples/                 # 可提交的脱敏样例数据
│   ├── images/              # 样例瓷砖图片
│   └── videos/              # 样例瓷砖视频
├── runtime/                 # 本地运行日志、缓存等临时数据
└── tmp/                     # 临时文件
```

## Legacy uploads 清理（BUG-0008 后）

对象存储迁移（BUG-0006）完成后，若 `data/uploads/` 下仍有与数据库 `object_key` 无关联的业务媒体孤儿文件，可执行：

```bash
# 预览待删除孤儿文件（默认 dry-run）
python scripts/clean_legacy_uploads.py

# 实际删除孤儿文件（保留 .gitkeep）
python scripts/clean_legacy_uploads.py --apply

# CI / 本地检查：无残留 exit 0，有残留 exit 1
python scripts/clean_legacy_uploads.py --check-only
```

脚本依据 SQLite 中 `brands.logo_object_key`、`users.avatar_object_key`、`tile_images.object_key`、`tile_videos.object_key` 构建引用白名单，**不会**删除 MinIO 对象。

## 媒体排查原则

1. 查 DB 中的 `object_key` / `logo_object_key` / `avatar_object_key`。
2. 在 MinIO Console 或 `data/minio/tile-info-platform/{object_key}` 确认对象存在。
3. **不要**以 `data/uploads` 是否有同名文件判断上传是否成功。

## 提交规则

- 可以提交 `.gitkeep`、README、脱敏样例数据。
- 禁止提交真实客户图片、真实客户视频、真实门店数据、真实数据库文件。
- 禁止提交 `.db`、`.sqlite`、`.sqlite3` 文件。
- 禁止提交包含密钥、手机号、客户信息的文件。

## AI更新规则

AI新增上传能力、视频处理能力、数据导入导出能力时，必须同步检查：

- `.gitignore`
- `.env.example`
- `docker-compose.yml`
- `rules/data-management.md`
- `rules/media.md`
- `docs/04-database-design.md`
- `docs/06-video-asset-management.md`
- `openspec/specs/media-assets/spec.md`
