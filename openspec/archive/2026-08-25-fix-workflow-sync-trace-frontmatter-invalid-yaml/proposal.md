## 背景

`BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml` 已确认：Workflow Sync 在更新 REQ / BUG `trace.md` frontmatter 时使用行级正则和字符串拼接维护 YAML 嵌套字段，缺少标准 YAML round-trip 校验。现场样本 `REQ-0120-webp-derived-image-variants` 的 frontmatter 已出现缺少 `openspec_changes:` 父键的缩进列表项，标准 YAML parser 无法解析，项目内简易解析器还会把内层 `status: applied` 误读为顶层状态。

`trace.md` 是 Issue 工作流机器事实源。若 frontmatter 非法或状态解析漂移，后续 Workflow Sync、registry、CHANGELOG、Sprint scope 和 OpenSpec apply 门禁都可能基于错误状态继续派生，因此需要通过 OpenSpec Change 修复。

## 变更内容

- 修复 Workflow Sync 对 Issue trace frontmatter 的结构化写入或写入后校验，确保生成结果可被标准 YAML parser 解析。
- 覆盖 `lifecycle.generated`、`openspec_changes[]`、`related_changes` / `related_change` 等嵌套字段，防止缺父键、缩进错位或内层状态污染顶层状态。
- 修复已知异常样本 `REQ-0120-webp-derived-image-variants/trace.md`，确保后续脚本读取不会把 `openspec_changes[].status` 误判为 Issue 主状态。
- 补充聚焦回归测试，覆盖 `req.generate`、`bug.generate`、`req.opsx` / `bug.opsx`、`opsx.apply` 相关 frontmatter 写入与幂等场景。

## 能力影响

### 修改能力

- `agent-workflow-tooling`：补充 Workflow Sync 写入 Issue trace frontmatter 的 YAML 合法性和状态语义隔离要求。
- `testing`：补充 workflow 脚本 frontmatter 合法性回归测试要求。

### 不涉及范围

- 不修改业务 API、数据库、Web、小程序、管理端页面或用户可见业务流程。
- 不新增环境变量，不需要 Orval。
- 不执行生产数据迁移。

## 回滚计划

- 若修复后 Workflow Sync 回归测试失败，回滚本 Change 对 `scripts/workflow_sync/*` 的实现修改和相关测试。
- 对已知异常 trace 样本的修复应保留为可审计文档事实源；如需回滚，必须先确认回滚后不会重新触发标准 YAML parser 失败。
- 回滚后继续采用临时规避：每次运行相关 Workflow Sync 事件后，用标准 YAML parser 校验目标 `trace.md` frontmatter，并暂停后续 apply/archive 门禁。

## 验证计划

- 运行聚焦 pytest，覆盖 Workflow Sync trace frontmatter 写入和状态解析。
- 运行 `python scripts/validate-openspec-language.py`。
- 运行 `openspec validate fix-workflow-sync-trace-frontmatter-invalid-yaml --strict`。
- 运行 `python scripts/sync-workflow-status.py --event opsx.apply --change fix-workflow-sync-trace-frontmatter-invalid-yaml --sprint auto --dry-run`，确认该 Change 已回填到 `sprint-025` scope 后可被 apply 门禁解析。
