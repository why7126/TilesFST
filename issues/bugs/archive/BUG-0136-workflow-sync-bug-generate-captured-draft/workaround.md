---
bug_id: BUG-0136-workflow-sync-bug-generate-captured-draft
created_at: 2026-08-22 21:24:15
updated_at: 2026-08-22 21:24:15
---

# Workaround

## 临时规避方案

正式修复前，执行 `/bug-generate` 后需要人工核对并修正目标 BUG 的状态事实源：

1. 确认 `bug.md` 已生成且内容完整。
2. 检查 `trace.md` frontmatter 与 fenced YAML 中的 `status` 是否为 `draft`，`lifecycle.generated` 是否为本次生成时间。
3. 检查 `issues/bugs/_registry.yaml` 中对应 BUG 状态是否为 `draft`。
4. 检查 `issues/bugs/CHANGELOG.md` 当前态行是否显示 `draft`，下一步是否为 `/bug-complete <BUG-id>`。

## 不足与风险

- 人工修正容易遗漏 frontmatter、fenced YAML、registry 或当前态看板之一，继续造成状态漂移。
- 重复运行 `bug.generate` Workflow Sync 可能再次把 `bug.md` 或派生看板拉回旧状态。
- 下游 `/bug-complete`、`/bug-review`、`/sprint-propose` 可能根据错误状态给出错误下一步。

## 正式修复方向

- 在 Workflow Sync 事件映射中补齐 `bug.generate` 的 `captured -> draft` 状态推进逻辑。
- 当 `bug.md` 已存在且事件为 `bug.generate` 时，同步 trace、registry、当前态看板与 `bug.md` frontmatter。
- 增加幂等测试，覆盖首次生成、重复生成、缺失 `bug.md` 的 warning 分支。
