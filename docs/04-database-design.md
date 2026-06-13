---
purpose: 数据库文档
content: SQLite表结构设计
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
---

# 数据库设计


## 核心表

- `tiles`：瓷砖主表
- `tile_categories`：分类表
- `tile_specs`：规格表
- `tile_images`：图片表
- `users`：内部员工用户表

## 设计原则

SQLite 存储结构化数据，MinIO 存储图片文件。


## V4媒体资产表建议

建议新增 `tile_media` 表统一管理图片、视频和文档：

| 字段 | 说明 |
|---|---|
| id | 媒体ID |
| tile_id | 瓷砖ID |
| media_type | image/video/document |
| bucket_name | MinIO存储桶 |
| object_key | 对象Key |
| mime_type | MIME类型 |
| file_size | 文件大小 |
| width | 图片/视频宽度 |
| height | 图片/视频高度 |
| duration | 视频时长 |
| cover_object_key | 视频封面对象Key |
| sort_order | 排序 |
| created_at | 创建时间 |
