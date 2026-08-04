---
purpose: 对象存储策略说明
content: 说明 MinIO/S3兼容对象存储/腾讯 COS 单桶策略、目录前缀、资源类型、迁移与维护规范
source: AI自动生成，人工确认
update_method: 对象存储策略或媒体资源类型变化时更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-04 11:32:00
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

SKU 图片在新建前允许进入 `images/default/tiles/pending/` 暂存目录；一旦图片被绑定到 SKU、保存为 SKU 图片或发布为公开商品，后端必须将 pending 原图复制到 `images/default/tiles/{tile_id}/` 正式商品目录，并同步更新 `tile_images.object_key` / `url`。目标 key 由后端生成或由受控迁移脚本按源文件名确定，前端不得提交目标路径。发布流程必须作为兜底门禁，公开商品主图不得长期引用 pending 目录。

SKU 商品列表缩略图采用与原图同目录、文件名后缀差异化的 Key 规则：原图
`images/default/tiles/pending/<uuid>.jpg` 对应列表缩略图
`images/default/tiles/pending/<uuid>.thumb.jpg`；已绑定 SKU 的
`images/default/tiles/{tile_id}/<uuid>.webp` 对应
`images/default/tiles/{tile_id}/<uuid>.thumb.webp`。`thumbnails/` 前缀仅作为历史兼容读取或迁移来源，不作为新生成 SKU 列表缩略图的最终写入位置。

SKU 图片上传链路必须生成真实轻量缩略图，而不是把原图 bytes 复制到 `.thumb` key。后端媒体模块使用 Pillow 解码 JPG、PNG、WebP，按约定最大宽高等比缩小且不放大小图，并尽量保留透明 PNG/WebP 的透明度。对于尺寸大于目标尺寸的原图，`.thumb` 对象应与原图 bytes 不同，像素宽高不超过目标最大宽高，文件体积通常小于原图。若缩略图生成失败，上传链路保持原图对象可读取并记录可观测告警，列表读取继续依赖 `.thumb` 缺失回退原图。

`/media/{object_key}` 受控读取在同路径 `.thumb` 缩略图缺失时可回退同目录原图，避免小程序商品卡片收到不可访问的缩略图 URL。历史数据可通过
`python scripts/audit-miniapp-card-images.py --backfill` 预览缺失缩略图，通过
`python scripts/audit-miniapp-card-images.py --backfill --execute` 重生成缺失、同 size 或同 bytes 的疑似无效缩略图；脚本输出原图存在、缩略图存在、疑似同 size、疑似同 bytes、需要重生成、跳过和失败原因摘要，不输出密钥、Authorization header、Cookie、`.env` 内容或本机路径。dry-run 不写数据库或对象存储，execute 可重复执行且不会破坏已合格缩略图。

历史公开 SKU 主图若仍位于 pending 目录，通过
`python scripts/migrate-pending-tile-images.py` 或
`python -m app.modules.media.maintenance formalize-pending-tile-images` 进行 dry-run 预览，通过
`--apply --confirm-backup` 执行迁移。脚本只处理公开 SKU 主图，输出待迁移数量、目标 key 脱敏摘要、对象缺失、缩略图处理、目标已存在和失败原因摘要；dry-run 不写数据库或对象存储，apply 可重复执行且不会破坏已迁移记录。执行前应先完成数据库与对象存储备份，迁移后再运行小程序卡片图片审计确认 `pending_main_image` 归零。

生产维护任务统一优先使用部署包装入口；包装脚本负责选择 local/prod Compose、env 文件和维护服务，后端包内入口负责执行真实任务：

```bash
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos object-key-audit --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos backfill-brand-certificate-thumbnails --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos formalize-pending-tile-images --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos migrate-certificate-image-keys --limit 100
./deploy/scripts/media-maintenance.sh prod mysql-tencent-cos bug-0116-media-drift --limit 100
```

`object-key-audit` 为只读任务，不支持 apply。`backfill-brand-certificate-thumbnails`、`formalize-pending-tile-images`、`migrate-certificate-image-keys` 与 `bug-0116-media-drift` 默认 dry-run；生产写入必须追加 `--apply --confirm-backup`，确认 MySQL 与对象存储 bucket/prefix 已备份。`bug-0116-media-drift` 是 BUG-0116 的聚合入口，按顺序覆盖 SKU pending 主图正式化、证书图片 `files/` 到 `images/` key 迁移、品牌 Logo/证书图片同目录 `.thumb` 缩略图回填和二次对象 key 审计。维护输出只允许出现对象 Key hash、标准前缀、统计摘要、失败原因枚举和媒体验收摘要，不得输出 access key、secret key、数据库连接串、Authorization header、Cookie、真实 `.env` 内容、本机绝对路径或未脱敏 object key。

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
