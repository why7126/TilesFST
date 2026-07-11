---
bug_id: BUG-0064-theme-selector-sidebar-placement
status: done
created_at: 2026-07-11 19:29:34
updated_at: 2026-07-11 20:04:35
severity_hint: medium
environment: local|docker
related_requirement: REQ-0020-theme-comfort-refine
related_bug:
captured_via: capture
classification_rationale: 现有管理端界面主题选择器已交付但位置与期望布局不一致，属于已有 UI 能力的布局偏差，归类为 BUG。
---

# 现象

管理端界面主题选择器当前显示在页面右上角内容区，用户期望将其移动到左侧侧边栏内，并放置在底部用户管理头像上方。

截图中右上角「界面主题 / 系统默认」区域被红框标注；侧边栏底部已有管理员头像与账号信息，目标位置应位于该用户信息块上方。

# 复现步骤

1. 以管理员身份登录管理端。
2. 进入任意管理端页面，例如「接口文档」。
3. 观察页面右上角是否显示「界面主题」选择器。
4. 观察左侧侧边栏底部管理员头像区域上方是否存在界面主题入口。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 界面主题选择器 MUST 放在管理端侧边栏内，位置位于底部用户管理头像/账号信息块上方；页面右上角不再显示该控件。 |
| **实际** | 界面主题选择器显示在页面右上角内容区，占用页面顶部操作区域，与用户期望的侧边栏布局不一致。 |

# 影响范围

- 影响端：Web 管理端。
- 影响页面：管理端 Shell 下所有显示右上角主题选择器的页面。
- 影响类型：UI 布局一致性与操作入口位置。

# 附件

- `/var/folders/26/jcqks9nx23185wqvs17rzgkw0000gn/T/codex-clipboard-86663c85-a966-4329-be49-f8537b9b7c5f.png`
