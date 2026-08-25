---
requirement_id: REQ-0120-webp-derived-image-variants
title: 图片上传生成 WebP 展示图和缩略图
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
created_at: 2026-08-22 21:37:49
updated_at: 2026-08-25 14:53:29
related_change: add-webp-derived-image-variants
---

# REQ-0120 图片上传生成 WebP 展示图和缩略图

## 1. 需求背景

系统已通过 `REQ-0115-media-multi-variant-images` 建立媒体图片 `thumbnail / display / original` 三规格模型，并让 Web 管理端、店主 Web 和小程序在列表、详情与预览场景中选择不同规格图片。当前实现的派生图生成策略仍以原图 MIME 为基础：JPEG 原图生成 JPEG 派生图，PNG 原图生成 PNG 派生图，WebP 原图生成 WebP 派生图。

图片密集页面的主要性能压力来自端侧实际展示资源，而不是后台保留的原始素材。将 `thumbnail` 与 `display` 派生图统一编码为 WebP，可以在保留原图审计与高清预览能力的同时，降低 SKU 列表、详情图、品牌 Logo、Banner 和证书图片等场景的传输体积，改善移动网络和小程序冷加载体验。

本需求用于明确图片上传与维护任务的 WebP 派生策略：原图继续保留上传格式，展示图和缩略图统一生成 WebP；Web 与小程序优先消费 WebP 派生图，派生对象缺失或生成失败时按既有 fallback 回退原图。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 微信小程序用户 | 列表和详情页图片加载更快，弱网下减少等待和流量消耗。 |
| 店主 / 展示端访问者 | 浏览商品图册、品牌和证书图片时获得稳定、清晰且轻量的展示体验。 |
| 企业管理端用户 | 上传图片后系统自动生成适合展示的 WebP 派生图，无需人工提前转码。 |
| 运营 / 内容维护人员 | 原图保留上传格式，便于素材复用、核对和高清预览。 |
| 后端 / 媒体能力开发 | 有统一的 WebP 派生对象 key、MIME、失败降级和历史补生成规则。 |
| 测试 / 发布负责人 | 能围绕 key、object、URL、render 和性能收益收集一致验收证据。 |

## 3. 需求目标

- 新上传 JPEG、PNG、WebP 图片后，系统 MUST 保留原图格式，并生成 WebP 格式的 `thumbnail` 与 `display` 派生图。
- Web 管理端、店主 Web 和小程序 SHOULD 优先消费 `thumbnail_url` / `display_url` 指向的 WebP 派生图。
- 高清预览、下载、审计或素材复用场景 SHOULD 继续使用 `original_url` 或等价原图 URL。
- 派生图对象 key、URL 和 MIME MUST 能清晰表达 WebP 格式，避免 `.jpg` key 返回 `image/webp` 等扩展名与内容不一致。
- SVG、PDF 首期不转 WebP；GIF、HEIC、TIFF、BMP 首期暂不转码，具体处理应记录为跳过、拒绝或原图 fallback。
- 历史已上传图片如需享受 WebP 派生收益，MUST 通过受控维护任务 dry-run / apply 补生成，不在需求实现中静默批量覆盖生产对象。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 新上传图片 WebP 派生 | JPEG、PNG、WebP 原图上传后生成 `.thumb.webp` 与 `.display.webp` 或等价标准 WebP 派生 key。 |
| 原图保留 | `original` 保留上传格式、MIME 和原始对象 key，不因派生图 WebP 化而被替换。 |
| 派生 key / URL 规则 | 明确 WebP 派生图 key、`thumbnail_url`、`display_url` 和 fallback 解析规则。 |
| 端侧优先消费 | Web 管理端、店主 Web、小程序在列表、详情等展示场景优先使用 WebP 派生图。 |
| 特殊格式策略 | SVG、PDF 跳过 WebP 派生；GIF、HEIC、TIFF、BMP 首期暂不转码，并给出可见 fallback 或错误策略。 |
| 历史对象补生成 | 提供历史图片 WebP 派生图补生成策略，必须支持 dry-run、apply、幂等性和脱敏摘要。 |
| 生成失败降级 | 派生图生成失败不阻断原图上传，端侧可回退原图或占位。 |
| 验收证据 | 按媒体 key、object、URL、render 和体积收益维度验收 WebP 派生效果。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 原图强制转 WebP | 原图继续保留上传格式，不把 JPEG、PNG 或 WebP 原图统一替换为 WebP。 |
| AVIF 或多格式协商 | 不在本期引入 AVIF、`picture` 多源协商或按浏览器能力动态选择格式。 |
| 视频转码 | 本需求只覆盖图片派生图，不覆盖视频多清晰度、封面转码或视频压缩。 |
| 前端直传对象存储 | 上传仍通过后端鉴权和对象存储适配层，不新增前端直传能力。 |
| 独立媒体处理平台 | 不新增独立可视化媒体处理后台。 |
| 保存配置自动重建历史对象 | 不通过系统设置保存动作自动扫描、重建或覆盖历史派生对象。 |
| 强制所有历史图片立即重建 | 历史补生成应由维护任务受控执行，不作为上线即刻强制动作。 |

