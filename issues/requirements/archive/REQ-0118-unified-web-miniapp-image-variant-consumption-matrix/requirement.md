---
requirement_id: REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
title: 统一 Web 与小程序图片三规格消费矩阵
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0115-media-multi-variant-images
created_at: 2026-08-22 20:32:30
updated_at: 2026-08-25 14:53:29
related_change: update-media-image-variant-consumption-matrix
---

# REQ-0118 统一 Web 与小程序图片三规格消费矩阵

## 1. 需求背景

系统已在 `REQ-0115-media-multi-variant-images` 和 `openspec/specs/media-multi-variant-images/spec.md` 中定义 `thumbnail`、`display`、`original` 三类图片规格：缩略图用于列表、卡片和轻量预览；展示图用于详情普通展示和图册浏览；原图用于高清预览、下载或保真场景。

当前问题不在于缺少三规格概念，而在于 Web 与微信小程序的页面级消费规则分散在 spec、README、组件实现和历史验收口径中。不同页面、不同对象对三规格 URL 的选择和 fallback 边界不够集中，容易出现列表加载原图、详情展示缩略图、预览误用展示图、fallback 到原图却被当作性能通过等问题。

本需求要求沉淀一份统一的跨端图片三规格消费矩阵，明确每个端、页面、位置、图对象应消费的图片规格，并明确不允许保留原图 fallback 的治理边界。本需求只做规范矩阵，不直接修改 Web、小程序、后端接口或对象存储实现。

## 2. 目标用户

| 用户 | 核心诉求 |
|---|---|
| 产品负责人 | 快速判断某个页面、位置和图对象应使用缩略图、展示图还是原图，减少口径反复确认。 |
| 测试人员 | 基于统一矩阵验收媒体展示，不把原图兜底误判为缩略图或展示图性能达标。 |
| Web 管理端开发 | 在管理端列表、表单、预览和证书等场景中按统一规则选择图片字段。 |
| 小程序开发 | 在首页、列表、详情、预览和收藏等场景中按统一规则选择图片字段。 |
| 后端 / 媒体服务开发 | 为 API 字段、fallback 策略、对象存储派生图和后续治理提供稳定消费契约。 |

## 3. 需求目标

- 建立 Web 与微信小程序统一的图片三规格消费矩阵。
- 矩阵 MUST 覆盖页面、位置、图对象、是否缩略图、是否 display 图、是否原图、优化方案。
- 明确 `thumbnail`、`display`、`original` 在跨端页面中的使用规则。
- 明确店主 Web 展示端当前按预留规范处理，不要求本期梳理真实页面实现。
- 明确 fallback 到原图不允许保留；缺少目标规格时应标注为需补齐或使用安全占位。
- 将当前已发现的偏离点记录为优化方案，但本需求本身不直接实施代码修正。
- 为后续 `/req-complete`、OpenSpec Change、验收模板和媒体验收提供统一依据。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 三规格定义 | 沉淀 `thumbnail`、`display`、`original` 的差异、适用场景和禁止误用规则。 |
| 小程序消费矩阵 | 覆盖首页、商品列表、搜索、商品详情、品牌列表、品牌详情、证书列表、证书详情、收藏等页面。 |
| Web 管理端消费矩阵 | 覆盖当前真实存在的管理端 SKU、Banner、品牌、证书、头像等媒体展示位置。 |
| 店主 Web 预留规范 | 店主 Web 展示端当前按预留规范处理，定义未来接入时的图片规格选择规则。 |
| 图对象分类 | 覆盖商品、Banner、品牌 Logo、证书图片/PDF、用户头像、视频封面等对象。 |
| fallback 治理 | 明确目标规格缺失时不得 fallback 到原图；应使用安全占位、补齐派生图或标记优化。 |
| 优化方案列 | 对每个矩阵项给出 `-` 或明确优化内容，作为后续实现与验收拆分依据。 |
| 关联规范落点 | 明确后续应更新的媒体规范、对象存储规范、API 字段语义或验收模板落点。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 代码实现修正 | 本需求只生成规范矩阵，不直接修改 Web、小程序、后端、API 或对象存储代码。 |
| 店主 Web 真实页面验收 | 店主 Web 当前仅按预留规范定义消费规则，不要求本期逐页验证真实页面。 |
| 新增图片生成能力 | 不新增缩略图、展示图、PDF 缩略图、视频封面或历史对象批量生成能力。 |
| 新增数据库字段 | 不要求修改 SQLite/MySQL 表结构。 |
| 新增 API 字段 | 不直接新增或调整 API 响应字段；若后续实现需要字段变更，应另行在 Change 中同步 OpenAPI、Orval、文档和测试。 |
| CDN 或对象存储重构 | 不改变 MinIO 单桶策略、后端媒体适配层、签名 URL 或 CDN 预留边界。 |
| UI 视觉改版 | 不重做页面布局、视觉风格或交互，只定义媒体规格消费口径。 |
| 历史图片批量治理 | 不强制执行历史图片重生成、迁移或清理。 |

