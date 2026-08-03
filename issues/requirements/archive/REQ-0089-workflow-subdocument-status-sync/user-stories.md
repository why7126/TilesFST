---
requirement_id: REQ-0089-workflow-subdocument-status-sync
title: REQ/BUG 子文档状态同步与验收结果回填机制 - 用户故事
status: done
created_at: 2026-08-01 09:52:35
updated_at: 2026-08-01 11:46:26
---

# 用户故事

## US-001 产品负责人查看 Issue 包当前状态

作为产品负责人，我希望打开 REQ/BUG 目录中的 `requirement.md` 或 `bug.md` 时能看到当前状态和闭环摘要，而不是只看到生成时的 `draft` 或评审时的 `approved`，以便快速判断需求或缺陷是否仍需跟进。

验收要点：

- 主文档状态与 `trace.md` 当前状态不冲突。
- 若主文档不再承载机器状态，必须明确引用 `trace.md` 或使用不混淆的字段名。
- 归档后的主文档不得残留未解释的早期阻塞状态。

## US-002 测试人员追踪验收结论和证据

作为测试或验收人员，我希望 `acceptance.md` 不只列出验收标准，还能记录验收是否通过、证据在哪里、哪些 AC 未通过或豁免，以便后续复查时不需要从 Sprint 报告、Change trace 和测试日志之间反复拼证据。

验收要点：

- `acceptance.md` 或等价验收结果文档包含 `acceptance_status`、时间、来源、证据和失败项。
- 未验收时必须说明下一步。
- 归档时必须能判断验收结论是通过、失败、部分通过还是豁免。

## US-003 AI Agent 执行状态变化命令

作为 AI Agent，我希望 `/req-review`、`/bug-review`、`/opsx-apply`、`/opsx-archive` 等命令有统一的子文档同步入口，以便不再依靠每个命令手工维护相同的状态字段。

验收要点：

- 状态传播逻辑集中在 Workflow Sync 或共享脚本中。
- 重复运行同步脚本不会产生重复记录或无意义 diff。
- Workflow Sync 摘要能报告子文档检查和更新数量。

## US-004 流程维护者治理历史漂移

作为流程维护者，我希望能对历史 archive 中的状态漂移进行 dry-run 扫描、分类和受控 apply，以便修复已有文档债务，同时避免误改语义不清的旧模板。

验收要点：

- dry-run 报告包含文件、字段来源、旧值、目标值和可修复分类。
- apply 只处理明确安全的修复项。
- 无法自动判断的文档保留人工确认或豁免入口。

## US-005 评审者关闭 Sprint 前检查中间态残留

作为评审者，我希望归档或 Sprint close 前能发现早期规划、验收未闭环、active Change 路径等中间态残留，以便 completed/archive 的机器状态和人工阅读结论一致。

验收要点：

- close 前校验能扫描 Issue 子文档和 Sprint 四件套中的中间态残留。
- 报告只输出命中文件、行号、字段和值，不展开大量正文。
- 残留必须修复或记录豁免原因后才能归档闭环。
