---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
status: done
created_at: 2026-08-25 09:28:29
updated_at: 2026-08-25 10:21:57
severity_hint: medium
environment: workflow-script
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

Workflow Sync 写入 REQ `trace.md` frontmatter 时可能生成非法 YAML 结构。已观察到 `REQ-0120-webp-derived-image-variants` 的 frontmatter 中出现缺少 `openspec_changes:` 父键的缩进列表项，标准 YAML parser 无法解析，项目内简易解析器还可能把内层 Change 状态误读成顶层状态。

# 复现步骤

1. 准备一个 REQ `trace.md`，frontmatter 中包含 `openspec_changes: []` 或缺少嵌套父键的 change 状态结构。
2. 运行会更新 Issue trace frontmatter 的 Workflow Sync 事件，例如 `req.generate`、`req.opsx` 或 `opsx.apply`。
3. 查看生成后的 REQ `trace.md` frontmatter。
4. 使用标准 YAML parser 解析 frontmatter，并对比项目内 `scripts/workflow_sync/collect.py` 的解析结果。

# 期望 vs 实际

- 期望：Workflow Sync 写入后的 `trace.md` frontmatter 始终是合法 YAML；`lifecycle.generated`、`openspec_changes[]`、`related_changes` 等字段保持父子结构完整；顶层 `status` 不受内层 change status 影响。
- 实际：已有 REQ trace frontmatter 出现非法缩进列表项，标准 YAML parser 报错；项目内简易解析器可能将内层 `status` 或 `type` 当作顶层字段，导致后续状态判断漂移。

# 影响范围

- `scripts/sync-workflow-status.py`
- `scripts/workflow_sync/patch.py`
- `scripts/workflow_sync/collect.py` 对 trace frontmatter 的解析结果
- REQ/BUG `trace.md` frontmatter 机器事实源
- Workflow Sync 后续状态同步、当前态看板、Sprint / OpenSpec 门禁判断

# 初步线索

- `scripts/workflow_sync/patch.py` 的 `patch_issue_trace()` 会同时更新 frontmatter 与 fenced `yaml` 块。
- `ensure_nested_yaml_scalar()` 与 `ensure_openspec_change_in_block()` 通过行级正则拼接 YAML，缺少标准 YAML round-trip 校验。
- 现有测试只断言 `generated:` 或 `change_id:` 出现次数，没有断言 frontmatter 能被标准 YAML parser 解析，也没有校验父子结构不漂移。
- 现场证据：`issues/requirements/archive/REQ-0120-webp-derived-image-variants/trace.md` frontmatter 中存在缩进列表项但缺少 `openspec_changes:` 父键。

# 建议验收或复现要点

- [ ] 构造 `req.generate` 场景，确认 `lifecycle.generated` 只写入合法父子结构，不生成孤立 `generated` 或错误缩进行。
- [ ] 构造 `req.opsx` / `opsx.apply` 场景，确认 `openspec_changes:` 父键保留且 change 状态不覆盖顶层 `status`。
- [ ] 使用标准 YAML parser 校验变更后的 trace frontmatter 可解析。
- [ ] 补充回归测试，覆盖 frontmatter 与 fenced `yaml` 块两处结构。
- [ ] 修复已有非法 REQ trace frontmatter，避免后续 Workflow Sync 继续读取漂移状态。

# 附件

- 暂无。
