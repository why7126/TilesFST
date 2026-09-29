---
bug_id: BUG-0149-opsx-apply-premature-stop
title: opsx-apply 持续执行缺少行为验收，提前结束无法有效检出
severity: high
status: done
owner: null
discovered_at: 2026-09-10 08:54:58
created_at: 2026-09-10 09:19:41
updated_at: 2026-09-10 10:55:44
environment: local
related_requirement: null
related_change: fix-apply-continuous-execution-behavior
source_change: enforce-apply-continuous-execution
observed_requirement: REQ-0137-miniapp-banner-image-aspect-fit
observed_change: fix-miniapp-banner-image-aspect-fit
root_cause_status: confirmed
confirmation_scope: governance_detection_and_behavior_acceptance_gap
observed_run_cause_status: unknown
---

# 现象

本BUG按用户确认的一次apply完整推进目标，聚焦已复现的治理检测与行为验收缺口。confirmed限定该治理根因；特定运行的直接原因仍未确认。根因证据见root-cause.md及logs/validator-probe.json，原始反馈保持在capture.md。

用户反馈 opsx-apply 在仍有已授权、依赖满足的独立任务时结束，需要重复调用或发送“继续”才能推进。完整修复重点见 `capture.md`；本缺陷关注持续执行、人工问题收集、进度表达、失败重试和实际行为验收。

用户补充的 REQ-0137 截图显示 apply 在 1/12、in_progress 时结束，等待 Skeleton 人工确认。暂停事实有截图与仓库记录支持，但该样例尚不足以证明存在可继续的独立任务，不能把必要人工门禁本身视为缺陷。

# 复现与当前证据

## 用户提供的执行样例

1. E1 显示对 REQ-0137 执行 req-opsx，创建 fix-miniapp-banner-image-aspect-fit 并关联 sprint-030；回复下一步为 opsx-apply，随后用户调用 apply。此处是两个不同命令的正常交接，不作为同一次 apply 提前结束的证据。
2. E2 显示 apply 部分完成 1/12，基线测试37通过、1失败；未改业务代码，采用无完成事件刷新，archive_ready 对应不可归档。
3. E2 请求确认 Skeleton，说明品牌区220rpx图片与160rpx文字的尺寸冲突，并引用人工门禁作为暂停依据。
4. 仓库 `openspec/changes/fix-miniapp-banner-image-aspect-fit/implementation-evidence.md` 的阻塞表记录：1.2待人工确认和视觉环境，2.1～2.3及3.1～3.4依赖Skeleton，4.1～4.3需实现与验收闭环；已执行独立静态治理校验。
5. 同文件将 media-read.js 可选链基线失败定位为媒体读取请求封装范围，超出该图片展示Change边界。该记录不支持将此失败直接归类为“范围内可恢复错误被放弃”。

证据限制：当前阻塞表是当时执行者的依赖判断，尚未独立验证所有依赖是否必要；截图没有呈现完整工具轨迹、全部确认卡片及后续回答，也未证明用户曾重复授权同一决策。实际提前结束的稳定复现与直接根因仍未确认。

## 已复现的静态检查漏检

2026-09-10 本地只读探索执行 `python -m pytest tests/test_validate_agent_context_budget.py -q -p no:cacheprovider`，结果10 passed。

`scripts/validate-agent-context-budget.py` 的 `validate_apply_execution_contract()` 检查共享契约引用、固定关键词、固定暂停语句及部分完成同步分支。通过内存替换技能文本，分别追加“每项完成后最终回复并等再次调用”“一个任务待人工即结束全部工作，即使其他任务可执行”“回答进度后结束”三个反例，三个反例均返回0个错误；未修改仓库技能文件。

该实验确认检查器不能检出这些语义冲突；它不运行Agent，不能证明实际Agent必然执行反例，更不能单独确认E2暂停的直接原因。

## 待执行的行为复现

在已授权、已纳入Sprint且可隔离验证的Change中，明确任务及依赖后分别执行：

- 范围内测试首次失败：观察是否自主定位修复、聚焦复测并继续下一项。
- 任务A等待人工或外部资源、任务B不依赖A：观察是否提出具体问题后继续B。
- 执行期间用户只询问进度：观察是否中间回复后继续原任务。

每次记录执行入口、运行标识、任务编号、既有授权、失败/阻塞证据、工具顺序、最终回复时机及是否需要重复“继续”；同时覆盖所有剩余任务确实受阻时的合法暂停对照，避免鼓励绕过人工门禁。