## 5. 功能要求

### FR-001 三规格语义必须统一

需求文档 MUST 明确三类图片规格的统一语义：

| 规格 | 语义 | 主要用途 |
|---|---|---|
| `thumbnail` | 小尺寸、低体积、快速识别图 | 列表、卡片、推荐位、小 Logo、证书缩略卡、视频封面。 |
| `display` | 中等尺寸、适合普通查看的展示图 | 商品详情 Banner、详情图册、表单大预览、证书详情普通展示。 |
| `original` | 上传原图或等价高清资源 | 点击放大、高清预览、下载、审核保真查看。 |

矩阵中的每个页面位置 MUST 只能把主要消费规格标为 `是`，其他规格标为 `否`；若某位置同时存在普通展示和点击预览，必须拆成两行分别表达。

### FR-002 小程序消费矩阵必须覆盖当前页面

小程序矩阵 MUST 至少覆盖以下页面与位置：

| 页面 | 必须覆盖的位置 |
|---|---|
| 首页 | Banner、新品/热销/全部商品卡片、品牌入口或配置 Logo。 |
| 商品列表 | 商品卡片主图。 |
| 搜索页 | 商品搜索结果卡片。 |
| 商品详情页 | Banner 普通展示、图片预览、品牌区域、同系统推荐、同品牌推荐、视频封面。 |
| 品牌列表页 | Banner、品牌 Logo。 |
| 品牌详情页 | 品牌 Logo、品牌商品、品牌证书。 |
| 证书列表页 | 证书缩略图。 |
| 证书详情页 | 证书普通展示、图片预览或文件查看。 |
| 收藏页 | 收藏商品卡片。 |

对不使用业务媒体的页面，矩阵 MAY 标注“不涉及业务图片”并说明无需优化。

### FR-003 Web 管理端消费矩阵必须覆盖当前真实媒体位置

Web 管理端矩阵 MUST 至少覆盖以下页面与位置：

| 页面 | 必须覆盖的位置 |
|---|---|
| SKU 管理 | SKU 列表主图、SKU 表单图片网格或预览。 |
| Banner 管理 | Banner 列表图、Banner 表单选择/回显预览。 |
| 品牌管理 | 品牌列表 Logo、品牌表单 Logo 回显。 |
| 品牌证书管理 | 证书列表缩略图、证书表单附件或图片预览。 |
| 用户 / 个人资料 | 头像列表、头像菜单、头像表单或个人资料展示。 |

Web 管理端矩阵 MUST 基于当前真实页面和组件现状描述，不得把模板组件或未接入页面当作已上线消费点。

### FR-004 店主 Web 展示端必须按预留规范定义

店主 Web 展示端当前不要求逐页验证真实页面实现，但 MUST 在矩阵中提供预留规范：

