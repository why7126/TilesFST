---
bug_id: BUG-0075-prod-admin-brand-banner-save-fails
title: 生产环境管理端品牌类型 Banner 配置无法保存
status: done
created_at: 2026-07-21 10:17:39
updated_at: 2026-07-22 08:59:18
severity_hint: high
environment: 生产环境
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 项目已有 Web 管理端 Banner 配置与品牌类型投放能力，生产环境配置品牌类型 Banner 无法保存属于既有管理端 Banner 保存链路的行为偏差，倾向记录为 BUG。
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug:
---

# 现象

生产环境 Web 管理端中，配置品牌类型的 Banner 后无法保存。

# 复现步骤

1. 登录生产环境 Web 管理端。
2. 进入 Banner 配置或 Banner 管理页面。
3. 新建或编辑一条 Banner，将类型或投放范围配置为品牌类型。
4. 填写必填信息后点击保存。
5. 观察页面提示、Network 请求响应和后端日志。

# 期望 vs 实际

期望：品牌类型 Banner 配置满足校验条件时可以保存成功，并在管理端列表、店主端或小程序对应展示入口按配置生效；若配置不合法，应明确提示具体字段与修正方式。

实际：生产环境配置品牌类型 Banner 时无法保存，暂未确认失败发生在前端表单校验、请求参数构造、后端 Pydantic 校验、权限鉴权、数据库写入或生产数据约束环节。

# 附件

- 用户原始反馈：`生产环境Web管理端，配置品牌类型的Banner无法保存`
- 暂无截图、Banner 表单字段、Network 响应体、错误码、后端日志；后续 `/bug-explore` 阶段需补充保存接口请求参数、响应状态和生产环境相关配置。
