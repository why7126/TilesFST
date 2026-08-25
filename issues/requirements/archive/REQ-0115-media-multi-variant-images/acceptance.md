---
requirement_id: REQ-0115-media-multi-variant-images
title: 媒体图片多规格展示图能力 - 验收标准
acceptance_status: passed
created_at: 2026-08-22 11:00:33
updated_at: 2026-08-25 14:51:36
---

# 验收标准

## 功能 AC

- [ ] AC-001 新上传图片生成 `thumbnail`、`display`、`original` 三类资源，并记录三者与同一媒体记录或业务对象的关系。
- [ ] AC-002 `thumbnail`、`display`、`original` 的 key/prefix、MIME、尺寸、体积和对象存在性可追溯，且遵守 MinIO 单 Bucket + 标准前缀策略。
- [ ] AC-003 上传或派生生成失败时有明确降级规则，不能暴露内部路径、对象存储密钥、Authorization header、Cookie 或真实 `.env` 内容。
- [ ] AC-004 商品、SKU 或媒体相关 API 返回或派生 `thumbnail_url`、`display_url`、`original_url`，并说明缓存、权限、签名或代理策略。
- [ ] AC-005 API 字段变更同步 OpenAPI、Orval、API 文档和接口测试；若最终不改 API 字段，必须写明由媒体服务统一适配的原因。
- [ ] AC-006 小程序列表页使用 `thumbnail_url`，商品详情普通展示使用 `display_url`，图片预览使用 `original_url` 或等价高清 URL。
- [ ] AC-007 小程序详情首屏外图片启用 lazy-load 或等价延迟加载策略，并通过静态测试、DevTools 或体验版证据确认。
- [ ] AC-008 Web 店主端和管理端若展示商品图片，按列表、详情、预览场景选择对应规格，并具备目标规格缺失时的 fallback。
- [ ] AC-009 存量图片批量生成纳入本期；治理入口具备 dry-run，输出待处理数量、跳过原因、失败分类、预计写入对象和脱敏风险摘要。
- [ ] AC-010 存量媒体 apply 必须显式触发，具备幂等性、成功/失败统计、重试建议和脱敏输出。
- [ ] AC-011 明确透明 PNG、非透明 PNG、JPG、WebP 等格式策略；无法统一时记录格式保留或转换规则。
- [ ] AC-012 明确 `display` 规格的目标宽高、质量、格式和体积上限；若暂不确定，评审时必须保留为待决策项。
- [ ] AC-013 对象存储直出纳入本期；验收必须覆盖签名、鉴权、缓存、公开范围、URL 过期、fallback 和后端代理兼容边界。
- [ ] AC-014 CDN 正式接入不作为本期必达项；验收需确认 URL 适配层为后续 CDN 接入保留扩展点。

## 媒体四联验收

| 维度 | 验收目标 | 最小证据 |
|---|---|---|
| key | 三规格 key 稳定、脱敏后可追溯，符合标准前缀 | key hash、标准前缀、资源类型、规格类型 |
| object | 三规格 object 真实存在且 MIME / size / 派生关系正确 | object 存在性、MIME、size、缩略收益或失败原因 |
| URL | 多端使用受控 URL、签名 URL、CDN URL 或代理 URL 的边界清晰 | URL 类型、HTTP 状态、业务状态、资源大小、耗时 |
| render | 列表、详情、预览真实使用对应规格，失败态可见 | 页面入口、截图/录屏/人工摘要、组件状态 |

## 小程序 Network Evidence

- [ ] AC-MINIAPP-001 记录列表页 `thumbnail_url` 请求的页面路径、URL 类型、HTTP 状态、资源大小和耗时。
- [ ] AC-MINIAPP-002 记录详情页 `display_url` 请求的页面路径、URL 类型、HTTP 状态、资源大小和耗时。
- [ ] AC-MINIAPP-003 记录预览场景 `original_url` 请求的页面路径、URL 类型、HTTP 状态、资源大小和耗时。
- [ ] AC-MINIAPP-004 DevTools Network 不等同于真机或体验版证据；缺少体验版或真机证据时必须标记 `blocked` 或 `follow_up`，不得写作已通过。
- [ ] AC-MINIAPP-005 验收记录不得包含敏感 header、Cookie、Authorization、真实 object key 全量值、本机绝对路径或真实客户数据。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 上传控件或媒体生成入口必须具备 `idle -> uploading -> done / failed` 状态机；失败态展示在控件或媒体对象附近，不能只依赖全局 toast。
- [ ] AC-XCUT-002 同一会话内上传成功后必须即时回显可见媒体入口；本需求中回显对象至少能证明 `thumbnail` 或 `display` 已生成或可派生。
- [ ] AC-XCUT-003 Docker Web `http://localhost:3000` 上传边界必须验收；图片边界文件从 Web 用户入口触发，不能只调用后端 `:8000`。
- [ ] AC-XCUT-004 `object_key` 与受控 `/media/` 代理或后续等价 URL 适配必须一致；证据包含脱敏 key、对象存在性、HTTP 状态、业务错误码和用户可见表现。
- [ ] AC-XCUT-005 新上传不得写入 `data/uploads/` 作为通过证据；必须写入对象存储适配层管理的标准前缀。

> 补充来源：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

- [ ] AC-XCUT-006 小程序媒体性能收益不得只用“对象存在”证明；必须同时覆盖 key、object、URL、render 四联。
- [ ] AC-XCUT-007 缩略图或展示图名义存在但尺寸/体积无收益时不得写作通过，必须记录 `thumbnail_no_benefit` 或等价失败分类。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 18:22:44
accepted_by: user
source_change: add-media-multi-variant-images
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

