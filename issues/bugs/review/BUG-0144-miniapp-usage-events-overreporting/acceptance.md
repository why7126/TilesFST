---
bug_id: BUG-0144-miniapp-usage-events-overreporting
acceptance_status: pending
created_at: 2026-08-26 08:38:14
updated_at: 2026-08-26 10:02:13
---

# 验收目标

治理小程序商品列表页与搜索页 usage-events 偏多问题，确保曝光和搜索输入埋点数量与真实用户行为规模相匹配，同时保留必要行为分析能力。

# 回归验收项

## AC-001 商品列表页曝光口径唯一或边界清晰

给定商品列表页首屏加载 12 个商品，当页面完成首屏渲染时：

- 同一批 SKU 不应同时以无边界的 `product_list_item_exposure` 和 `product_card_exposure` 重复计入。
- 若保留两类事件，必须明确一个为页面级汇总、一个为组件级明细，且两者具备互斥、层级或可解释聚合规则。
- usage-events 请求数量不应随首屏商品数量逐条线性增长到不可控规模。

## AC-002 搜索输入高频上报受控

给定用户在搜索页连续输入 4-6 个字符，当输入尚未提交搜索时：

- `search_input` 不应按每个字符变化即时逐条上报，或必须通过防抖、合并、采样等策略控制频率。
- 搜索建议请求防抖不应成为唯一频控点，输入埋点本身也必须受控。
- 清空、取消、提交搜索等关键行为仍可被正常上报。

## AC-003 搜索结果曝光与商品卡曝光不重复计入

给定搜索结果页展示 SKU 结果，当 `search_result_exposure` 与 `product_card_exposure` 都存在时：

- 两类事件必须有明确边界，避免同一 SKU、同一搜索 `requestId`、同一结果模块被重复解释为两次真实曝光。
- 最佳匹配、分组结果、Tab 切换、筛选应用和加载更多时，去重窗口必须可解释。
- 切换关键词或重新提交搜索后，应允许记录新的真实曝光。

## AC-004 曝光去重键覆盖关键上下文

给定商品列表、搜索结果和商品卡组件共用曝光治理策略，当触发曝光事件时：

- 去重键至少覆盖页面、来源模块、列表上下文、SKU、搜索关键词或列表请求上下文、`requestId` 等必要维度。
- 同一列表实例内重复渲染、属性 observer 重复触发或相同数据重复 setData 不应重复上报。
- 刷新、分页、筛选切换、搜索关键词切换时，去重窗口应按设计规则重置或延续。

## AC-005 事件字典与安全字段保持兼容

给定修复后保留的 usage-events 事件，当后端接收 payload 时：

- 保留事件仍应满足后端 `EVENT_DEFINITIONS` 必填字段和禁止字段校验。
- 不得新增 Authorization、Cookie、原始对象 key、本机路径、内部备注、手机号等禁止字段。
- 埋点失败不得阻断商品列表浏览、搜索输入、搜索结果展示、商品点击、分享或跳转。

## AC-006 回归测试与人工证据

修复完成后应补充或更新以下验证：

- 静态或单元测试覆盖商品列表页曝光口径不再无边界双报。
- 静态或单元测试覆盖搜索输入埋点频控策略。
- 后端 usage-events 字典测试继续覆盖保留事件的合法 payload。
- 小程序开发者工具网络面板或等价日志记录修复前后 `/api/v1/usage-events` 数量和事件名分布对比。

# 验收结果回填

| 时间 | 结果 | 证据 | 说明 |
|---|---|---|---|
| 2026-08-26 10:02:13 | pending | `issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095600-product-list-usage-events.png`；`issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095610-search-input-usage-events.png`；`issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095620-search-result-usage-events.png` | 已补充微信开发者工具 Network 人工截图，覆盖商品列表页、搜索连续输入与搜索结果页三个验收场景；待 `/opsx-archive` 最终确认验收结论。 |
| 2026-08-26 09:50:30 | pending | `openspec/changes/fix-miniapp-usage-events-overreporting/implementation/usage-events-evidence.md`；`uv run pytest tests/test_miniapp_static.py -q`；`uv run pytest tests/test_miniapp_home.py -q -k "usage_events_validate_dictionary or contract_drift_usage_events"`；`node --check` 三个小程序 JS 文件 | 已完成代码实现和静态/字典回归；微信开发者工具 Network 数量截图仍建议在人工验收时补充。 |

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: fix-miniapp-usage-events-overreporting
source_sprint: sprint-026
evidence:
  - openspec/changes/fix-miniapp-usage-events-overreporting/implementation/usage-events-evidence.md
  - issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095600-product-list-usage-events.png
  - issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095610-search-input-usage-events.png
  - issues/bugs/review/BUG-0144-miniapp-usage-events-overreporting/screenshots/20260826095620-search-result-usage-events.png
  - uv run pytest tests/test_miniapp_static.py -q
  - uv run pytest tests/test_miniapp_home.py -q -k "usage_events_validate_dictionary or contract_drift_usage_events"
failed_items: []
source_event: opsx.apply
notes: 已补充静态测试、后端字典测试和微信开发者工具 Network 截图；后续 archive 时回填最终验收结论。
```