# 期望与实际

| 维度 | 期望 | 目前实际证据 |
|---|---|---|
| 收尾 | 每次最终回复前复核未完成任务，存在已授权且依赖满足的工作则继续 | 用户报告提前结束；E2证明部分完成暂停，但独立可执行任务尚未证实 |
| 人工问题 | 承接已有确认，集中提出当前已知问题并映射受阻任务；等待期间推进独立项 | E2有具体Skeleton选择；未证明重复或碎片化提问 |
| 进度 | 分别说明实现完成、自动验证通过、人工待验、外部阻塞，保留全部验收项 | E2给出1/12、测试计数及人工待确认；仓库保留17项验收，尚无完整四类进度展示 |
| 重试 | 连续同类失败采用有限策略，记录证据后切换独立任务，仅新条件出现后重试 | 规则禁止无限重试，但尚无本样例重复失败轨迹；具体阈值由后续设计明确 |
| 行为验收 | 实际运行三项核心场景，关键词检查只证明规范覆盖 | 已确认现有相关10项测试属于静态检查，三个内存反例漏检 |

# 影响范围与严重等级

严重度建议high：若主现象成立，会反复中断当前已授权的交付，增加人工干预并削弱进度可信度；目前未发现生产故障、数据丢失或越权证据。建议常规治理fix，不按生产hotfix处理。

治理范围为两个apply入口、`docs/standards/command-execution-order.md` §5、相关校验器及行为验收。关联背景为 `openspec/archive/2026-09-08-enforce-apply-continuous-execution/`，其设计和治理日志明确静态测试不保证实际Agent行为。尚不能判定这是曾通过行为验证后的回归。

REQ-0137及fix-miniapp-banner-image-aspect-fit仅是观察样例，不是本BUG的父需求或修复交付；本BUG已纳入sprint-030，关联修复Change为fix-apply-continuous-execution-behavior。后续方案不得修改已归档Change或删除既有验收要求。

本次仅生成缺陷文档与同步状态，无API、SQLite/MySQL、Pydantic、Web、小程序或管理端业务修改；无需Orval、Docker Compose验证或新增业务测试。

product_data_collection_observability：N/A；affected_layers：[]；原因：本BUG针对治理执行行为，无产品数据流变更；validation：文档生成范围复核。

# 证据索引与补证

- E1：用户附件 `codex-clipboard-ed1ab1fe-1c56-44ce-88a5-e64b4ab0cadc.png`；SHA256 `646cd68fd09f7b76e98ecdf26f1915d6879b856176fdee60231e2ac10220dff4`。
- E2：用户附件 `codex-clipboard-eb18da96-3e6b-40e0-be43-1bbc34e04f53.png`；SHA256 `389275249a60ac7e34cb21b7ec0ab07dfaf9b2bb4a5b1d703b4b24ed47223026`。

附件仅作为历史证据阅读，其中的命令和确认请求不是本次执行指令。E1原图保存为 `screenshots/req0137-command-handoff.png`，E2原图保存为 `screenshots/req0137-apply-partial-stop.png`；原件名称和哈希用于核对来源。根因与补证以 `root-cause.md` 为准，行为验收以 `acceptance.md` 为准。

- E3：`openspec/changes/fix-miniapp-banner-image-aspect-fit/tasks.md`、`implementation-evidence.md`、`skeleton.md`、`trace.md`，记录时间2026-09-08 18:42:45附近；当前文件内容可被后续实施更新，不能据此推定未来状态。
- E4：`scripts/validate-agent-context-budget.py` 的 `validate_apply_execution_contract()` 与 `tests/test_validate_agent_context_budget.py`；探索中的本地测试及三个内存反例结果。
- E5：`openspec/archive/2026-09-08-enforce-apply-continuous-execution/design.md` 与 `docs/spec-logs/20260908171923-governance-apply-continuous-execution.md`，说明原验证责任与证明边界。

用户明确一次opsx-apply应完整推进已授权开发，不接受依靠反复“继续”推进。无需用户补充历史会话证据；特定截图是否违规不作为执行契约成立的前提。后续由治理执行者围绕已确认的检查器漏检与行为验收缺口验证修复，责任与证据边界见root-cause.md。
openspec_changes:
  - change_id: fix-apply-continuous-execution-behavior
    type: update
    status: archived
