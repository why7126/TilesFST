---
change_id: fix-miniapp-search-prototype-alignment
type: fix
status: proposed
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 18:14:29
source_bug: BUG-0066-search-component-prototype-deviation
source_requirement: REQ-0046-search-component-application
source_change: add-miniapp-search-component
iteration: sprint-009
affected_capabilities:
  - miniapp-search
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
---

# Proposal - fix-miniapp-search-prototype-alignment

## Why

`BUG-0066-search-component-prototype-deviation` 已确认微信小程序搜索组件和独立搜索页虽然具备基础搜索能力，但搜索首页、联想、结果、筛选和无结果状态与 `REQ-0046-search-component-application` 的 5 个 HTML/PNG 原型差异较大。

`add-miniapp-search-component` 已归档，且其原型验收任务曾被标记完成；当前偏差会影响 REQ-0046 的交付可信度，需要通过独立 `fix-*` Change 修复，而不是直接修改源码或回改已归档 Change。

## What Changes

- 对齐独立搜索页顶部结构：返回按钮、搜索框、取消/搜索按钮、安全区和触控尺寸按原型落地。
- 修复搜索首页、联想、综合结果和无结果状态的页面结构与交互，并移除搜索结果页筛选 UI。
- 确保独立搜索页复用 `components/search-entry`，或保持与该通用组件一致的关键词、清空、提交、取消/返回、禁用态、`scope` 和 `sourcePage` 行为。
- 渲染后端 `sections` 综合分区，覆盖相关 SKU、相关类目、相关证书等结构，不再只展示扁平 SKU 列表。
- 结果页不展示快捷筛选、筛选按钮或筛选抽屉；品牌、SKU、证书结果以卡片式结构展示。
- 强化无结果页结构，展示当前关键词、搜索图标、调整建议列表和推荐搜索词，并保持搜索范围外入口不展示。
- 补充小程序静态或单元测试，防止原型关键结构再次被任务清单误判为完成。

## Capabilities

### Modified Capabilities

- `miniapp-search`: 修复微信小程序搜索页与搜索通用组件的原型对齐、综合分区、筛选和无结果状态验收。

## Impact

- **Miniapp:** 影响 `src/miniapp/pages/search/*`、`src/miniapp/components/search-entry/*` 及相关小程序静态测试。
- **API:** 默认不新增或修改 API；若实现中发现当前搜索响应缺少 `sections`、facets、价格区间或结果数量字段，必须先在本 Change 内补充 API delta、docs、OpenAPI/Orval 和接口测试。
- **Database:** 默认不变更 SQLite/MySQL 表结构。
- **Web/Admin:** 不影响 Web 展示端或企业管理端。
- **Storage/Media:** 不涉及上传、MinIO 或对象存储策略。
- **Testing:** 必须补充回归测试，覆盖原型关键结构、分区结果、筛选和无结果状态。

## Rollback Plan

- 若修复导致小程序搜索主流程异常，可回退本 Change 对 `src/miniapp/pages/search/*` 与 `components/search-entry/*` 的修改，保留已新增测试作为回归线索。
- 若发现必须调整 API 契约但本期无法完成，应停止实现并更新本 Change 的 proposal/design/spec/tasks，明确 API 影响与 Orval 同步范围后再继续。
- 回退不得修改已归档的 `add-miniapp-search-component`；BUG trace 与 Sprint 状态应通过 Workflow Sync 记录后续状态变化。
