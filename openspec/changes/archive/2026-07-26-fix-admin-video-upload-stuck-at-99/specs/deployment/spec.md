## ADDED Requirements

### Requirement: 生产环境上传路径代理配置

生产部署 MUST 对管理端上传路径 `/api/v1/admin/uploads/` 提供与业务上传上限匹配的代理配置。外层 HTTPS Nginx、容器内 Web Nginx、CDN、网关或等价反代 MUST 避免使用默认 60 秒级 upstream 超时截断大文件上传响应链路。上传路径的请求体大小、客户端 body timeout、upstream send/read timeout 和请求缓冲策略 MUST 可被部署验证。

#### Scenario: 容器内 Web Nginx 上传路径配置生效

- **WHEN** Web 容器使用生产镜像或生产等价镜像启动
- **THEN** 运行中的 Nginx 配置 MUST 包含 `/api/v1/admin/uploads/` 专用 location
- **AND** 该 location MUST 配置不低于业务上传上限的 `client_max_body_size`
- **AND** 该 location MUST 配置上传专用 `proxy_send_timeout`、`proxy_read_timeout`、`client_body_timeout` 与 `send_timeout`
- **AND** 验收记录 MUST 说明 `proxy_request_buffering` 策略是否为 `off` 或等价可接受配置。

#### Scenario: 外层 HTTPS 反代上传路径配置生效

- **WHEN** 生产流量经外层 HTTPS Nginx、CDN 或网关进入 Web / backend
- **THEN** 外层代理 MUST 对 `/api/v1/admin/uploads/` 配置上传专用超时
- **AND** 上传合法视频时 MUST NOT 因默认 60 秒 upstream 超时返回 504 或记录 499
- **AND** 若外层代理不由本仓库管理，部署验收记录 MUST 记录配置摘要、验证时间和负责人确认。

#### Scenario: 生产上传 smoke 覆盖 99% 问题

- **WHEN** 发布或修复涉及上传代理、Web 镜像、对象存储或 SKU 视频上传体验
- **THEN** 团队 MUST 执行一次生产或生产等价视频上传 smoke
- **AND** smoke MUST 记录浏览器 Network 状态码、请求总耗时、对象 key、对象存储存在性、`/media/{object_key}` 读取结果
- **AND** smoke MUST 确认管理端 SKU 表单能将上传视频加入列表并保存闭环
- **AND** smoke MUST 记录外层与容器内 Nginx/backend 日志中无同类 60 秒 499/504。
