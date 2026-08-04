---
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
title: 管理端列表字段展示统一 adapter 检查表
terminal: web-admin
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-04 08:27:12
updated_at: 2026-08-04 09:29:56
---

# REQ-0095 管理端列表字段展示统一 adapter 检查表

## 1. 需求背景

管理端列表页承载品牌、证书、SKU、Banner、分类等核心运营对象。运营人员在列表中通常需要快速识别对象图片、对象名称、关联信息和状态，判断是否需要编辑、发布、下线或补齐素材。

当前管理端已经存在若干局部展示 helper，例如品牌 Logo 来源选择、品牌首字母兜底、Banner 跳转目标与图片来源、SKU 状态和时间格式化等。但 image、name、fallback 三类展示口径仍分散在各页面和局部工具函数中：有的列表在页面内直接判断图片，有的列表使用业务 helper，有的空值展示为 `—`，有的展示为“未设置”，有的媒体加载失败仅隐藏图片。

本需求要求建立一份统一的管理端列表字段展示 adapter 检查表，用于后续设计、开发、验收和回归时统一检查图片、名称与兜底展示规则，减少每个列表页各自实现造成的不一致。

## 2. 目标用户

| 角色 | 核心诉求 |
|---|---|
| 后台运营 | 在不同列表页中稳定识别对象图片、名称和缺失信息，减少误判。 |
| 后台管理员 | 统一管理端列表展示质量，避免页面之间出现明显体验差异。 |
| 产品 / 设计 | 用固定检查表描述列表展示口径，减少需求和验收遗漏。 |
| 前端开发 | 明确 image、name、fallback 的字段优先级与展示兜底，避免重复临时判断。 |
| QA / 验收人员 | 按统一清单覆盖无图、空名称、关联缺失和加载失败等边界场景。 |

## 3. 需求目标

- 建立管理端列表字段展示统一检查表，覆盖 image adapter、name adapter 和 fallback adapter。
- 明确首批需要纳入检查的管理端列表范围。
- 统一图片字段的来源优先级、占位、加载失败和无图态检查口径。
- 统一名称字段的主名称、辅助名称、空值、截断和关联缺失检查口径。
- 统一兜底文案与异常数据展示口径，降低页面之间的视觉和语义差异。
- 为后续 OpenSpec、实现、测试和回归提供可执行验收依据。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 检查表定义 | 形成一份可用于后续需求、设计、开发与验收的 image/name/fallback adapter 检查表。 |
| 首批列表覆盖 | 至少覆盖品牌列表、证书列表、SKU 列表、Banner 列表。 |
| image adapter | 明确图片来源优先级、缩略图优先、主图选择、无图态、加载失败态和 alt / aria 语义检查项。 |
| name adapter | 明确主名称、辅助名称、关联对象名称、空值、截断、长文本和重复字段展示检查项。 |
| fallback adapter | 明确空值、未设置、已删除关联对象、接口字段缺失、无权限和媒体加载失败等兜底检查项。 |
| 现状盘点 | 梳理首批列表中已有 helper、页面内判断和样式兜底，标记可复用与待统一项。 |
| 验收口径 | 要求后续实现或治理变更按检查表逐项回归，避免仅凭视觉主观判断。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 立即重构所有列表 | 本需求先建立检查表与验收口径，不要求本阶段直接改造所有页面实现。 |
| 新增业务字段 | 不新增品牌、证书、SKU、Banner 等业务对象字段。 |
| 新增接口能力 | 不要求新增接口、筛选条件、排序条件或响应结构。 |
| 公开端展示治理 | 不覆盖店主 Web 或微信小程序列表展示，除非后续需求另行纳入。 |
| 上传链路改造 | 不调整媒体上传、缩略图生成、对象存储或图片压缩策略。 |
| 设计系统大改 | 不重做管理端表格组件体系；如需抽公共组件，应在后续 OpenSpec 阶段评估。 |

## 5. 核心概念

### 5.1 image adapter

image adapter 指列表页将业务对象转换为可展示图片信息的规则集合，包括图片 URL 来源优先级、缩略图优先策略、主图选择、无图占位、加载失败兜底、图片尺寸与可访问性语义。

### 5.2 name adapter

