---
requirement_id: REQ-0071-request-snapshot-logging
title: API 请求日志统一 Request Snapshot - 验收标准
status: done
owner: product
source: requirement.md
created_at: 2026-07-26 13:02:56
updated_at: 2026-07-26 16:52:07
---

# 验收标准

## 功能 AC

- [ ] AC-001 每个可采集 API 请求均生成统一 Request Snapshot，并关联对应请求日志记录。
- [ ] AC-002 Snapshot 至少包含 method、path、route template、query 白名单摘要、body schema 摘要、业务资源标识、status code、error code、duration、操作者、客户端、环境、请求开始时间和响应结束时间。
- [ ] AC-003 后台管理端、店主 Web 展示端和微信小程序请求使用兼容 Snapshot 字段结构，无法提供的字段以空值或 `未采集` 表达。
- [ ] AC-004 route template 能稳定表达 FastAPI 路由模板；无法识别时有明确降级值，不把带查询串的 path 当作唯一上下文。
- [ ] AC-005 query 参数只按白名单采集；未列入白名单的字段默认忽略或只记录字段名。
- [ ] AC-006 body 只保存 schema 摘要、字段类型、字段数量、长度、业务安全字段或脱敏结果，不保存原始敏感 body。
- [ ] AC-007 Authorization、Cookie、密码、Token、真实密钥、数据库 DSN、MinIO AccessKey/SecretKey、内部路径、原始文件名不得进入 Snapshot。
- [ ] AC-008 上传、登录、认证、系统设置等敏感接口采用更严格字段白名单，并有测试证明敏感字段未落库。
- [ ] AC-009 错误请求能在 Snapshot 中关联 status code、业务 error code、duration、route template、client type、actor 和错误摘要。
- [ ] AC-010 慢请求可通过 `duration_ms` 被识别，并与现有日志审计策略保持一致。
- [ ] AC-011 管理端日志详情展示 Request Snapshot 分组：请求信息、输入摘要、业务资源、响应结果、操作者 / 客户端、环境与时间。
- [ ] AC-012 Snapshot 缺少字段、metadata 为空或 JSON 解析失败时，日志列表和详情页仍可展示基础字段，不出现页面崩溃。
- [ ] AC-013 日志详情访问继续受系统管理员或等价权限控制，未授权角色访问返回 403 或管理端无权限页。
- [ ] AC-014 Snapshot 扩展后，日志列表分页和详情查询在 demo 数据量下无明显性能退化；生产实现需说明索引或 JSON 字段查询策略。
- [ ] AC-015 SQLite demo schema、MySQL schema、Pydantic Schema、API 响应、OpenAPI / Orval、接口文档和测试在实现阶段保持同步。

## 非功能 AC

- [ ] AC-NF-001 后端白名单、脱敏和截断策略是最终安全边界；前端脱敏不得作为可信安全边界。
- [ ] AC-NF-002 Snapshot 字段命名、枚举值和空值表达在 API 文档中可追溯。
- [ ] AC-NF-003 请求日志采集失败不得阻断主业务请求，但应记录可观测错误摘要。
- [ ] AC-NF-004 生产日志保留周期、敏感字段脱敏和敏感操作审计策略与系统审计配置保持一致或明确差异。

## 横切 AC（knowledge-base）

无横切 AC。本 REQ 为 API / 后端日志治理为主，虽包含管理端日志详情展示，但不命中 `req-complete` 定义的 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 四类横切 UI 场景。
