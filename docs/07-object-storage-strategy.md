---
purpose: 对象存储策略说明
content: 说明 MinIO/S3兼容对象存储/腾讯 COS 单桶策略、目录前缀、资源类型、迁移与维护规范
source: AI自动生成，人工确认
update_method: 对象存储策略或媒体资源类型变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-26 15:19:59
note: V5 从多桶策略调整为单桶 + 前缀策略；支持 MinIO、S3 兼容云对象存储与腾讯 COS
---

# 对象存储策略

## 1. 当前策略

本项目使用 MinIO、S3 兼容对象存储或腾讯云 COS，采用：

```text
一个项目一个 Bucket
桶内使用二级目录/前缀区分资源类型
```

默认：

```text
OBJECT_STORAGE_BUCKET=tilesfst
```

后端应用统一使用 `OBJECT_STORAGE_BUCKET`。当 `OBJECT_STORAGE_PROVIDER=tencent-cos` 时，后端使用腾讯云 `qcloud_cos` 官方 SDK 访问 COS；当 provider 为 `minio`、`self-hosted-minio`、`s3-compatible`、`volcengine-tos` 等值时，继续使用 S3 兼容适配层。所有 provider 仍使用同一 bucket 和相同对象 Key 前缀。

## 2. 目录前缀

| 前缀 | 用途 |
|---|---|
| `images/` | 图片类上传（头像、Logo、SKU 图等） |
| `videos/` | 原始视频 |
| `files/` | 文档类（预留） |
| `audios/` | 音频类（预留） |
| `thumbnails/` | 缩略图 |
| `processed/` | 处理后的资源 |
| `tmp/` | 临时文件 |
| `imports/` | 批量导入文件 |
| `exports/` | 导出文件 |
| `videos/covers/` | 视频封面 |
| `videos/transcoded/` | 转码后视频 |
| `original/` | **Deprecated** — 存量迁移前遗留；新上传不得使用 |

当前后端上传入口使用以下 Key 前缀（`resource_type` 见 `rules/object-storage.md`）：

| 上传入口 | 对象 Key 前缀 |
|---|---|
| 头像 | `images/default/user/avatars/` |
| 品牌 Logo | `images/default/brands/logos/` |
| SKU 图片 | `images/default/tiles/{tile_id\|pending}/` |
| SKU 视频 | `videos/default/tiles/{tile_id\|pending}/` |

上传响应保持 `{ object_key, url }`，其中 `url` 为后端受控读取地址 `/media/{object_key}`。

视频读取由后端 `/media/{object_key}` 受控代理，支持 `GET`、`HEAD` 与视频 `Range` 请求。小程序原生视频预览、保存和转发可能先发送 `HEAD` 探测资源元信息；后端必须返回正确 `Content-Type`、`Content-Length`，并对视频返回 `Accept-Ranges: bytes`。

## 3. 本地持久化与 legacy 清理

| 路径 | 职责 |
|---|---|
| `data/minio/tilesfst/` | 本地 Docker 下 MinIO 桶物理存储；对象增长属预期 |
| `data/uploads/` | BUG-0006 前本地上传历史目录；迁移后新上传 **不得** 写入 |

对象存储从本地 `UPLOAD_DIR` 迁移至 MinIO 后，应清理 `data/uploads` 中与数据库 `object_key` 无关联的孤儿文件：

```bash
python scripts/clean_legacy_uploads.py          # dry-run
python scripts/clean_legacy_uploads.py --apply
python scripts/clean_legacy_uploads.py --check-only
```

详见 `data/README.md`。

## 4. 适用原因

瓷砖信息管理平台的媒体资源主要围绕同一个业务域，单桶便于部署、迁移、备份和权限管理。云上对象存储部署时，bucket、region、TLS、访问风格和最小权限由运维前置准备，应用不在生产环境隐式创建云 bucket。

## 5. 上传响应超时与孤儿对象检查

腾讯云 COS、火山云 TOS 或外部 S3 兼容存储中已经出现 `videos/default/tiles/...` 对象，但浏览器仍收到 `504` 时，通常表示对象写入完成后响应链路被外层或容器内 Nginx 超时截断。此时不得直接判定为 COS 写入失败，应同时检查：

- `/api/v1/admin/uploads/` 外层 HTTPS 反代与 Web 容器 Nginx 的 `proxy_send_timeout`、`proxy_read_timeout`、`send_timeout` 是否不低于生产上传建议值
- Web 容器上传路径是否关闭或正确评估 `proxy_request_buffering`
- COS 中已写入但业务表未引用的对象，按 `videos/default/tiles/{tile_id|pending}/` 前缀、上传时间窗口和管理端保存记录进行人工核对，必要时纳入后续受控清理脚本
- 用户重试后可能产生多个同名业务含义的不同 UUID 对象，验收时以 API 返回并被业务表保存的 `object_key` 为准

## 6. 管理端视频上传 99% 诊断结论

管理端视频上传采用后端受控中转链路：

```text
浏览器 -> Web/Nginx -> Backend -> 对象存储
```

浏览器上传进度只能反映 `浏览器 -> Backend` 阶段。当该阶段完成后，前端进度会接近 99%；若 Backend 仍在执行 `storage_put` 上传到 COS/TOS/MinIO，用户会看到“正在保存视频，请稍候”停留较久。

2026-07-24 对生产 `8T812.mp4`（约 23 MB）排查结论：

| 阶段 | 生产观测 |
|---|---:|
| `file_read_done` | 约 15 ms |
| `validation_done` | 约 0 ms |
| `storage_put_done` | 约 64,000 ms |

因此瓶颈不在前端、Nginx 接收、FastAPI 读取上传文件或业务校验，而在 `Backend -> 腾讯 COS` 的对象写入链路。按 23 MB / 64 s 估算，VPS 到 COS 公网写入吞吐约 360 KB/s。即使 `tencent-cos` provider 切换为腾讯云 `qcloud_cos` 官方 SDK，若服务器出口到 COS 的网络质量不变，耗时仍可能保持在 60 秒量级。

旧 Django 项目看起来没有同类 99% 问题，不应直接推断为 Django 上传路径更快。该项目同样通过 Django Admin 服务端中转到 COS，但存在以下体验与部署差异：

- Django Admin 是传统表单提交，没有展示“浏览器上传已完成但服务器仍在保存到 COS”的 99% 进度节点；
- 旧项目可能部署在不同主机或更接近腾讯云 COS 的网络环境，服务器到 COS 的公网/内网链路不可直接与 FST 当前 VPS 对比；
- 旧项目返回 COS 原始公网 URL，FST 返回 `/media/{object_key}` 后端受控读取地址，读取体验链路不同，但上传阶段瓶颈仍以 `storage_put` 日志为准；
- 两边测试文件大小、上传时间窗口、服务器出口带宽可能不同，必须使用同一文件、同一 bucket、同一 endpoint 的阶段耗时日志做对照。

若要消除 99% 后的长等待，推荐通过 OpenSpec Change 引入“后端签发短期凭证或预签名上传 URL，管理端前端直传对象存储，再由后端确认并保存 `object_key`”的受控直传方案。该方案必须继续由后端负责鉴权、对象 Key 生成、大小与 MIME 约束、前缀边界和最终业务保存，禁止前端持有永久密钥。

## 7. 何时考虑多桶

只有在生命周期策略、权限隔离、合规要求或资源规模明确要求时，才通过 OpenSpec Change 引入多桶。
