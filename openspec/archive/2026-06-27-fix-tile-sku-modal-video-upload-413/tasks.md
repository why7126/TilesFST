## 1. 准备与门禁

- [x] 1.1 阅读 `BUG-0020-tile-sku-modal-video-upload-413` 的 bug.md、root-cause.md、acceptance.md、review.md
- [x] 1.2 确认 BUG 状态为 `approved` 或 `in_sprint`
- [x] 1.3 确认与 `BUG-0018` / `fix-tile-sku-modal-video-upload-display` scope 边界（0020=413+env；0018=UI 回显）

## 2. Nginx 与部署

- [x] 2.1 `src/web/nginx.conf` 设置 `client_max_body_size` ≥ `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`（默认 `512m`）
- [x] 2.2 更新 `docs/standards/file-upload.md` 说明 Nginx 与 env 对齐及 Web 镜像重建要求
- [x] 2.3 若需更新 `docs/02-deployment.md` 中 Web 大文件上传说明

## 3. 后端 env 上传限制

- [x] 3.1 `config.py`：`MAX_IMAGE_SIZE_MB`、`MAX_VIDEO_SIZE_MB`、`ALLOWED_IMAGE_TYPES`、`ALLOWED_VIDEO_TYPES`
- [x] 3.2 `uploads.py`：MIME 校验与 `save_upload_file` 分别传入图片/视频大小上限
- [x] 3.3 `storage.py`：`save_upload_file(file, object_key, max_size_mb)`；扩展视频扩展名映射
- [x] 3.4 同步根目录 `.env.example`、`src/backend/.env.docker`、`src/backend/.env.example`
- [x] 3.5 移除或废弃未接入的 `MAX_UPLOAD_SIZE_MB` 作为唯一上限（若仍存在）

## 4. 测试

- [x] 4.1 pytest：图片/视频超限返回 400 + `FILE_SIZE_EXCEEDED`
- [x] 4.2 pytest：可配置 `ALLOWED_VIDEO_TYPES`（如 `video/quicktime`）
- [x] 4.3 pytest：`Settings` 解析逗号分隔 MIME 列表
- [x] 4.4 运行 `cd src/backend && uv run pytest tests/test_admin_brands.py tests/test_upload_settings.py`

## 5. Docker 验收与追溯

- [x] 5.1 重建 Web 镜像：`docker compose build web`（或项目等价脚本）
- [x] 5.2 手工：经 `localhost:3000` 上传 2MB～50MB MP4 → 200，非 413
- [x] 5.3 对照 BUG acceptance AC-001～AC-008，记录于本 change `trace.md`
- [x] 5.4 更新 `BUG-0020-tile-sku-modal-video-upload-413/trace.md` 中 `openspec_changes` 状态
- [x] 5.5 评估 `docs/knowledge-base/incidents/`（基础设施缺口，通常不需要）
