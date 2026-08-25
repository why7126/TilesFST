---
change_id: fix-workflow-sync-bug-generate-status-transition
source_bug: BUG-0136-workflow-sync-bug-generate-captured-draft
sprint: sprint-025
created_at: 2026-08-22 21:36:45
updated_at: 2026-08-22 21:36:45
---

# 设计

## 根因摘要

根因状态为 `confirmed`。`/bug-generate BUG-0136` 的复现显示：`bug.md` 生成后，Workflow Sync 对 `bug.generate` 事件返回成功，但 trace 与 registry 被报告为 `Skipped (no delta)`，BUG 主状态未从 `captured` 推进到 `draft`。同时 `bug.md` frontmatter 曾被同步回 `captured`，说明当前同步以旧 trace 主状态为准刷新子文档，而缺少 `bug.generate` 的主状态转换。

## 修复方案

1. 在 Workflow Sync 事件状态映射中补齐 `bug.generate`：
   - 当前状态为 `captured`、`exploring` 或等价生成前状态，且目标 BUG 包含 `bug.md` 时，目标状态为 `draft`。
   - 同步 `lifecycle.generated`、`updated_at` 和 `## 变更记录`。
2. 保持子文档同步顺序：
   - 先计算事件目标主状态。
   - 再用目标主状态刷新 `bug.md`、trace、registry 与当前态看板。
   - 避免用旧 trace 状态覆盖刚生成的 `bug.md`。
3. 对缺少 `bug.md` 的异常输入：
   - 不推进主状态到 `draft`。
   - 输出 warning 或 no-op 摘要，提示先生成 `bug.md`。
4. 回归测试：
   - 构造最小 BUG fixture，验证 `bug.generate` 的首次运行和重复运行。
   - 验证缺少 `bug.md` 时不误推进。
   - 对比 `req.generate` 路径，确保 BUG / REQ generate 语义一致。

## 影响分析

| 范围 | 影响 |
|---|---|
| API | 不影响 |
| 数据库 | 不影响 |
| Web | 不影响 |
| 小程序 | 不影响 |
| 管理端 | 不影响 |
| Workflow Sync | 影响 `bug.generate` 事件主状态转换、Issue 子文档同步和当前态看板 |
| 测试 | 需要补充 `scripts/workflow_sync` 聚焦回归测试 |

## 风险与缓解

- 风险：目标 BUG 缺少 `bug.md` 时被误推进到 `draft`。
  - 缓解：以 `bug.md` 存在作为推进前置条件，并补测试覆盖。
- 风险：重复运行 `bug.generate` 重复追加变更记录。
  - 缓解：使用既有幂等写入策略或按事件/时间窗口去重。
- 风险：修复 BUG generate 时影响 REQ generate。
  - 缓解：补充 REQ/BUG generate 对照测试，保证既有 REQ 行为不回退。
