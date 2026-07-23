---
requirement_id: REQ-0065-sku-metadata-name-sku-dedup
title: 瓷砖 SKU 元数据名称与编码展示去重验收标准
status: done
created_at: 2026-07-21 17:50:00
updated_at: 2026-07-22 09:59:30
---

# 验收标准

## 功能 AC

- [ ] AC-001 管理端 SKU 新增/编辑弹窗将原“SKU 名称”字段调整为“商品名称”，并作为正式创建 SKU 的必填字段。
- [ ] AC-002 管理端 SKU 新增/编辑弹窗不要求运营手工填写 SKU 编码；保存草稿和正式创建时均由系统生成或保持唯一 SKU 编码。
- [ ] AC-003 系统生成的 SKU 编码唯一、稳定，编辑商品名称、品牌、类目、规格、价格、图片或视频时不得自动改变既有 SKU 编码。
- [ ] AC-004 管理端 SKU 列表主标题展示商品名称；SKU 编码如展示，只能作为弱化的内部辅助信息，不与商品名称并列成为用户主识别字段。
- [ ] AC-005 管理端关键词搜索继续支持商品名称和 SKU 编码；通过 SKU 编码命中后，列表仍以商品名称作为主展示。
- [ ] AC-006 管理端上架、下架、删除等确认文案使用商品名称，不使用 SKU 编码作为确认对象主标题。
- [ ] AC-007 小程序/店主端商品卡片只展示商品名称，不展示 SKU 编码。
- [ ] AC-008 小程序/店主端 SKU 详情页标题、参数区、同系列推荐、同品牌推荐和收藏列表均不展示 SKU 编码。
- [ ] AC-009 小程序/店主端搜索结果中的 SKU 项以商品名称为主展示；即使支持 SKU 编码搜索，命中结果也不得展示编码。
- [ ] AC-010 分享标题、分享摘要和分享卡片展示使用品牌名称 + 商品名称，不拼接 SKU 编码。
- [ ] AC-011 既有 SKU 的 `sku_code` 保持不变，既有 `name` 作为商品名称继续展示。
- [ ] AC-012 历史数据中商品名称与 SKU 编码高度相似时，本需求不做自动清洗；只调整后续录入、展示和接口兼容策略。
- [ ] AC-013 若历史 SKU 缺少 SKU 编码，系统需补齐唯一编码后才能保存为可用状态或进入公开展示链路。

## API / 数据 AC

- [ ] AC-014 SQLite/MySQL 继续保留 SKU 编码唯一字段，除非后续 OpenSpec 明确设计兼容迁移方案。
- [ ] AC-015 若管理端创建请求不再传入 `sku_code`，Pydantic Schema、OpenAPI、Orval、接口文档和前端调用必须同步调整。
- [ ] AC-016 若小程序/店主端响应仍包含 `sku_code`，前端不得直接渲染该字段，并需通过测试覆盖隐藏行为。
- [ ] AC-017 后端测试覆盖自动生成 SKU 编码、唯一性冲突处理、编辑商品名称不改变编码、历史数据兼容。
- [ ] AC-018 前端测试覆盖管理端表单无需填写编码、小程序/店主端不展示编码、分享标题不包含编码。

## UI AC

- [ ] AC-019 管理端字段 label 使用“商品名称”和“SKU 编码”，不得继续使用“SKU 名称”作为用户填写字段名称。
- [ ] AC-020 商品名称在管理端列表和弹窗中保持主视觉层级；编码若展示，字号、颜色或位置必须弱于商品名称。
- [ ] AC-021 管理端搜索 placeholder 表达为“商品名称 / SKU 编码”或等价文案，避免暗示用户创建时必须填写编码。
- [ ] AC-022 小程序/店主端不出现“SKU 编码：xxx”参数行、卡片副标题或分享标题片段。
- [ ] AC-023 原型 `prototype/web/sku-metadata-name-sku-dedup.html` 可直接预览管理端列表与弹窗目标状态，且 context 明确小程序/店主端隐藏编码策略。

## 非功能 AC

- [ ] AC-024 自动编码生成逻辑不得依赖商品名称文本，避免商品名称修改导致编码漂移。
- [ ] AC-025 搜索兼容 SKU 编码时不得泄露其他内部字段、对象存储 key、审计字段或敏感配置。
- [ ] AC-026 API/DB/Orval 变更如发生，必须在同一 OpenSpec Change 中同步 docs、tests 和 `.env.example` 影响结论（如无 env 变化也需注明 N/A）。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` — 预防管理端列表与弹窗回归类缺陷

- [ ] AC-XCUT-001 管理端 SKU 列表改动后，分页 DOM 仍保持 `page-summary` + `page-right` 结构，与用户管理基准对齐。
- [ ] AC-XCUT-002 管理端 SKU 列表改动后，状态成功/失败反馈使用 fixed toast，不得以文档流 notice 推挤 hero、筛选区或表格。
- [ ] AC-XCUT-003 管理端 SKU 列表涉及上架、下架、删除等状态/危险操作时，必须使用 DS confirm modal，不得使用 `window.confirm`。
- [ ] AC-XCUT-004 管理端 SKU 列表摘要指标卡 DOM 如被触及，必须保持 `.metric-label`、`.metric-value`、`.metric-desc` 结构；本需求若未触及指标卡，实现阶段需标注 N/A 证据。
- [ ] AC-XCUT-005 管理端 SKU 新增/编辑弹窗 TSX 不得同时挂载通用 `modal-card` 与 `sku-modal-card` 等专属类。
- [ ] AC-XCUT-006 管理端 SKU 弹窗字段调整后，Computed width 仍与 SKU 弹窗设计一致；宽弹窗按现有 SKU 弹窗 880px 基准验收。
- [ ] AC-XCUT-007 管理端 SKU 弹窗字段调整后，矮视口下 modal body 可滚动，底部操作区不遮挡商品名称、品牌、类目、规格、价格、图片或视频字段。
- [ ] AC-XCUT-008 管理端 SKU 弹窗 CSS 栈测试需覆盖可能冲突的 admin CSS，防止通用 `.modal-card` 宽度规则覆盖专属弹窗宽度。