## 5. 功能要求

### FR-001 WebP 派生图生成策略

系统 MUST 在支持的图片上传链路中，将 `thumbnail` 和 `display` 派生图编码为 WebP。

首期支持的输入格式：

| 输入类型 | 原图处理 | 派生处理 |
|---|---|---|
| JPEG / JPG | 保留原格式 | 生成 WebP `thumbnail` 与 WebP `display` |
| PNG | 保留原格式 | 生成 WebP `thumbnail` 与 WebP `display`，透明图需明确透明度处理 |
| WebP | 保留原格式 | 生成 WebP `thumbnail` 与 WebP `display` |
| SVG | 保留或按上传策略处理 | 跳过 WebP 派生 |
| PDF | 走文档/证书文件策略 | 不生成 WebP 图片派生 |
| GIF / HEIC / TIFF / BMP | 按现有上传策略处理 | 首期暂不转码，必须记录跳过或 fallback |

若某类上传入口不适合生成 `display` 或 `thumbnail`，实现文档和验收记录 MUST 明确说明不适用原因。

### FR-002 原图保留与派生对象独立

系统 MUST 保留原图对象，且原图对象的 key、MIME 和访问语义不因 WebP 派生策略改变。

- `original_url` 或等价高清 URL 继续指向原图。
- `thumbnail_url` 指向 WebP 缩略图。
- `display_url` 指向 WebP 展示图。
- 派生图缺失或不可读时，端侧 MUST 能回退到原图或占位，不得空白或无限重试。

该策略用于兼顾性能、素材保真、证书核验、透明图兼容和未来批处理回滚。

### FR-003 WebP key 与 MIME 一致性

WebP 派生对象 key MUST 与内容格式一致，推荐形态为同目录 suffix + `.webp`：

```text
images/default/tiles/42/main.jpg
  original:  images/default/tiles/42/main.jpg
  thumbnail: images/default/tiles/42/main.thumb.webp
  display:   images/default/tiles/42/main.display.webp
```

系统 MUST 避免新生成 `.thumb.jpg` / `.display.png` 但对象内容为 `image/webp` 的不一致状态。若兼容历史同格式派生 key，读取层 SHOULD 保留 fallback 候选，避免历史页面或旧对象失效。

### FR-004 多上传入口覆盖

WebP 派生策略 SHOULD 覆盖所有图片上传入口，包括但不限于：

- 用户头像。
- 品牌 Logo。
- Banner 图片。
- SKU 图片。
- 品牌证书图片。

PDF 证书继续走文件策略。若某入口当前只返回原图 URL 或只生成缩略图，后续 PRD 完善、OpenSpec 或实现阶段 MUST 明确本期是否扩展到 display 图与 WebP 派生。

