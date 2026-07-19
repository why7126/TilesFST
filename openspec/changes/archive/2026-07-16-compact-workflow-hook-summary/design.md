## Context

当前工作流命令在完成主流程后通常会执行 Workflow Sync，再执行 AI usage post-command hook。正式 spec 已要求 Workflow Sync 支持摘要模式、AI usage hook 统一入口和安全脱敏，但调用链上仍存在三类噪音风险：成功同步时打印大量 `skipped no-delta` 文件明细，hook JSON 被完整转述，命令技能把脚本成功日志和派生块一并暴露给用户。

本变更聚焦命令成功路径的输出契约，不改变工作流状态机、Sprint/Issue/Change 事实源，也不改变 AI usage 的持久化安全边界。

## Goals / Non-Goals

**Goals:**

- Workflow Sync 默认摘要输出只展示 event、focus、Sprint 解析、updated/skipped/errors 聚合数量和 detail 提示。
- AI usage post-command hook 的用户可见输出固定为 compact summary 字段：`status`、`usage_mode`、`command_run_count`、`sprint_snapshot`、`warning_count`、`recommended_action`。
- 成功路径不默认输出完整 skipped 文件列表、完整 JSON、session 内容、snapshot 内容、工具日志、OpenAPI/Orval 大 diff 或测试日志全文。
- 失败、drift、异常和安全扫描阻断路径保留可定位的错误原因，并允许通过详细模式展开必要明细。
- 用测试覆盖默认摘要、详细模式、hook 降级和安全 warning 场景。

**Non-Goals:**

- 不新增业务 API、数据库表、前端页面或小程序能力。
- 不重新设计 AI usage command run 的归因、脱敏和存储结构。
- 不改变 REQ/BUG/Sprint/OpenSpec 生命周期状态流转。
- 不删除详细输出能力，只调整默认成功路径。

## Decisions

1. 默认输出由脚本层负责压缩，而不是依赖每个技能手动筛选。

   - 方案：Workflow Sync 的 summary 模式在报告构建函数中聚合 `updated`、`skipped`、`errors`，AI usage hook 在统一 summary builder 中裁剪字段。
   - 理由：脚本层是所有命令共享入口，能减少技能文件重复逻辑和遗漏。
   - 备选：只修改技能说明让 Agent 少转述日志。该方案无法防止脚本 stdout 自身过长，稳定性不足。

2. 详细模式作为显式调试入口保留。

   - 方案：Workflow Sync 保留 `--output detail` 或等价参数；默认 summary 遇到错误时仍输出错误明细，必要时提示 detail。
   - 理由：成功路径降噪不能牺牲 drift、marker、文件状态问题的可诊断性。
   - 备选：完全隐藏逐文件明细。该方案会降低维护效率。

3. AI usage hook compact summary 使用字段白名单。

   - 方案：hook JSON 输出仍可供机器消费，但命令技能和人类输出只展示固定字段，release 命令已有额外 `release_artifact` 的既有契约不在本次收窄范围内。
   - 理由：字段白名单清晰、可测，也能避免误打印 session、snapshot 或安全 warning 的长上下文。
   - 备选：按字符数截断完整 JSON。该方案会产生不稳定输出，也可能截断掉推荐动作。

4. 测试以输出契约为主。

   - 方案：为 summary/detail 输出、no-delta 聚合、hook unavailable、unsafe skipped、Sprint snapshot skipped 等场景补充单元或脚本级测试。
   - 理由：本变更的风险在“输出过长或隐藏错误”，用契约测试比端到端跑完整工作流更直接。

## Risks / Trade-offs

- [Risk] 摘要模式隐藏了维护者想看的单个 skipped 文件。→ Mitigation: 保留 `--output detail`，并在摘要中提示可用详细模式。
- [Risk] 错误路径被误归为成功摘要，导致诊断不足。→ Mitigation: errors 数量大于 0 或 drift/check 失败时必须输出每条错误原因并返回非零。
- [Risk] hook 字段白名单漏掉 release 现有字段。→ Mitigation: 本次聚焦 req/bug/opsx/sprint 标准字段；release 额外摘要保持既有契约，并在任务中检查不回退。
- [Risk] 技能文件与脚本行为不同步。→ Mitigation: 更新共享 `workflow-sync` 技能说明，再按命中清单同步调用技能中的输出要求。
