---
requirement_id: REQ-0033-acceptance-report-summary-ac-reference
title: acceptance-report 拆分最终验收摘要与原始 AC 引用 - 验收标准
status: archived
created_at: 2026-07-11 16:03:39
updated_at: 2026-07-11 20:13:04
---

# 验收标准

## 报告结构

- [ ] AC-001 `acceptance-report.md` MUST 包含独立“最终验收摘要”或等价章节，且位置早于原始 AC 明细。
- [ ] AC-002 `acceptance-report.md` MUST 包含独立“原始 AC 引用”或等价章节，用于追溯 REQ/BUG `acceptance.md`。
- [ ] AC-003 最终验收摘要与原始 AC 引用 MUST 有职责说明，明确最终摘要用于归档判断，原始 AC 用于追溯和人工复核。
- [ ] AC-004 报告 MUST 提供独立人工 sign-off 记录位置，记录验收人、验收时间、遗留复核项或说明。

## 最终验收摘要

- [ ] AC-010 最终验收摘要 MUST 展示 Sprint archive readiness gate 结果。
- [ ] AC-011 最终验收摘要 MUST 展示 Change archived / applied / proposed 数量或等价状态汇总。
- [ ] AC-012 最终验收摘要 MUST 展示 tasks 完成计数，或明确引用 readiness gate 对 tasks 的检查结果。
- [ ] AC-013 最终验收摘要 MUST 展示 Sprint `status` 与 `lifecycle_stage`。
- [ ] AC-014 最终验收摘要 MUST 能让读者不阅读原始 AC 明细即可判断 Sprint 是否满足关闭条件。

## 原始 AC 引用

- [ ] AC-020 原始 AC 引用 MUST 保留 REQ/BUG 编号、标题或摘要、来源 `acceptance.md` 路径。
- [ ] AC-021 原始 AC 引用 MUST 保留 issue 状态和关联 Change 状态摘要。
- [ ] AC-022 原始 AC 引用 SHOULD 优先使用路径、状态摘要和必要摘录，避免复制过长 AC 全文。
- [ ] AC-023 若原始 AC 区域出现 `- [ ]` 未勾选项，MUST 标明其语义：待人工 sign-off、阻断归档或历史追溯。
- [ ] AC-024 历史追溯类未勾选项 MUST NOT 自动覆盖最终验收摘要中的归档结论。

## Workflow Sync 与自动化

- [ ] AC-030 Workflow Sync MAY 刷新派生 note、issue 状态行和 Change 状态摘要。
- [ ] AC-031 Workflow Sync MUST NOT 覆盖人工填写的最终验收结论、验收人或 sign-off 说明。
- [ ] AC-032 Workflow Sync MUST NOT 将原始 AC 未勾选项自动解释为 Sprint 未完成。
- [ ] AC-033 正文无实质变化时，Workflow Sync SHOULD NOT 仅因派生时间漂移刷新 `updated_at`。
- [ ] AC-034 Fact Sheet 或复盘信号提取 SHOULD 优先读取最终验收摘要和最终归档检查，而不是原始 AC 明细中的孤立“未完成”文本。

## Sprint archive 门禁

- [ ] AC-040 `/sprint-archive` MUST 继续以 readiness gate、Change archive 和 tasks 完成情况作为关闭硬门禁。
- [ ] AC-041 本需求 MUST NOT 放宽 OpenSpec archive、tasks 完成、Workflow Sync 或目录迁移门禁。
- [ ] AC-042 readiness gate 失败时，最终验收摘要 MUST 标明阻断项，Sprint 不得被标记为 completed/archive。
- [ ] AC-043 readiness gate 通过但仍有人工 QA 复核项时，报告 MUST 将其记录为 sign-off open item 或遗留复核项。

## 范围与兼容性

- [ ] AC-050 本需求默认影响后续新 Sprint 或后续主动更新的 `acceptance-report.md`，不强制批量迁移全部历史报告。
- [ ] AC-051 若选择迁移历史 Sprint 报告，MUST 保留原始来源路径和最终归档事实，不得改写历史事实。
- [ ] AC-052 本需求 MUST NOT 修改 Web 管理端、店主端、微信小程序、后端业务 API 或数据库结构。
- [ ] AC-053 本需求 MUST NOT 修改 REQ/BUG 原始 `acceptance.md` 的 AC 编写、编号和勾选规则。

## 横切 AC（knowledge-base）

本需求为 Sprint 文档治理与 Workflow Sync 质量改进，不涉及 `admin-list`、`admin-form`、`admin-modal`、`media-upload` UI 场景标签，因此无 AC-XCUT。
