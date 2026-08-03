---
change_id: fix-media-thumbnail-generation
created_at: 2026-08-01 08:05:25
updated_at: 2026-08-01 08:05:25
status: applied
---

# Implementation Notes

## Summary

- 后端媒体模块新增 `generate_image_thumbnail()`，使用 Pillow 对 JPG、PNG、WebP 进行解码、EXIF 方向修正、等比缩小和重编码。
- SKU 图片上传链路在写入原图后生成同目录 `.thumb` 对象；缩略图生成失败时记录告警并跳过 `.thumb` 写入，不复制原图 bytes，读取层继续通过缺失缩略图回退原图。
- pending SKU 图片正式化时，如源 `.thumb` 缺失，尝试从原图生成真实缩略图；异常图片不复制原图作为缩略图。
- 历史小程序商品卡片图片审计脚本支持识别缺失、同 size、同 bytes 的疑似无效 `.thumb`，dry-run 不写对象，execute 幂等重生成。

## Dependencies

- 新增后端运行依赖：`Pillow>=10.4.0`，锁定解析为 `pillow==12.3.0`。
- 后端 Docker 镜像构建使用 `uv sync --locked --no-dev --no-install-project`，已验证镜像内可导入 `PIL`。

## Compatibility

- API 请求、响应字段和错误码无变化，不需要同步 OpenAPI、Orval 或 `docs/03-api-index.md`。
- 数据库表结构、迁移和 Pydantic Schema 无变化，不需要同步 `docs/04-database-design.md`。
- 环境变量无变化，不需要同步 `.env.example`。
- 对象存储仍使用单 Bucket、同目录 `.thumb` key、后端 `/media/{object_key}` 受控读取和缺失缩略图回退。

## Validation

- 聚焦 pytest：14 passed。
- 历史审计 dry-run：输出聚合统计、失败原因摘要和 `items`，未输出密钥、Authorization header、Cookie、`.env` 内容或本机路径。
- 后端 Docker build：`tilesfst-backend:bug0100-thumbnail-check` 构建成功。
- Docker 依赖验证：容器内 `import PIL` 输出 `12.3.0`。
