---
bug_id: BUG-0077-miniapp-category-secondary-name-truncated
title: 微信小程序分类页二级分类名称超过 4 个字被省略
status: done
created_at: 2026-07-21 10:25:27
updated_at: 2026-07-22 09:15:11
severity_hint: medium
environment: 微信小程序
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 项目已有微信小程序分类页与二级分类展示能力，二级分类名称超过 4 个字时被省略为省略号属于既有页面展示行为偏差，倾向记录为 BUG。
related_requirement: REQ-0045-category-list-page
related_bug:
---

# 现象

微信小程序分类页中，二级分类名称超过 4 个字时无法正常完整显示，会被截断并省略成 `...`。

# 复现步骤

1. 打开微信小程序。
2. 进入分类页。
3. 选择或查看包含二级分类的一级分类。
4. 找到名称长度超过 4 个字的二级分类。
5. 观察二级分类名称在列表、筛选入口或分类导航中的展示效果。

# 期望 vs 实际

期望：二级分类名称超过 4 个字时仍可正常辨识，页面应通过换行、合理宽度、字号、布局或完整标题展示等方式保证用户能读懂分类名称。

实际：二级分类名称超过 4 个字后被省略为 `...`，用户无法从分类页直接识别完整分类名称。

# 附件

- 用户原始反馈：`微信小程序 分类页，二级分类名称超过4个字时，无法正常显示，被会省略成...`
- 关联需求：`REQ-0045-category-list-page`
- 暂无截图、真机型号、具体分类名称与页面路径；后续 `/bug-explore` 阶段需补充。
