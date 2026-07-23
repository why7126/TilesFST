---
bug_id: BUG-0076-prod-miniapp-video-temporarily-unplayable
title: 生产环境微信小程序提示视频暂时无法播放
severity: high
status: approved
owner:
discovered_at: 2026-07-21 10:23:03
created_at: 2026-07-21 14:59:56
updated_at: 2026-07-21 15:24:31
environment: 生产环境微信小程序
related_requirement:
related_change: fix-prod-miniapp-video-upstream-502
related_bug: BUG-0069-miniapp-sku-detail-carousel-video-not-playable
---

# 现象

生产环境微信小程序中，进入包含视频播放能力的页面后，视频位置显示「视频暂时无法播放」。该提示来自小程序视频组件加载失败兜底，意味着当前视频 `src` 未能被微信小程序正常加载或播放。

# 复现步骤

1. 打开生产环境微信小程序。
2. 进入包含视频媒体的页面，当前待确认具体页面路径，例如 SKU 商品详情页、品牌/产品内容页或 Banner 视频入口。
3. 等待视频区域加载，或点击视频播放区域。
4. 观察页面是否显示「视频暂时无法播放」。
5. 同步检查小程序接口、视频资源 URL、生产 Nginx、后端服务和对象存储访问情况。

# 期望结果

- 生产环境中已配置且允许展示的视频可以正常加载封面并播放。
- 视频资源 URL 应来自后端授权、公开安全 URL 或对象存储适配层生成结果。
- 当视频资源缺失、过期、格式不支持或访问受限时，系统应留下可诊断日志，并给用户展示明确的失败提示。
- 图片媒体和 SKU 文本等非视频内容不应因单个视频失败而不可浏览。

# 实际结果

- 小程序视频区域显示「视频暂时无法播放」。
- `/bug-explore` 阶段在 `2026-07-21 14:44:47` 至 `2026-07-21 14:44:49` 只读访问生产域名时，根路径、`/api/v1/health` 和 `/api/v1/miniapp/skus/1` 均返回 `HTTP/1.1 502 Bad Gateway`，Server 为 `nginx/1.26.2`。
- 当前证据显示生产外层 Nginx 或其上游服务存在不可用风险；若小程序视频 URL 指向同域 `/media/...`，该 502 会直接触发视频组件加载失败。

# 影响范围

- 影响端：微信小程序。
- 影响环境：生产环境。
- 影响能力：视频播放、SKU/内容媒体浏览、受控 `/media/{object_key}` 读取链路。
- 影响用户：装修客户、设计师、门店导购、品牌访客无法查看商品或内容视频素材。
- 潜在横向影响：若生产域名整体 502，不只影响视频播放，还可能影响小程序 API、Web 静态站点、健康检查和媒体读取。

# 严重等级说明

严重等级为 `high`。该问题不一定阻断小程序所有页面展示，但会使已交付的视频展示能力不可用；若 502 覆盖生产根路径、健康检查和 API，则影响面可能扩大到整个生产服务入口。由于该反馈来自生产环境，且视频媒体是商品详情表达的重要内容，应优先完成生产链路排查。

# 初步分析

当前仓库已包含 `BUG-0069-miniapp-sku-detail-carousel-video-not-playable` 的修复结果：后端小程序详情接口从 `tile_videos.object_key` 组装视频媒体地址，并将对象 key 转换为 `/media/{object_key}`，测试也覆盖了 `object_key` 与原始上传文件名不同的场景。因此，本地代码层面暂未看到同类 `file_name` URL 回归证据。

本次更可疑的方向是生产部署或运行时链路：

1. 外层 Nginx 到 Web 容器或后端容器的 upstream 不可用。
2. `tilesfst-web` 或 `tilesfst-backend` 容器未运行、重启中、端口映射异常或网络不通。
3. 生产域名反代未正确指向 `HOST_PORT_WEB` 或后端服务。
4. 后端可用后，仍需进一步确认 `/media/{object_key}` 是否可读、对象是否存在、对象存储权限是否正确、视频 MIME/编码是否被小程序支持。

# 建议后续验证

1. 在生产服务器检查外层 Nginx upstream、`tilesfst-web`、`tilesfst-backend` 容器状态与端口映射。
2. 在生产服务器本机访问 `http://127.0.0.1:<HOST_PORT_BACKEND>/health`，确认后端是否直接可用。
3. 访问 Web 容器或外层域名的 `/api/v1/health`、`/api/v1/miniapp/skus/<实际 SKU ID>` 和实际视频 `/media/...` URL。
4. 若整体 502 消失但视频仍失败，记录视频 URL 的 HTTP 状态码、`Content-Type`、`Content-Length`、Range 请求支持、对象存储日志和微信真机基础库版本。
5. 对比 `BUG-0069` 修复范围，确认生产镜像是否已包含该修复，且生产数据中的 `tile_videos.object_key` 不为空。
