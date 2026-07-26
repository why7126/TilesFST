---
bug_id: BUG-0083-prod-admin-brand-banner-save-500
title: 生产环境创建品牌类型 Banner 保存接口返回 500
status: done
created_at: 2026-07-23 10:35:53
updated_at: 2026-07-23 22:59:48
severity_hint: high
environment: prod
source: 用户反馈
source_command: /capture
related_requirement: REQ-0062-admin-banner-placement-scope
related_bug: BUG-0075-prod-admin-brand-banner-save-fails
captured_via: capture
classification_rationale: 项目已有管理端 Banner 配置与品牌类型投放能力，且历史 BUG-0075 已修复归档；生产环境创建品牌类型 Banner 时保存接口仍返回 500，属于既有能力在生产环境下的回归或残留偏差，按 BUG 记录。
lifecycle_stage: plan
---

# 现象

生产环境创建品牌类型 Banner 时，点击保存仍然失败。

本次明确观测到保存接口返回：

- 请求方法：`POST`
- 请求地址：`https://tilesfst.wjoyhappy.site/api/v1/admin/banners`
- HTTP 状态：`500 Internal Server Error`

# 复现步骤

1. 登录生产环境管理端。
2. 进入 Banner 管理或 Banner 配置页面。
3. 创建一条品牌类型 Banner。
4. 填写必填信息后点击保存。
5. 在浏览器 Network 中观察 `POST /api/v1/admin/banners` 响应。

# 期望 vs 实际

- 期望：合法的品牌类型 Banner 可以保存成功；保存失败时应返回可定位的业务错误码和字段提示，不应返回未处理的 500。
- 实际：生产环境创建品牌类型 Banner 时保存接口返回 `500 Internal Server Error`，导致配置无法保存。

# 影响范围

- 生产环境管理端 Banner 创建流程。
- 品牌类型 Banner 投放配置。
- 后端管理接口：`POST /api/v1/admin/banners`。
- 可能影响运营配置品牌 Banner 的上线与回归验收。

# 初步线索

- 历史缺陷 `BUG-0075-prod-admin-brand-banner-save-fails` 已针对“生产环境管理端品牌类型 Banner 配置无法保存”完成修复并归档。
- 本次反馈为“保存还是失败”，且接口已经明确返回 500，倾向为回归缺陷、生产数据差异、请求 payload 与后端 Schema/数据库约束漂移，或历史修复未覆盖创建路径。
- 需要对比本地/demo 与生产环境在品牌数据、Banner 枚举、关联字段、迁移状态和后端日志中的差异。

# 建议验收或复现要点

- 保存失败时记录完整请求 payload、响应 body、request_id、后端异常日志和当前登录账号权限。
- 分别验证品牌类型 Banner 的新增、编辑、启用/停用是否都正常。
- 验证非品牌类型 Banner 保存是否仍正常，以缩小缺陷范围。
- 验证关联品牌 ID 存在、状态可用，并符合后端外键或业务校验。
- 修复后确保接口不再返回裸 500；对已知非法输入返回明确 4xx 错误码。

# 附件

暂无截图或后端日志。当前证据来自用户反馈的生产接口 Network 结果。
