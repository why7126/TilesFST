---
bug_id: BUG-0076-prod-miniapp-video-temporarily-unplayable
status: approved
created_at: 2026-07-21 15:21:40
updated_at: 2026-07-21 15:24:31
classification: deploy/runtime/proxy/media
related_requirement:
related_change: fix-prod-miniapp-video-upstream-502
related_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
---

# Root Cause - BUG-0076 生产环境微信小程序提示视频暂时无法播放

## 直接原因

当前直接证据指向生产域名入口异常：`/bug-explore` 阶段在 `2026-07-21 14:44:47` 至 `2026-07-21 14:44:49` 只读访问生产域名时，根路径、`/api/v1/health` 与 `/api/v1/miniapp/skus/1` 均返回 `HTTP/1.1 502 Bad Gateway`，响应 Server 为 `nginx/1.26.2`。

微信小程序视频播放链路会消费接口返回的 `/media/{object_key}` 或完整媒体 URL。若生产域名整体或 `/media/` 反向代理返回 502，小程序 `<video>` 组件会触发 `binderror`，页面兜底展示「视频暂时无法播放」。

## 根本原因

根本原因待生产服务器日志确认。基于现有证据，最高优先级怀疑方向是生产运行时或反向代理链路不可用，而不是当前仓库内 `BUG-0069` 同类代码回归：

1. 外层 Nginx upstream 指向的 Web 容器、后端容器或宿主端口不可用。
2. `tilesfst-web` 或 `tilesfst-backend` 容器未运行、重启中、网络不通或端口映射与外层 Nginx 配置不一致。
3. 后端服务启动失败，导致 `/api/v1/health` 与 `/media/...` 均无法通过反向代理访问。
4. 若整体 502 修复后视频仍失败，则需继续检查对象存储读取链路、视频对象是否存在、MIME/编码、Range 请求支持和小程序合法域名配置。

## 排除或降级的假设

| 假设 | 当前判断 | 依据 |
|---|---|---|
| 小程序详情接口继续使用 `tile_videos.file_name` 作为视频 URL | 暂不支持 | 当前仓库中小程序详情媒体查询使用 `tile_videos.object_key`，并由服务层生成 `/media/{object_key}` |
| 小程序 video 组件缺失错误兜底 | 暂不支持 | 小程序页面已有 `binderror="onMediaError"`，失败时展示「视频暂时无法播放」 |
| 单个 SKU 视频对象损坏 | 待确认 | 当前还没有实际 SKU ID、媒体 URL 与对象存储日志；生产整体 502 优先级更高 |
| 微信合法域名或视频编码问题 | 待确认 | 若生产 API 与 `/media/` 恢复 200 后仍失败，再进入该分支 |

## 触发条件

满足以下条件时可触发或高概率触发：

1. 用户打开生产环境微信小程序。
2. 页面包含视频媒体项，视频 `src` 指向生产域名下的 `/media/...` 或依赖生产 API 返回媒体 URL。
3. 生产外层 Nginx 到 Web/Backend upstream 不可用，或 `/media/...` 受控读取链路返回 502/5xx。
4. 小程序 video 组件加载失败并触发 `onMediaError`。

## 分类

| 分类 | 判断 |
|---|---|
| deploy/runtime | 是。生产域名健康检查和业务接口均返回 Nginx 502 |
| proxy | 是。响应来自 Nginx，需检查外层 Nginx upstream 与容器端口 |
| media | 是。用户可见现象发生在视频媒体播放链路 |
| code | 暂无直接证据。当前仓库已包含 `BUG-0069` 的 object_key 视频 URL 修复 |
| db | 待确认。若 502 修复后个别视频仍失败，需检查 `tile_videos.object_key` 是否为空或对象不存在 |
| object-storage | 待确认。若 `/media/...` 返回 404/502，需检查 MinIO/COS 权限、对象存在性与后端读取日志 |
| miniapp-config | 待确认。若资源可 HTTP 200 读取但真机仍失败，需检查合法域名、HTTPS、视频格式与基础库兼容 |

## 影响判断

该问题至少影响生产小程序视频播放体验；如果 502 覆盖根路径、健康检查与小程序 API，则影响范围可能扩展到生产 Web/API 入口和所有依赖同域媒体资源的展示能力。由于视频媒体是商品详情表达的重要内容，且问题发生在生产环境，建议按高优先级处理。
