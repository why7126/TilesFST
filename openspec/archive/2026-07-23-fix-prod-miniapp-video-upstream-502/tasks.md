## 1. 生产故障定位

- [ ] 1.1 确认 `BUG-0076` 实际反馈页面路径、SKU/内容 ID、视频 object_key 或媒体 URL。
- [ ] 1.2 检查生产外层 Nginx upstream，确认 `tilesfst.wjoyhappy.site` 指向正确的 Web 容器宿主端口。
- [ ] 1.3 检查 `tilesfst-web`、`tilesfst-backend`、MinIO/COS 依赖和数据库连接状态。
- [ ] 1.4 验证生产根路径、`/api/v1/health`、实际 SKU 接口和实际 `/media/...` URL 不再返回 Nginx 502。

## 2. 反代与运行时修复

- [ ] 2.1 若外层 Nginx upstream 错误，修复 upstream 目标、端口或服务 reload 流程。
- [ ] 2.2 若 Web 容器反代错误，修复 `/api/`、`/media/`、`/openapi.json`、`/docs`、`/redoc` 的代理顺序，保持 SPA fallback 不吞后端路由。
- [ ] 2.3 若 Backend 容器启动失败，修复生产环境变量、DB 连接、对象存储连接或启动脚本问题，不提交真实密钥。
- [ ] 2.4 若 `/media/{object_key}` 读取失败，修复对象存储读取、对象 key、权限、MIME/Content-Type 或错误映射。

## 3. 小程序与媒体回归

- [ ] 3.1 验证实际 SKU 详情接口返回的视频 `media[].url` 不为空，且来自 `/media/{object_key}` 或完整安全 URL。
- [x] 3.2 验证小程序不直连 MinIO/COS 未授权地址，不硬编码生产视频 URL。
- [ ] 3.3 使用微信真机打开实际反馈页面，确认视频可加载并播放，不再显示「视频暂时无法播放」。
- [ ] 3.4 验证视频失败兜底仍可用：资源不存在或权限异常时页面提示可理解，其他媒体和 SKU 文本不受阻断。

## 4. 测试与文档

- [x] 4.1 运行 `uv run pytest tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states`。
- [ ] 4.2 如修改部署或 Nginx 配置，补充 Docker / 生产等价 smoke 记录。
- [ ] 4.3 如修改 API schema、错误码或响应字段，同步 OpenAPI、Orval、`docs/03-api-index.md` 和 API 测试。
- [ ] 4.4 如修改对象存储或 `/media/` 行为，同步对象存储文档、媒体文档和相关 pytest。
- [ ] 4.5 更新 `BUG-0076` trace、Change trace 与验收证据。
- [ ] 4.6 修复完成后评估是否需要沉淀到 `docs/knowledge-base/incidents/`；若无复用价值，在验收输出中说明不新增知识库条目。
