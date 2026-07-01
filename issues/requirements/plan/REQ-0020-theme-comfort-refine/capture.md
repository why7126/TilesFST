---
req_id: REQ-0020-theme-comfort-refine
status: captured
created_at: 2026-06-30 11:34:04
updated_at: 2026-06-30 11:34:04
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0000-build-design-system
captured_via: capture
classification_rationale: 用户反馈主题色长期观看不舒适，属于 Design System 视觉策略与主题舒适度优化需求。
---

# 一句话

当前主题色过深，用户长时间使用会感觉眼睛疲劳，需要优化 Web / 管理端主题色舒适度，在保持品牌质感的前提下降低视觉压迫感。

# 原始描述

用户使用反馈，这个主题色太深了，看久了眼睛疼。

# 背景与关联

- 父需求：`REQ-0000-build-design-system`
- 关联规范：`rules/ui-design.md` 当前定义“工业石材 · 暗色旗舰风”，页面底色为深色体系
- 影响范围：Web 展示端、Web 管理端、Design System Token、`/design-system` 预览页
- 预期后续：需要通过 OpenSpec Change 评审是否调整默认主题、增加舒适暗色/浅色模式，或提供主题切换策略

# 待澄清

- [ ] 反馈主要来自管理端长时间操作，还是店主端/展示端浏览
- [ ] 目标是整体调亮默认暗色主题，还是新增浅色/舒适模式并允许切换
- [ ] 是否需要保留“工业石材 · 暗色旗舰风”作为品牌展示主题
- [ ] 验收方式是否需要包含连续使用场景、对比截图和可访问性对比度检查

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目是用户体验反馈驱动的视觉策略优化，并非某个页面偏离既有原型或组件规范的单点缺陷，因此判定为 REQ。
