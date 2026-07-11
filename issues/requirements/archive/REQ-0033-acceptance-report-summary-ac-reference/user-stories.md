---
requirement_id: REQ-0033-acceptance-report-summary-ac-reference
title: acceptance-report 拆分最终验收摘要与原始 AC 引用 - 用户故事
status: archived
created_at: 2026-07-11 16:03:39
updated_at: 2026-07-11 20:13:04
---

# 用户故事

## US-001 产品负责人查看最终验收结论

作为产品负责人，我希望打开 Sprint `acceptance-report.md` 时优先看到最终验收摘要和归档门禁结果，以便快速判断 Sprint 是否可以关闭，而不是从长篇原始 AC 清单中推断状态。

验收要点：

- 报告顶部或靠前位置存在独立“最终验收摘要”。
- 摘要能直接展示 readiness gate、Change archive、tasks 完成数和 Sprint 状态。
- 摘要不依赖原始 AC 勾选状态作为唯一判断依据。

## US-002 QA 区分人工 sign-off 与原始 AC 追溯

作为 QA，我希望原始 AC 引用明确标注其用途和未勾选项语义，以便知道哪些是待人工 sign-off、哪些是阻断归档、哪些只是历史追溯。

验收要点：

- 原始 AC 区域与最终验收摘要分区展示。
- `- [ ]` 未勾选项必须有状态说明或归类。
- 人工 sign-off 记录可独立追踪，不覆盖 Sprint 关闭状态。

## US-003 开发负责人执行 Sprint archive

作为开发负责人，我希望 `/sprint-archive` 关闭 Sprint 时更新最终归档检查，而不是要求手工逐条勾完历史 AC 后才能表达已关闭状态。

验收要点：

- Sprint 关闭事实来自 readiness gate、Change archive 和 tasks 完成情况。
- 归档报告记录 Sprint `completed/archive` 状态。
- 原始 AC 未勾选项如不阻断归档，必须以复核项或历史追溯项呈现。

## US-004 Workflow Sync 刷新派生状态

作为 Workflow Sync，我希望有稳定的验收报告章节边界，以便只刷新派生状态区，不误改人工结论、验收人和 sign-off 说明。

验收要点：

- 自动刷新区域与人工维护区域边界清晰。
- 自动刷新不会把原始 AC 未勾选项解释为 Sprint 未完成。
- 正文无实质变化时不因派生时间漂移刷新文档。

## US-005 复盘读者追溯原始 AC

作为复盘读者，我希望仍能从验收报告追溯每个 REQ/BUG 的原始 `acceptance.md`，同时能明确最终归档事实来源。

验收要点：

- 原始 AC 引用保留 REQ/BUG 编号、来源路径和状态摘要。
- 报告避免复制过长 AC 全文，优先提供路径、摘要和必要摘录。
- Fact Sheet 或复盘读取时优先使用最终摘要判断 Sprint 状态。
