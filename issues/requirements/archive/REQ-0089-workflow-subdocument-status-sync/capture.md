---
req_id: REQ-0089-workflow-subdocument-status-sync
status: done
created_at: 2026-08-01 09:40:07
updated_at: 2026-08-01 11:46:26
recorded_by: product
source: /opsx-explore
priority_hint: P1
parent_requirement:
---

# 一句话

完善 REQ/BUG 子文档状态同步与验收结果回填机制，避免 `bug.md`、`requirement.md`、`acceptance.md` 等文档停留在生成或评审早期状态。

# 原始描述

在 `/opsx-explore` 梳理中发现当前命令、流程和规范仍存在文档更新不及时的问题：

- `BUG-XXX/bug.md` 仍停留在 `/bug-generate` 生成时的版本，后续 BUG 状态更新没有持续反写。
- `REQ-XXX/requirement.md` 内容和状态也会停留在某个阶段，不一定随 `trace.md`、registry、Sprint 或 OpenSpec Change 状态变化而同步。
- `acceptance.md` 主要承载验收标准，但是否已验收、验收是否通过、证据在哪里，没有稳定回填机制。
- 当前 Workflow Sync 主要同步 `trace.md`、registry、Sprint 派生块和部分归档 residual，子文档状态更多依赖归档阻塞后的补救，而不是日常命令的一等同步能力。
- 只读扫描显示 archive 目录已有较多历史子文档仍含早期非闭环状态，说明需要同时治理未来流程和历史漂移。

# 初步范围

- 明确 `trace.md`、`bug.md`、`requirement.md`、`acceptance.md`、`review.md` 等文档的事实源边界和同步责任。
- 扩展 Workflow Sync 或新增等价能力，在 `req.review`、`bug.review`、`req.opsx`、`bug.opsx`、`opsx.apply`、`opsx.archive`、`sprint.archive` 等状态变化后同步顶层子文档状态。
- 为 `acceptance.md` 建立验收结果回填模型，记录通过状态、验收时间、证据、失败项、来源 Change/Sprint/命令。
- 增加 drift check，使 `sync-workflow-status.py --check` 或专用校验能发现 `trace.md`、目录阶段和子文档 frontmatter/yaml 状态不一致。
- 将历史 residual 修复设计为受控 dry-run → apply 流程，先输出影响报告，再人工确认批量修复。

# 待澄清

- [ ] 子文档是否都保留 `status` 字段，还是改为只有 `trace.md` 保持机器状态、子文档使用 `document_status` 或移除状态字段。
- [ ] `acceptance.md` 是继续同时承载验收标准和验收结果，还是拆分出独立 `acceptance-result.md` / `verification.md`。
- [ ] 哪些命令必须同步子文档状态，哪些只记录 `trace.md` 即可。
- [ ] 历史 archive 漂移是否一次性批量修复，还是只在后续触达某个 REQ/BUG 时修复。
- [ ] 状态字段目标值是否统一为 `done`，还是允许 `archived`、`resolved`、`completed` 等历史闭环状态继续存在。

# 探索结论

本事项归类为单条流程治理 REQ：它围绕同一条工作流可靠性问题，目标是让 Issue 包内人类可读文档、机器事实源和归档门禁保持一致。后续可通过 `/req-generate` 展开 PRD，再通过 OpenSpec Change 落到 Workflow Sync、命令 Skill、规则文档和校验脚本。
