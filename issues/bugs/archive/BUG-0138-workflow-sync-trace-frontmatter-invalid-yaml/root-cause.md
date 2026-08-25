---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
root_cause_status: confirmed
root_cause_type: code
created_at: 2026-08-25 09:44:00
updated_at: 2026-08-25 09:44:00
---

# 根因分析

## 根因状态

`confirmed`

## 直接原因

Workflow Sync 在更新 Issue `trace.md` frontmatter 时使用行级正则和字符串拼接维护 YAML 嵌套字段，缺少标准 YAML round-trip 解析与结构校验。在已有异常或边界结构下，脚本可能写出缺少父键的缩进列表项，导致 frontmatter 不是合法 YAML。

## 根本原因

`scripts/workflow_sync/patch.py` 将 frontmatter 和正文 fenced `yaml` 块都当作文本块处理：

- `patch_issue_trace()` 在 frontmatter 中调用 `ensure_nested_yaml_scalar()` 和 `ensure_openspec_change_in_block()` 写入 `lifecycle.generated`、`openspec_changes[]` 与关联字段。
- `ensure_nested_yaml_scalar()` 仅通过 `_yaml_section_bounds()` 定位父级范围，再插入缩进行。
- `ensure_openspec_change_in_block()` 仅用正则判断是否存在 `change_id` 和 `openspec_changes` 段，缺少写入后 YAML 结构验证。

这种实现对字段缩进、父键存在性和嵌套列表边界过于敏感，无法保证 frontmatter 持续符合标准 YAML。

## 触发条件

- 运行 `req.generate`、`bug.generate`、`req.opsx`、`bug.opsx`、`opsx.apply` 等会更新 Issue trace frontmatter 的 Workflow Sync 事件。
- 目标 trace frontmatter 中存在 `openspec_changes: []`、既有 change 列表、缺父键的历史残留，或其他可被正则误判边界的结构。
- 写入后没有用标准 YAML parser 校验 frontmatter。

## 证据链

| 证据 | 类型 | 结论 |
|---|---|---|
| `scripts/workflow_sync/patch.py:1034` | 代码定位 | `patch_issue_trace()` 同时更新 frontmatter 与 fenced `yaml` 块，是问题写入入口。 |
| `scripts/workflow_sync/patch.py:799` | 代码定位 | `ensure_nested_yaml_scalar()` 基于行级正则插入嵌套 YAML 字段，缺少解析器级结构保障。 |
| `issues/requirements/archive/REQ-0120-webp-derived-image-variants/trace.md:1` | 现场样本 | frontmatter 中 `updated_at` 后直接出现缩进 `- change_id`，缺少 `openspec_changes:` 父键。 |
| `python -c "import yaml; ... yaml.safe_load(frontmatter)"` | 复现 | 标准 YAML parser 报 `ScannerError: mapping values are not allowed here`，证明 frontmatter 非法。 |
| `scripts.workflow_sync.collect.parse_frontmatter_yaml(...)` | 复现 | 项目简易解析器将内层 Change 状态误读为顶层 `status`，证明状态解析可能漂移。 |

## 影响判断

- 影响 workflow 文档事实源，不直接影响业务 API 或用户页面。
- 后续 Workflow Sync 可能基于错误的顶层状态刷新 registry、CHANGELOG、Sprint scope 或 OpenSpec 门禁判断。
- 现有测试只验证字段文本出现次数，无法阻止非法 YAML frontmatter 进入仓库。

## 验证方式

修复前验证：

1. 读取 `REQ-0120-webp-derived-image-variants/trace.md` frontmatter。
2. 使用标准 YAML parser 解析，确认报错。
3. 使用项目简易解析器解析，确认顶层 `status` 被误读为内层 Change 状态。

修复后验证：

1. 构造 `req.generate`、`req.opsx`、`opsx.apply` 相关 fixture。
2. 运行 Workflow Sync 后，用标准 YAML parser 校验 frontmatter 可解析。
3. 断言顶层 `status` 与 `openspec_changes[].status` 各自保持正确语义。
4. 回归确认 fenced `yaml` 块与 frontmatter 的主状态一致。

## 人工补证

当前根因已确认，无必须人工补证项。若后续发现更多非法 trace 样本，可在修复 Change 中补充样本路径和对应事件来源。
