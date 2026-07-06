---
bug_id: BUG-0060-audit-log-request-id-copy-error
status: captured
created_at: 2026-07-05 20:31:10
updated_at: 2026-07-05 20:31:10
severity_hint: medium
severity: medium
environment: local
related_requirement: REQ-0024-product-usage-logging
related_bug:
captured_via: capture
classification_rationale: 日志审计页为既有能力，列表中复制 request_id 报错属于已有交互功能异常。
---

# 现象

日志审计页列表中，点击复制 `request_id` 时出现报错，导致无法正常复制请求编号用于排查。

# 复现步骤

1. 打开管理端日志审计页。
2. 在日志列表中找到任意一条带有 `request_id` 的记录。
3. 点击列表中的复制 `request_id` 操作。
4. 观察页面报错或复制失败提示。

# 期望 vs 实际

- 期望：点击复制后，`request_id` 应成功写入剪贴板，并给出稳定的成功反馈。
- 实际：点击复制 `request_id` 时报错，用户无法确认或完成复制动作。

# 附件

- 用户曾提供截图路径：`/var/folders/26/jcqks9nx23185wqvs17rzgkw0000gn/T/codex-clipboard-04474d51-2862-465b-8cd5-d722487665c8.png`
- 当前系统读取该截图失败：`No such file or directory`，疑似临时剪贴板文件已被清理。

# 分类说明（/capture）

该问题发生在已交付的日志审计页复制交互中，属于已有能力在特定操作下的功能异常，因此归类为 BUG。输入只涉及同一页面、同一操作和同一失败点，按最小可修复单元保持为单条 BUG。
