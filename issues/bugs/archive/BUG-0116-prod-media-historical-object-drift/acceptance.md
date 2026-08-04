---
bug_id: BUG-0116-prod-media-historical-object-drift
title: 生产历史媒体对象与缩略图存在规范漂移验收标准
severity: high
acceptance_status: passed
created_at: 2026-08-04 10:43:35
updated_at: 2026-08-04 23:12:32
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
---

# 生产历史媒体对象与缩略图存在规范漂移验收标准

## 验收范围

本 BUG 是媒体类 BUG，验收必须引用 `docs/standards/media-bug-four-point-acceptance-template.md`，并覆盖 `key`、`object`、`URL`、`render` 四联。验收对象包括：

- SKU 商品图片：公开 SKU 主图、同目录 `.thumb` 缩略图、暂存目录正式化。
- 品牌 Logo：`brands.logo_object_key` 原图与同目录 `.thumb` 缩略图。
- 品牌证书图片：`brand_certificates.file_key`、`brand_certificate_images.file_key` 中的 JPG、PNG、WebP 图片和同目录 `.thumb` 缩略图。
- 品牌证书文档：PDF 或其他文档类证书继续保留在 `files/default/brand-certificates/`，仅作为不误迁移检查对象。

## AC-0116-001 dry-run 审计覆盖三类历史媒体

- Given 生产等价数据库与对象存储环境已配置且完成只读连接验证。
- When 执行历史媒体 dry-run 审计。
- Then 审计结果必须分别统计 SKU、品牌 Logo、证书图片三类对象。
- And SKU 统计必须包含公开主图总数、暂存主图数量、缺失原图数量、缺失缩略图数量、同 size 缩略图数量、同 bytes 缩略图数量。
- And 品牌 Logo 统计必须包含 Logo 总数、缺失原图数量、缺失缩略图数量、需重新生成缩略图数量和失败原因摘要。
- And 证书图片统计必须包含图片证书总数、仍位于 `files/default/brand-certificates/` 的 JPG/PNG/WebP 数量、PDF/文档证书跳过数量、缺失原图数量、缺失缩略图数量、需重新生成缩略图数量和失败原因摘要。
- And dry-run 不得写数据库或对象存储。

## AC-0116-002 SKU 图片 key 正式化

- Given dry-run 已确认可迁移的公开 SKU 暂存主图。
- When 执行受控 apply。
- Then 可迁移 SKU 主图必须从 `images/default/tiles/staging/` 正式化到 `images/default/tiles/{tile_id}/` 或等价商品目录。
- And `tile_images.object_key` 和 `tile_images.url` 必须同步更新为目标 key 与 `/media/{target_key}`。
- And 二次审计中公开 SKU 主图 `staging_main_image` 必须为 0，或每个 remaining 项都有明确失败原因和返修计划。
- And apply 必须幂等，重复执行不得重复迁移已完成记录。

## AC-0116-003 SKU 缩略图真实轻量化

- Given SKU 主图 object 存在。
- When 执行缩略图审计或回填。
- Then 每个公开 SKU 主图应具备同目录 `.thumb` 缩略图。
- And 缩略图不应与原图 bytes 完全一致。
- And 若缩略图与原图 size 一致，必须确认是小图无需缩放但经过当前生成逻辑处理，或记录为需重新生成/人工判断。
- And 小程序商品卡片、商品详情、店主 Web 或管理端 SKU 列表涉及缩略图入口时，必须通过后端受控 URL 读取。

## AC-0116-004 品牌 Logo 缩略图回填

- Given `brands.logo_object_key` 非空。
- When 执行品牌 Logo 缩略图审计或回填。
- Then 每个可读品牌 Logo object 应具备同目录 `.thumb` 缩略图。
- And 缩略图必须由当前后端图片处理逻辑生成，不得只是原图 bytes 复制品。
- And 品牌列表、品牌详情和依赖品牌 Logo 的 Banner 选图场景应通过 `/media/{logo_thumb_key}` 或等价受控 URL 展示缩略图，原图作为明确 fallback。
- And object 缺失、存储不可用或图片格式不可处理时，必须记录失败原因和补救方式。

