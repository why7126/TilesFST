## 1. 配置与 Key 生成

- [x] 1.1 更新 `app/core/config.py`：新增 `minio_prefix_images`（`MINIO_PREFIX_IMAGES`，默认 `images/`）；文档化 `minio_prefix_original` 为 deprecated
- [x] 1.2 更新 `build_object_key()`：移除 `{YYYY}/{MM}`；形态 `{prefix}/{tenant}/{resource_type}/{uuid}.{ext}`
- [x] 1.3 更新 `build_upload_object_key()` / `storage.py`：从 settings 读取 prefix，禁止新上传硬编码 `original`

## 2. 上传 API 映射

- [x] 2.1 `upload_image`：`images` + `user/avatars`
- [x] 2.2 `upload_brand_logo`：`images` + `brands/logos`
- [x] 2.3 `upload_tile_image`：`images` + `tiles/{id|pending}`（去掉 `/images` 后缀）
- [x] 2.4 `upload_tile_video`：保持 `videos` + `tiles/{id|pending}`（仅受益于去日期分片）
- [x] 2.5 确认四 API 响应仍为 `{ object_key, url: "/media/{object_key}" }`

## 3. 迁移脚本

- [x] 3.1 实现 `scripts/migrate_object_keys.py`：`--dry-run` / `--apply`
- [x] 3.2 覆盖四类 DB 字段：`users.avatar_object_key`、`brands.logo_object_key`、`tile_images.object_key`、`tile_videos.object_key`
- [x] 3.3 MinIO copy → verify → delete 旧 Key；DB 缺失对象 MUST 报错中止（AC-022）
- [x] 3.4 脚本 docstring / `--help` 含 backup 与回滚说明

## 4. 测试

- [x] 4.1 更新 `test_upload_endpoints_store_expected_minio_prefixes` 等 pytest 断言为新前缀
- [x] 4.2 单元测试：Key 不含 `/20` 年月段；头像/Logo/SKU 路径形态
- [x] 4.3 迁移脚本 dry-run 集成测试（fixtures 或 mock MinIO）
- [x] 4.4 运行 `cd src/backend && uv run pytest`

## 5. 文档与配置

- [x] 5.1 更新 `rules/object-storage.md`：语义前缀、`original/` deprecated、新 Key 形态
- [x] 5.2 更新 `docs/07-object-storage-strategy.md` 上传入口对照表
- [x] 5.3 同步根目录 `.env.example`、`src/backend/.env.example`、`src/backend/.env.docker`（`MINIO_PREFIX_IMAGES` 等）
- [x] 5.4 更新 `data/README.md` 媒体排查示例 Key

## 6. Docker 冒烟

- [x] 6.1 `./scripts/docker-up.sh`：上传 Logo + 访问 `/media/...` 200
- [x] 6.2 迁移 dry-run 在 Docker 环境可执行

## 7. 追溯

- [x] 7.1 更新 `issues/requirements/archive/REQ-0012-object-storage-key-layout/trace.md`（openspec_changes、status）
- [x] 7.2 勾选 `issues/requirements/archive/REQ-0012-object-storage-key-layout/acceptance.md` 对应 AC（apply 完成后）

## 8. 归档准备

- [x] 8.1 本文件全部 `[x]` 后执行 `/opsx-archive update-object-storage-key-layout`
