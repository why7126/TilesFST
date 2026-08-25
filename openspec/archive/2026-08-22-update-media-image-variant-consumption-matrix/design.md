## 上下文

`media-multi-variant-images` 现有规格已经定义三类图片资源的通用语义和 API 字段方向，但缺少“页面位置如何消费”的统一事实源。REQ-0118 已确认三个范围决策：

- 本期只做规范矩阵。
- 店主 Web 展示端当前按预留规范处理。
- 非原图目标场景不允许保留 fallback 到原图。

本 Change 以规范更新为主，不引入实现改造。现有 Web 管理端、小程序中的偏离点只进入矩阵“优化方案”，作为后续拆分 Change 或 BUG 的依据。

## 目标 / 非目标

**目标：**

- 在 OpenSpec 中沉淀跨端三规格消费矩阵，覆盖微信小程序、Web 管理端和店主 Web 预留规范。
- 固定矩阵字段和拆行规则，使普通展示、预览、下载等场景不混写。
- 明确禁止非原图目标场景 fallback 到 `original`。
- 明确后续实现偏离点需要拆分处理，避免本规范 Change 混入代码修复。

**非目标：**

- 不修改 `src/`。
- 不新增或调整 API 字段、Pydantic Schema、OpenAPI 或 Orval。
- 不修改 SQLite/MySQL 表结构。
- 不新增图片派生生成、历史批量治理、CDN 或对象存储改造。
- 不做店主 Web 真实页面验收。

## 决策

### D1 矩阵归属到 `media-multi-variant-images`

选择修改 `media-multi-variant-images`，因为三规格消费规则是三规格媒体能力的直接下游契约。`object-storage` 继续负责 key、object、受控读取和存储边界，不重复承载页面矩阵。

替代方案是新增独立 capability，例如 `image-variant-consumption-matrix`。该方案会让三规格语义和消费规则分裂成两个事实源，后续评审需要同时查两份 spec，因此不采用。

### D2 店主 Web 使用预留规范

店主 Web 当前不作为真实页面验收对象，只写“预留规范”。这样能给未来店主 Web 商品卡、详情图册、证书展示留下清晰规则，同时避免把未接入或模板页面误写成已完成实现。

### D3 非原图目标场景不允许原图 fallback

列表、卡片、推荐位、小 Logo 和详情普通展示的目标分别是 `thumbnail` 或 `display`。这些场景如果 fallback 到 `original`，会掩盖派生图缺失，并可能造成移动端冷加载和对象存储流量问题。因此矩阵要求：缺目标规格时使用安全占位、补齐派生图或记录优化，不把原图 fallback 写作通过。

### D4 偏离点只记录不修复

REQ-0118 已明确只做规范矩阵。本 Change 的 tasks 只更新 OpenSpec 规格、Issue trace 和 Sprint scope，不修复小程序商品详情品牌 Logo、证书详情 display、Web Banner 表单、Web 品牌表单或头像等偏离点。

## 冲突处理

`prototype/web/context.md` 明确本需求不需要 HTML / PNG 原型。事实源优先级为：

```text
REQ-0118 acceptance.md 目标消费矩阵
  > requirement.md 范围与非目标
  > prototype/web/context.md 原型策略
  > rules/ui-design.md
  > 既有 OpenSpec 规格
```

如后续具体实现 Change 引入 UI 修改，应在对应 Change 中重新建立 UI Contract，并引用 REQ-0118 的消费矩阵作为媒体字段选择基线。

## 风险 / 权衡

| 风险 | 缓解 |
|---|---|
| 只更新规范，不修复现有偏离点，短期仍可能存在原图请求 | 在矩阵“优化方案”中标出偏离点，后续以独立 BUG/REQ/Change 修复。 |
| `media-multi-variant-images` 规格变长 | 只新增一个消费矩阵 requirement，不复制上传生成和对象存储细节。 |
| 店主 Web 预留规范被误读为已上线验收 | 规格和验收均标注“预留规范，非当前实现验收”。 |
| 禁止原图 fallback 可能与历史实现不一致 | 本 Change 只定义目标规则，历史实现需后续拆分修正。 |

## 知识库引用

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`