## AC-0116-005 证书图片 key 分流正确

- Given 品牌证书历史数据中存在图片和文档两类文件。
- When 执行证书图片 key 迁移。
- Then JPG、JPEG、PNG、WebP 图片证书必须使用 `images/default/brand-certificates/` 或等价图片前缀。
- And PDF 或其他文档类证书必须继续使用 `files/default/brand-certificates/`。
- And `brand_certificates.file_key` 与 `brand_certificate_images.file_key` 中可迁移图片引用必须同步更新。
- And 二次审计中图片类证书不得继续停留在 `files/default/brand-certificates/`，除非记录明确失败原因和返修计划。
- And 迁移脚本必须支持 dry-run、apply 和幂等重复执行摘要。

## AC-0116-006 证书图片缩略图回填

- Given 图片类证书 object 存在。
- When 执行证书图片缩略图审计或回填。
- Then 每个可读证书图片 object 应具备同目录 `.thumb` 缩略图。
- And 缩略图 key 必须与图片归属前缀一致；图片证书使用 `images/default/brand-certificates/`，PDF/文档证书不要求缩略图。
- And 证书列表、证书详情和小程序证书页面应使用缩略图或明确 fallback，不得暴露原始 object key 给用户。
- And 缩略图生成失败时必须记录 MIME、扩展名、失败原因类别和重试条件，且不得泄露敏感信息。

## AC-0116-007 媒体四联验收记录完整

修复验收必须按以下表格记录，任一维度为 `fail` 或 `blocked` 时不得视为通过。

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0116-prod-media-historical-object-drift |
| 标题 | 生产历史媒体对象与缩略图存在规范漂移 |
| 严重等级 | high |
| 影响范围 | Web 管理端 / 店主 Web / 小程序 / 对象存储 / 发布检查 |
| 复现入口 | 生产等价媒体审计脚本、管理端 SKU/品牌/证书页面、小程序 SKU/品牌/证书页面 |
| 受影响端 | admin / web / miniapp / backend / storage |
| 环境 | production-media / production-equivalent / docker-web-3000 / miniapp-devtools 或 miniapp-device |
| 媒体类型 | image / logo / certificate / thumbnail |
| 业务资源 | 脱敏 SKU、品牌、证书图片记录 |
| 修复前实际结果 | 历史对象存在 staging、files 图片证书、缺缩略图或无效缩略图 |
| 修复后期望结果 | key、object、URL、render 四联一致，缩略图真实轻量化 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | passed | SKU、品牌 Logo、证书图片脱敏 key 均符合单 Bucket 与标准前缀；图片证书在 `images/default/brand-certificates/`，PDF/文档证书在 `files/default/brand-certificates/` | 修复归档后为 passed；若仍有漂移，记录具体类型和数量 |
| object | passed | 原图 object、同目录 `.thumb` object、MIME、size、扩展名、权限、同 bytes 检查和 dry-run/apply/幂等摘要 | object 缺失或存储不可用时标记 blocked/fail 并记录重试条件 |
| URL | passed | `/media/{object_key}` 或等价后端受控 URL，HTTP 状态、业务错误码和用户可见表现 | 403/404/代理错误需记录入口、资源类型和失败原因 |
| render | passed | Web 管理端、店主 Web、小程序页面的展示、预览、占位和失败态 evidence | 缺少小程序真机/体验版证据时标记 blocked，不得视为通过 |

## AC-0116-008 安全与证据边界

- 验收记录只允许保存脱敏 object key、相对 URL、HTTP 状态、命令摘要、统计摘要、截图或人工验收摘要。
- 验收记录不得保存生产 AccessKey、SecretKey、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。
- 生产 apply 前必须记录备份完成摘要；若备份不可确认，apply 验收必须标记 `blocked`。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-04 23:12:32
accepted_by: workflow-sync
source_change: fix-prod-media-historical-object-drift
source_sprint: sprint-019
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

