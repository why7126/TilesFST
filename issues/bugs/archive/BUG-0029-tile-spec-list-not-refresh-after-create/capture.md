---
bug_id: BUG-0029-tile-spec-list-not-refresh-after-create
status: captured
created_at: 2026-06-28 13:13:16
updated_at: 2026-06-28 13:13:16
severity_hint: high
environment: local|docker
related_requirement: REQ-0009-tile-spec-management
related_bug:
---

# 现象

Web 管理端「瓷砖规格」新增弹窗点击「保存」后，后端创建成功且弹窗关闭，但列表页未即时展示新建记录，须手动刷新浏览器页面才能看到新数据。

# 复现步骤

1. 以 admin 登录 Web 管理端，进入「瓷砖规格」列表页。
2. 记录当前列表条数或清空筛选条件。
3. 点击「+ 新增瓷砖规格」，填写必填项（宽度、长度、排序等）后点击「保存」。
4. 观察弹窗关闭后列表是否出现新记录；不刷新页面时新记录不可见。
5. 手动刷新页面（F5）后，新记录出现。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 保存成功后列表自动刷新（或乐观更新），立即显示新建规格，统计卡片同步更新。 |
| **实际** | 保存成功但列表仍为旧数据，必须手动刷新页面。 |

# 附件

- screenshots/tile-spec-add-save-no-list-refresh.png
