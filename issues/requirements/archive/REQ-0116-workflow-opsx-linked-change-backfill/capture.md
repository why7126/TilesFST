---
req_id: REQ-0116-workflow-opsx-linked-change-backfill
status: done
created_at: 2026-08-22 14:18:08
updated_at: 2026-08-22 14:55:53
recorded_by: product
source: 用户反馈 + /explore 只读分析
priority_hint: P1
parent_requirement:
captured_via: capture
classification_rationale: "属于新增 workflow 治理能力；目标是增强 req.opsx 与 bug.opsx 两条链路的自动回填一致性，不是已交付业务功能偏差。"
---

# 一句话

Workflow Sync 应在 `req.opsx` 与 `bug.opsx` 创建或确认 linked Change 后，自动回填 Issue trace、主文档与 registry 中的 `openspec_changes`、`related_changes` / `related_change`，避免后续 `/opsx-apply <REQ|BUG-id>`、看板推导和人工阅读出现关联漂移。

# 原始描述

标题：增强 opsx linked Change 自动回填

背景：刚收到建议“增强 `req.opsx` 对 `openspec_changes` 与 `related_change` 的自动回填”。经 `/explore` 只读分析，当前规则已经要求 `/req-opsx` 与 `/bug-opsx` 维护 linked Change，但脚本层面主要同步 trace 与 Sprint scope；`requirement.md` / `bug.md` 主文档和 `_registry.yaml` 中的 `related_change` 仍可能滞后。用户确认采纳，并要求 REQ/BUG 两条 opsx 链路一起增强。

影响范围：Workflow Sync、`req.opsx`、`bug.opsx`、Issue trace、REQ/BUG 主文档、`issues/requirements/_registry.yaml`、`issues/bugs/_registry.yaml`、后续 `/opsx-apply <REQ|BUG-id>` 与 `/opsx-archive <REQ|BUG-id>` 解析链路。

建议验收或复现要点：对已纳入 Sprint 的 REQ 与 BUG 分别执行 `req.opsx` / `bug.opsx` 后，Workflow Sync 应幂等刷新 trace、主文档、registry 与 Sprint scope；重复运行不产生重复条目；后续 `/opsx-apply --sprint auto` dry-run 能从 linked Change 解析到同一 Sprint。

# 分类分析

| 条目 | 类型 | 拆分判断 | 理由 |
|---|---|---|---|
| 增强 `req.opsx` / `bug.opsx` linked Change 自动回填 | REQ | 合并为单条 | 两条链路共享 Workflow Sync 同步机制，验收目标一致；拆成两条会增加实现与验收重复。 |

# 背景与关联

- 关联命令：`/req-opsx`、`/bug-opsx`、`/opsx-apply`、`/opsx-archive`
- 关联能力：Workflow Sync、Issue lifecycle、Sprint scope 派生
- 已观察样例：`REQ-0115-media-multi-variant-images` 的 `trace.md` 已记录 `openspec_changes`，但 `requirement.md` 状态块缺少 linked Change 回填，说明主文档入口存在漂移风险
- 实现倾向：优先沉到 `scripts/sync-workflow-status.py --event req.opsx|bug.opsx` 和子文档同步逻辑，而不是让每次 opsx 命令手工多点补写

# 待澄清

- [ ] 主文档中是否统一使用单值 `related_change`，还是同时保留 `openspec_changes[]` 结构化列表
- [ ] 对历史已存在漂移的 REQ/BUG 是否在本需求实现时提供 focused dry-run / apply 修复入口
- [ ] registry 的 `related_change` 在多 Change Issue 场景下应记录当前 active linked Change、最新 linked Change，还是保留首个主 Change

# 建议验收要点

- [ ] `req.opsx` 成功后，目标 REQ `trace.md` frontmatter 与 yaml 块均包含当前 `openspec_changes[]`，并同步 `related_changes[]` 或等价 linked Change 字段。
- [ ] `req.opsx` 成功后，目标 `requirement.md` 主文档可读入口自动引用当前 linked Change，不再只同步 `status`。
- [ ] `req.opsx` 成功后，`issues/requirements/_registry.yaml` 对应条目的 `related_change` 自动更新为当前 linked Change。
- [ ] `bug.opsx` 成功后，目标 BUG `trace.md`、`bug.md` 和 `issues/bugs/_registry.yaml` 同步当前 linked Change。
- [ ] 自动回填必须幂等：重复运行 Workflow Sync 不重复追加 `openspec_changes`、`related_changes` 或变更记录。
- [ ] 已纳入 Sprint 的 REQ/BUG 创建 Change 后，同步继续补齐 `sprint.yaml` 的 `changes[]` 与 `scope_estimates[].change`，并通过 `/opsx-apply --sprint auto --dry-run` 解析门禁。
- [ ] 增加或更新聚焦测试，覆盖 REQ 与 BUG 两条 opsx 链路的 trace、主文档、registry 和 Sprint scope 同步结果。

# 探索结论

采纳。该增强属于 workflow 治理能力，价值在于消除 linked Change 的多入口漂移，降低后续命令解析、看板推导和人工确认成本。
