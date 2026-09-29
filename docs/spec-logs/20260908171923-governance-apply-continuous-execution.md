---
created_at: 2026-09-08 17:19:23
updated_at: 2026-09-08 17:20:07
---

# Apply 持续执行治理

## 目标与决策

统一两个 apply 入口持续执行当前 Change 的行为，区分可恢复错误、必要人工决策和局部依赖阻塞。详细契约归属 docs/standards/command-execution-order.md §5。已采纳范围内自主修复与独立任务继续推进；未采纳忽略错误、绕过人工确认或自动归档发布。静态规则与检查器只能约束已知回退，后续实际任务观察仍用于验证 Agent 执行效果。

## 关联与范围

来源：spec-opt；Change：enforce-apply-continuous-execution；Sprint：sprint-030。无 REQ/BUG 来源，不创建额外 follow-up。

更新文件：.agents/skills/opsx-apply/SKILL.md、.agents/skills/openspec-apply-change/SKILL.md、.agents/skills/workflow-sync/SKILL.md、AGENTS.md、rules/agent-context-budget.md、docs/standards/command-execution-order.md、scripts/validate-agent-context-budget.py、tests/test_validate_agent_context_budget.py、关联 Change 材料与 Sprint 四件套派生状态、docs/spec-logs/CHANGELOG.md。

## 行为与验证

- 完成一组任务和上下文压缩不终止当前命令；范围内错误先修复复测；真正阻塞记录证据与恢复条件，继续独立任务。
- 任务验证通过才勾选；部分完成执行无完成事件的状态刷新，全部完成才发送 opsx.apply 事件；人工验收决定归档就绪，归档发布不自动执行。
- pytest tests/test_validate_agent_context_budget.py：10 passed，含两入口正常契约、旧暂停语句回退、部分同步分支缺失及关键执行维度缺失。
- 实际 2/3 任务时先 dry-run 再执行无事件 Workflow Sync，Sprint 表显示 in_progress 2/3；此证据覆盖纯治理 Change，不代表所有关联 Issue 的运行路径均已测试。
- 上下文预算、OpenSpec 语言、目录结构、目标 Change、Sprint scope 校验通过。
- 聚焦文档卫生检查报告 7 条既有历史叙述提示，未发现新增契约问题。
- Sprint 纳入脚本生成条目存在 YAML 缩进差异，已聚焦修复新条目缩进并重新同步、通过范围校验；未改动该工具逻辑。

## 影响与责任

API、数据库、Web、微信小程序、管理端业务无变化，Orval 与 Docker Compose 验证不适用。product_data_collection_observability 为 N/A，affected_layers 为空，仅治理资产。由治理执行者完成本地校验；实际 apply 的连续执行效果在后续使用中观察，发现新暂停模式时补充证据与校验。

遵循 rules/agent-context-budget.md、rules/iterations-lifecycle.md、rules/document-governance.md、rules/language.md、rules/testing.md、rules/security.md、rules/directory-structure.md 与 rules/root-cause-evidence.md；正式 specs 未修改。

## 完成同步

任务 3/3，Workflow Sync 完成事件成功，Sprint 派生状态为 applied，Errors 0；未归档。AI Usage：status ok、usage_mode actual、command_run_count 1、sprint_snapshot refreshed、warning_count 0、recommended_action 无。
