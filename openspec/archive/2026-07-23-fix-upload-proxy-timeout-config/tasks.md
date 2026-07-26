## 1. 配置方案

- [x] 1.1 确认 Web 容器 Nginx 使用模板渲染、启动脚本或等价机制支持上传超时环境变量。
- [x] 1.2 定义上传相关环境变量默认值，至少覆盖 body size、client body timeout、proxy send/read timeout、send timeout 和 request buffering。
- [x] 1.3 确保默认值不低于生产视频上传建议：超时默认 600 秒，body size 默认不小于 512m。

## 2. Docker Web Nginx 修复

- [x] 2.1 在通用 `/api/` 前增加 `/api/v1/admin/uploads/` 上传专用 location。
- [x] 2.2 保留现有代理头，确保 `/api/`、`/media/`、`/docs`、`/redoc`、`/openapi.json` 和 SPA fallback 不回退。
- [x] 2.3 评估并配置 `proxy_request_buffering off`，若不启用需在 design/trace 说明理由。
- [x] 2.4 更新生产 Compose Web 服务环境变量，确保默认值可覆盖。

## 3. 文档同步

- [x] 3.1 更新 `.env.example`，说明上传反代超时变量用途、默认值和生产安全边界。
- [x] 3.2 更新 `docs/02-deployment.md`，补充外层 HTTPS Nginx 上传 location 与重载步骤。
- [x] 3.3 更新 `docs/standards/file-upload.md`，补充反代超时、request buffering 与 99%/504 诊断。
- [x] 3.4 按需更新 `docs/07-object-storage-strategy.md` 或对象存储说明，记录 COS 已写入但响应超时导致孤儿对象的运维检查。

## 4. 测试与验证

- [x] 4.1 增加 Nginx 配置或模板渲染测试，覆盖默认 600 秒和环境变量覆盖。
- [x] 4.2 运行 `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py`。
- [x] 4.3 若修改 Web 镜像启动脚本，执行 Web 构建或等价配置校验。
- [x] 4.4 生产或生产等价 smoke：上传同类视频返回 200，COS 对象存在，SKU 表单保存闭环。
- [x] 4.5 确认同类上传不再出现浏览器 504、外层 504、容器 Nginx 60 秒后 499。

## 5. 追溯与知识沉淀

- [x] 5.1 更新 `BUG-0081` trace、Change trace 与验收证据。
- [x] 5.2 修复完成后评估是否沉淀到 `docs/knowledge-base/incidents/`；若不新增，需在验收输出说明理由。
