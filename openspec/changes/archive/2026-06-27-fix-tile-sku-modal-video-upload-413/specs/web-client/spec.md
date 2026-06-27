## ADDED Requirements

### Requirement: Docker Web 反代必须允许大文件上传

Docker Compose 部署的 Web 容器（Nginx 反代 `/api/` 至 backend）MUST 配置 `client_max_body_size` 不小于 `max(MAX_IMAGE_SIZE_MB, MAX_VIDEO_SIZE_MB)`。当运营或部署人员调大 `.env` 中图片或视频上传上限时，MUST 同步提高 Nginx `client_max_body_size` 并重建 Web 镜像，否则大文件上传 MAY 在代理层失败并返回 413。

#### Scenario: Nginx body 限制与 env 对齐

- **GIVEN** 根目录 `.env` 中 `MAX_VIDEO_SIZE_MB=500` 且 `MAX_IMAGE_SIZE_MB=20`
- **WHEN** 检查 `src/web/nginx.conf` 随本 change 部署后的配置
- **THEN** `client_max_body_size` MUST ≥ 500MB（或项目文档声明的等价值）
- **AND** `docs/standards/file-upload.md` MUST 说明该对齐关系

#### Scenario: 重建 Web 镜像后大文件上传可用

- **GIVEN** 已修改 `nginx.conf` 并完成 Web 镜像重建与容器重启
- **WHEN** 用户经 `localhost:3000` 上传大于 1MB 的合法 MP4
- **THEN** 请求 MUST 到达后端 FastAPI
- **AND** 成功时 MUST 返回 JSON 统一响应结构（非 Nginx 默认 HTML 413 页）
