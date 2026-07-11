---
requirement_id: REQ-0036-clipboard-helper-best-practice-docs
title: Clipboard helper best-practice 文档用户故事
status: approved
created_at: 2026-07-11 23:47:07
updated_at: 2026-07-11 23:53:49
---

# User Stories

## US-001 前端开发人员接入复制入口

作为前端开发人员，我希望在新增复制入口时能查看统一 best-practice 文档，以便明确应该如何编写提示文案、处理 fallback 和判断敏感值边界。

验收要点：

- 文档应说明适用范围：Web 管理端调用 Clipboard helper 的复制入口。
- 文档应明确调用方负责业务文案、toast / `role="status"` 反馈、fallback 接入和埋点边界。
- 文档应链接或引用 `REQ-0032` 已沉淀的 Clipboard helper 能力，避免把 helper 实现要求重复写散。

## US-002 QA 验证复制失败路径

作为 QA，我希望 best-practice 文档提供固定检查清单，以便验证复制成功、失败、API 不存在、空值和手动复制兜底都被覆盖。

验收要点：

- checklist 应覆盖 `success`、`failed`、`unavailable`、`empty` 等结构化结果。
- checklist 应要求失败路径有可操作提示，不得出现点击后无反馈。
- checklist 应要求自动复制失败或 API 不可用时有手动复制 fallback 或明确禁用策略。

## US-003 产品负责人统一调用方文案

作为产品负责人，我希望复制提示文案保留业务语义，以便用户知道复制的是 `request_id`、随机密码、版本号还是其他业务对象。

验收要点：

- 文档应提供成功、失败、浏览器不支持、内容为空的推荐文案原则。
- 文档应要求成功文案保留业务对象名称，而不是统一写成“复制成功”。
- 文档应要求敏感值不得在 toast、错误消息或帮助文案中原文回显。

## US-004 安全负责人确认敏感值边界

作为安全或技术负责人，我希望文档明确哪些值允许复制、哪些值谨慎复制、哪些值禁止或默认不复制，以便复制入口不扩大敏感信息暴露面。

验收要点：

- 文档应至少区分允许复制、谨慎复制、禁止或默认不复制三类数据。
- 文档应说明 AccessKey、SecretKey、Token、Cookie、Authorization 和客户隐私原文等默认不提供复制入口。
- 文档应要求复制内容不得写入日志、埋点 payload、测试快照、控制台输出或错误消息。

## US-005 后续 reviewer 评审复制入口

作为代码 reviewer，我希望文档包含示例与反例，以便在评审新增复制入口时快速判断调用方是否符合约定。

验收要点：

- 文档应提供至少一个普通复制场景示例，例如复制 `request_id`。
- 文档应提供至少一个谨慎复制场景示例，例如复制一次性密码但不记录原文。
- 文档应提供反例，例如 toast 回显 Token、埋点记录复制内容、无 Clipboard API 时静默失败。
