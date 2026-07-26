---
change_id: fix-upload-proxy-timeout-config
status: in_progress
created_at: 2026-07-23 09:09:35
updated_at: 2026-07-23 09:37:50
source_bug: BUG-0081-prod-cos-video-upload-fails
related_requirement:
sprint: sprint-011
---

# Trace - fix-upload-proxy-timeout-config

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | BUG-0081-prod-cos-video-upload-fails | 生产环境腾讯 COS 视频上传 99% 后返回 504，但 COS 中已有对象 |

## 决策

| 时间 | 决策 | 说明 |
|---|---|---|
| 2026-07-23 09:09:35 | 创建 fix Change | 使用 `fix-upload-proxy-timeout-config`，聚焦上传反代超时、Nginx 内外层配置和环境变量化 |
| 2026-07-23 09:17:23 | 纳入 sprint-011 | 作为 sprint-011 唯一正式修复范围，容量估算 3.0 人天 |
| 2026-07-23 09:37:50 | 应用容器内上传反代修复 | Web 镜像改用 `src/web/nginx.conf.template` 运行时渲染，上传路径默认 `512m`、`600s`、`proxy_request_buffering off`，Compose 可用 `UPLOAD_*` 覆盖 |
| 2026-07-23 09:37:50 | 同步外层 HTTPS 反代指引 | `docs/02-deployment.md` 补充 `/api/v1/admin/uploads/` 外层 Nginx 专用 location、`nginx -t`、reload 与 Web 容器重建步骤 |

## 验证记录

| 时间 | 验证 | 结果 |
|---|---|---|
| 2026-07-23 09:37:50 | `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py` | 12 passed, 1 warning |
| 2026-07-23 09:37:50 | `openspec validate fix-upload-proxy-timeout-config` | passed |
| 2026-07-23 09:37:50 | `docker compose config --services` | `backend`, `web` |
| 2026-07-23 09:37:50 | `docker compose -f docker-compose.prod.yml config --services` | `minio`, `backend`, `web`, `minio-init` |
| 2026-07-23 09:37:50 | `docker compose -f docker-compose.prod.external.yml config --services` | `backend`, `web` |
| 2026-07-23 09:40:30 | `docker compose build web` | passed；Vite 仅输出既有 CSS at-rule/chunk-size warning |
| 2026-07-23 09:40:30 | `docker run --rm --add-host backend:127.0.0.1 projecttilesfst-web nginx -t` | passed；模板渲染后 Nginx 配置语法通过 |

生产现场同类视频上传 smoke 尚未在本机执行，需部署后确认：合法视频返回 200、COS 对象存在、返回 `/media/{object_key}` 可读取、SKU 表单保存闭环，且不再出现浏览器 504、外层 504 或容器 Nginx 60 秒后 499。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-23 09:09:35 | /bug-opsx | 由 BUG-0081 创建 OpenSpec Change |
| 2026-07-23 09:17:23 | /sprint-propose | 纳入 sprint-011 正式范围 |
| 2026-07-23 09:37:50 | /opsx-apply | 完成本地可验证项：上传反代超时环境变量化、Web Nginx 上传专用 location、部署文档与测试；生产 smoke 待执行 |
