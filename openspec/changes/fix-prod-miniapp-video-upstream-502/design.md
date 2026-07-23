## 背景

`BUG-0076` 的用户现象是生产微信小程序视频区域显示「视频暂时无法播放」。小程序页面中该文案来自 video 组件加载失败兜底，不直接区分是视频 URL 无效、媒体资源不可读、对象存储异常、微信域名/格式限制，还是生产入口整体不可用。

探索阶段已获得更强的生产入口证据：生产域名根路径、`/api/v1/health` 和 `/api/v1/miniapp/skus/1` 均返回 Nginx `502 Bad Gateway`。这说明修复应优先从生产反代和运行时链路切入，而不是先修改小程序播放器。

## 根因假设

### 已确认事实

- 小程序视频失败会显示「视频暂时无法播放」。
- 生产域名在探索时对根路径、健康检查和 SKU 接口均返回 Nginx 502。
- 当前仓库中 SKU 详情视频媒体查询使用 `tile_videos.object_key`，服务层生成 `/media/{object_key}`，已有测试覆盖 `object_key` 与 `file_name` 不同的场景。

### 待确认根因

1. 外层 Nginx upstream 指向的 Web 容器端口不可用。
2. Web 容器内 Nginx 到 Backend `backend:8000` 不可达。
3. Backend 容器未运行、启动失败、DB/对象存储配置阻塞启动。
4. 整体入口恢复后，实际视频 `/media/{object_key}` 仍因对象不存在、权限、MIME/编码、Range 请求或微信合法域名失败。

## 修复方案

### 1. 生产入口与反代恢复

- 检查外层 Nginx upstream 是否指向正确的 `HOST_PORT_WEB`。
- 检查 `tilesfst-web` 和 `tilesfst-backend` 容器状态、端口映射和 Docker 网络。
- 验证 Web 容器 Nginx 对 `/api/`、`/media/` 和 `/openapi.json` 的代理仍指向 backend。
- 验证 `https://tilesfst.wjoyhappy.site/` 和 `https://tilesfst.wjoyhappy.site/api/v1/health` 不再返回 502。

### 2. 小程序 SKU 与媒体链路验证

- 使用实际反馈 SKU ID 请求 `/api/v1/miniapp/skus/<SKU ID>`。
- 确认视频媒体项 `media[].url` 不为空，且为 `/media/{object_key}` 或完整安全 URL。
- 访问实际视频 `/media/{object_key}`，确认 HTTP 200、Content-Type 为可播放视频类型，响应不是 Nginx 502 HTML。
- 真机打开同一 SKU 页面播放视频，确认不再显示「视频暂时无法播放」。

### 3. 代码修复分支

若生产入口恢复后仍存在视频播放失败，再按证据进入对应代码修复分支：

- 后端返回错误 URL：修复 SKU 详情媒体 URL 组装，并保留 `BUG-0069` 回归测试。
- `/media/` 返回 404/502：修复对象存储读取、错误映射或对象 key 迁移。
- 资源 200 但真机失败：检查 Content-Type、视频编码、HTTPS 证书、微信合法域名和 Range 请求支持。

## 测试策略

- 保留并运行 SKU 视频 URL 回归测试：
  - `tests/test_miniapp_home.py::test_miniapp_sku_detail_returns_public_media_recommendations_and_share`
  - `tests/test_miniapp_static.py::test_miniapp_sku_detail_page_covers_media_favorite_share_and_empty_states`
- 如修改部署脚本或 Nginx 配置，补充配置静态检查或 Docker smoke。
- 如修改媒体读取，补充 `/media/{object_key}` 200、404、非法 object_key、对象存储不可用测试。
- 生产验收必须包含 curl 证据和小程序真机截图/录屏。

## API / Orval

默认不需要 API schema 或 Orval 变更。若实现阶段新增健康检查字段、媒体错误响应结构、SKU 详情字段或上传/媒体接口契约，必须同步 OpenAPI、Orval、API 文档和测试。

## 风险

- 仅恢复生产入口可能掩盖实际单个视频对象缺失问题，因此必须继续验证实际反馈 SKU 和实际视频 URL。
- 若外层 Nginx 与 Docker Web Nginx 双层代理配置不一致，可能出现 Web 首页恢复但 `/api/` 或 `/media/` 仍失败。
- 若后端启动失败由生产环境变量导致，修复时不得提交真实密钥或生产连接串。
