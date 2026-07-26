## Why

`BUG-0081-prod-cos-video-upload-fails` 已评审通过。生产环境管理端上传 SKU 视频时，浏览器请求 `POST https://tilesfst.wjoyhappy.site/api/v1/admin/uploads/tile-videos?tile_id=3` 进度卡在 99%，最终返回 `504 Gateway Time-out`，但腾讯 COS Bucket 中已经出现对应视频对象。

现场证据显示容器 Nginx 将请求体缓冲到 `/var/cache/nginx/client_temp/...`，同一上传请求约 60 秒后记录为 `499`。这说明 COS 写入已经成功或接近成功，失败发生在上传接口成功响应返回浏览器的反代链路。当前外层 HTTPS Nginx 与容器内 Web Nginx 均没有 `/api/v1/admin/uploads/` 上传专用超时；外层 443 server 的 `client_max_body_size 100m` 也小于项目默认 `MAX_VIDEO_SIZE_MB=500`。

该缺陷会让管理端视频上传在业务上失败，同时在 COS 中留下无法被 SKU 业务数据引用的孤儿对象。需要通过 OpenSpec Change 正式修复容器内上传反代配置，并将上传超时时间环境变量化，方便不同生产环境按网络和对象存储性能调整。

## What Changes

- 为 Docker Web Nginx 增加 `/api/v1/admin/uploads/` 上传专用 location，配置大文件上传 body size、读写超时和请求缓冲策略。
- 将上传反代超时时间做成部署环境变量或等价部署参数，默认建议 600 秒。
- 同步 `.env.example`、生产 Compose、部署文档和文件上传标准，说明外层 HTTPS 反代也必须配置不短于内层的上传超时。
- 补充配置/部署测试，验证 Nginx 上传 location、默认超时和环境变量覆盖能正确生效。
- 保持上传 API 路径、请求/响应 Schema、对象 Key、鉴权和受控 `/media/{object_key}` 读取策略不变。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `deployment`: 增加大文件上传反代超时、环境变量化配置、外层 HTTPS 反代同步要求和 Docker Web Nginx 上传 location 验收。
- `object-storage`: 强化管理端上传写入对象存储后的响应可靠性，避免 COS 已写入但上传接口因反代超时返回失败。

## Impact

- **api:** 上传 API 路径和响应结构不变，预期不需要 Orval；若实现中改变 Schema，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和测试。
- **backend:** 上传服务逻辑不变；如后续发现需要流式上传或对象存储客户端超时参数，必须纳入任务和测试。
- **web/admin:** 容器内 Web Nginx 配置会新增上传专用 location；管理端上传体验应不再卡 99% 后 504。
- **miniapp:** 不直接影响小程序；媒体受控读取和对象存储策略保持不变。
- **database:** 无数据库结构变更。
- **object-storage:** 继续使用单 Bucket + `videos/` 前缀；减少上传失败造成的 COS 孤儿对象。
- **deployment:** 需要更新 `.env.example`、Docker Compose Web 服务环境变量、`src/web/nginx.conf` 或模板/入口脚本，以及外层 Nginx 配置说明。
- **tests:** 需补充 Nginx 配置或模板渲染测试，并运行对象存储/部署相关测试。
- **docs:** 需同步 `docs/02-deployment.md`、`docs/standards/file-upload.md`、`docs/07-object-storage-strategy.md` 或相关说明。

## Rollback Plan

如修复后 Web 静态资源、`/api/`、`/media/`、Swagger 代理或上传接口出现异常，应回滚 Docker Web Nginx 上传专用 location、环境变量渲染脚本或 Compose 环境变量到上一版配置。回滚后保留 `BUG-0081` 为未解决状态，并继续使用生产外层 Nginx 手工超时配置作为临时规避。
