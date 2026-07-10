---
bug_id: BUG-0060-audit-log-request-id-copy-error
title: 日志审计页复制 request_id 时报错根因分析
status: enriching
severity: medium
created_at: 2026-07-09 08:06:13
updated_at: 2026-07-09 08:06:13
---

# BUG-0060 根因分析

## 结论

该缺陷属于 Web 管理端日志审计页的复制交互健壮性问题。

直接原因是日志审计页在复制 `request_id` 时直接调用 `navigator.clipboard.writeText(value)`，未先判断 Clipboard API 是否可用，也未在浏览器拒绝写入、非安全上下文或权限受限时提供手动复制兜底。

## 直接原因

当前日志审计页复制函数存在以下风险：

- 直接访问 `navigator.clipboard.writeText`，当 `navigator.clipboard` 不存在时会抛出运行时错误。
- 当浏览器拒绝剪贴板写入、页面不满足安全上下文或权限策略限制时，仅显示通用失败提示，用户无法继续完成复制。
- 未复用或抽象已有的复制兜底模式，导致同类复制交互行为不一致。

## 根本原因

根本原因是日志审计页实现 `request_id` 复制时，只覆盖了理想成功路径，没有把浏览器 Clipboard API 的平台限制纳入交互契约。

项目内已有密码复制弹窗使用了更稳健的模式：先读取 `navigator.clipboard?.writeText`，不可用或失败时选中文本并提示用户手动复制。日志审计页未采用类似兜底，导致真实浏览器环境与测试环境之间出现缺口。

## 触发条件

满足以下任一条件时可能触发：

- 浏览器不支持 Clipboard API。
- 当前页面不满足 Clipboard API 的安全上下文要求。
- 浏览器或系统权限拒绝写入剪贴板。
- `navigator.clipboard.writeText` 调用失败或被测试外的真实环境策略拦截。
- 用户点击带有 `request_id` 的日志记录复制按钮。

## 测试缺口

现有日志审计页测试 mock 了 `navigator.clipboard.writeText` 成功路径，并断言复制成功和埋点上报。

缺少以下回归覆盖：

- Clipboard API 不存在时的兜底反馈。
- `writeText` reject 时的兜底反馈。
- 空 `request_id` 时不触发复制并提示用户。
- 失败路径不触发成功埋点。

## 分类

- 缺陷类型：code
- 影响端：Web 管理端
- 影响模块：日志审计页
- 关联需求：REQ-0024-product-usage-logging
- 是否涉及 API：否
- 是否涉及数据库：否
- 是否涉及权限放宽：否
