---
created_at: 2026-07-21 13:00:21
updated_at: 2026-07-21 13:00:21
---

# 实现记录

## 影响范围

| 范围 | 结论 |
|---|---|
| API | 不变；上传接口和 `/media/{object_key}` 读取语义保持不变 |
| 数据库 | 不涉及；SQLite/MySQL schema 和 Pydantic 业务模型不变 |
| Web | 不涉及页面和 Orval 生成物；管理端仍使用后端上传与媒体 URL |
| 小程序 | 不涉及代码；仍通过后端返回的媒体 URL 读取 |
| 管理端 | 上传链路保持后端授权、MIME/大小校验和受控读取 |
| Orval | 不需要；没有新增或修改 API schema |
| Docker Compose | 已更新生产自建 MinIO 与外部对象存储 Compose 的对象存储环境变量 |
| 测试 | 已补充配置、对象存储客户端和 Compose 配置测试 |

## 环境变量收敛

后端应用侧统一使用 `OBJECT_STORAGE_*` 与 `OBJECT_STORAGE_PREFIX_*`。不再同时暴露 `MINIO_ENDPOINT`、`MINIO_ACCESS_KEY`、`MINIO_SECRET_KEY`、`MINIO_SECURE`、`MINIO_BUCKET` 或 `MINIO_PREFIX_*` 作为应用配置，避免同一含义存在两套变量。自建 MinIO 容器仍按官方镜像要求使用 `MINIO_ROOT_USER` / `MINIO_ROOT_PASSWORD`，其值由 `OBJECT_STORAGE_ACCESS_KEY` / `OBJECT_STORAGE_SECRET_KEY` 映射。

## 验证记录

| 类型 | 命令或方式 | 结果 |
|---|---|---|
| OpenSpec | `openspec validate "support-cloud-object-storage" --type change --strict` | 通过 |
| Workflow Sync dry-run | `python scripts/sync-workflow-status.py --event opsx.apply --change support-cloud-object-storage --sprint auto --dry-run` | 通过；纯技术治理 Change，Sprint skipped |
| Pytest | `uv run pytest src/backend/tests/test_upload_settings.py tests/test_media_storage.py tests/test_cloud_object_storage_deployment.py src/backend/tests/test_auth.py` | 22 passed |
| 外部对象存储 Compose | `docker compose -f docker-compose.prod.external.yml config --services`（示例 env） | 输出 `backend`、`web` |
| 自建 MinIO Compose | `docker compose -f docker-compose.prod.yml config --services`（示例 env） | 输出 `minio`、`minio-init`、`backend`、`web` |

## 生产等价 Smoke

未执行真实 COS/TOS/外部 MinIO 上传 smoke，因为当前环境没有真实云 bucket、region、endpoint、最小权限凭据和网络白名单。后续生产验证 MUST 使用运维预创建的 bucket，完成一次品牌 Logo 或 SKU 图片上传，并通过 `/media/{object_key}` 读取成功；记录时不得写入真实密钥。
