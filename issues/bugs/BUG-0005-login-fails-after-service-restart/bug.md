---
bug_id: BUG-0005-login-fails-after-service-restart
title: 服务重启后正确账号密码无法登录管理端
severity: high
status: in_sprint
owner: product
discovered_at: 2026-06-26 09:54:07
environment: local|docker
related_requirement: REQ-0001-user-login
related_change: fix-admin-login-service-restart
---

# 缺陷说明

## 1. 现象

每次重启本地或 Docker 服务后，刷新页面进入 Web 管理端登录页，使用已知正确的管理员账号和密码仍无法成功登录。

当前已知页面表现：

- 页面：管理端登录页 `/admin/login`
- 账号：`admin`
- 密码：用户反馈为正确密码
- 错误提示：`账号或密码错误`
- 附件截图：`screenshots/login-failure-after-service-restart.png`

## 2. 复现步骤

1. 重启本地或 Docker 服务。
2. 刷新浏览器页面，进入 `/admin/login`。
3. 输入已知正确的管理员账号和密码。
4. 点击「登录」。

## 3. 期望结果

服务重启后，正确账号和密码仍应可以登录 Web 管理端，并进入管理后台首页。

## 4. 实际结果

登录失败，页面提示「账号或密码错误」。

## 5. 影响范围

| 维度 | 影响 |
|---|---|
| Web 管理端 | 影响 `/admin/login` 登录入口，阻断管理员进入后台 |
| 后端认证 | 待分析；可能涉及认证、密码校验、管理员初始化或会话签发链路 |
| 运行时数据 | 待分析；可能涉及服务重启后的 SQLite 数据文件、seed 数据或 Docker 数据卷状态 |
| 环境配置 | 待分析；可能涉及密码哈希、密钥或环境变量在重启前后的稳定性 |
| 店主 Web 展示端 | 暂未发现直接影响 |
| 微信小程序 | 暂未发现直接影响 |

## 6. 严重等级说明

严重等级暂定为 `high`。

理由：

- 该缺陷发生在服务重启后的管理端登录链路，可能导致内部员工无法进入后台维护瓷砖、品牌、媒体等业务数据。
- 登录失败提示为账号或密码错误，容易误导用户排查账号凭据，而真实原因仍待分析。
- 缺陷可能同时影响本地开发环境与 Docker 环境，若确认稳定复现，将影响开发、演示和验收流程。
