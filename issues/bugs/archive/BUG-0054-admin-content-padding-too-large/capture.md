---
bug_id: BUG-0054-admin-content-padding-too-large
status: captured
created_at: 2026-07-03 13:15:19
updated_at: 2026-07-03 13:45:04
severity: medium
severity_hint: medium
environment: local
related_requirement: REQ-0013-admin-shell-padding-refine
related_bug:
captured_via: capture
classification_rationale: 管理端 Shell 与页面内容区已存在全局布局规范，右侧内容区域内边距过大导致有效展示面积偏小，属于既有 UI 布局与体验基线偏差。
---

# 现象

管理端右侧主内容区域的全局内边距偏大，导致多个管理页面的中间内容显示区域偏小；用户以日志审计页截图举例，红框标注的外侧空白和内容上方空间较大，页面密度不符合管理端列表页高效浏览预期。

# 复现步骤

1. 打开 Web 管理端。
2. 进入任一使用管理端 Shell 主内容容器的页面，例如「系统 / 日志审计」。
3. 观察右侧主内容区域与侧栏之间、主内容右侧边缘、页面顶部标题区上方的留白。
4. 对照截图中红框标注区域，确认内容区域被全局过大内边距压缩。

# 期望 vs 实际

- 期望：管理端全局右侧内容区域应收窄不必要的外侧留白，提升指标卡、筛选区、表格与表单等模块的可用宽度；整体仍遵守 Design System 的暗色旗舰风、semantic token、管理端列表页间距层级。
- 实际：右侧内容区域全局内边距偏大，导致内容显示略小，中间有效空间浪费明显。

# 影响范围

- Web 管理端全局 Shell / 主内容容器。
- 已知样例：日志审计页。
- 主要影响管理端列表页可读性、信息密度与视觉一致性。
- 不涉及后端接口、数据库、MinIO、媒体上传、小程序。

# 附件

- `screenshots/admin-content-padding-example.png`

# 待澄清

- [x] 修复范围已由用户确认：不止日志审计页，应作为全局性管理端内容区内边距调整。
- [ ] 目标验收宽度是否以当前截图视口为基准，或需覆盖 1366px、1440px、1920px 等常见桌面宽度。

# 分类说明（/capture）

用户反馈的是已存在管理端 Shell / 内容区域的全局视觉布局偏差，且截图明确指出实际页面留白过大；该问题可通过一次全局页面布局/样式修复闭环，因此判定为 BUG，并关联管理端 Shell 间距父需求 `REQ-0013-admin-shell-padding-refine`。
