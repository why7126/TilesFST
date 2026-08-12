---
purpose: spec-study 学习报告去重治理迭代日志
content: 记录 spec-study 同一次学习应用流程只生成一份正式 study 报告的规则变更
source: /spec-opt avoid-duplicate-spec-study-reports
created_at: 2026-08-07 11:22:49
updated_at: 2026-08-07 11:54:47
---

# spec-study 学习报告去重治理迭代日志

## 迭代目标

避免 `/spec-study` 在一次学习应用流程中同时生成内容重复的 `study` 学习报告和 `governance` 治理日志，统一为“一次流程，一份正式 study 报告”。

## 变更摘要

- `/spec-study` 同一次学习应用流程只生成一份 `YYYYMMDDhhmmss-study-xxx.md`。
- `/spec-study` 触发的治理资产应用结果汇总到同一份 `study` 报告，不额外生成内容重复的 `YYYYMMDDhhmmss-governance-xxx.md`。
- 学习阶段候选内容不另行落盘为第二份正式 `study` 报告。
- 同一流程已有 study 报告时，后续补充、验证和应用结果必须更新同一报告。
- `/spec-study` 学习报告不得包含本机绝对路径；涉及路径证据时使用仓库相对路径或 `<local-project>`、`<user-home>` 等脱敏占位符。
- `docs/spec-logs/README.md` 与 `rules/agent-context-budget.md` 同步去重要求。

## 影响范围

- API：不影响。
- 数据库：不影响。
- Web：不影响。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要验证。
- 测试：业务测试不适用，执行治理校验。

## 更新文件

- `.agents/skills/spec-study/SKILL.md`
- `docs/spec-logs/README.md`
- `docs/spec-logs/20260807112249-governance-spec-study-single-report.md`
- `rules/agent-context-budget.md`
- `openspec/changes/avoid-duplicate-spec-study-reports/`

## 隐私检查结果

- 本日志只记录治理结论和聚合描述。
- 未记录用户隐私数据、真实客户数据、密钥、访问令牌、本机绝对路径、未脱敏日志、学习对象源码或截图中的个人信息。

## 验证结果

- `openspec validate avoid-duplicate-spec-study-reports`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python scripts/validate-sprint-scope.py sprint-022 --item avoid-duplicate-spec-study-reports`：通过。
- `python scripts/sync-workflow-status.py --event opsx.apply --change avoid-duplicate-spec-study-reports --sprint auto`：通过；首次 Updated 2，修正 study/governance 去重语义后 Updated 1，补充本机绝对路径边界后 Updated 1，Errors 0。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change avoid-duplicate-spec-study-reports --sprint sprint-022 --json`：通过；AI Usage sprint snapshot 已刷新。

## 后续建议

- 后续执行 `/spec-study` 时，若学习阶段已有同流程报告，应用完成只更新该报告。
