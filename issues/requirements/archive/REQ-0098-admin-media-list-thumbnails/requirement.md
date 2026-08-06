---
requirement_id: REQ-0098-admin-media-list-thumbnails
title: 管理端图片密集列表使用缩略图展示
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-05 09:07:28
updated_at: 2026-08-05 22:36:57
---

# REQ-0098 管理端图片密集列表使用缩略图展示

## 1. 需求背景

管理端 SKU、品牌、证书和 Banner 列表都是运营人员高频浏览的图片密集页面。列表页通常只需要快速识别对象，不需要加载原图级资源；但当前部分列表仍直接使用原图 URL，导致首屏、翻页和滚动时图片加载体感偏慢，也带来不必要的带宽与媒体读取成本。

现有系统已经具备媒体缩略图基础能力，品牌和证书列表也已经出现缩略图优先展示策略。SKU 列表与 Banner 列表仍缺少对应的缩略图响应字段和前端使用策略，造成同类管理端列表的图片加载口径不一致。

本需求要求管理端图片密集列表统一采用“列表优先缩略图，详情/编辑/预览继续使用原图”的资源边界，补齐 SKU 与 Banner 列表的缩略图字段，并复核品牌、证书列表已有策略，提升管理后台列表浏览体验。

## 2. 目标用户

| 角色 | 核心诉求 |
|---|---|
| 后台运营人员 | 在 SKU、品牌、证书、Banner 列表中快速浏览对象图片，减少等待和破图干扰。 |
| 后台管理员 | 降低管理端图片密集页面的加载成本，保持不同列表的展示策略一致。 |
| 产品 / QA | 能明确列表缩略图、原图和 fallback 的验收边界，避免只凭体感判断。 |
| 前后端开发 | 有清晰字段契约和前端优先级规则，避免页面各自临时拼接或重复判断。 |

## 3. 需求目标

- SKU 管理列表响应提供主图缩略图字段，列表页优先展示缩略图。
- Banner 管理列表响应提供图片缩略图字段，列表页优先展示缩略图。
- 品牌列表与证书列表复核并保持缩略图优先、原图兜底的现有策略。
- 前端列表页在缩略图缺失、加载失败或不可用时安全 fallback 到原图或既有占位。
- 详情、编辑、放大预览、原文件查看等需要清晰资源的场景继续使用原图。
- API 契约变化必须同步 OpenAPI / Orval，并补充必要后端和前端测试。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| SKU 列表缩略图字段 | 管理端 SKU 列表响应增加 `main_image_thumbnail_url`，由后端受控媒体路径派生。 |
| Banner 列表缩略图字段 | 管理端 Banner 列表响应增加 `image_thumbnail_url`，由 `image_object_key` 或等价媒体 key 派生。 |
| 前端列表优先级 | SKU 与 Banner 列表优先使用缩略图字段，缺失时 fallback 到原图。 |
| 品牌与证书复核 | 确认品牌列表、证书列表继续优先使用已有缩略图字段，并补齐必要测试或验收说明。 |
| 原图使用边界 | 详情、编辑、上传预览、放大查看和原文件查看继续使用原图或原文件。 |
| API 与类型同步 | 新增响应字段需要同步 OpenAPI、Orval 生成代码和前端类型使用。 |
| 回归测试 | 覆盖字段返回、前端优先级、fallback 和缩略图缺失场景。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 新建缩略图生成体系 | 不重新设计媒体上传或缩略图生成机制，优先复用已有同目录缩略图能力。 |
| 数据库结构变更 | 不新增 SKU、Banner、品牌或证书表字段，缩略图 URL 由现有 object key 派生。 |
| 视频缩略图 | 不新增 SKU 视频、Banner 视频或其他视频缩略图能力。 |
| PDF 首页缩略图 | 证书 PDF 首页渲染缩略图不属于本需求范围。 |
| 历史媒体批量补齐强制执行 | 本需求不强制新增历史媒体维护任务；若后续发现存量缩略图缺失严重，可另行评估。 |
| 管理端视觉重设计 | 不重做列表布局、表格体系或卡片视觉，只调整图片资源选择和必要兜底。 |
| 店主 Web / 小程序改造 | 本需求聚焦 Web 管理端列表，不改变公开端或小程序展示策略。 |

## 5. 功能要求

### FR-001 SKU 列表返回主图缩略图

管理端 SKU 列表响应 MUST 为每个存在主图的 SKU 提供 `main_image_thumbnail_url` 字段。该字段 SHOULD 基于 SKU 主图 object key 派生受控 `/media/...` 缩略图路径。

当 SKU 无主图时，`main_image_thumbnail_url` MUST 为 `null` 或等价空值，并保持现有无图展示逻辑。系统不得要求前端直连对象存储或自行猜测未授权存储地址。

### FR-002 Banner 列表返回图片缩略图

管理端 Banner 列表响应 MUST 为每个存在图片的 Banner 提供 `image_thumbnail_url` 字段。该字段 SHOULD 基于 `image_object_key` 派生受控 `/media/...` 缩略图路径。

当 Banner 图片来源为 SKU 主图、SKU 图集、品牌 Logo、专题封面或自定义上传时，列表缩略图字段 MUST 与最终 `image_object_key` 指向的资源保持一致，不应使用跳转目标的其他图片。