### FR-005 端侧消费与 fallback 顺序

Web 管理端、店主 Web 与小程序 SHOULD 继续通过既有字段消费图片规格，不新增端侧硬编码对象存储 key 的逻辑。

推荐消费顺序：

| 场景 | 首选 | 备选 |
|---|---|---|
| 列表 / 卡片 | `thumbnail_url` | `display_url` 或原图 URL |
| 详情普通展示 | `display_url` | `thumbnail_url` 或原图 URL |
| 高清预览 / 下载 | `original_url` | `display_url` |
| 分享封面 | 视平台限制使用原图或 display 图 | 缺失时使用缩略图或占位图 |

端侧 MUST 在目标 URL 缺失或加载失败时有明确 fallback，避免图片空白、布局跳动或重复请求。

### FR-006 历史图片 WebP 补生成

系统 SHOULD 提供历史图片 WebP 派生图补生成能力，用于让已上传对象获得 WebP 展示收益。

维护任务 MUST 满足：

- 默认 dry-run，只输出待处理数量、已存在数量、跳过原因、失败分类和预计写入数量。
- apply 必须显式触发，并要求生产执行前确认数据库与对象存储 bucket/prefix 已备份。
- 执行必须幂等，重复运行不得重复生成无变化对象或破坏已有引用。
- 输出必须脱敏，不得泄露真实 `.env`、密钥、Authorization header、Cookie、数据库连接串、本机绝对路径或未脱敏 object key 全量值。
- 维护任务需要覆盖 key、object、URL、render 和体积收益验收摘要。

### FR-007 生成质量、体积和可观测性

WebP 派生图 SHOULD 使用可配置或可维护的质量、最大宽高和体积目标策略。

- `thumbnail` 面向列表和卡片，应优先控制体积。
- `display` 面向详情展示，应在清晰度和体积之间平衡。
- 若目标体积无法达到，系统 SHOULD 记录 warning，但不得阻断原图上传。
- 上传 trace 或媒体日志 SHOULD 能区分原图写入、WebP thumbnail 生成、WebP display 生成和跳过原因。

### FR-008 API、兼容性与数据边界

如果现有接口已具备 `thumbnail_url`、`display_url`、`original_url` 字段，本需求 SHOULD 优先复用这些字段，不新增等价字段。

若因 WebP key 规则变化导致响应示例、Schema 或生成客户端变化，MUST 同步：

- OpenAPI。
- Orval 生成物。
- API 文档。
- 后端接口测试。
- Web / 小程序字段消费测试。

本需求不要求新增业务表字段。若后续实现选择记录派生对象生成状态、尺寸、MIME 或体积，必须在 OpenSpec 阶段说明 SQLite/MySQL schema 与迁移影响。

## 6. UI / UE 约束

- Web 管理端上传后即时回显应优先展示 WebP `display_url` 或 `thumbnail_url`。
- 管理端列表、卡片和图册不应为了展示加载原图，除非派生图缺失或用户进入高清预览。
- 小程序列表应优先使用 `thumbnail_url`，详情普通展示优先使用 `display_url`，预览使用 `original_url`。
- 小程序首屏外图片应继续使用 lazy-load 或等价延迟加载策略。
- 端侧不展示对象 key、转码异常堆栈、对象存储路径或内部配置。
- 若需要展示维护任务结果，应使用紧凑状态、统计摘要和失败分类，不在 UI 中展示未脱敏 key 全量。

## 7. 非功能约束

