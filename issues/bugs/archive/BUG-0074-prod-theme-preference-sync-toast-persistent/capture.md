---
bug_id: BUG-0074-prod-theme-preference-sync-toast-persistent
title: 生产环境主题偏好同步失败提示持续不消失
status: done
created_at: 2026-07-21 10:14:45
updated_at: 2026-07-22 08:56:27
severity_hint: medium
environment: 生产环境
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 项目已有主题切换与账号偏好同步能力，生产环境提示“主题已在本机生效，但账号偏好同步失败，请稍后重试”且提示持续存在，属于既有偏好同步与 Toast 生命周期处理的行为偏差。
related_requirement:
related_bug:
---

# 现象

生产环境切换主题后出现提示：

```text
主题已在本机生效，但账号偏好同步失败，请稍后重试
```

同时该提示一直存在，不会自动消失。

# 复现步骤

1. 登录生产环境 Web 端。
2. 执行主题切换操作。
3. 观察页面是否出现“账号偏好同步失败”提示。
4. 停留一段时间或继续操作页面，观察提示是否自动消失。

# 期望 vs 实际

期望：主题本机切换成功后，账号偏好应正常同步；若同步失败，应展示可自动消失、可关闭且不阻塞后续操作的错误提示，并允许用户稍后重试。

实际：生产环境提示账号偏好同步失败，且提示一直存在，不会自动消失。

# 附件

- 用户原始反馈：`生产环境提示【主题已在本机生效，但账号偏好同步失败，请稍后重试】同时该提示一直存在，不会消失`
- 暂无截图、浏览器信息、Network 响应体、后端日志；后续 `/bug-explore` 阶段需补充主题偏好同步接口响应、用户账号状态和 Toast 状态。
