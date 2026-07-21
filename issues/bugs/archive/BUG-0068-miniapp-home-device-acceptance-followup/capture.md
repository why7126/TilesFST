---
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
title: Sprint 008 小程序首页 DevTools 与真机验收残留未闭环
status: done
created_at: 2026-07-19 17:27:51
updated_at: 2026-07-19 21:39:11
severity_hint: high
environment: 微信开发者工具 / 真机
source: Sprint 008 强制关闭后的人工 follow-up
source_sprint: sprint-008
source_command: /bug-capture
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
---

# 现象

Sprint 008 归档时保留的小程序首页人工验收风险尚未形成独立 follow-up 闭环：`fix-miniapp-home-preview-runtime-entry` 仍需在微信开发者工具真实预览中确认首页首屏恢复，`add-miniapp-global-custom-navigation-bar` 仍需在微信开发者工具或真机上确认 320/375/430 pt 及 320-430 pt 逻辑宽度范围内的胶囊避让和内容不遮挡。

# 复现步骤

1. 使用微信开发者工具打开 `src/miniapp/`。
2. 预览 `pages/index/index` 首页，确认实际加载的是小程序运行脚本而非静态原型或自动化替代证据。
3. 分别在 320、375、390、430 pt 及 320-430 pt 逻辑宽度范围检查首页首屏。
4. 在真机或等效微信开发者工具预览中检查微信原生胶囊区域、状态栏、品牌导航、搜索入口、Banner、快捷入口、推荐模块和底部 TabBar。
5. 记录截图或验收 evidence，确认内容没有进入胶囊区域、没有被 fixed header / TabBar 遮挡、没有横向滚动或关键文本不可读。

# 期望 vs 实际

期望：Sprint 008 遗留的首页真实预览、320-430 pt 布局、胶囊避让与内容不遮挡验收有独立 Issue 追踪；后续修复或验收必须提供微信开发者工具 / 真机 evidence，不得用静态测试或自动化结果替代真实设备验收结论。

实际：Sprint 008 已强制关闭并归档，自动化与静态检查已留存，但真实 DevTools / 真机预览、320-430 pt 布局与胶囊避让验收仍是人工 follow-up 风险，尚未独立进入 BUG 生命周期。

# 附件

- 暂无截图；后续 `/bug-explore` 或 `/bug-generate` 阶段补充微信开发者工具 / 真机截图。
- 来源：`iterations/archive/sprint-008/acceptance-report.md`