name adapter 指列表页将业务对象转换为可读名称信息的规则集合，包括主名称、辅助名称、编号、关联对象名称、空名称兜底、长文本截断和重复字段去重。

### 5.3 fallback adapter

fallback adapter 指列表页面对缺失、异常或不可展示数据时的统一兜底规则，包括空字段、未设置、已删除关联对象、无权限、接口字段缺失、媒体加载失败和未知枚举值。

### 5.4 检查表

检查表不是单次页面文案，而是后续需求、设计、实现、测试和验收可引用的固定清单。它应足够具体，能让开发和 QA 判断某个列表页是否满足展示一致性要求。

## 6. 功能要求

### FR-001 检查表归属与结构

- MUST 建立管理端列表字段展示统一 adapter 检查表。
- 检查表 MUST 至少包含 image adapter、name adapter、fallback adapter 三个章节。
- 检查表 MUST 明确适用范围、适用列表、字段类型、检查项、期望表现和验证方式。
- 检查表 SHOULD 标记哪些规则是强制项，哪些规则是推荐项。
- 检查表 SHOULD 支持在后续 OpenSpec design、验收标准或测试用例中直接引用。

### FR-002 首批管理端列表覆盖

- 首批覆盖范围 MUST 至少包含品牌列表、证书列表、SKU 列表和 Banner 列表。
- SHOULD 评估是否纳入分类列表、规格列表、用户列表、审计日志列表和上传资源列表。
- 每个纳入范围的列表 MUST 标记是否存在图片字段、主名称字段、关联名称字段和空值兜底场景。
- 对不适用 image adapter 的列表，MUST 在检查表中标记为“不适用”，不得遗漏。

### FR-003 image adapter 检查项

- MUST 明确图片来源优先级，例如缩略图优先于原图，主图优先于普通图片。
- MUST 明确无图态展示规则，避免某些列表空白、某些列表显示不同占位。
- MUST 明确图片加载失败后的兜底表现，例如显示占位、首字母、文件类型标识或统一缺图态。
- MUST 明确多图对象的主图选择规则，例如优先 `is_main`，否则按排序或第一张兜底。
- MUST 明确图片容器尺寸、裁切方式和行高稳定性要求，避免列表抖动。
- SHOULD 明确图片 `alt` 或 `aria-label` 语义，避免纯装饰图片和识别图片混用。

### FR-004 name adapter 检查项

- MUST 明确主名称字段来源，例如品牌名、证书名、SKU 名称、Banner 标题。
- MUST 明确辅助名称字段来源，例如编号、品牌、分类、文件名、跳转目标名称。
- MUST 明确名称为空、仅空格或接口字段缺失时的兜底展示。
- MUST 明确长名称截断、换行或 tooltip 策略，避免表格列宽被撑开。
- MUST 避免在同一行重复展示语义相同的名称或编号。
- SHOULD 明确关联对象缺失时的展示，例如“关联对象已删除”或统一兜底文案。

### FR-005 fallback adapter 检查项

- MUST 区分“未设置”“无数据”“不适用”“加载失败”“未知枚举值”等语义，不得全部混用同一个文案。
- MUST 明确空时间、空编号、空备注、空关联对象和空媒体字段的展示规则。
- MUST 明确接口字段缺失或值不可解析时页面不得崩溃。
- MUST 明确未知枚举值的兜底展示，优先显示安全可读值而不是空白。
- MUST 明确无权限字段的展示策略，避免泄露敏感信息或误导用户。
- SHOULD 保持兜底文案在首批列表内一致，例如统一使用 `—` 或统一业务文案，并说明适用场景。

### FR-006 现状盘点与复用建议

- MUST 盘点首批列表中已有的展示 helper、页面内判断和样式兜底。
- SHOULD 识别可复用的现有逻辑，例如品牌 Logo 来源选择、Banner 图片来源、SKU 主图选择、用户名称兜底等。
- SHOULD 标记需要后续治理的分散逻辑，例如页面内直接判断图片 URL、各自定义空值文案、媒体失败态不一致。
- 本需求不强制抽象公共 adapter；是否抽函数、组件或模板应在后续 OpenSpec design 中评估。

### FR-007 UI 与体验一致性

