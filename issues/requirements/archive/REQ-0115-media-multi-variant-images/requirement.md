---
requirement_id: REQ-0115-media-multi-variant-images
title: 媒体图片多规格展示图能力
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0012-object-storage-key-layout
created_at: 2026-08-22 10:52:29
updated_at: 2026-08-25 14:53:29
related_change: add-media-multi-variant-images
---

# REQ-0115 媒体图片多规格展示图能力

## 1. 需求背景

小程序商品详情页冷加载性能分析显示，部分商品详情在图片下载阶段耗时过长，直接加载原图或大体积 PNG 会影响首屏基础浏览体验。相关缺陷已拆分为 `BUG-0132-miniapp-sku-detail-large-image-cold-load` 处理具体页面偏差，但该问题背后暴露出媒体能力层缺少统一的多规格展示图机制。

当前媒体图片在列表、详情普通展示和高清预览场景中对同一原图 URL 的依赖较重，难以按场景控制下载体积、显示清晰度和代理流量。后续若接入 CDN 或对象存储直出，也需要稳定的派生对象 key、URL 字段和多端选择策略作为基础。

本需求用于沉淀通用媒体多规格图能力：上传后生成 `thumbnail`、`display`、`original` 三类资源，并让小程序、Web 展示端和管理端在不同场景中选择合适 URL，降低冷加载成本和后端 `/media` 代理压力。

## 2. 目标用户

| 用户 | 诉求 |
|---|---|
| 微信小程序用户 | 商品列表和详情首屏图片加载更快，点击预览时仍可查看高清图。 |
| 店主 / 展示端访问者 | 浏览商品图册时获得稳定、清晰且不过度消耗流量的图片体验。 |
| 企业管理端用户 | 上传图片后系统自动产出适合展示和预览的多规格资源，无需手工处理多份图片。 |
| 后端 / 媒体能力开发 | 有统一的派生对象、URL 字段、失败降级和历史媒体处理边界。 |
| 测试 / 发布负责人 | 能围绕上传生成、API 字段、多端使用和历史对象维护收集一致证据。 |

## 3. 需求目标

- 建立媒体图片 `thumbnail / display / original` 三规格资源模型。
- 上传后 SHOULD 自动生成适合列表缩略、详情展示和高清预览的派生资源。
- 商品相关 API SHOULD 返回或派生 `thumbnail_url`、`display_url`、`original_url`，供多端按场景选择。
- 微信小程序列表默认使用 `thumbnail`，详情普通展示默认使用 `display`，点击预览使用 `original`。
- 详情页首屏外图片 SHOULD 使用 lazy-load，避免非首屏图阻塞基础浏览。
- 存量媒体批量生成多规格资源纳入本期，并提供明确治理入口、dry-run / apply 与风险边界。
- 对象存储直出纳入本期能力边界；为后续 CDN 接入预留稳定字段、key/prefix 和缓存边界。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 多规格资源定义 | 明确 `thumbnail`、`display`、`original` 的业务语义、使用场景和关系。 |
| 上传生成策略 | 新上传图片生成多规格资源，并记录生成成功、失败和降级行为。 |
| URL 字段扩展 | 商品或媒体相关接口返回可供多端选择的多规格 URL 字段。 |
| 小程序图片选择策略 | 列表、详情展示、高清预览使用不同规格图片，并对首屏外图片启用 lazy-load。 |
| 对象存储 key/prefix | 多规格资源必须遵守对象存储 key 布局和 MinIO 单桶前缀策略。 |
| 存量媒体批量生成 | 存量图片批量生成多规格资源纳入本期，必须提供 dry-run / apply、幂等性、失败统计和脱敏输出。 |
| 对象存储直出 | 对象存储直出纳入本期，必须明确签名、鉴权、缓存、公开范围、fallback 和后端代理兼容边界。 |
| CDN 预留 | 字段和资源模型需支持后续切换 CDN，不把后端代理或对象存储直出写死为唯一 URL 形态。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 单个页面缺陷修复 | `BUG-0132` 负责已发现的小程序详情冷加载偏差，本需求负责通用能力建设。 |
| 视频转码或多清晰度 | 本需求只覆盖图片多规格展示图，不覆盖视频转码、封面生成或多清晰度播放。 |
| 外部 CDN 正式接入 | 本期纳入对象存储直出，但不默认完成生产 CDN 改造。 |
| 绕过后端鉴权上传 | 上传、派生生成和对象访问仍必须经过既有后端媒体服务和对象存储适配层。 |
| 无授权批量改写生产历史对象 | 存量媒体重生成必须有 dry-run、备份或人工确认，不自动改写生产对象。 |
| 新建独立图片处理平台 | 本期不建设可视化媒体处理平台或独立运维控制台。 |

