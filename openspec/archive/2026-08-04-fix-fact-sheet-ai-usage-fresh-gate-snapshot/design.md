## 上下文

Sprint Fact Sheet 和 `/sprint-exps` 已使用 `data/ai-usage` 的 Sprint snapshot 作为真实 token 成本分析事实源。fresh gate 负责判断 snapshot 是否可用：只有 snapshot 存在、usage mode 为真实统计、矩阵字段存在且覆盖当前 Sprint scope 时，才允许输出真实成本矩阵。

`BUG-0113` 的现象显示 snapshot 已刷新但 fresh gate 仍可能判定 stale，说明 fresh gate 的输入来源或 mode 映射可能与 snapshot 写入端不一致。

## 目标 / 非目标

**目标：**

- 让已刷新且覆盖当前 Sprint scope 的 snapshot 通过 fresh gate。
- 让过期、缺失、失败、覆盖不足或必要矩阵缺失的 snapshot 继续被阻断。
- 统一 snapshot status 与 usage mode 的映射，避免 refreshed / actual 类状态被降级为 stale、skipped 或 unavailable。
- 让 blocker 输出包含可诊断原因和刷新建议，而不是只给出笼统 stale。
- 用回归测试固定该契约。

**非目标：**

- 不重构 AI usage command run 存储结构。
- 不改变完整 `usage_matrices` 的数据模型。
- 不新增业务 API、数据库表、Web 页面或小程序页面。
- 不绕过 fresh gate 输出真实成本矩阵。

## 根因假设

当前根因需在实现阶段通过代码定位确认，重点检查：

1. fresh gate 的 stale 判定是否读取了旧 snapshot 文件、旧 payload 或错误的时间源。
2. snapshot 刷新后 `generated_at`、coverage、usage mode 和矩阵 presence 是否都写入同一事实源。
3. summary 模式是否在压缩 AI usage 输出时误改了原始 snapshot status 或 usage mode。
4. usage mode 映射是否缺少 refreshed / actual 的优先级，导致 fallback 分支覆盖真实状态。

## 修复方案

1. 收敛 fresh gate 输入。

   fresh gate MUST 基于同一个 Sprint snapshot payload 判定 `snapshot_status`、`usage_mode`、`generated_at`、coverage 与矩阵 presence。不得混用旧缓存、命令运行时间或非目标 Sprint 文件作为最终 gate 事实。

2. 明确 stale 判定顺序。

   - snapshot 缺失或读取失败时输出 `missing` 或 `failed`。
   - snapshot 的 `generated_at` 早于 Sprint scope、关联 Issue trace 或 Change trace 的关键更新时间时输出 `stale`。
   - snapshot 覆盖不足或矩阵缺失时输出 blocker，但不得把已刷新 snapshot 简化为 stale。
   - snapshot 当前且 coverage / matrices 通过时输出 fresh/pass。

3. 明确 mode 映射。

   `actual` 只在真实 command run 与 Sprint snapshot 覆盖通过时成立；`estimated_fallback`、`skipped`、`unavailable` 必须保留原因，不能覆盖已通过 fresh gate 的真实状态。

4. 增强 compact 诊断。

   Fact Sheet summary 中保留 compact gate 字段，至少包含 status、snapshot_status、ai_usage_mode、generated_at、coverage status、usage_matrices presence、warning_count 和 recommended_action。

## 测试策略

- 构造当前有效 snapshot，断言 fresh gate pass 且 summary 不输出 stale blocker。
- 构造过期 snapshot，断言 fresh gate blocker 且原因指向 stale timestamp。
- 构造缺失或失败 snapshot，断言 blocker 与 recommended_action 清晰。
- 构造 coverage 不足或矩阵缺失 snapshot，断言不得误报为 fresh。
- 构造 `actual` 与 fallback mode，断言 mode 映射不会互相串位。

## 风险 / 权衡

- [风险] 放宽 stale 判定可能误放行旧 snapshot。缓解：严格比较 snapshot `generated_at` 与 Sprint scope / trace 关键更新时间，并保留 coverage gate。
- [风险] 字段命名与已有 tests 不一致。缓解：尽量复用现有 `ai_usage_snapshot` 字段，新增 compact 诊断字段时保持向后兼容。
- [风险] 当前工作区已有其他 workflow Change 同时调整 Fact Sheet。缓解：实现阶段先读取相关 active Change 和 tests，避免覆盖已完成的 compact summary 行为。
