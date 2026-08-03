---
requirement_id: REQ-0087-admin-sku-list-sort-optimization
title: 管理端 SKU 列表排序优化 - 验收标准
status: done
owner: product
created_at: 2026-08-01 07:11:09
updated_at: 2026-08-01 08:19:56
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-015-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 验收标准

## 功能 AC

- [ ] AC-001 管理端 SKU 列表默认排序 MUST 先展示未上架 SKU，再展示已上架 SKU。
- [ ] AC-002 未上架 SKU 分组内 MUST 按创建时间降序排列，最新创建的 SKU 排在前面。
- [ ] AC-003 已上架 SKU 分组内 MUST 按发布时间降序排列，最新发布的 SKU 排在前面。
- [ ] AC-004 已上架 SKU 的主排序字段 MUST 使用发布时间，不得用更新时间替代发布时间。
- [ ] AC-005 上架状态判断 MUST 使用系统现有状态字段或后端统一派生字段，不得仅通过前端显示文案推断。
- [ ] AC-006 OpenSpec Change MUST 明确未上架状态集合，例如草稿、待完善、已下架、已停用等是否全部属于未上架分组。
- [ ] AC-007 创建时间相同的未上架 SKU MUST 使用稳定次级排序字段，例如 SKU ID 降序或更新时间降序。
- [ ] AC-008 发布时间相同的已上架 SKU MUST 使用稳定次级排序字段，例如 SKU ID 降序或更新时间降序。
- [ ] AC-009 创建时间为空、缺失或不可解析时，MUST 使用稳定兜底顺序，不得导致列表报错。
- [ ] AC-010 已上架 SKU 发布时间为空、缺失或不可解析时，MUST 使用稳定兜底顺序，不得出现随机顺序。
- [ ] AC-011 关键词搜索后的结果 MUST 继续应用本需求默认排序规则。
- [ ] AC-012 品牌、类目、状态、素材完整度等筛选后的结果 MUST 继续应用本需求默认排序规则。
- [ ] AC-013 分页 MUST 基于排序后的完整结果集切分，不能只在当前页内排序。
- [ ] AC-014 翻页、调整每页条数、刷新列表后，同一数据集排序结果 MUST 保持稳定。
- [ ] AC-015 新建 SKU 后刷新列表，未上架 SKU MUST 按创建时间进入正确位置。
- [ ] AC-016 SKU 上架后刷新列表，该 SKU MUST 进入已上架分组并按发布时间进入正确位置。
- [ ] AC-017 SKU 下架后刷新列表，该 SKU MUST 进入未上架分组并按创建时间进入正确位置。
- [ ] AC-017A SKU 下架后，管理端列表、详情与下架响应 MUST 继续返回并展示最近一次发布时间，不得把历史 `published_at` 派生为空。
- [ ] AC-018 本需求不新增显式排序控件、说明卡片、创建时间筛选或发布时间筛选。
- [ ] AC-019 SKU 列表视觉结构、筛选区、分页区、状态标签、操作列和加载/空态/失败态 MUST 保持现有样式。
- [ ] AC-020 若管理端 SKU 列表由后端分页接口提供，排序 SHOULD 在后端分页前完成。
- [ ] AC-021 若当前实现为前端获取完整结果集后分页，前端 MUST 在分页前完成排序。
- [ ] AC-022 若新增或修改排序参数、响应字段或派生字段，MUST 同步 Pydantic Schema、OpenAPI、Orval、接口文档和相关测试。
- [ ] AC-023 接口鉴权、分页结构、错误码和既有筛选参数不得因排序优化发生不兼容变化。
- [ ] AC-024 排序能力只在管理端授权 SKU 列表中生效，不得绕过管理端鉴权。
- [ ] AC-025 排序字段 MUST 使用参数化查询、ORM 排序或等价安全机制，不得拼接不可信 SQL。
- [ ] AC-026 后端或前端测试 MUST 覆盖未上架 SKU 优先于已上架 SKU。
- [ ] AC-027 测试 MUST 覆盖未上架 SKU 按创建时间降序。
- [ ] AC-028 测试 MUST 覆盖已上架 SKU 按发布时间降序。
- [ ] AC-029 测试 MUST 覆盖时间相同和时间为空时的稳定排序。
- [ ] AC-030 测试 MUST 覆盖搜索或筛选后排序仍然正确。
- [ ] AC-031 若排序由后端分页接口实现，测试 MUST 覆盖分页前排序而非页内排序。
- [ ] AC-032 原型策略 MUST 提供管理端 SKU 列表排序前后结构说明和静态 HTML/context；PNG Golden Reference 可在后续设计确认后导出。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷；结合 `docs/knowledge-base/retrospectives/sprint-015-retrospective.md` 中管理端筛选下拉统一 gate。

- [ ] AC-XCUT-001 SKU 列表排序优化后，分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 SKU 列表如展示摘要指标卡，DOM MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc`；若该页无摘要指标卡，验收记录应标注 N/A — 页面无指标卡区域。
- [ ] AC-XCUT-003 筛选下拉 MUST 继续使用统一筛选下拉组件或 shared admin filter select，触发框、弹层宽度、选中态、重置态、空态、加载态、窄屏和裁切表现不得回退为页面级临时样式。
- [ ] AC-XCUT-003A SKU 列表筛选区 MUST 参照其他管理端列表页铺满 filter-card 可用宽度，右侧不得因多预留网格列出现明显空白。
- [ ] AC-XCUT-004 列表加载失败、保存/状态操作成功失败等反馈 MUST 使用 fixed toast 或等价固定层，不得造成页面头部、筛选区或表格纵向位移。
- [ ] AC-XCUT-005 N/A — 本需求不新增启停、冻结、上架/下架、删除、重置密码等危险状态变更；若后续实现顺带触及危险操作，MUST 使用 DS confirm modal。
- [ ] AC-XCUT-006 SKU 列表实现 MUST 不调用 `window.confirm`；本期无确认操作时以静态检查或代码 review 说明 N/A。
