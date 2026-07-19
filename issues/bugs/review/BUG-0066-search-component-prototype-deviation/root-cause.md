---
bug_id: BUG-0066-search-component-prototype-deviation
status: approved
created_at: 2026-07-19 13:17:45
updated_at: 2026-07-19 13:21:10
classification: design/frontend/test
related_requirement: REQ-0046-search-component-application
source_change: add-miniapp-search-component
---

# Root Cause - BUG-0066 搜索组件整体交互与原型差异较大

## 直接原因

`add-miniapp-search-component` 实现时完成了微信小程序搜索的主要数据流和基础页面骨架，但搜索页 WXML/WXSS 没有完整按 REQ-0046 的 5 个原型状态落地：

- 搜索页顶部使用 `custom-navigation` + 自建 `search-shell`，而不是原型中的返回按钮、搜索框、取消/搜索按钮一体结构。
- 独立搜索页没有复用已创建的 `components/search-entry` 通用组件，导致“通用组件应用”与页面实现脱节。
- `SearchResponse.sections` 已写入页面 data，但页面没有渲染相关 SKU、相关类目、相关证书等综合分区。
- 快捷筛选只展示品牌 facet，未形成品牌、类目、规格的组合筛选入口。
- 筛选抽屉缺少价格区间输入或选择控件。
- 无结果状态使用简化文案，未呈现原型中的搜索图标、调整建议列表和推荐搜索区域。

## 根本原因

根本原因是实现与验收之间缺少“原型结构级”门禁。任务清单将 `prototype/*.html`、`prototype/*.png` 和 `prototype/context.md` 的视觉验收项标记完成，但代码层面的静态测试主要覆盖接口、事件、搜索入口存在性和部分状态能力，没有断言以下原型关键结构：

- 独立搜索页必须使用搜索通用组件或保持同等结构。
- 综合结果必须按 `sections` 分区渲染。
- 快捷筛选必须覆盖品牌、类目、规格。
- 完整筛选必须包含价格区间。
- 无结果状态必须包含关键词、建议列表和推荐搜索词。
- 顶部搜索区域必须贴合原型安全区与返回/取消结构。

因此，功能实现能通过现有静态检查和后端测试，但仍与产品原型存在明显体验偏差。

## 触发条件

满足以下任一操作即可观察到偏差：

1. 进入小程序搜索首页并对照 `01-search-home.html`。
2. 输入中文 1 字或英文/数字 2 字触发联想，并对照 `02-search-suggestions.html`。
3. 提交有结果关键词并对照 `03-search-results.html`。
4. 打开筛选抽屉并对照 `04-search-filter.html`。
5. 提交无结果关键词并对照 `05-search-empty.html`。

## 分类

| 分类 | 判断 |
|---|---|
| code | 是。小程序 WXML/WXSS 与数据绑定未完整实现原型结构 |
| design | 是。产品原型验收基准未被完整转译为页面结构 |
| test | 是。缺少覆盖原型关键结构的静态或视觉验收测试 |
| api | 否。当前证据未显示搜索 API 契约本身失败 |
| db | 否。当前证据未涉及数据库结构或数据写入问题 |
| security | 否。当前证据未发现权限绕过或敏感信息泄露 |

## 影响判断

该问题影响 REQ-0046 的搜索体验验收，不影响后台数据安全，也不阻断搜索 API 主流程。但它会导致用户看到的小程序搜索体验与已评审产品原型明显不一致，并让 `add-miniapp-search-component` 的 applied 状态存在交付可信度风险。
