---
requirement_id: REQ-0120-webp-derived-image-variants
title: 图片上传生成 WebP 展示图和缩略图 - 验收标准
acceptance_status: passed
created_at: 2026-08-22 21:45:57
updated_at: 2026-08-25 14:51:36
---

# 验收标准

## 功能 AC

- [x] AC-001 上传 JPEG / JPG 图片后，原图对象保持 JPEG 格式，系统生成 WebP `thumbnail` 与 WebP `display` 派生对象。
- [x] AC-002 上传 PNG 图片后，原图对象保持 PNG 格式，系统生成 WebP `thumbnail` 与 WebP `display` 派生对象，并明确透明图处理结果。
- [x] AC-003 上传 WebP 图片后，原图对象保持 WebP 格式，系统生成尺寸和体积受控的 WebP `thumbnail` 与 WebP `display` 派生对象。
- [x] AC-004 WebP 派生对象 key、扩展名和 MIME 一致，不出现 `.thumb.jpg` 或 `.display.png` 对象内容却为 `image/webp` 的新生成状态。
- [x] AC-005 `thumbnail_url`、`display_url`、`original_url` 或等价字段分别指向 WebP 缩略图、WebP 展示图和原图，并保持受控 `/media`、签名 URL 或直出 URL 边界清晰。
- [x] AC-006 SVG 和 PDF 不生成 WebP 派生图；GIF、HEIC、TIFF、BMP 首期暂不转码，并在上传、维护任务或验收记录中体现跳过、拒绝或 fallback 策略。
- [x] AC-007 派生图生成失败时不阻断原图上传，且记录可定位 warning、任务 span 或失败原因枚举。
- [x] AC-008 Web 管理端、店主 Web 和小程序在列表 / 卡片场景优先使用 WebP `thumbnail_url`，目标 URL 缺失时可回退。
- [x] AC-009 Web 管理端、店主 Web 和小程序在详情普通展示场景优先使用 WebP `display_url`，高清预览仍使用 `original_url`。
- [x] AC-010 历史图片 WebP 补生成维护任务支持 dry-run，输出待处理数量、已存在数量、跳过原因、失败分类和预计写入数量。
- [x] AC-011 历史图片 WebP 补生成 apply 必须显式触发，生产执行前确认数据库和对象存储 bucket/prefix 已备份，执行结果具备幂等性。
- [x] AC-012 维护任务输出必须脱敏，不包含真实 `.env`、密钥、Authorization header、Cookie、数据库连接串、本机绝对路径或未脱敏 object key 全量值。
- [x] AC-013 若接口字段、Schema、示例或前端生成客户端发生变化，必须同步 OpenAPI、Orval、API 文档和相关测试。
- [x] AC-014 若不新增数据库字段，OpenSpec 和实现记录必须说明派生 key 可由原图 key 推导；若新增字段，必须同步 SQLite/MySQL schema、迁移、数据库文档和测试。

## 媒体五联验收

| 维度 | 验收目标 | 最小证据 |
|---|---|---|
| key | 原图 key 与 WebP 派生 key 稳定、可追溯且符合单 Bucket 标准前缀 | 脱敏 key hash、标准前缀、资源类型、规格类型、扩展名 |
| object | WebP 派生 object 真实存在且 MIME / size / 尺寸正确 | object 存在性、`image/webp`、size、尺寸、体积收益或跳过原因 |
| URL | 多端访问 URL 指向正确规格，权限和缓存边界清晰 | URL 类型、HTTP 状态、业务状态、缓存响应、fallback 结果 |
| render | Web 与小程序真实渲染使用 WebP 派生图 | 页面入口、截图/录屏/人工摘要、失败态与 fallback |
| benefit | WebP 派生图相对原图有可解释的体积或加载收益 | 原图与派生图字节数、Network 耗时、无收益原因分类 |

## 小程序媒体四联验收

| 维度 | 状态 | 证据 |
|---|---|---|
| key | pass | 自动化测试覆盖 `.thumb.webp` / `.display.webp` key 推导和原图 key 保留。 |
| object | pass | 自动化测试覆盖派生对象 `image/webp`、bytes 小于原图、PDF 跳过派生 URL。 |
| URL | pass | 自动化测试覆盖 `/media` 受控 URL、direct URL、缺失 WebP 派生 fallback。 |
| render | pass | 用户提供微信开发者工具截图：品牌页可见卡片渲染，Network 过滤 `.webp` 后存在多条 `.thumb.webp` / `.display.webp` 请求；选中 `display.webp` 返回 `200 OK`。 |

Network evidence:

- source: 用户提供微信开发者工具截图，2026-08-25 12:02
- page_path: 品牌页 / 品牌 Tab
- media_kind: brand logo thumbnail/display
- media_url_type: `/media/images/default/brands/logos/<object-key-hash>.display.webp` and `.thumb.webp`
- request_domain: `127.0.0.1:8000`
- http_status: `200 OK`
- business_status: pass
- resource_bytes: `content-length: 13126` for selected `display.webp`
- duration_ms: n/a
- render_result: pass
- blocker_or_follow_up: 小程序截图证据已补；Docker Web `http://localhost:3000` 上传边界证据已由 SKU 图片上传与 `display.webp` 展示截图补齐。

## Docker Web 上传边界验收

| 维度 | 状态 | 证据 |
|---|---|---|
| upload boundary | pass | 用户提供 Docker Web Network 截图：`POST http://localhost:3000/api/v1/admin/uploads/tile-images` 返回 `200 OK`，业务响应 `code: 0`、`message: success`。 |
| original format | pass | 上传文件为 `test.png`，响应中原图 URL 保持媒体原始 PNG 路径，`mime_type=image/png`，`size=1189508`。 |
| derived URL | pass | 响应包含同一对象 key 的 WebP 缩略图 URL 与展示图 URL。 |
| render | pass | 用户提供 SKU 编辑弹窗截图：商品图片已即时回显；Network 选中 WebP 展示图请求，状态 `200`。 |
| benefit | pass | 同一样本原图约 `1189508` bytes；Docker Web Network 中 `display.webp` 传输约 `26.96 kB`，展示链路使用轻量派生图。 |

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [x] AC-XCUT-001 上传控件或媒体生成入口必须具备 `idle -> uploading -> done / failed` 状态机；失败态展示在控件或媒体对象附近，不能只依赖全局 toast。
- [x] AC-XCUT-002 同一会话内上传成功后必须即时回显可见媒体入口；本需求中回显对象至少能证明 WebP `thumbnail` 或 WebP `display` 已生成、可读或已按 fallback 显示。
- [x] AC-XCUT-003 Docker Web `http://localhost:3000` 上传边界必须验收；图片边界文件从 Web 用户入口触发，不能只调用后端 `:8000`。
- [x] AC-XCUT-004 `object_key` 与受控 `/media/` 代理或后续等价 URL 适配必须一致；证据包含脱敏 key、对象存在性、HTTP 状态、业务错误码和用户可见表现。

> 补充来源：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

- [x] AC-XCUT-005 小程序媒体验收必须覆盖 key、object、URL、render 四联；DevTools、真机或体验版 Network evidence 与历史对象审计结果分开记录。
- [x] AC-XCUT-006 WebP 派生图名义存在但尺寸、体积或加载收益无改善时，不得写作通过；必须记录无收益原因或后续优化项。
- [x] AC-XCUT-007 小程序验收记录不得包含敏感 header、Cookie、Authorization、真实 object key 全量值、本机绝对路径或真实客户数据。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 14:18:06
accepted_by: user
source_change: add-webp-derived-image-variants
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

