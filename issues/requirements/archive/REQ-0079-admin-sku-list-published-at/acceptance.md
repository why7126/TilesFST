---
requirement_id: REQ-0079-admin-sku-list-published-at
title: 管理端瓷砖 SKU 列表新增发布时间列 - 验收标准
status: done
owner: product
created_at: 2026-07-28 22:46:01
updated_at: 2026-07-29 07:54:16
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-012-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 验收标准

## 功能 AC

- [ ] AC-001 管理端瓷砖 SKU 列表 MUST 展示“发布时间”列。
- [ ] AC-002 “发布时间”列 MUST 位于“更新时间”列之前。
- [ ] AC-003 “发布时间”列标题、单元格文字样式、对齐方式和行高 MUST 与“更新时间”列保持一致。
- [ ] AC-004 “发布时间”列 MUST 使用与“更新时间”列完全一致的日期时间格式化策略。
- [ ] AC-005 若“更新时间”当前展示秒级时间，“发布时间”也 MUST 展示秒级时间。
- [ ] AC-006 若“更新时间”当前按管理端本地时区格式化，“发布时间”也 MUST 使用同一时区策略。
- [ ] AC-007 发布时间为空、缺失或不可解析时，MUST 展示统一占位，例如 `-`，不得出现 `null`、`undefined`、`Invalid Date` 或空白塌陷。
- [ ] AC-008 “更新时间”原有字段来源、展示格式、排序行为和空值展示 MUST 保持不变。
- [ ] AC-009 实现 MUST 明确发布时间字段来源，不得直接用更新时间冒充发布时间。
- [ ] AC-010 若管理端 SKU 列表响应已包含发布时间字段，前端 MUST 复用该字段并保持类型兼容。
- [ ] AC-011 若管理端 SKU 列表响应不包含发布时间字段，后端 MUST 补充响应字段，并同步 Pydantic Schema、OpenAPI、Orval、接口文档和测试。
- [ ] AC-012 若数据模型当前没有可用发布时间来源，OpenSpec Change MUST 明确新增字段或历史数据兼容兜底策略。
- [ ] AC-013 新增列后，SKU 列表分页、关键词搜索、品牌筛选、类目筛选、状态筛选、加载态、空态和失败态 MUST 保持原有行为。
- [ ] AC-014 新增列不得改变列表默认排序规则。
- [ ] AC-015 新增列不得遮挡 SKU 名称、品牌、类目、状态、更新时间和操作列等既有核心信息。
- [ ] AC-016 1440x1024 桌面视口下，发布时间与更新时间两列 MUST 能完整辨识，不发生文本重叠。
- [ ] AC-017 窄屏或移动调试视口下，新增列 MUST 遵循现有表格横向滚动或列隐藏策略，不破坏操作列可用性。
- [ ] AC-018 前端测试 MUST 覆盖“发布时间”列头存在且位于“更新时间”列头之前。
- [ ] AC-019 前端测试 MUST 覆盖发布时间和更新时间使用同一格式化结果。
- [ ] AC-020 前端测试 MUST 覆盖发布时间为空时的占位展示。
- [ ] AC-021 若调整后端响应，后端测试 MUST 覆盖列表响应包含发布时间字段、字段类型和空值场景。
- [ ] AC-022 若同步 OpenAPI/Orval，MUST 运行生成与类型检查，并避免手改生成物。
- [ ] AC-023 发布时间字段只在管理端授权 SKU 列表接口中展示，不得绕过既有管理端鉴权。
- [ ] AC-024 前端不得直连数据库、对象存储或未授权接口获取发布时间。
- [ ] AC-025 原型策略 MUST 至少提供管理端 SKU 列表列顺序 HTML/context；PNG Golden Reference 可在后续设计确认后导出。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷。

- [ ] AC-XCUT-001 SKU 列表新增发布时间列后，分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 SKU 列表如展示摘要指标卡，DOM MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc`；若该页无摘要指标卡，验收记录应标注 N/A — 页面无指标卡区域。
- [ ] AC-XCUT-003 列表加载失败、保存/状态操作成功失败等反馈 MUST 使用 fixed toast 或等价固定层，不得造成页面头部、筛选区或表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求只新增列表展示列，不包含启停、冻结、上架/下架、删除、重置密码等危险状态变更；若后续实现顺带触及危险操作，MUST 使用 DS confirm modal。
- [ ] AC-XCUT-005 SKU 列表实现 MUST 不调用 `window.confirm`；本期无确认操作时以静态检查或代码 review 说明 N/A。
