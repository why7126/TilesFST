---
req_id: REQ-0111-miniapp-media-four-part-acceptance-practice
status: archived
created_at: 2026-08-12 14:21:48
updated_at: 2026-08-12 21:37:14
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement:
---

# 沉淀小程序媒体四联验收最佳实践

将 BUG-0125、BUG-0126 暴露出的媒体验收经验沉淀为可复用最佳实践，避免后续只验证对象存在而漏掉真实访问、加载与渲染问题。

# 原始描述

类型倾向：REQ

标题：沉淀小程序媒体四联验收最佳实践

背景：BUG-0125、BUG-0126 均暴露媒体性能验收不能只看对象存在。

影响范围：docs/knowledge-base、miniapp、backend media、测试 helper。

建议验收要点：覆盖 key/object/URL/render 四联、DevTools/真机 Network evidence、历史对象审计与回填策略。

# 待澄清

- [ ] 四联验收实践是否作为现有媒体验收模板的升级，还是独立知识库条目。
- [ ] 历史对象审计与回填策略是否需要提供脚本级 helper，或仅沉淀操作步骤与测试建议。
- [ ] DevTools 与真机 Network evidence 的最低留存格式和归档位置。

# 探索结论

（/req-explore 后人工确认写入）
