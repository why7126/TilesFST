---
bug_id: BUG-0149-opsx-apply-premature-stop
status: done
severity: high
created_at: 2026-09-10 08:54:58
updated_at: 2026-09-10 10:56:25
lifecycle_stage: archive
lifecycle:
  reviewed: 2026-09-10 10:18:37
  approved: 2026-09-10 10:18:37
  captured: 2026-09-10 08:54:58
  enriched: 2026-09-10 09:24:08
  completed: 2026-09-10 09:24:08
  generated: 2026-09-10 09:19:42
iteration: sprint-030
openspec_changes:
  - change_id: fix-apply-continuous-execution-behavior
    type: fix
    status: archived
related_requirement: null
related_bug: null
related_change: fix-apply-continuous-execution-behavior
source_change: enforce-apply-continuous-execution
source_sprint: sprint-030
root_cause_status: confirmed
confirmation_scope: governance_detection_and_behavior_acceptance_gap
observed_run_cause_status: unknown
---

# 缺陷追踪

## 来源与边界

来源命令：opsx-apply。用户报告及建议行为验收见 `capture.md`。
关联背景为 `openspec/archive/2026-09-08-enforce-apply-continuous-execution/`；该归档 Change 不是本 BUG 的修复交付，不回写其状态。当前 BUG 已评审通过，已纳入 sprint-030，修复 Change 为 fix-apply-continuous-execution-behavior。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-09-10 10:55:45 | lifecycle-stage-migrate | review → archive（/opsx-archive fix-apply-continuous-execution-behavior） |
| 2026-09-10 10:55:44 | /opsx-archive | Change `fix-apply-continuous-execution-behavior` 已归档，状态同步完成。 |
| 2026-09-10 10:53:26 | /opsx-apply | Change `fix-apply-continuous-execution-behavior` apply 完成，待 archive。 |
| 2026-09-10 10:18:37 | lifecycle-stage-migrate | plan → review（/bug-review） |
| 2026-09-10 08:54:58 | /bug-capture | 记录提前收尾现象与持续执行行为验收要求；证据来源为用户反馈，尚未复现，根因 unknown。 |
| 2026-09-10 09:24:08 | /bug-complete | draft → enriching → pending_review；补齐根因、规避、12项行为验收与原图证据；根因unknown，approve门禁仍阻塞。 |
| 2026-09-10 10:07:06 | 用户澄清 | 明确一次apply完整推进要求；取消向用户索取历史补证，行为验证由治理执行者承担；保留真实根因状态。 |
| 2026-09-10 10:14:35 | /bug-complete | 基于用户明确的治理范围复测两入口6个漏检反例与2个阳性对照；治理根因confirmed，历史运行因果不作确认；保留pending_review与全部验收。 |
| 2026-09-10 10:18:37 | /bug-review | 治理根因门禁通过，批准high/P1常规修复；推荐sprint-030，未正式纳入，全部行为验收保持待验。 |
| 2026-09-10 10:25:57 | /bug-opsx | 创建修复Change fix-apply-continuous-execution-behavior，状态proposed，回填同一Sprint。 |

## 完善结果

文档齐备；治理检测与行为验收缺口根因confirmed，特定运行直接原因unknown。自动行为验收12项通过，用户归档确认已记录；证据见acceptance.md与logs/behavior/suite-summary.json。已纳入sprint-030，修复Change为fix-apply-continuous-execution-behavior。根因与证明范围见root-cause.md，临时处理见workaround.md。产品数据采集与链路观测N/A，affected_layers为空，仅治理资产与隔离行为测试。

## 验证责任

用户无需补充历史会话。一次apply完整推进要求已明确，治理执行者已完成两个入口共14次受控行为验证；修复实现完成，Change与BUG均已归档。
- 2026-09-10 10:55:44 workflow-sync：状态同步为 done（Change archived）
