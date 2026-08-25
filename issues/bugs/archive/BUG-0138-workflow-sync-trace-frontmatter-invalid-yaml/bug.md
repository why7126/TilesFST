---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
title: Workflow Sync 写入 REQ trace frontmatter 时可能生成非法 YAML 结构
severity: medium
status: done
owner: product
discovered_at: 2026-08-25 09:28:29
environment: workflow-script
related_requirement:
related_change:
fix-workflow-sync-trace-frontmatter-invalid-yaml
updated_at: 2026-08-25 14:53:29
created_at: 2026-08-25 10:04:00
---

# 缺陷说明

Workflow Sync 在更新 REQ `trace.md` frontmatter 时，可能生成标准 YAML parser 无法解析的非法结构。当前已观察到 `REQ-0120-webp-derived-image-variants` 的 frontmatter 出现缩进列表项，但缺少对应的 `openspec_changes:` 父键。

由于 `trace.md` 是 Issue 机器状态事实源，这类非法 frontmatter 会影响后续 Workflow Sync、当前态看板、Sprint scope 和 OpenSpec 门禁对状态的判断。

# 现象

- 标准 YAML parser 解析异常 REQ trace frontmatter 时会报错。
- 项目内简易解析器可能把内层 Change 状态字段、`type: update` 误读为顶层字段。
- 顶层 Issue 状态可能从真实迭代范围状态漂移为 change 内层状态，影响后续同步判断。

# 复现步骤

1. 准备一个 REQ `trace.md`，frontmatter 中包含 `openspec_changes: []` 或缺少嵌套父键的 change 状态结构。
2. 运行会更新 Issue trace frontmatter 的 Workflow Sync 事件，例如 `req.generate`、`req.opsx` 或 `opsx.apply`。
3. 查看生成后的 REQ `trace.md` frontmatter。
4. 使用标准 YAML parser 解析 frontmatter。
5. 对比 `scripts/workflow_sync/collect.py` 对同一 frontmatter 的解析结果。

# 期望结果

- Workflow Sync 写入后的 `trace.md` frontmatter 始终是合法 YAML。
- `lifecycle.generated`、`openspec_changes[]`、`related_changes` 等字段保持父子结构完整。
- 顶层 `status` 只表达 Issue 主状态，不会被 `openspec_changes[].status` 覆盖或污染。
- frontmatter 与正文 fenced `yaml` 块两处机器状态保持一致。

# 实际结果

- 已有 REQ trace frontmatter 存在非法缩进列表项，标准 YAML parser 无法解析。
- 项目内简易解析器可能将内层 change 字段当作顶层字段。
- 现有测试只断言 `generated:` 或 `change_id:` 出现次数，未校验 frontmatter YAML 可解析、父子结构正确。

# 影响范围

- `scripts/sync-workflow-status.py`
- `scripts/workflow_sync/patch.py`
- `scripts/workflow_sync/collect.py`
- REQ / BUG `trace.md` frontmatter 机器事实源
- Workflow Sync 后续状态同步、当前态看板、Sprint / OpenSpec 门禁判断

# 严重等级说明

严重等级为 `medium`。该问题不直接影响业务用户页面或生产 API，但会污染项目 workflow 事实源，可能导致后续状态同步、迭代纳入和 OpenSpec 门禁判断漂移；若不修复，会在后续治理命令中持续放大排查成本。

# 初步证据

- `scripts/workflow_sync/patch.py` 的 `patch_issue_trace()` 会同时更新 frontmatter 与 fenced `yaml` 块。
- `ensure_nested_yaml_scalar()` 与 `ensure_openspec_change_in_block()` 通过行级正则拼接 YAML，缺少标准 YAML round-trip 校验。
- `issues/requirements/archive/REQ-0120-webp-derived-image-variants/trace.md` frontmatter 中存在缺少 `openspec_changes:` 父键的缩进列表项。

# 建议验证

- 构造 `req.generate` 场景，确认 `lifecycle.generated` 只写入合法父子结构。
- 构造 `req.opsx` / `opsx.apply` 场景，确认 `openspec_changes:` 父键保留，且 change 状态不覆盖顶层 `status`。
- 使用标准 YAML parser 校验变更后的 trace frontmatter 可解析。
- 补充回归测试，覆盖 frontmatter 与 fenced `yaml` 块两处结构。
openspec_changes:
  - change_id: fix-workflow-sync-trace-frontmatter-invalid-yaml
    type: update
    status: archived
