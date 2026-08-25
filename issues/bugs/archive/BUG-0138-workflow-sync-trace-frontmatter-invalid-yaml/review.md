---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
review_result: approved
reviewed_at: 2026-08-25 09:46:24
reviewer: product
created_at: 2026-08-25 09:46:24
updated_at: 2026-08-25 09:46:24
---

# 缺陷评审

## 评审结论

`approved`

确认该问题需要修复。Workflow Sync 当前会维护 REQ / BUG / Sprint / OpenSpec 多处机器事实源，REQ trace frontmatter 非法 YAML 会导致状态解析和后续门禁判断漂移，属于需要进入修复流程的 workflow 脚本缺陷。

## 评审清单

- [x] `root_cause_status: confirmed` 且证据链可定位。
- [x] 严重等级 `medium` 合理：不直接影响业务用户页面，但会污染 workflow 事实源。
- [x] 回归验收明确：需覆盖 YAML parser 可解析、父子结构完整、顶层状态不被 change 状态覆盖。
- [x] 暂不需要 hotfix 路径：建议纳入 Sprint 后通过 OpenSpec Change 修复。

## 评审依据

- 根因证据链已定位到 `scripts/workflow_sync/patch.py` 的字符串/正则式 YAML 写入逻辑。
- 现场样本 `REQ-0120-webp-derived-image-variants/trace.md` frontmatter 已可复现标准 YAML parser 报错。
- 项目简易解析器会把内层 change 状态字段误读为顶层状态，影响 workflow 状态事实源可信度。

## 后续建议

1. 先通过 `/sprint-propose` 纳入 Sprint。
2. 再通过 `/bug-opsx` 创建修复 Change。
3. 修复时优先补回归测试，防止 Workflow Sync 再次写出非法 frontmatter。
