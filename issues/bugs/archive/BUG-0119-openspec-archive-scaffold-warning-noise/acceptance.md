---
bug_id: BUG-0119-openspec-archive-scaffold-warning-noise
title: OpenSpec 归档反复暴露英文脚手架兼容 warning 验收标准
acceptance_status: passed
created_at: 2026-08-06 10:27:26
updated_at: 2026-08-06 17:17:37
---

# 验收标准

## AC-001 已知 CLI 兼容 warning 可被吸收

- [ ] 当 OpenSpec CLI 仅输出 `proposal.md` 缺少英文 `## Why` / `## What Changes` 相关 warning，且项目中文语言校验通过时，归档最终说明不再重复展示固定非阻塞提示。
- [ ] 归档成功结论仍能明确表达 Change 已完成归档。
- [ ] 不要求为消除该 warning 回填英文脚手架标题。

## AC-002 真实错误仍正常暴露

- [ ] 当 OpenSpec CLI 返回非零退出码时，归档流程仍失败并输出必要错误信息。
- [ ] 当 stderr 包含未知 warning 或 error 时，归档最终输出仍保留该信息，避免误吞真实风险。
- [ ] 当 `python scripts/validate-openspec-language.py` 失败时，归档流程仍按项目语言门禁阻断。

## AC-003 项目语言规范保持优先

- [ ] Change 文档继续遵守中文优先规则。
- [ ] `proposal.md`、`design.md`、`tasks.md` 不因本缺陷修复而新增英文脚手架标题。
- [ ] 归档脚本注释或说明清楚区分上游 CLI 兼容 warning 与项目语言校验结果。

## AC-004 回归验证覆盖

- [ ] 新增或更新脚本级测试，覆盖“仅已知 CLI warning + 中文语言校验通过”的成功静默场景。
- [ ] 新增或更新脚本级测试，覆盖“未知 stderr 仍暴露”的场景。
- [ ] 新增或更新脚本级测试，覆盖“中文语言校验失败仍阻断”的场景。

## AC-005 不扩大运行时影响

- [ ] 不修改后端 API 路径、请求、响应或错误码。
- [ ] 不修改数据库 schema 或迁移。
- [ ] 不修改 Web、小程序或管理端运行时功能。
- [ ] 不需要 Orval 生成。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: fix-openspec-archive-scaffold-warning-noise
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

