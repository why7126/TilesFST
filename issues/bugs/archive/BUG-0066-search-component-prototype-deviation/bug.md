---
bug_id: BUG-0066-search-component-prototype-deviation
title: 搜索组件整体交互与原型差异较大
severity: high
status: done
owner: product
discovered_at: 2026-07-19 13:02:10
environment: local
related_requirement: REQ-0046-search-component-application
related_change:
source_change: add-miniapp-search-component
created_at: 2026-07-19 13:12:05
updated_at: 2026-07-20 22:47:26
---

# BUG-0066 搜索组件整体交互与原型差异较大

## 现象

微信小程序搜索组件与搜索页已完成基本功能实现，但整体交互与 `REQ-0046-search-component-application` 的产品原型差异较大。REQ-0046 明确要求以 `prototype/*.html`、`prototype/*.png` 和 `prototype/context.md` 为视觉与交互验收基准，且 `add-miniapp-search-component` 的任务清单已将原型验收项标记完成；当前源码仍存在搜索首页、联想、结果、筛选和无结果状态未完全按原型呈现的问题。

## 复现步骤

1. 打开微信小程序搜索页：`src/miniapp/pages/search/index.wxml`。
2. 对照 REQ-0046 原型文件逐项检查：
   - `issues/requirements/archive/REQ-0046-search-component-application/prototype/01-search-home.html`
   - `issues/requirements/archive/REQ-0046-search-component-application/prototype/02-search-suggestions.html`
   - `issues/requirements/archive/REQ-0046-search-component-application/prototype/03-search-results.html`
   - `issues/requirements/archive/REQ-0046-search-component-application/prototype/04-search-filter.html`
   - `issues/requirements/archive/REQ-0046-search-component-application/prototype/05-search-empty.html`
3. 分别验证搜索首页、输入联想、提交结果、打开筛选抽屉、无结果关键词等状态。
4. 观察顶部结构、分区结果、筛选项、价格区间、无结果状态和原型视觉层级是否一致。

## 期望结果

- 搜索页顶部结构应与原型一致，呈现返回按钮、搜索框、取消/搜索按钮，并固定在顶部安全区下方。
- 搜索通用组件应在独立搜索页中被复用，支持关键词、清空、提交、取消/返回、禁用态、`scope` 和 `sourcePage`。
- 搜索首页应按原型展示最近搜索、热门搜索和最近浏览。
- 联想态应按原型分组展示最近搜索、品牌、SKU 和搜索建议。
- 综合结果页应展示最多 1 条最佳匹配，并按相关 SKU、相关类目、相关证书等分区呈现。
- 快捷筛选应包含品牌、类目、规格；完整筛选抽屉应包含品牌、类目、规格、价格区间、重置和确认。
- 无结果页应展示当前关键词、搜索图标、调整建议列表和推荐搜索词。
- 搜索空状态、加载态、联想态、结果态、筛选态和无结果态之间切换不应出现明显布局跳动。

## 实际结果

- 搜索页当前先渲染 `custom-navigation`，再渲染搜索框，与原型中的返回按钮 + 搜索框 + 取消/搜索按钮结构不一致。
- `components/search-entry` 已存在，但独立搜索页未复用该通用组件，搜索页自行实现了搜索框结构。
- `SearchResponse.sections` 已写入页面 data，但 WXML 没有按原型渲染“相关 SKU / 相关类目 / 相关证书”等分区，仅展示扁平 SKU 列表。
- 快捷筛选区域当前只遍历品牌 facet，缺少原型中的品牌、类目、规格快捷筛选组合。
- 筛选抽屉展示品牌、类目和规格，但未提供价格区间输入或选择控件。
- 无结果状态较简化，缺少原型中的搜索图标、结构化调整建议列表和完整推荐搜索区域。

## 影响范围

| 影响面 | 说明 |
|---|---|
| 微信小程序搜索页 | 搜索首页、联想、结果、筛选、无结果 5 个状态与原型不一致 |
| 搜索通用组件应用 | `search-entry` 组件存在但独立搜索页未复用，组件应用验收存在偏差 |
| REQ-0046 验收 | 影响 AC-012、AC-013、AC-016、AC-017、AC-018、AC-021 及 AC-UI-001 至 AC-UI-007 |
| Sprint / Change 交付可信度 | `add-miniapp-search-component` 的原型验收任务已标记完成，但源码仍存在结构性偏差 |

## 严重等级说明

严重等级标记为 `high`。理由是该问题不是单一颜色、间距或文案偏差，而是 REQ-0046 搜索体验的核心原型状态未完整落地；同时关联 Change `add-miniapp-search-component` 已处于 applied 状态，任务清单中原型验收项已勾选完成，存在交付验收误判风险。该问题暂未发现数据损坏、权限绕过或搜索主流程完全不可用，因此不标记为 `critical` 或 `blocker`。

## 关联证据

| 类型 | 路径 / 位置 | 说明 |
|---|---|---|
| REQ | `issues/requirements/archive/REQ-0046-search-component-application/requirement.md` | 明确搜索组件与搜索页范围、UI 约束和原型优先级 |
| Acceptance | `issues/requirements/archive/REQ-0046-search-component-application/acceptance.md` | 定义搜索首页、联想、结果、筛选、无结果和原型验收 AC |
| Prototype | `issues/requirements/archive/REQ-0046-search-component-application/prototype/` | 5 个搜索状态 HTML/PNG 原型 |
| Change Tasks | `openspec/changes/add-miniapp-search-component/tasks.md` | 原型视觉与小程序验收任务已标记完成 |
| Current WXML | `src/miniapp/pages/search/index.wxml` | 当前搜索页结构与原型存在差异 |
| Current Component | `src/miniapp/components/search-entry/index.wxml` | 搜索入口组件存在，但独立搜索页未复用 |

## 后续建议

下一步执行：

```text
/bug-opsx BUG-0066-search-component-prototype-deviation
```

后续修复应通过 `fix-*` OpenSpec Change 处理，不应直接修改 `src/` 绕过流程。
