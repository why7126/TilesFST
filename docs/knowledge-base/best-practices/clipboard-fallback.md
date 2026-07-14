---
title: Clipboard helper fallback 最佳实践
purpose: 统一 Web 管理端 Clipboard helper 调用方的文案、fallback、敏感值边界与评审 checklist
content: Clipboard helper 调用方最佳实践
source: REQ-0036-clipboard-helper-best-practice-docs
update_method: 新增复制入口模式、敏感值策略或 Clipboard helper 结果结构变化时更新
owner: 前端负责人
status: draft
created_at: 2026-07-12 00:00:00
updated_at: 2026-07-12 00:00:00
note: 适用于 Web 管理端 Clipboard helper 调用方；不替代 REQ-0032 的 helper 实现要求
---

# Clipboard helper fallback 最佳实践

## 适用范围

本文档适用于 Web 管理端 Clipboard helper 调用方，用于新增或评审复制入口时统一用户反馈、fallback 策略、敏感值边界和测试检查。

本文档不替代 `REQ-0032` 的 helper 实现要求。调用方仍应统一使用 `src/shared/lib/clipboard.ts` 的 `copyTextToClipboard`，由 helper 归一化文本、调用 Clipboard API 并返回 `success`、`failed`、`unavailable`、`empty` 结构化结果；调用方负责 toast、`role="status"`、弹窗提示、业务 DOM、埋点与测试。

## 结果文案原则

复制反馈必须保留业务对象名称，让用户知道复制的是哪一类内容；不得无差别只显示“复制成功”或“复制失败”。提示文案不得直接回显 Token、密钥、Cookie、Authorization、客户隐私原文或其他敏感值。

| helper 结果 | 调用方文案原则 | 推荐示例 |
|---|---|---|
| `success` | 告知业务对象已复制，不回显敏感原文 | `request_id 已复制`、`临时密码已复制，请及时保存`、`版本号已复制` |
| `failed` | 告知复制失败，并给出下一步 | `request_id 复制失败，请手动选择后复制` |
| `unavailable` | 说明当前环境不支持自动复制，并提供手动路径 | `当前浏览器不支持自动复制，请手动选择文本` |
| `empty` | 说明当前内容为空，优先避免可点击入口 | `当前 request_id 为空，无法复制` |

## Fallback 策略

调用方不得让复制点击在失败路径下没有用户可感知反馈。Clipboard helper 与 UI 保持解耦，fallback 的可见提示和 DOM 交互由调用方负责。

| 场景 | 调用方策略 |
|---|---|
| 自动复制成功 | 显示短时 toast 或 `role="status"` 状态文本，保留业务对象名。 |
| Clipboard API 不可用 | 提示用户手动复制；若页面已有只读输入框或代码块，应聚焦并选中文本。 |
| 写入失败 | 提示失败原因的用户可行动版本，例如“请手动选择后复制”；不要暴露底层异常。 |
| fallback 回调失败 | 显示兜底失败提示，并保留可见文本供用户手动选择。 |
| 待复制内容为空 | 优先隐藏或禁用复制入口；若入口必须保留，点击后提示当前内容为空。 |
| 文本不应复制 | 不渲染复制按钮，或渲染为禁用态并提供安全原因提示。 |

密码、一次性口令、`request_id`、版本号等输入型或代码型场景，可以在 fallback 中聚焦并选中文本。表格行、详情卡和弹窗中复制入口应避免因为 fallback 提示改变页面布局。

## 敏感值边界

复制入口只能复制用户已授权查看的内容，不得通过 helper 绕过权限边界。helper 和调用方不得将复制原文写入日志、埋点 payload、测试快照、控制台输出或错误消息。

| 分类 | 典型内容 | 策略 |
|---|---|---|
| 允许复制 | 公开 ID、`request_id`、版本号、公开 SKU 编码、已展示的业务编号 | 可提供复制入口；提示保留业务对象名。 |
| 谨慎复制 | 随机密码、一次性口令、临时邀请码、短期有效链接、对象存储 key 摘要 | 仅在用户已授权查看且业务需要时提供；提示中不回显原文；避免写入日志和快照。 |
| 禁止或默认不复制 | AccessKey、SecretKey、Token、Cookie、Authorization、客户手机号原文、身份证件原文、真实生产签名 URL | 默认不提供复制入口；如后续确需支持，必须先补专门安全流程与验收。 |

## 调用方 checklist

- [ ] 复制内容已在当前权限下可见，复制入口没有扩大用户可访问范围。
- [ ] 待复制数据已完成敏感值分类，禁止或默认不复制的数据没有入口。
- [ ] `success`、`failed`、`unavailable`、`empty` 四类结果都有用户可感知反馈。
- [ ] 成功和失败提示保留业务对象名称，不直接回显敏感原文。
- [ ] Clipboard API 不可用和写入失败时有手动复制、选中文本、禁用入口或明确提示策略。
- [ ] 空值场景优先隐藏或禁用入口，或展示“当前内容为空，无法复制”类提示。
- [ ] 日志、埋点 payload、测试快照、控制台输出和错误消息不包含复制原文。
- [ ] 代表场景已覆盖测试或人工验收：成功、失败、API 不可用、空值、敏感值不渲染入口。

## 推荐示例

```tsx
const result = await copyTextToClipboard(requestId, {
  fallbackTarget: requestIdInputRef.current,
})

showStatus({
  success: "request_id 已复制",
  failed: "request_id 复制失败，请手动选择后复制",
  unavailable: "当前浏览器不支持自动复制，请手动选择 request_id",
  empty: "当前 request_id 为空，无法复制",
}[result.status])
```

```tsx
const canCopyTemporaryPassword = userCanViewTemporaryPassword && temporaryPassword.length > 0

return (
  <Button
    disabled={!canCopyTemporaryPassword}
    onClick={copyTemporaryPassword}
  >
    复制临时密码
  </Button>
)
```

## 反例

```tsx
await navigator.clipboard.writeText(secretKey)
console.log("copied", secretKey)
toast.success(`已复制 ${secretKey}`)
```

问题：

- 绕过共享 helper，调用方重复散落 Clipboard API 分支。
- 复制 `SecretKey`，属于禁止或默认不复制类别。
- 在控制台和 toast 中回显敏感原文。

```tsx
toast.success("复制成功")
```

问题：

- 缺少业务对象名称，用户无法确认复制的是 `request_id`、版本号还是其他字段。
- 没有覆盖失败、不可用、空值路径。

## 追溯

- `REQ-0036-clipboard-helper-best-practice-docs`
- `openspec/changes/archive/2026-07-11-add-clipboard-helper-best-practice-docs/`
- `docs/knowledge-base/retrospectives/sprint-006-retrospective.md` A-005 行动项