## 5. 功能要求

### FR-001 多规格资源模型

- 系统 MUST 将媒体图片区分为 `thumbnail`、`display`、`original` 三类规格。
- `thumbnail` MUST 面向列表、卡片、轻量预览等低成本场景。
- `display` MUST 面向商品详情、图册普通浏览等清晰展示场景。
- `original` MUST 保留上传原图或等价高清资源，用于高清预览、下载或需要保真的场景。
- 三类资源 MUST 能追溯到同一原始媒体记录或媒体业务对象。
- 三类资源的 key、MIME、尺寸、质量、体积上限和生成状态 SHOULD 可被后端服务或维护任务追踪。

### FR-002 上传生成与失败降级

- 新上传图片 SHOULD 在上传链路中生成 `thumbnail` 和 `display` 派生资源，并保留 `original`。
- 生成策略 MUST 明确触发时机，包括上传成功后同步生成、异步生成、懒生成或维护任务补生成。
- 生成失败 MUST 有可观测记录，并明确是否阻断原图上传。
- 当派生资源缺失或生成失败时，系统 MUST 有明确 fallback 规则，例如回退 `original_url`、保留旧派生图或显示占位。
- 系统 MUST 避免使用用户原始文件名作为对象 key。
- 系统 MUST 不暴露内部本机路径、对象存储密钥、Authorization header、Cookie 或真实 `.env` 内容。

### FR-003 URL 字段与接口返回

- 商品、SKU 或媒体相关 API SHOULD 返回 `thumbnail_url`、`display_url`、`original_url`，或通过统一媒体服务适配为同等语义字段。
- API 字段 MUST 明确缓存策略、访问权限和过期策略，特别是代理 URL、签名 URL、CDN URL 或对象存储直出 URL 的差异。
- 字段新增或响应结构调整 MUST 同步 OpenAPI、Orval、API 文档和相关测试。
- API 兼容性 MUST 明确旧客户端在缺少多规格字段时的降级行为。
- 错误响应 MUST 使用项目统一错误码，不得暴露对象存储内部实现细节。

### FR-004 多端图片选择策略

- 微信小程序列表页 MUST 优先使用 `thumbnail_url`。
- 微信小程序商品详情普通展示 MUST 优先使用 `display_url`。
- 微信小程序图片高清预览 MUST 使用 `original_url` 或等价高清 URL。
- 详情页首屏外图片 SHOULD 开启 lazy-load，减少非关键图片对首屏基础浏览的影响。
- Web 店主展示端和管理端若使用商品图片，也 SHOULD 按列表、详情、预览场景选择合适规格。
- 当目标规格 URL 缺失或加载失败时，前端 MUST 按统一 fallback 顺序处理，避免空白或无限重试。

### FR-005 存量媒体批量生成

- 系统 MUST 支持存量图片批量生成 `thumbnail` 和 `display`。
- 存量媒体维护入口 MUST 支持 dry-run，输出待处理数量、预计写入对象、跳过原因和风险提示。
- 写入型 apply MUST 具备幂等性、失败统计、重试建议和脱敏输出。
- 存量维护 MUST 明确是否修改数据库记录；不改表时必须说明只生成派生对象或更新可派生 URL。
- 维护任务 MUST 遵守对象存储前缀、上传安全和真实客户数据保护规则。

### FR-006 对象存储直出与后续 CDN 预留

