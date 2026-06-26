---
bug_id: BUG-0005-login-fails-after-service-restart
status: captured
recorded_at: 2026-06-26 09:54:07
severity_hint: high
environment: local|docker
related_requirement: REQ-0001-user-login
---

# 现象

每次重启服务后，刷新页面进入管理端登录页，使用正确的账号和密码仍无法成功登录。

当前截图显示：

- 账号：`admin`
- 密码：用户反馈为正确密码
- 页面错误提示：`账号或密码错误`
- 页面：管理端登录页

# 复现步骤

1. 重启本地或 Docker 服务。
2. 刷新浏览器页面，进入 `/admin/login`。
3. 输入已知正确的管理员账号和密码。
4. 点击「登录」。

# 期望 vs 实际

| 项目 | 内容 |
|---|---|
| 期望 | 服务重启后，正确账号和密码仍可登录管理端，并进入管理后台首页。 |
| 实际 | 登录失败，页面提示「账号或密码错误」。 |

# 附件

- `screenshots/login-failure-after-service-restart.png`

# 初步备注

- 疑似与服务重启后的账号初始化、运行时数据库、密码哈希/密钥、环境变量或数据卷状态有关。
- 本阶段仅 capture，不进行根因判断；后续通过 `/bug-explore BUG-0005-login-fails-after-service-restart` 复现与分析。
