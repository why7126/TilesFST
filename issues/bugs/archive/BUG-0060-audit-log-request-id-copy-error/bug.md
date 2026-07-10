---
bug_id: BUG-0060-audit-log-request-id-copy-error
title: 日志审计页复制 request_id 时报错
severity: medium
status: draft
owner:
discovered_at: 2026-07-05 20:31:10
environment: local
related_requirement: REQ-0024-product-usage-logging
related_change:
created_at: 2026-07-09 08:03:09
updated_at: 2026-07-09 08:03:09
---

# BUG-0060 日志审计页复制 request_id 时报错

## 现象

管理端日志审计页列表中，用户点击某条日志记录的 `request_id` 复制按钮时，页面出现复制失败或报错反馈，导致请求编号无法稳定复制到剪贴板。

该问题影响日志排障链路：管理员或开发人员无法快速复制 `request_id` 去关联后端请求日志、错误响应或使用行为事件。

## 复现步骤

1. 登录管理端并打开日志审计页。
2. 在日志列表中找到任意一条带有 `request_id` 的记录。
3. 点击该记录 `request_id` 旁的复制按钮。
4. 观察页面反馈与系统剪贴板内容。

## 期望结果

- `request_id` 成功写入剪贴板。
- 页面给出稳定、固定位置的成功反馈。
- 复制反馈不应造成表格或页面布局位移。
- 当浏览器 Clipboard API 不可用或被拒绝时，应给出可理解的失败反馈或手动复制指引。

## 实际结果

- 点击复制 `request_id` 时出现报错或复制失败提示。
- 用户无法确认 `request_id` 是否已写入剪贴板。
- 在 Clipboard API 不可用、权限被拒绝或浏览器阻止写入时，当前交互缺少稳定兜底。

## 影响范围

- 影响端：Web 管理端。
- 影响页面：日志审计页。
- 影响用户：系统管理员、运维排障人员、开发排障人员。
- 影响能力：`REQ-0024-product-usage-logging` 中的日志审计列表与 `request_id` 复制能力。
- 不涉及后端 API 契约、数据库结构、MinIO / 媒体上传、小程序。

## 严重等级说明

严重等级为 `medium`。

理由：

- 该问题不阻断日志列表查询、筛选、详情查看等主流程。
- 但会降低排障效率，尤其在需要通过 `request_id` 串联前端反馈、接口响应和后端日志时影响明显。
- 复制交互属于 `REQ-0024-product-usage-logging` 已交付验收点，属于既有能力异常。