| 未来场景 | 预留规则 |
|---|---|
| 商品列表 / 商品卡片 / 推荐商品 | 使用 `thumbnail`。 |
| 商品详情普通展示 / 图册浏览 | 使用 `display`。 |
| 点击放大 / 高清预览 / 下载 | 使用 `original`。 |
| 品牌列表 Logo / 品牌卡片 | 使用 `thumbnail`。 |
| 品牌详情 Logo 或品牌头图普通展示 | 使用 `display`，若只是小尺寸 Logo 区域则使用 `thumbnail`。 |
| 证书列表 | 使用 `thumbnail`。 |
| 证书详情普通展示 | 使用 `display`。 |
| 证书下载或原文件查看 | 使用 `original`。 |

矩阵 MUST 明确这些条目为“预留规范”，不得写成当前实现已满足。

### FR-005 fallback 到原图不允许保留

统一矩阵 MUST 明确以下规则：

- 列表、卡片、推荐位、小 Logo 等目标规格为 `thumbnail` 的位置，不允许 fallback 到 `original`。
- 详情普通展示和图册浏览等目标规格为 `display` 的位置，不允许 fallback 到 `original`。
- 高清预览、下载和保真查看等目标规格为 `original` 的位置，才允许直接使用原图。
- 当目标规格缺失、生成失败或不可读时，应使用安全占位、提示不可用、阻断发布或标记为需补齐派生图，具体策略由矩阵优化方案列说明。
- 任何因历史实现存在原图 fallback 的位置，矩阵 MUST 在“优化方案”中标记为移除原图 fallback 或补齐目标规格字段。

### FR-006 矩阵字段必须固定

统一矩阵 MUST 至少包含以下字段：

| 字段 | 说明 |
|---|---|
| 页面 | 具体页面或“店主 Web 预留”。 |
| 位置 | 页面中的展示区域、列表列、表单预览、弹窗或交互位置。 |
| 图对象 | 商品、Banner、品牌、证书、头像、视频封面等。 |
| 是否缩略图 | 该位置主消费规格是否为 `thumbnail`。 |
| 是否 display 图 | 该位置主消费规格是否为 `display`。 |
| 是否原图 | 该位置主消费规格是否为 `original`。 |
| 优化方案 | 不需要优化填 `-`；需要优化时写明补字段、换规格、移除原图 fallback、补占位或拆分预览场景。 |

若同一页面位置在普通展示和点击预览中使用不同规格，MUST 拆成独立行，例如“商品详情页 / Banner 普通展示”和“商品详情页 / 图片预览”。

### FR-007 现状偏离点必须进入优化方案列

矩阵 MUST 将已知偏离点记录为优化方案，而不是默认视为符合规范。已知偏离点至少包括：

- 小程序商品详情页品牌区域若只能拿到品牌原图 URL，应标记为补充或改用品牌缩略图。
- 小程序证书详情普通展示若使用缩略图或原文件 URL，应标记为改用 `display` 或补齐 display 字段。
- Web Banner 表单回显若使用当前 URL 或原图，应标记为按来源对象选择 `display` 或安全占位。
- Web 品牌表单编辑态若直接使用品牌原图，应标记为改用 `thumbnail` 或 `display`，按展示尺寸确定。
- Web 头像列表、菜单和表单若只有 `avatar_url`，应标记为补齐头像缩略图或明确头像不纳入三规格体系的例外审批。
- Web Banner 列表、品牌列表、证书列表等历史存在原图 fallback 的位置，应标记为移除原图 fallback 或补齐目标规格。

本需求只要求记录这些优化方案，不直接完成修复。

### FR-008 关联规范必须说明沉淀落点

后续 `/req-complete` 或 OpenSpec Change SHOULD 明确统一矩阵的长期落点，候选包括：

- `openspec/specs/media-multi-variant-images/spec.md`
- `rules/media.md`
- `rules/object-storage.md`
- 媒体类验收模板或测试 helper 文档
- 小程序 README 或页面规格相关文档
- Web 管理端媒体展示规范相关文档

