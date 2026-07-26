## Context

REQ-0032 已在 `issues/requirements/archive/REQ-0032-clipboard-copy-helper-best-practice/` 完成 capture、PRD、用户故事、业务流程、AC、prototype 和评审，状态为 `approved`。现有 Web 管理端中至少有两类复制交互：

- `/admin/logs` 日志审计列表复制 `request_id`，成功后记录 `copy_request_id` 埋点，失败时提示手动复制。
- 用户管理重置密码结果弹窗复制随机密码，失败时聚焦并选中密码输入框。

相关知识库引用：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/retrospectives/sprint-005-retrospective.md`

## Goals / Non-Goals

**Goals:**

- 建立共享 Clipboard helper 或等价工具，统一结果模型与失败路径。
- 保留调用方业务语义：日志审计仍展示 `request_id` 复制文案，重置密码仍展示密码复制文案。
- 保留日志审计成功复制后的 `copy_request_id` 埋点边界：只有自动写入剪贴板成功时记录成功事件。
- 对 Clipboard API 不存在、reject、空值、fallback 调用和 fallback 抛错提供测试。
- 将 admin-list fixed toast 无 layout shift 与 admin-modal 宽度/滚动横切 AC 纳入验收。

**Non-Goals:**

- 不新增业务复制入口。
- 不新增后端 API、数据库字段、Orval 生成物或 Docker 配置。
- 不引入新的 toast / dialog 体系。
- 不实现微信小程序 Clipboard API 适配。
- 不开发浏览器权限探测或自定义权限弹窗。

## Decisions

### D1. UI strategy: tailwind-ds / shared-helper

采用 `tailwind-ds` / 共享 helper 策略，不做 CSS Port。

原因：

- `prototype/web/clipboard-copy-helper.html` 是交互说明，不是新的生产页面视觉源。
- 复制交互应复用既有 `AdminToast`、弹窗内 `role="status"`、现有按钮和 semantic token，而不是 port 原型中的静态 CSS。
- `rules/ui-design.md` 要求新增/修改 Web UI 使用 semantic token、既有组件和 `cn()`。

### D2. Helper 返回结构化结果，不直接展示 UI

helper 只负责：

- trim / 空值判断；
- 检查 `navigator.clipboard.writeText` 是否可用；
- 调用 `writeText` 并保留正确调用上下文；
- 在失败或不可用时调用可选 `fallbackSelect`；
- 返回 `success`、`failed`、`unavailable`、`empty` 等结构化状态。

helper 不负责 toast、dialog、埋点或业务文案。这样可以让日志审计、重置密码、未来接口路径复制等场景保留自己的业务语义。

### D3. 敏感内容不得进入日志或埋点

随机密码、token、Authorization、Cookie、对象存储 key 等敏感文本不得被 helper 记录到日志、错误消息或埋点 metadata。测试中也不得输出真实敏感值。

### D4. 代表场景迁移

实现阶段至少覆盖：

- `src/web/src/pages/admin/LogAuditPage.tsx`
- `src/web/src/features/admin/components/ResetPasswordDialog.tsx`

若实现时发现已有代码已经满足某个场景，可保留现有 UI，但复制分支应尽量收敛到共享 helper 或等价工具。

## Conflict Resolution

优先级：HTML > PNG > context.md > acceptance.md > ui-design.md > openspec/specs。

| 来源 | 结论 |
|---|---|
| `prototype/web/clipboard-copy-helper.html` | 仅作为交互状态示意，不作为生产 CSS Port 来源。 |
| `prototype/web/context.md` | 明确列表 fixed toast 与弹窗内 `role="status"` 是代表场景。 |
| `acceptance.md` | 功能 AC 与 AC-XCUT 必须进入实现验收。 |
| `rules/ui-design.md` | 生产 UI 必须使用 semantic token / 既有组件；不得复制原型裸 Hex。 |
| `openspec/specs/product-usage-logging/spec.md` | 日志审计 request_id 已有 fallback 要求，本 change 只补充共享 helper 迁移边界。 |

无 PNG golden reference；不需要导出 PNG 作为本 change 的阻塞项。

## Risks / Trade-offs

| 风险 | 缓解 |
|---|---|
| helper 过度抽象导致业务文案丢失 | helper 只返回状态，文案和 toast 仍由调用方处理。 |
| 随机密码等敏感内容泄露 | helper 和测试不得记录复制文本；日志审计只记录 request_id 成功复制事件。 |
| Clipboard API 在非安全上下文或权限拒绝时失败 | 用 `failed` / `unavailable` 状态和 `fallbackSelect` 提供手动路径。 |
| 列表页 toast 造成布局位移回归 | 继续使用 fixed toast 或等价不占文档流反馈，并保留测试/验收。 |
| 弹窗复制失败文案导致布局回归 | 保持重置密码结果弹窗宽度、body scroll 和 footer 可达性验收。 |

## Migration Plan

1. 新增共享 helper 与单元测试。
2. 迁移日志审计 `request_id` 复制，保留成功后埋点。
3. 迁移重置密码随机密码复制，保留失败时选中输入框。
4. 更新 Web README 或 Design System 说明中的复制 helper 使用边界。
5. 运行相关前端测试，必要时补充 design-system/代表场景 smoke。

## Open Questions

- 未来是否需要把 Clipboard helper 扩展到店主 Web 展示端；本 change 不做小程序适配。