- 检查表 MUST 要求列表行高度、图片尺寸、名称截断和操作列布局保持稳定。
- 检查表 MUST 要求图片缺失或加载失败时不改变表格列宽和行高。
- 检查表 MUST 要求空值兜底文案不遮挡后续字段，不造成文本重叠。
- 检查表 SHOULD 要求状态标签、图片占位和文本颜色使用 Design System semantic token。
- 检查表不得要求新增说明卡片或营销式引导区域。

### FR-008 测试与验收支撑

- 后续实现或治理变更 MUST 基于检查表补充测试或验收记录。
- 验收 MUST 覆盖至少一种无图、一种图片加载失败、一种空名称、一种关联对象缺失和一种未知枚举值场景。
- 若场景难以自动化，MUST 在验收记录中说明人工验证方式和样例数据。
- 对首批覆盖列表，MUST 明确哪些项已通过、哪些项不适用、哪些项需后续治理。

## 7. UI 约束

- 管理端列表继续遵守现有暗色旗舰风和 Design System semantic token。
- 图片、名称和兜底状态不得引入裸 Hex 颜色或临时视觉体系。
- 列表页不新增大面积说明区、卡片化营销内容或与工作流无关的装饰。
- 表格单元格应保持可扫描、稳定、紧凑，避免因长名称、缺图或加载失败造成布局抖动。
- 如需要图标表示无图、文件类型或加载失败，应优先复用现有图标与状态样式。

## 8. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 本需求通常不要求新增或修改表结构。 |
| Pydantic Schema | 通常不要求新增 Schema；若后续为列表补齐缩略图、主图或关联名称字段，则需另行评估。 |
| OpenAPI/Orval | 本需求默认不需要；若后续接口契约变化，必须同步 OpenAPI 和 Orval。 |
| 管理端 Web | 建立列表字段展示检查表，并可能在后续 Change 中推动页面或 helper 统一。 |
| 小程序 | 本期不涉及。 |
| 店主 Web | 本期不涉及。 |
| 测试 | 后续实现需覆盖检查表中的关键兜底场景。 |

## 9. 关联需求与现状参考

| 关联项 | 关系 |
|---|---|
| `REQ-0005-brand-management` | 品牌列表涉及 Logo、品牌名称和无图兜底。 |
| `REQ-0038-brand-certificate-management` | 证书列表涉及证书图片、证书名、编号、有效期和文件类型。 |
| `REQ-0006-tile-sku-management` | SKU 列表涉及主图、SKU 名称、品牌、分类、素材完整度和状态。 |
| `REQ-0016-banner-management` | Banner 列表涉及展示图、标题、跳转目标和有效期兜底。 |
| `REQ-0092-brand-certificate-image-thumbnails` | 相关媒体需求，涉及品牌与证书真实缩略图生成。 |
| `src/web/src/features/admin/lib/brand-display.ts` | 现有品牌 Logo 与首字母兜底 helper。 |
| `src/web/src/features/admin/lib/banner-display.ts` | 现有 Banner 状态、跳转和图片来源 helper。 |
| `src/web/src/features/admin/lib/tile-sku-display.ts` | 现有 SKU 状态与时间展示 helper。 |
| `src/web/src/features/admin/lib/brand-certificate-display.ts` | 现有证书类型、有效期与展示状态 helper。 |

## 10. 状态块

```yaml
requirement_id: REQ-0095-admin-list-field-display-adapter-checklist
status: done
priority: P1
readiness: Ready
parent_requirement: null
terminal: web-admin
target_clients:
  web_admin: included
  web_catalog: not_included
  wechat_miniapp: not_included
api_change_required: unlikely
database_change_required: false
orval_required: false
prototype_required: false
next_step: /opsx-apply standardize-admin-list-field-display-adapters
notes:
  - 已纳入 sprint-019，可在 Sprint 门禁通过后进入 opsx-apply。
  - 本需求定位为管理端列表展示治理检查表，首批覆盖品牌、证书、SKU、Banner 列表。
  - 后续 design.md 必须引用 trace.md 中的 knowledge_base_refs。
  - 是否抽公共 adapter 函数或组件应在 OpenSpec design 中结合现有实现评估。
```
