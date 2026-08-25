---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
acceptance_status: passed
created_at: 2026-08-25 09:44:00
updated_at: 2026-08-25 14:51:36
---

# 验收标准

## 回归 AC

- AC-001：运行 `req.generate` / `bug.generate` 后，目标 Issue `trace.md` frontmatter 可被标准 YAML parser 解析，`lifecycle.generated` 位于 `lifecycle` 父键下。
- AC-002：运行 `req.opsx` / `bug.opsx` 后，`openspec_changes:` 父键必须存在，change 条目保持合法列表结构。
- AC-003：运行 `opsx.apply` 后，顶层 `status` 继续表达 Issue 主状态，`openspec_changes[].status` 只表达 Change 状态，不得互相覆盖。
- AC-004：Workflow Sync 回归测试必须同时校验 frontmatter 与 fenced `yaml` 块，不能只校验 `generated:`、`change_id:` 文本出现次数。
- AC-005：已知异常样本 `REQ-0120-webp-derived-image-variants/trace.md` 被修复后，标准 YAML parser 可解析，项目简易解析器不再把内层 change status 误读为顶层 Issue status。

## 验收证据要求

- 提供聚焦测试命令与通过摘要。
- 提供至少一个修复前失败、修复后通过的 YAML parser 校验证据。
- 提供已知异常 trace 样本修复后的 frontmatter 摘要。
- 若修复涉及 Workflow Sync 解析器或写入器，需说明是否影响现有 REQ/BUG trace、registry、CHANGELOG 和 Sprint scope 派生逻辑。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 10:21:52
accepted_by: workflow-sync
source_change: fix-workflow-sync-trace-frontmatter-invalid-yaml
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

