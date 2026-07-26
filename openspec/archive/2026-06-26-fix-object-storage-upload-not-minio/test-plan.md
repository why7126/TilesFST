---
change_id: fix-object-storage-upload-not-minio
bug_id: BUG-0006-object-storage-upload-not-minio
status: proposed
created_at: 2026-06-26 13:47:54
---

# 测试计划

## 1. 自动化测试

| 类型 | 建议命令 | 覆盖 |
|---|---|---|
| Backend unit / pytest | `cd src/backend && uv run pytest tests/test_admin_brands.py tests/test_admin_tile_skus.py tests/test_auth.py` | 品牌 Logo、SKU 图片/视频、头像上传回归 |
| Media storage tests | `cd src/backend && uv run pytest tests/ -k "upload or media or storage"` | MinIO 写入、受控读取、非法 object_key、MinIO 不可用 |
| Full backend smoke | `cd src/backend && uv run pytest tests/` | API 与权限回归 |

测试实现可使用 fake MinIO client 或 monkeypatch storage adapter，避免依赖真实密钥。Docker 验证可作为集成验收补充。

## 2. 手工 / Docker 验证

1. 启动 Docker Compose。
2. 确认 `minio-init` 已创建 `tile-info-platform`。
3. 使用管理端上传品牌 Logo、SKU 图片、SKU 视频或头像。
4. 打开 MinIO Console 或使用 `mc ls` 查看对象是否位于 `tile-info-platform`。
5. 访问返回的 `/media/{object_key}` 或等价 URL，确认可读取内容。
6. 尝试非法 object_key，例如包含 `..` 或绝对路径，确认返回 4xx。

## 3. 回归范围

- `/admin/brands` Logo 上传、列表展示、编辑弹窗回显。
- `/admin/users` 头像上传。
- `/admin/tile-skus` SKU 图片与视频上传、保存、回显。
- 既有 MIME 校验、权限边界、错误结构。

## 4. 不做项

- 不新增媒体元数据统一表。
- 不实现视频转码、多清晰度或自动封面。
- 不自动迁移历史 `data/uploads` 文件，除非实现阶段另行确认。
