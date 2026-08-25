## 根因摘要

根因状态为 `confirmed`。Workflow Sync 当前将 Issue `trace.md` frontmatter 当作纯文本块处理，通过正则查找父级字段范围，再插入缩进行。该方式无法可靠保障 YAML 父子结构、列表边界和字段语义，导致已有样本出现缺少 `openspec_changes:` 父键的缩进列表项。

证据入口：

- `scripts/workflow_sync/patch.py:1034`：`patch_issue_trace()` 同时更新 frontmatter 与 fenced `yaml` 块。
- `scripts/workflow_sync/patch.py:799`：`ensure_nested_yaml_scalar()` 基于行级正则插入嵌套 YAML 字段。
- `issues/requirements/archive/REQ-0120-webp-derived-image-variants/trace.md:1`：frontmatter 中存在缩进 change 列表但缺少父键。
- 标准 YAML parser 对该 frontmatter 报 `ScannerError`。
- 项目简易解析器会把内层 `status: applied` 误读为顶层 `status`。

## 修复方案

### 1. Frontmatter 写入安全化

优先方案：让 Workflow Sync 对 frontmatter 使用结构化 YAML 解析/序列化，至少覆盖本 Change 涉及的 Issue trace 字段：

- `status`
- `updated_at`
- `lifecycle.generated`
- `openspec_changes[]`
- `related_changes[]`
- `related_change`
- `iteration`

若短期继续保留文本拼接 helper，必须在每次写入 frontmatter 后用标准 YAML parser 校验，并在校验失败时返回错误或 blocker，禁止把非法 frontmatter 写入文件。

### 2. 状态语义隔离

解析 Issue trace frontmatter 时，顶层 `status` 只能来自 frontmatter 顶层字段。`openspec_changes[].status` 只能表达 Change 状态，不得被 `parse_frontmatter_yaml()` 或等价解析入口提升为 Issue 主状态。

### 3. 已知样本修复

修复 `REQ-0120-webp-derived-image-variants/trace.md` frontmatter，使其恢复为：

```yaml
openspec_changes:
  - change_id: add-webp-derived-image-variants
    type: update
    status: applied
related_changes:
  - add-webp-derived-image-variants
```

修复后必须同时校验标准 YAML parser 和项目解析器的结果。

### 4. 回归测试

补充聚焦测试，覆盖以下场景：

- `req.generate` / `bug.generate` 写入 `lifecycle.generated` 后 frontmatter 可被标准 YAML parser 解析。
- `req.opsx` / `bug.opsx` 写入 linked Change 后 `openspec_changes:` 父键存在，且幂等运行不重复追加。
- `opsx.apply` 更新 `openspec_changes[].status` 后顶层 Issue `status` 不被覆盖。
- 已知异常样本修复前失败、修复后通过。

## 风险与边界

- 该修复会触碰 workflow 治理脚本，风险集中在 REQ/BUG trace、registry、CHANGELOG 与 Sprint scope 派生。
- 不涉及业务 API、DB、UI、对象存储、媒体处理或小程序。
- 若引入 YAML 库序列化，需避免重排整个 trace frontmatter 造成大范围无意义 diff；可以限制为目标字段局部更新后校验。

## 文档与测试影响

- OpenSpec delta 更新 `agent-workflow-tooling` 和 `testing` 能力。
- 需要补充或更新 `tests/test_workflow_sync_time_drift.py` 或等价 Workflow Sync 聚焦测试。
- 不需要更新 OpenAPI / Orval / `.env.example`。
