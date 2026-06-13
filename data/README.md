---
purpose: 数据目录说明
content: 说明本地开发数据、样例数据、上传文件、SQLite文件、视频处理产物的存放规则
source: AI自动生成初稿，项目团队确认
update_method: 新增数据类型、上传目录、视频处理流程、数据库持久化方式时由AI辅助更新，人工Review
note: data目录用于本地开发、演示、测试样例和运行时数据；生产环境应使用正式对象存储和持久化卷
---

# data 目录规范

`data/` 用于承载本地开发、演示、测试样例、上传文件和运行时数据。该目录不是业务源码目录，也不是正式文档目录。

## 目录说明

```text
data/
├── sqlite/                  # SQLite本地数据库文件，运行时生成，不提交真实db
├── uploads/                 # 本地上传文件缓存，运行时生成，不提交真实客户数据
│   ├── images/              # 瓷砖图片上传缓存
│   ├── videos/              # 瓷砖视频上传缓存
│   └── documents/           # 规格书、质检报告等文档上传缓存
├── processed/               # 处理后产物
│   ├── videos/              # 视频转码、压缩、格式化产物
│   └── thumbnails/          # 图片/视频封面图
├── samples/                 # 可提交的脱敏样例数据
│   ├── images/              # 样例瓷砖图片
│   └── videos/              # 样例瓷砖视频
├── runtime/                 # 本地运行日志、缓存等临时数据
├── tmp/                     # 临时文件
└── minio/                   # 可选：本地MinIO文件映射目录，默认Docker卷不使用此目录
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
