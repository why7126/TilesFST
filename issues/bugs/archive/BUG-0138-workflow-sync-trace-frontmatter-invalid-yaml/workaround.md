---
bug_id: BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
created_at: 2026-08-25 09:44:00
updated_at: 2026-08-25 09:44:00
---

# 临时规避方案

## 当前可用规避

在正式修复前，执行会更新 Issue trace frontmatter 的 Workflow Sync 事件后，应对目标 `trace.md` 做聚焦检查：

1. 抽取 frontmatter。
2. 使用标准 YAML parser 校验可解析。
3. 确认顶层 `status` 未被 `openspec_changes[].status` 覆盖。
4. 若发现缺父键缩进列表项，暂停后续评审、Sprint 纳入或 OpenSpec apply，先修复 trace 事实源。

## 不建议的规避

- 不建议仅依赖 `scripts/workflow_sync/collect.py` 的简易解析结果判断 trace 是否正常，因为该解析器已被证实会把内层字段误读为顶层字段。
- 不建议批量手工修改历史 trace；应先通过修复 Change 增加解析校验与回归测试，再对已知异常样本做受控修正。

## 正式修复方向

- 让 Workflow Sync 对 frontmatter 写入使用结构化 YAML 解析/序列化，或在字符串拼接后强制标准 YAML parser 校验。
- 增加回归测试，覆盖 frontmatter 合法性、嵌套字段父键存在性、顶层状态不漂移。
- 修复已知异常样本 `REQ-0120-webp-derived-image-variants/trace.md`。
