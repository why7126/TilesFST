## 上下文

REQ-0116 指向一个 workflow 治理缺口：Issue linked Change 在 `req.opsx` / `bug.opsx` 后可能只在部分事实源中出现。现有能力已经覆盖：

- Issue 子文档状态同步；
- REQ/BUG 来源后续 opsx 命令继续使用原始 Issue ID；
- 已纳入 Sprint 的 Issue 创建 Change 后回填 Sprint scope；
- 当前态看板 next-step 刷新。

缺口在于 linked Change 多入口一致性没有被定义为一等同步目标。`trace.md`、`requirement.md` / `bug.md`、`_registry.yaml`、Sprint scope 各自更新时，容易出现“机器事实源正确，但人类入口或 registry 滞后”的状态。

## 目标 / 非目标

**目标：**

- 在 `req.opsx` 与 `bug.opsx` 中统一 linked Change 回填模型。
- 让 Workflow Sync 集中维护 trace、主文档、registry、Sprint scope 的 linked Change。
- 保持重复运行幂等，不重复追加 `openspec_changes[]`、`related_changes[]` 或 `related_change`。
- 通过测试覆盖 REQ 与 BUG 两条链路。

**非目标：**

- 不批量修复所有历史 archive 漂移。
- 不改变 `/opsx-apply <REQ-id|BUG-id>` 使用原始 Issue ID 的命令契约。
- 不新增业务 API、DB 表、Web UI、小程序页面或对象存储能力。
- 不让 `sprint.md` 手工 Scope 表替代 `sprint.yaml` 机器事实源。

## 决策

### D1：以 `trace.md.openspec_changes[]` 作为机器事实源

`trace.md.openspec_changes[]` 继续作为 Issue linked Change 的结构化事实源。`requirement.md` / `bug.md` 和 `_registry.yaml.related_change` 作为人类入口和索引派生字段。

理由：

- 已有 `/opsx-apply <REQ|BUG-id>` 解析规则依赖 `trace.md.openspec_changes[]`。
- registry 与主文档适合展示当前主 linked Change，但不适合承载多 Change 历史全部语义。

### D2：`related_change` 采用“当前 active 或最新主 linked Change”单值策略

当 Issue 只有一个 linked Change 时，`related_change` 直接等于该 Change。多 Change 场景下，设计阶段优先选择当前 active 且未 archived 的 Change；若多个候选同阶段并存，Workflow Sync 报告 blocker，要求人工选择，不静默覆盖。

理由：

- registry 行需要单值便于当前态看板和人类扫描。
- 多 Change 自动猜测风险高，应显式暴露决策点。

### D3：Workflow Sync 负责写入派生字段

`/req-opsx` / `/bug-opsx` 只负责创建或确认 Change 并调用 Workflow Sync。派生字段写入集中在 `scripts/workflow_sync/**`。

理由：

- 避免 Skill、脚本、Sprint 更新分散维护同一套字段。
- 可用单测覆盖同步逻辑，而不是依赖每个命令手工补写。

### D4：Sprint scope 继续以 `sprint.yaml` 为机器事实源

当 Issue 已在 Sprint scope 中，`req.opsx` / `bug.opsx` 的 Workflow Sync 必须把新 Change 回填同一 `sprint.yaml.changes[]` 和 `scope_estimates[].change`。`sprint.md` 仅由 Workflow Sync 派生刷新。

理由：

- `/opsx-apply --sprint auto` 解析依赖 `changes[]`。
- Product-facing Sprint scope 必须从机器事实源派生，避免手工 Scope 表漂移。

## 风险 / 取舍

| 风险 | 缓解 |
|---|---|
| 多 Change Issue 的主 `related_change` 选择不明确 | 多候选 active Change 时输出 blocker，要求用户明确选择。 |
| 自动同步覆盖了具有历史语义的主文档字段 | 仅同步明确语义的 frontmatter / 状态块字段；语义不明时报 warning。 |
| 修复当前需求时发现历史 registry 漂移较多 | 本 Change 只做 focused sync / dry-run，不默认批量改 archive。 |
| Sprint scope 与 Issue trace 更新顺序导致短暂不一致 | `req.opsx` / `bug.opsx` Final Step 必须运行 Workflow Sync，并以 dry-run 验证 `/opsx-apply` 可解析 Sprint。 |

## 迁移计划

1. 扩展 Workflow Sync 的 Issue linked Change 写入能力。
2. 更新 registry patch 逻辑，使 `related_change` 能随 `req.opsx` / `bug.opsx` 同步。
3. 更新 Issue 主文档子文档同步逻辑，写入或更新 `related_change` / linked Change 状态块。
4. 增加 REQ 与 BUG 两条 opsx 链路测试。
5. 跑聚焦验证：Workflow Sync、Sprint scope 校验、OpenSpec 语言与结构校验。

## 待确认

- 多 Change Issue 中，如果存在多个 active Change 且均未归档，是否需要新增 CLI 参数让用户选择主 linked Change。
- 是否在后续治理中提供历史 archive linked Change 漂移批量 dry-run 报告。