### FR-003 前端列表优先使用缩略图

SKU 列表页和 Banner 列表页 MUST 优先使用缩略图字段展示图片。推荐优先级如下：

```text
缩略图 URL → 原图 URL → 既有无图/占位展示
```

缩略图字段为空、加载失败或不可用时，页面 MUST fallback 到原图或既有占位，不得显示浏览器默认破图，也不得造成表格行高或列宽明显抖动。

### FR-004 品牌与证书列表策略复核

系统 MUST 复核品牌列表和证书列表的图片展示策略，确认其已优先使用缩略图字段，并在缺失时回退原图或既有占位。

若品牌或证书列表存在页面内直接使用原图、字段优先级不一致、加载失败兜底缺失等问题，后续实现 MUST 在同一 Change 中修正，或明确记录不适用原因。

### FR-005 原图使用边界

详情页、编辑弹窗、上传预览、放大预览、原文件查看和下载场景 SHOULD 继续使用原图或原文件，以保证运营人员能检查图片清晰度和文件真实性。

列表页缩略图优化不得降低编辑、审核和预览场景的图片质量，不得改变用户保存、发布、上下线或删除流程。

### FR-006 API 契约与 Orval 同步

新增 `main_image_thumbnail_url` 和 `image_thumbnail_url` 属于管理端 API 响应契约变化。后续实现 MUST 同步：

- 后端 Pydantic Schema。
- OpenAPI 输出。
- Orval 生成客户端与类型。
- 前端列表页字段使用。
- 相关后端与前端测试。

API 字段应保持向后兼容：新增字段不得移除或改变现有 `main_image_url`、`image_url` 的语义。

### FR-007 缩略图不可用时的回退

系统 MUST 明确缩略图不可用时的处理策略：

- 缩略图字段不存在或为空：前端 fallback 到原图。
- 缩略图请求失败：前端 fallback 到原图或既有占位。
- 原图也不可用：展示既有无图、首字母、文件类型或缺图占位。
- 失败态不得阻塞列表数据展示和行操作。

后续实现 MAY 记录媒体加载失败的前端或后端可观测信息，但不得在 PRD 阶段引入额外日志字段作为强制范围。

## 6. UI 约束

- 管理端列表继续遵守现有暗色旗舰风和 Design System semantic token。
- 图片容器尺寸、裁切方式和行高应保持稳定，不因缩略图、原图或占位切换造成布局抖动。
- SKU 与 Banner 列表不新增说明卡片、营销式引导或大面积视觉改版。
- 图片加载失败时不得显示浏览器破图，应沿用既有缺图占位、空态或业务 fallback。
- 缩略图仅用于列表快速识别，不应替代详情、编辑和放大预览中的原图检查能力。

## 7. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 不要求新增或修改表结构。 |
| Pydantic Schema | 需要为管理端 SKU 与 Banner 列表项新增缩略图响应字段。 |
| OpenAPI/Orval | 需要同步 OpenAPI 与 Orval 生成物。 |
| 管理端 Web | 需要调整 SKU 与 Banner 列表图片字段优先级，并复核品牌、证书列表。 |
| 小程序 | 不涉及。 |
| 店主 Web | 不涉及。 |
| 媒体上传 / 对象存储 | 不改变上传鉴权和对象存储访问边界，复用后端受控媒体路径。 |
| 测试 | 需要补充 API 字段、前端渲染优先级和 fallback 测试。 |

## 8. 关联需求与现状参考

| 关联项 | 关系 | 说明 |
|---|---|---|
| REQ-0006-tile-sku-management | 关联业务域 | SKU 列表需要补齐主图缩略图字段和列表展示策略。 |
| REQ-0016-banner-management | 关联业务域 | Banner 列表需要补齐图片缩略图字段和列表展示策略。 |
| REQ-0038-brand-certificate-management | 关联业务域 | 证书列表需要复核缩略图优先与原图预览边界。 |
| REQ-0092-brand-certificate-image-thumbnails | 能力基础 | 品牌与证书图片真实缩略图能力可作为本需求的现有基础。 |
| REQ-0095-admin-list-field-display-adapter-checklist | 展示治理参考 | 管理端列表 image adapter 规则可作为验收检查口径。 |

## 9. 状态块

```yaml
requirement_id: REQ-0098-admin-media-list-thumbnails
status: done
priority: P1
readiness: Ready
parent_requirement: null
terminal: web-admin
target_clients:
  web_admin: included
  web_catalog: not_included
  wechat_miniapp: not_included
api_change_required: true
database_change_required: false
orval_required: true
prototype_required: false
next_step: /opsx-apply optimize-admin-media-list-thumbnails
open_questions:
  - 品牌与证书列表是否只需补测试验收，还是需要同步改造字段命名或加载失败兜底。
  - 缩略图请求失败后前端 fallback 到原图时，是否需要记录可观测事件。
  - 是否需要在后续 Change 中补充历史媒体缩略图 dry-run 检查，或保持为独立后续需求。
notes:
  - 本需求仅生成 PRD，不直接实现接口、前端或 OpenSpec Change。
  - 新增响应字段必须保持向后兼容，不改变现有原图 URL 字段语义。
```
