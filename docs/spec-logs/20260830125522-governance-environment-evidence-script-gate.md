---
purpose: 环境分层证据脚本门禁治理日志
content: 记录环境分层验收与生产证据后置规则从文档规范升级为脚本强门禁的事实
source: /spec-opt enforce-environment-tiered-evidence-gates
update_method: 后续调整脚本规则、命令接入或发布门禁时更新或追加新日志
created_at: 2026-08-30 12:55:22
updated_at: 2026-08-30 12:55:22
---

# 环境分层证据脚本门禁治理日志

## 背景

`standardize-environment-tiered-evidence-gates` 已明确开发、体验版和生产发布 evidence 分层，但只靠文档规则仍可能出现三类回退：开发证据冒充生产通过，体验版 / 真机 Network 缺可定位证据却标 `passed`，以及 `production_only_pending` 在生产发布前未重新判定。

本次治理将规则升级为可执行门禁，覆盖单 Change 归档、Sprint 归档 readiness、release status 与 release publish。

## 变更摘要

- 新增 `scripts/environment_tiered_evidence.py` 作为复用核心，新增 `scripts/validate-environment-tiered-evidence.py` 作为 CLI。
- `scripts/validate-archive-evidence.py` 接入单 Change 归档证据检查。
- `scripts/validate-sprint-archive-readiness.py` 接入 Sprint 范围检查，并在 readiness report 中输出环境分层 evidence 结果。
- `scripts/validate-release.py` 接入 release status / publish 校验；生产目标下 `production_only_pending` 转为发布阻塞。
- 更新 `AGENTS.md`、`rules/{testing,release,agent-context-budget}.md`、`docs/standards/command-execution-order.md` 和相关命令 Skill。

## 验证摘要

- `python scripts/validate-environment-tiered-evidence.py --change enforce-environment-tiered-evidence-gates`：通过。
- `python scripts/validate-environment-tiered-evidence.py --sprint sprint-028`：通过。
- 聚焦 pytest：环境门禁、Sprint readiness 接入、release status 生产重判与 development follow-up 共 8 项通过。

## 已知上下文

同跑 `tests/test_release_validation.py` 全文件时，3 个 usage-docs 旧夹具仍因截图共享资产规则失败；该失败与本次环境分层 evidence 门禁无关，未在本次治理中修复。

## 跨项目落地提示词

```text
/spec-opt 将环境分层验收与生产证据后置规则做成脚本强门禁：新增 validate-environment-tiered-evidence.py，检查开发证据不得冒充体验版/真机/生产通过，体验版或真机 Network passed 必须有可定位 evidence，production_only_pending 在生产发布目标前必须重新判定；接入 opsx-archive、sprint-archive、release-status 和 release-publish 的现有 validator，并补充聚焦测试与治理日志。
```
