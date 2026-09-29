---
bug_id: BUG-0149-opsx-apply-premature-stop
root_cause_status: confirmed
classification: governance
evidence_source: user_screenshots_and_repository_inspection
created_at: 2026-09-10 09:24:08
updated_at: 2026-09-10 10:14:35
confirmation_scope: governance_detection_and_behavior_acceptance_gap
observed_run_cause_status: unknown
---

# 根因分析

## 结论与确认范围

根因状态confirmed，限定于本BUG的治理缺陷：持续执行契约已存在，但验证仅覆盖规则文本，缺少实际执行序列与收尾决策的行为验收，无法有效检出提前结束。

用户确认的交付目标是一次opsx-apply持续完成当前Change内已授权且依赖满足的实现、测试、文档及同步，不依靠反复发送“继续”。据此围绕可复现的治理缺口进行修复；不把历史会话补证作为用户前置任务。

confirmed不表示REQ-0137的暂停已判违规，也不表示已定位模型内部决策原因；该样例的具体运行因果仍为unknown。保留此区别，不以用户要求替代实际根因证据。

## 直接原因

`scripts/validate-agent-context-budget.py` 的 `validate_apply_execution_contract()` 只接收技能文件路径并检查文本：共享规则引用、固定关键词、固定暂停语句、部分完成无事件分支。它不消费任务依赖、既有授权、工具轨迹或最终回复时机。

在两个入口的当前技能文本后分别追加三种明确违反持续执行要求的语句，保留所有必需关键词时，六个反例均返回0个错误。两个已知暂停语句对照均被检出，说明调用路径有效；不是实验未运行或检查器完全失效。

## 根本原因

持续执行交付的验证责任停留在规范覆盖和静态回退检测，没有以真实Agent执行来检验“测试失败后继续修复”“局部阻塞后继续独立项”“回答进度后继续工作”。已有测试可以通过，同时仍缺少证明这些行为达标的证据。

这解释了治理验收为何不能有效发现或阻止提前结束；并不声称静态检查器导致了每一次运行暂停。只增加同义词黑名单仍不能补齐该验证缺口。

## 触发条件与分类

- 触发：两入口技能保留共享契约与必需词语，但出现固定回退清单之外的提前结束指令；或治理验收没有采集实际运行行为。
- 分类：governance / validation-design；影响两个apply入口、共享执行契约、检查器与验收设计。
- 排除：正常命令交接、全局准入失败、用户明确停止、所有剩余工作确实受阻的合法暂停；不移除Skeleton、权限及不可逆动作门禁。
- 无业务API、数据库、媒体或端请求封装变更；product_data_collection_observability为N/A，affected_layers为空。

## 证据链

| 编号 | 入口与类型 | 结果 | 证明边界 |
|---|---|---|---|
| RC-01 | docs/standards/command-execution-order.md §5；两个apply入口Implementation Loop | 明确要求持续执行与独立任务推进 | 规则存在，不证明实际执行通过 |
| RC-02 | scripts/validate-agent-context-budget.py::validate_apply_execution_contract；代码定位 | 检查输入和断言均为规则文本，无运行序列或任务依赖输入 | 确認静态检测范围 |
| RC-03 | logs/validator-probe.json；本地内存反例实验，含时间、源文件SHA256及精确反例 | 两入口各1个干净基线、3个漏检反例、1个已知语句检出对照；合计6个漏检、2个检出 | 可重复证明治理检测盲区，不是Agent行为复现 |
| RC-04 | tests/test_validate_agent_context_budget.py的4个apply测试；bug.md已有10 passed记录 | 验证文本正常、固定语句回退、部分同步分支和关键词缺失 | 不覆盖三项真实行为场景 |
| RC-05 | openspec/archive/2026-09-08-enforce-apply-continuous-execution/design.md的验证责任；docs/spec-logs/20260908171923-governance-apply-continuous-execution.md | 原验证明确仅证明规范与检查器，实际行为留给使用观察 | 确认行为验收未在该交付内闭环，不将旧报告曲解为虚报 |
| RC-06 | screenshots/req0137-command-handoff.png与screenshots/req0137-apply-partial-stop.png；关联implementation-evidence.md | 命令交接、1/12人工门禁暂停及独立校验结果 | 背景/合法暂停候选对照，不用于证明违规或作为confirmed依据 |

## 复现方法

在仓库根目录用Python导入校验器。对APPLY_SKILLS的两个入口分别读取原文本，在内存中追加logs/validator-probe.json的cases内容，使用unittest.mock.patch.object替换Path.read_text返回值，调用validate_apply_execution_contract。依次运行原文本基线、三个反例、APPLY_PAUSE_REGRESSIONS首项阳性对照。恢复patch后结束，不修改技能或实现代码。

预期治理检测：矛盾指令不能被当作行为已合格的证据。实际：三个反例在两个入口均返回零错误，已知语句均被检出。报告保存源哈希以区分后续变更；后续版本复测结果需单独记录，不能覆盖修复前证据。

## 修复与验证责任

修复目标包含可核对的收尾检查、已知问题集中处理、四类进度和有限重试策略；不只扩充关键词。治理执行者在修复阶段按acceptance.md实际运行两个入口的B1～B6，保留工具与任务序列，验证前后行为。

全部12项行为AC尚未执行或通过，不能把根因确认或静态探针成功当作修复验收。若后续发现具体运行原因，应补充独立证据，不反向改写本报告的证明范围。

## 补证与评审

治理根因已有代码定位、可重复实验及历史验证边界三类证据，可提交评审。无需用户提交历史会话。实际行为验收由治理执行者负责；如执行环境缺失，只标记具体场景阻塞并推进其他可执行验证，不向用户泛化索取历史材料。

尚未自动评审、纳入Sprint、创建修复Change或实施代码。