- MUST 遵守 `rules/media.md` 和 `rules/object-storage.md` 的上传、前缀、权限和单 Bucket 策略。
- MUST 继续通过后端鉴权上传和后端媒体适配层读取，前端不得直连未授权对象存储。
- MUST 限制文件大小、MIME Type 和扩展名，并禁止使用用户原始文件名作为对象 key。
- MUST 保持媒体相关代码集中在 media 模块或既有媒体服务边界内。
- SHOULD 避免上传请求因 WebP 生成明显变慢；如同步生成成本过高，应在 OpenSpec 设计中评估异步或维护任务补生成。
- SHOULD 保持旧派生图读取兼容，避免上线后历史 `.thumb.jpg` / `.display.png` 立即失效。
- SHOULD 为 WebP 派生失败、对象缺失、URL fallback 和历史补生成失败提供可定位日志或测试证据。
- 涉及 API 变更时 MUST 同步 OpenAPI / Orval / docs / tests。
- 涉及 DB 变更时 MUST 同步 SQLite/MySQL schema、数据库文档和测试；若不涉及，必须在实现记录中说明。

## 8. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 默认不新增业务表；若记录派生对象状态、尺寸或 MIME，需在 OpenSpec 阶段明确 schema 与迁移。 |
| Pydantic Schema | 优先复用现有 `thumbnail_url`、`display_url`、`original_url`；如新增字段或调整示例需同步。 |
| OpenAPI / Orval | 若接口字段结构或示例变化，需要同步生成物；仅对象 key 后缀变化也应更新相关测试期望。 |
| 后端媒体模块 | 需要调整派生图编码、WebP key 推导、MIME、fallback 候选和维护任务。 |
| 对象存储 | 新派生对象使用同 Bucket、同业务目录、`.thumb.webp` / `.display.webp` 或等价标准 key。 |
| Web 管理端 | 上传回显、列表图片和表单图片优先使用 WebP 派生 URL。 |
| 店主 Web | 图片展示链路优先使用 WebP 派生 URL。 |
| 小程序 | 列表、详情、预览和分享图按场景消费合适规格，并保留 fallback。 |

## 9. 关联需求与缺陷

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 父需求 | `REQ-0115-media-multi-variant-images` | 已建立三规格资源模型，本需求在其基础上收敛派生图格式策略。 |
| 关联需求 | `REQ-0118-unified-web-miniapp-image-variant-consumption-matrix` | 端侧消费矩阵需要确认 WebP 派生 URL 优先级。 |
| 关联需求 | `REQ-0119-admin-display-image-size-limit-setting` | display 图体积目标配置会影响 WebP display 生成效果。 |
| 关联需求 | `REQ-0099-global-thumbnail-size-limit` | thumbnail 体积目标策略与 WebP 缩略图生成相关。 |
| 关联规范 | `rules/media.md` | 后续实现需同步媒体格式、派生图、维护任务和验收规则。 |
| 关联规范 | `rules/object-storage.md` | 后续实现需同步 WebP 派生 key、对象前缀和读取 fallback 规则。 |

## 10. 状态块

```yaml
requirement_id: REQ-0120-webp-derived-image-variants
status: done
lifecycle_stage: review
readiness: Partially Ready
next_command: /opsx-archive REQ-0120-webp-derived-image-variants
notes:
  - 已根据 capture 与 req-explore 结论生成 PRD。
  - 已补齐 user-stories、business-flow、acceptance 与 prototype 策略。
  - 已确认原图保留上传格式，thumbnail/display 派生图统一 WebP。
  - 已确认特殊格式策略：首期只支持 JPEG、PNG、WebP 生成 WebP 派生图；SVG、PDF 跳过；GIF、HEIC、TIFF、BMP 暂不转码。
  - 已完成需求评审并通过，可进入 Sprint 规划。
  - Readiness 为 Partially Ready：已写入媒体上传与小程序媒体验收横切 AC；因本需求不新增独立 UI，HTML/PNG 原型暂不生成。
  - 评审已通过；推荐先纳入 Sprint，再创建 OpenSpec Change。
  - 已纳入 sprint-025；推荐创建 OpenSpec Change 并回填同一 Sprint scope。
```
openspec_changes:
  - change_id: add-webp-derived-image-variants
    type: update
    status: archived