- 多规格资源 MUST 遵守 `REQ-0012-object-storage-key-layout` 的对象 key 布局。
- 多规格资源 MUST 遵守 MinIO 单 Bucket + 前缀策略，不因规格扩展新增独立 Bucket。
- URL 生成 MUST 通过后端媒体服务或统一对象存储适配层封装，避免前端硬编码存储实现。
- 对象存储直出 MUST 明确签名 URL、公开 URL、受控 `/media` 代理 URL 的选择条件、过期策略、缓存策略和 fallback。
- 能力设计 SHOULD 允许未来切换 CDN URL。
- 对象存储直出策略 MUST 保持鉴权、公开范围和缓存边界清晰，不得默认公开所有原图。

## 6. UI / UE 约束

- 小程序列表图片应优先保证快速可见，避免为卡片列表加载高清原图。
- 小程序详情首屏应优先加载核心商品信息和可见图片，首屏外图应延迟加载。
- 图片预览应保持高清体验，不能因列表和详情优化而丢失原图查看能力。
- 管理端若展示生成状态、失败原因或维护任务结果，应使用紧凑表格、状态标识和可扫描的失败摘要。
- Web 管理端或店主端 UI 变更必须遵守 Design System semantic token，不得直接使用裸 Hex。
- 不应在用户界面暴露对象 key、内部路径、异常堆栈或存储服务细节。

## 7. 非功能约束

- MUST 遵守上传安全规则，包括文件大小、MIME Type、扩展名和对象 key 安全。
- MUST 通过后端鉴权和媒体适配层处理上传与对象访问，前端不得直连未授权对象存储。
- MUST 保持媒体相关代码集中在 media 模块或既有媒体服务边界内。
- MUST 区分小程序、店主展示端和管理端权限边界。
- SHOULD 通过尺寸、质量、格式或体积上限控制派生图片下载成本。
- SHOULD 为生成失败、对象缺失、URL 失效和存量维护失败提供可定位日志或测试证据。
- 若涉及 DB 结构变化，MUST 同步 SQLite/MySQL schema、迁移文档和测试。
- 若涉及 API 变化，MUST 同步 OpenAPI / Orval / API 文档 / 测试。

## 8. 关联需求与缺陷

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 父需求 | `REQ-0012-object-storage-key-layout` | 多规格资源 key/prefix 必须遵守既有对象存储布局。 |
| 关联需求 | `REQ-0099-global-thumbnail-size-limit` | 提供缩略图体积、尺寸和生成策略治理基础。 |
| 关联 BUG | `BUG-0132-miniapp-sku-detail-large-image-cold-load` | 本需求来源于小程序详情页冷加载问题背后的通用能力缺口。 |
| 关联 BUG | `BUG-0125-miniapp-sku-detail-media-original-load` | 历史详情页原图加载问题，可作为规格选择策略参考。 |
| 关联 BUG | `BUG-0110-miniapp-card-banner-thumbnail-usage` | 历史卡片缩略图使用问题，可作为列表图选择策略参考。 |
| 关联规范 | `rules/media.md` | 后续实现需同步媒体生成、URL 和验收规则。 |
| 关联规范 | `rules/object-storage.md` | 后续实现需同步对象存储 key、URL 和直出策略。 |

## 9. 状态块

```yaml
requirement_id: REQ-0115-media-multi-variant-images
status: done
lifecycle_stage: review
readiness: Partially Ready
next_command: /opsx-archive REQ-0115-media-multi-variant-images
notes:
  - 已根据 capture 生成 requirement.md。
  - 已补齐 user-stories、business-flow、acceptance、trace 扩展信息和原型策略。
  - 本需求聚焦媒体图片多规格展示图通用能力，不直接修复单个页面缺陷。
  - Readiness 为 Partially Ready：命中的 knowledge-base 文档为 draft，且 UI 原型当前为策略说明，PNG 待后续 OpenSpec Change 阶段导出。
  - 评审已确认存量图片批量生成纳入本期，对象存储直出纳入本期，CDN 正式接入仅预留。
  - 已纳入 sprint-025 正式范围，后续可执行 /req-opsx REQ-0115。
  - 后续 req-opsx 需确认 display 规格、格式转换策略、API 字段落点和对象存储直出的签名/缓存/权限边界。
```
openspec_changes:
  - change_id: add-media-multi-variant-images
    type: update
    status: archived
