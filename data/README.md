---
purpose: 数据目录说明
content: 说明本地开发数据、样例数据、上传文件、SQLite文件、视频处理产物、AI 使用量事实的存放规则
source: AI自动生成初稿，项目团队确认
update_method: 新增数据类型、上传目录、视频处理流程、数据库持久化方式时由AI辅助更新，人工Review
note: data目录用于本地开发、演示、测试样例和运行时数据；生产环境应使用正式对象存储和持久化卷
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-11 18:51:16
---

# data 目录规范

`data/` 用于承载本地开发、演示、测试样例和运行时数据。该目录不是业务源码目录，也不是正式文档目录。

**业务媒体正式存储**：MinIO 单桶 `MINIO_BUCKET`（本地 Docker 物理落盘为 `data/minio/tile-info-platform/`）。

**本地日志审计数据**：REQ-0024 新增 `request_logs` 与 `usage_events` 表，随 SQLite 运行时数据库一起位于 `data/sqlite/`。这些日志仅用于本地开发、演示和排查，不得提交真实运行数据库文件。

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
├── ai-usage/                # 从本地 Codex session 派生的脱敏 AI 命令使用量事实
└── tmp/                     # 临时文件
```

## AI 使用量事实源

`data/ai-usage/` 只保存从本地 Codex session JSONL 派生的脱敏事实，不保存原始 prompt、系统/developer 指令、技能全文、工具输出正文、本机绝对路径、密钥、`.env` 内容或客户数据。

可提交：

- `data/ai-usage/README.md`
- 脱敏样例：`data/ai-usage/samples/**`
- 经人工确认安全的 Sprint 聚合快照：`data/ai-usage/sprints/<sprint-id>.json`

仅本地保留：

- 原始 `~/.codex/sessions/**/*.jsonl`
- `data/ai-usage/raw/**`
- `data/ai-usage/local/**`
- 任何包含 prompt、工具输出正文、真实路径、密钥或客户数据的中间文件

提取命令示例：

```bash
python scripts/extract-ai-usage.py --session-jsonl ~/.codex/sessions/<session>.jsonl --sprint sprint-006
python scripts/generate-sprint-fact-sheet.py --sprint sprint-006 --json
```

`/sprint-exps` 优先读取 `data/ai-usage/sprints/<sprint-id>.json` 的真实快照；缺失时必须明确标注“无精确 token 计量”，只能做估算分析。

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

## 日志审计排查原则

1. API 请求链路优先查 `request_logs.request_id`，前端或接口响应头中的 `x-request-id` 可用于定位。
2. 产品使用行为优先查 `usage_events.event_name`、`actor_user_id`、`page_path` 与 `metadata`。
3. `metadata` 只能保存脱敏后的业务上下文，不得写入密码、Token、Authorization、密钥、客户隐私或真实联系方式。
4. 本地 `data/sqlite/*.db`、`*.sqlite`、`*.sqlite3` 仍属于运行时数据，禁止提交。

示例 Key（REQ-0012 新布局）：

```text
images/default/brands/logos/<uuid>.webp
images/default/user/avatars/<uuid>.png
videos/default/tiles/pending/<uuid>.mp4
```

存量 `original/.../{YYYY}/{MM}/...` 布局迁移：

```bash
python scripts/migrate_object_keys.py --dry-run
python scripts/migrate_object_keys.py --apply
```

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
