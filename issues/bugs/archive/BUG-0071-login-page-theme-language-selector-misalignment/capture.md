---
bug_id: BUG-0071-login-page-theme-language-selector-misalignment
title: 登录页右上角主题选择模块与语言选择模块没有对齐
status: done
created_at: 2026-07-21 08:35:25
updated_at: 2026-07-22 08:35:48
severity_hint: medium
environment: Web 登录页
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 已有登录页 UI 能力下，主题选择模块与语言选择模块出现视觉对齐偏差，属于现有实现与预期布局不一致。
related_requirement:
related_bug:
---

# 现象

登录页右上角主题选择模块与语言选择模块没有对齐，两个模块在同一区域展示时存在视觉错位。

# 复现步骤

1. 打开 Web 登录页。
2. 查看页面右上角的主题选择模块。
3. 查看同一区域的语言选择模块。
4. 对比两个模块的顶部、垂直居中或基线对齐效果。

# 期望 vs 实际

期望：登录页右上角主题选择模块与语言选择模块在同一行内对齐，视觉高度、间距和交互热区保持一致。

实际：主题选择模块与语言选择模块没有对齐，导致登录页右上角工具区视觉不一致。

# 附件

- 暂无截图或日志；后续 `/bug-explore` 阶段补充登录页截图、视口尺寸和具体错位方向。
