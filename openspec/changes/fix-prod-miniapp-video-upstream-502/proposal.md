## Why

`BUG-0076-prod-miniapp-video-temporarily-unplayable` 已评审通过。生产环境微信小程序中，视频区域显示「视频暂时无法播放」。`/bug-explore` 阶段在 `2026-07-21 14:44:47` 至 `2026-07-21 14:44:49` 只读访问生产域名时，根路径、`/api/v1/health` 与 `/api/v1/miniapp/skus/1` 均返回 `HTTP/1.1 502 Bad Gateway`，响应 Server 为 `nginx/1.26.2`。

当前仓库已包含 `BUG-0069` 的视频 URL 修复：小程序详情接口应基于 `tile_videos.object_key` 返回 `/media/{object_key}` 或完整安全 URL。本次缺陷更可疑的方向是生产外层 Nginx、Web/Backend upstream、容器端口映射或生产运行时依赖不可用。若生产域名整体或 `/media/` 反代返回 502，小程序 `<video>` 会触发错误兜底并显示「视频暂时无法播放」。

## What Changes

- 增加生产入口 smoke 要求：根路径、`/api/v1/health`、实际小程序 SKU 接口和实际 `/media/{object_key}` 必须不返回 Nginx 502。
- 明确生产反向代理、Docker Web Nginx 与 Backend `/media/` 受控读取链路的排查和验收边界。
- 保留小程序视频 URL 安全要求：小程序不得直连对象存储，仍消费后端返回的安全可播放 URL。
- 补充生产视频播放回归：实际反馈 SKU 的视频 URL 可读、Content-Type 可播放、真机不再显示「视频暂时无法播放」。
- 若修复仅为生产配置或部署恢复，验收记录必须说明未修改 API / DB / Web / 小程序代码，不需要 Orval；若发现代码缺陷，再按本 Change 的任务执行代码修复与测试同步。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `deployment`: 增加生产入口、健康检查、API 与媒体读取 smoke 验收，防止外层 Nginx / Web / Backend upstream 502 影响小程序媒体播放。
- `object-storage`: 强化生产 `/media/{object_key}` 受控读取可用性与可诊断性，覆盖视频媒体读取。
- `miniapp-sku-detail-page`: 增加生产视频播放 smoke 和失败诊断要求，保持 `BUG-0069` 的安全媒体 URL 回归覆盖。

## Impact

- **api:** 可能不改 API；若发现健康检查、媒体错误响应或 SKU 详情响应需要调整，必须同步 OpenAPI、Orval、`docs/03-api-index.md` 和测试。
- **backend:** 可能需要修复启动失败、生产配置读取、媒体读取错误处理或对象存储连接；不得绕过 `/media/{object_key}` 受控读取。
- **web/admin:** 可能需要修复 Docker Web Nginx 或生产外层 Nginx upstream；不应影响 SPA fallback、`/api/`、`/media/`、`/docs` 代理顺序。
- **miniapp:** 主要做生产真机回归；若视频失败仅由生产 502 导致，不需要修改小程序播放器。
- **database:** 无业务表结构变更预期；若生产后端启动失败由 DB 配置导致，需记录配置修复证据。
- **object-storage:** 继续使用单 Bucket + 标准前缀；确认实际视频对象可通过后端读取，不允许小程序直连对象存储。
- **deployment:** 需要生产或生产等价 smoke：域名根路径、健康检查、SKU 接口、媒体 URL 和容器/反代状态。
- **tests:** 继续运行既有 SKU 视频 URL 回归测试；如代码修改涉及部署/媒体读取，补充对应 pytest 或配置校验。
- **docs:** 若修复涉及部署、端口、对象存储或小程序发布说明，需同步 `docs/02-deployment.md`、`docs/07-object-storage-strategy.md`、`src/miniapp/README.md` 或相关发布记录。

## Rollback Plan

如修复后生产 API、Web 静态页、媒体读取或小程序视频播放出现更大范围异常，应回滚外层 Nginx upstream、Docker Compose 端口配置、后端镜像或对象存储配置到上一版可用状态。回滚后 `BUG-0076` 不得关闭，需要重新确认是生产部署、后端启动、对象存储读取、微信合法域名还是视频资源本身导致。
