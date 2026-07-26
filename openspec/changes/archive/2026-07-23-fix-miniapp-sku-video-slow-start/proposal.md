## Why

`BUG-0082-prod-miniapp-sku-video-slow-start` 已评审通过。生产环境微信小程序商品详情页在播放 SKU 视频时启动很慢，影响商品素材展示和客户演示体验。

现有 SKU 详情能力已要求视频由用户主动播放，并使用详情接口返回的安全可播放 URL；对象存储能力已要求 `/media/{object_key}` 可受控读取视频对象。但当前规格尚未明确视频播放链路必须支持 Range/206 分段响应、视频封面兜底和生产首帧体验验收，导致生产环境大视频或对象存储链路较慢时容易出现长时间等待。

## What Changes

- 为 `/media/{object_key}` 视频读取补充 Range 请求与 `206 Partial Content` 响应要求。
- 为小程序 SKU 详情视频媒体补充封面兜底与加载中体验要求。
- 明确生产或生产等价验收必须记录 SKU、视频大小/编码/时长、机型、网络和首帧耗时。
- 保持上传、对象 Key、数据库表结构和小程序页面入口不变。
- 将本修复约束在后端媒体读取、小程序详情页媒体体验和测试验收范围内；转码、压缩、多清晰度、CDN 直连播放作为后续增强，不在本 Change 中强制实现。

## Capabilities

### New Capabilities

- 无。

### Modified Capabilities

- `miniapp-sku-detail-page`: 补充 SKU 详情页视频慢启动修复约束，包括视频封面兜底、首帧体验和生产真机验收。
- `object-storage`: 补充视频媒体受控读取的 Range/206 分段响应要求，避免 `/media/{object_key}` 按整文件读取模型阻碍播放器起播。

## Impact

- 后端：`src/backend/app/modules/media/`、`src/backend/app/main.py` 或媒体读取相关测试可能受影响。
- 小程序：`src/miniapp/pages/tile-detail/`、`src/miniapp/services/api.*` 或静态测试可能受影响。
- API：`/media/{object_key}` 非 JSON 媒体读取语义会增强；若 `GET /api/v1/miniapp/skus/{sku_id}` 新增视频封面或播放 URL 字段，需要同步 OpenAPI、Orval、docs 和测试。
- 数据库：默认不新增表；若实现选择持久化 `cover_object_key` 或转码 URL，必须另行同步 SQLite/MySQL schema 与文档。
- 对象存储：继续使用单桶和标准前缀，不允许前端或小程序绕过后端上传。
- Docker/部署：如实现需要调整 Nginx `/media/` 代理缓存或 Range 透传，需同步部署文档与生产 smoke 清单。

## Rollback Plan

1. 如 Range/206 实现导致 `/media/{object_key}` 图片或文件读取回归，回滚媒体读取接口到原普通响应路径，并保留小程序封面兜底不影响业务播放。
2. 如新增 SKU 视频封面字段导致契约兼容问题，先保留原 `media[].url` 播放逻辑，撤回新增字段渲染入口。
3. 回滚后必须重新验证图片读取、视频播放、`MEDIA_NOT_FOUND`、非法 object key 和小程序详情页媒体浏览不回归。