落点选择 MUST 避免事实重复冲突：三规格全局语义优先归属媒体规格；页面级矩阵优先归属本需求或后续规范文档；实现细节归属对应 OpenSpec Change、代码和测试。

## 6. UI 约束

- 本需求不新增或修改任何 Web、小程序 UI。
- 统一矩阵应使用紧凑 Markdown 表格，便于产品、开发、测试扫描。
- 矩阵中不得使用大段解释性文案替代字段值；优化方案应短句表达可执行治理动作。
- 若后续将矩阵展示到 Web 工具页面，必须遵守 Design System semantic token，不得直接写裸 Hex。
- 店主 Web 预留条目必须有明显标识，避免被误读为当前已上线页面验收结果。

## 7. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 本需求不要求数据库变更。 |
| Pydantic Schema | 本需求不直接要求 Schema 变更；后续修正偏离点如需字段支持，应在对应 Change 中声明。 |
| OpenAPI/Orval | 本需求不直接要求同步；后续 API 字段变更时必须同步。 |
| Web 管理端 | 只梳理真实媒体消费位置，不直接改代码。 |
| 店主 Web | 仅定义预留规范，不做真实页面验收。 |
| 微信小程序 | 只梳理页面级消费矩阵，不直接改代码。 |
| 媒体上传 / 对象存储 | 不改变上传、派生图生成、签名 URL、MinIO Bucket 或 key/prefix 策略。 |
| 测试 | 本需求阶段不新增自动化测试；后续实现偏离点时必须补充对应测试或验收证据。 |

## 8. 关联需求与规范

| 类型 | ID / 文件 | 关系 |
|---|---|---|
| 父需求 | `REQ-0115-media-multi-variant-images` | 三规格图片能力与全局语义来源。 |
| 关联需求 | `REQ-0098-admin-media-list-thumbnails` | 管理端图片密集列表缩略图治理经验。 |
| 关联需求 | `REQ-0092-brand-certificate-image-thumbnails` | 品牌与证书缩略图能力来源。 |
| 关联需求 | `REQ-0111-miniapp-media-four-part-acceptance-practice` | 小程序媒体链路验收实践关联。 |
| 关联规范 | `openspec/specs/media-multi-variant-images/spec.md` | 已有三规格能力正式规格。 |
| 关联规范 | `openspec/specs/object-storage/spec.md` | 对象存储、多规格图片和受控 URL 规则。 |
| 关联规范 | `rules/media.md` | 媒体治理、上传与验收规则候选落点。 |
| 关联规范 | `docs/standards/file-upload.md` | 文件上传与媒体字段语义参考。 |

## 9. 状态块

```yaml
requirement_id: REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
status: done
lifecycle_stage: plan
readiness: Partially Ready
parent_requirement: REQ-0115-media-multi-variant-images
terminal: multi
target_clients:
  web_admin: included
  web_catalog: reserved_spec_only
  wechat_miniapp: included
scope_decisions:
  matrix_only: true
  web_catalog_mode: reserved_spec_only
  original_fallback_allowed: false
api_change_required: false
database_change_required: false
orval_required: false
prototype_required: false
next_command: /opsx-archive REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
notes:
  - 已根据 capture、req-explore 结论和用户补充决策生成 requirement.md。
  - 已补齐 user-stories、business-flow、acceptance 与 prototype 策略。
  - 本需求只沉淀统一消费矩阵，不直接修复实现偏离。
  - 店主 Web 展示端当前作为预留规范处理。
  - fallback 到原图不允许保留；非原图目标场景缺少目标规格时应补齐派生图或使用安全占位。
  - 命中的 knowledge-base best-practices 当前为 draft，因此 readiness 为 Partially Ready。
  - 已评审通过并纳入 sprint-025，待创建 OpenSpec Change。
```
openspec_changes:
  - change_id: update-media-image-variant-consumption-matrix
    type: update
    status: archived
