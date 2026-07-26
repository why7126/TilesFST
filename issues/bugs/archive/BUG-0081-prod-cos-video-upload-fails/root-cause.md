---
bug_id: BUG-0081-prod-cos-video-upload-fails
status: done
created_at: 2026-07-23 09:00:31
updated_at: 2026-07-23 10:08:26
classification: deploy/runtime/proxy/media/object-storage
related_requirement:
related_change: fix-upload-proxy-timeout-config
related_bug:
---

# Root Cause - BUG-0081 生产环境腾讯 COS 视频上传 99% 后返回 504

## 直接原因

生产环境上传 SKU 视频时，外层 HTTPS 反代或容器内 Web Nginx 的上传请求超时时间不足。视频对象已经写入腾讯 COS，但上传接口未能在反代超时窗口内把成功响应返回浏览器，导致浏览器看到 `504 Gateway Time-out`，容器 Nginx 日志中同一请求约 60 秒后记录为 `499`。

直接证据：

1. 浏览器请求 `POST https://tilesfst.wjoyhappy.site/api/v1/admin/uploads/tile-videos?tile_id=3` 返回 `504 Gateway Time-out`。
2. 腾讯 COS Bucket 中已经出现对应视频对象，说明 `put_object` 已成功或接近成功。
3. Nginx error log 显示上传请求体被缓冲到 `/var/cache/nginx/client_temp/0000000005`。
4. 同一上传请求从 `2026-07-23 00:42:53 +0000` 到 `2026-07-23 00:43:53 +0000` 约 60 秒后记录为 `499`，与默认反代超时特征吻合。

## 根本原因

根本原因是大文件上传链路没有独立的生产反代超时与请求缓冲策略，且超时时间没有通过环境变量或部署参数统一配置。

当前链路为：

```text
浏览器 HTTPS 请求
→ 外层 HTTPS Nginx
→ 容器内 Web Nginx
→ FastAPI backend
→ 腾讯 COS S3 兼容 put_object
→ backend 返回 { object_key, url }
→ Nginx 返回浏览器
```

其中：

- 用户提供的外层 443 Nginx 只有通用 `location /`，未对 `/api/v1/admin/uploads/` 配置 `proxy_read_timeout`、`proxy_send_timeout`、`client_body_timeout` 或 `send_timeout`。
- 外层 443 Nginx 的 `client_max_body_size 100m` 小于项目默认 `MAX_VIDEO_SIZE_MB=500`。
- 容器内 `src/web/nginx.conf` 的 `/api/` 反代同样没有上传专用超时设置。
- 当前项目文档只要求 `client_max_body_size` 大于文件大小上限，没有覆盖大文件上传到云对象存储时的反代超时、请求缓冲和环境变量化配置。
- 后端上传接口必须等待 COS `put_object` 完成后才能返回 `object_key` 与 `url`；当浏览器上传、Nginx 缓冲、backend 读取、COS 写入和响应返回的总耗时超过反代默认超时，就会出现“COS 已有对象，但前端失败”的状态不一致。

## 触发条件

满足以下条件时高概率触发：

1. 生产环境走 `tilesfst.wjoyhappy.site` HTTPS 外层反代。
2. 上传视频文件较大，或网络/COS 写入速度较慢。
3. Nginx 将请求体缓冲到临时文件后再转发 backend。
4. backend 将完整文件写入腾讯 COS 的耗时，加上前置缓冲耗时，超过外层或内层默认 60 秒超时。
5. 前端等待上传接口响应，进度停在 99%，最终收到 `504` 或连接被关闭。

## 排除或降级的假设

| 假设 | 当前判断 | 依据 |
|---|---|---|
| 腾讯 COS 完全写入失败 | 不支持 | COS 中已有对应视频对象 |
| 前端上传进度计算错误 | 降级 | 即使进度卡 99%，浏览器实际收到 504，属于请求结果失败 |
| 文件类型或大小被后端校验拒绝 | 暂不支持 | 若校验拒绝通常应返回 400；当前已有 COS 对象 |
| 仅 `client_max_body_size` 不足 | 部分相关但不是主因 | 外层 100m 确实不合规，但本次请求能进入缓冲并写入 COS，不像 413 |
| 后端业务保存数据库失败 | 不支持 | 上传接口只返回上传结果，不直接保存 SKU 视频到数据库 |
| 小程序播放问题 | 不属于本 BUG 主链路 | 本次问题发生在管理端上传接口；播放 404/502 可另行追踪 |

## 分类

| 分类 | 判断 |
|---|---|
| deploy/runtime | 是。生产外层 Nginx 与容器内 Web Nginx 部署配置不足 |
| proxy | 是。504/499 与 60 秒超时特征直接指向反代链路 |
| media | 是。问题发生在视频上传能力 |
| object-storage | 相关。COS 写入耗时是触发条件之一，但当前证据不支持 COS 写入失败 |
| code | 需要后续修复。需要修改 Nginx 配置模板、Compose/env 文档或启动渲染机制 |
| db | 否。上传接口不直接写业务数据库 |
| frontend | 否。前端暴露失败结果，但不是根因 |

## 影响判断

该问题会让管理端视频上传在业务上失败，同时在 COS 中留下已写入但未被 SKU 表单引用的孤儿对象。若用户重复上传，会增加对象存储垃圾数据和费用。图片、品牌 Logo、证书等小文件上传通常不触发，但在网络慢或文件较大时也存在同类风险。
