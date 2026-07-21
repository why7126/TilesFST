---
req_id: REQ-0052-miniapp-device-evidence-template
status: done
created_at: 2026-07-19 17:02:14
updated_at: 2026-07-19 19:05:20
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement:
---

# 小程序 DevTools/真机验收 evidence 模板

为微信小程序 DevTools 预览和真机验收建立可复用 evidence 模板，统一记录设备、环境、页面、视口、截图、阻塞项和剩余风险，避免设备验收证据散落在 OpenSpec tasks、acceptance 或 Sprint 验收报告中。

# 原始描述

为小程序 DevTools/真机验收建立可复用 evidence 模板，避免设备验收散落在 tasks 与 acceptance 中

# 待澄清

- [ ] 模板最终沉淀位置是 `docs/standards/`、OpenSpec Change 模板、Sprint 验收报告模板，还是多处引用同一事实源。
- [ ] 模板是否只覆盖微信开发者工具与真机人工验收，还是也纳入静态测试、脚本测试和截图自动化摘要。
- [ ] evidence 必填字段需要覆盖哪些内容，例如设备型号、系统版本、微信版本、基础库版本、页面路径、视口宽度、截图路径、执行人和结论。
- [ ] 历史残留项如 sprint-008 的 DevTools/真机 follow-up 是否需要回填到新模板，还是只约束后续 Change。
- [ ] 后续 `/req-complete` 是否需要把模板与小程序相关 Skill、acceptance-report 结构或 OpenSpec tasks 生成规则关联。

# 探索结论

（/req-explore 后人工确认写入）
