---
purpose: 规范工程变更历史
content: 汇总记录规范、脚本、技能、命令与治理文档的更新历史
source: /spec-opt add-spec-logs-change-history
update_method: 每次 /spec-opt 完成治理资产更新后追加或更新条目；详细事实仍以单次 spec log 与 OpenSpec Change 为准
created_at: 2026-08-08 20:57:09
updated_at: 2026-08-12 09:15:58
---

# 规范工程变更历史

本文档用于汇总 `docs/spec-logs/` 下的规范工程变更历史，帮助快速查看规范、脚本、技能、命令和治理文档的演进。详细背景、验证输出与影响范围仍以单次 `YYYYMMDDhhmmss-governance-*.md` 日志、`YYYYMMDDhhmmss-study-*.md` 学习报告和对应 OpenSpec Change 为准。

## 记录规则

- 新增条目按时间倒序排列，最新在前。
- 每条记录保留摘要级信息，不粘贴大段日志、业务源码、用户原文或未脱敏数据。
- “跨项目落地提示词”列记录其他项目复用该治理规范时可直接给 AI 的 Prompt；提示词必须脱敏、可复制、避免携带本项目业务数据。
- `/spec-opt` 完成治理资产更新后 MUST 维护本文件，并同步写入或更新对应单次 `governance` 日志。
- `/spec-study` 学习报告可在本文件登记摘要，但不得替代 `study` 报告。

## 变更历史

| 时间 | 来源命令 | 关联 Change | 类型 | 影响范围 | 更新文件 | 验证结果 | 详细日志 | 跨项目落地提示词 |
|---|---|---|---|---|---|---|---|---|
| 2026-08-12 09:15:58 | `/spec-opt` | `optimize-release-workflow-ux` | 命令规范 | 发布版本、usage docs、公开公告、镜像准备、镜像构建、发布确认 | `.agents/skills/{release-propose,release-prepare,release-publish,image-prepare,image-build,usage-docs-generate}/SKILL.md`、`rules/{release,agent-context-budget}.md`、`openspec/changes/optimize-release-workflow-ux/`、`iterations/change/sprint-023/` | 上下文预算、OpenSpec 语言、目录结构和目标 Change 校验通过 | [20260812091558-governance-release-workflow-ux.md](20260812091558-governance-release-workflow-ux.md) | `/spec-opt 固化发布流程体验优化：release-propose 输出 usage docs、公开公告、镜像构建三类决策摘要；release-prepare 输出可执行阻塞修复路径；image-prepare/image-build 区分 warning/blocker；release-publish 支持发布后补公告且不触发镜像重建，前提是稳定发布范围和镜像输入未变。` |
| 2026-08-11 22:13:43 | `/spec-opt` | `refine-capture-explore-modify-stage-routing` | 命令规范 | `/capture`、`/explore`、`/opsx-modify` 阶段分流 | `.agents/skills/{capture,explore,opsx-modify}/SKILL.md`、`openspec/archive/2026-08-11-refine-capture-explore-modify-stage-routing/`、`openspec/specs/agent-workflow-tooling/spec.md`、`iterations/change/sprint-022/sprint.yaml`、`iterations/change/sprint-022/sprint.md` | 上下文预算、OpenSpec 语言、目录结构、目标 Change、Sprint scope、归档证据、Workflow Sync 和 AI Usage Hook 通过 | [20260811221343-governance-stage-routing.md](20260811221343-governance-stage-routing.md) | `/spec-opt 将需求相关“不如预期”的阶段分流标准写入 capture、explore、opsx-modify：active Change 内原验收偏差走 opsx-modify；Change 归档后或 Sprint 归档后作为新生命周期输入，已交付能力偏差走 bug-capture，新增能力走 req-capture；必须通过 OpenSpec Change 与 Sprint scope 承载。` |
| 2026-08-10 23:28:57 | `/spec-study ProjectMoonBox apply 全部候选项` | `apply-projectmoonbox-governance-learnings` | 跨项目学习应用 | `/spec-study`、`/git-check`、原型 UI 验收、Issue 当前态看板、引导式反馈、治理校验 | `.agents/skills/{spec-study,git-check,req-opsx,opsx-apply,opsx-modify,opsx-archive}/SKILL.md`、`scripts/{git-check.py,validate-agent-context-budget.py}`、`docs/standards/prototype-ui-acceptance.md`、`issues/{requirements,bugs}/CHANGELOG.md`、`rules/{agent-context-budget,security,ui-design,issues-lifecycle,document-governance,directory-structure}.md`、`AGENTS.md`、`docs/README.md` | 上下文预算、OpenSpec 语言、目录结构、目标 Change、Sprint scope、git-check、Workflow Sync 和 AI Usage Hook 通过 | [20260810232857-study-projectmoonbox-governance.md](20260810232857-study-projectmoonbox-governance.md) | `/spec-study apply：学习 ProjectMoonBox 的治理实践并按当前项目语境落地日志优先 spec-study、推送前 git-check 安全门禁、原型驱动 UI 验收、Issue 当前态看板和命令引导式反馈；必须通过 OpenSpec Change 与 Sprint scope 承载，禁止修改业务 src，并写入单份 study 报告。` |
| 2026-08-08 20:59:12 | `/spec-opt` | `add-spec-logs-change-history` | 文档规范 | `docs/spec-logs` 变更历史、文档治理、OpenSpec delta | `docs/spec-logs/CHANGELOG.md`、`docs/spec-logs/README.md`、`docs/README.md`、`rules/document-governance.md`、`rules/directory-structure.md`、`AGENTS.md`、`.agents/skills/spec-opt/SKILL.md`、`openspec/changes/add-spec-logs-change-history/` | 通过治理文档、目录、Sprint scope 与 OpenSpec 校验 | [20260808205912-governance-spec-logs-change-history.md](20260808205912-governance-spec-logs-change-history.md) | `/spec-opt 在 docs/spec-logs/ 下新增 CHANGELOG.md 规范工程变更历史总账，并要求每次规范、脚本、技能、命令更新后维护该总账；表格需包含时间、来源命令、关联 Change、类型、影响范围、更新文件、验证结果、详细日志和跨项目落地提示词。` |
| 2026-08-07 11:22:49 | `/spec-opt` | `avoid-duplicate-spec-study-reports` | 命令规范 | `/spec-study` 学习报告去重规则 | `docs/spec-logs/20260807112249-governance-spec-study-single-report.md` | 已记录 | [20260807112249-governance-spec-study-single-report.md](20260807112249-governance-spec-study-single-report.md) | `/spec-opt 优化 spec-study 规则：同一次跨项目 Harness 学习应用流程只生成一份正式 study 报告，后续应用结果、验证结果或修正更新同一报告，避免重复落盘。` |
| 2026-08-07 10:32:44 | `/spec-opt` | `add-spec-logs-governance-log-convention` | 目录规范 | `docs/spec-logs` 日志命名和边界 | `docs/spec-logs/20260807103244-governance-spec-logs.md` | 已记录 | [20260807103244-governance-spec-logs.md](20260807103244-governance-spec-logs.md) | `/spec-opt 新增 docs/spec-logs 规范工程日志目录约定：spec-study 学习报告使用 YYYYMMDDhhmmss-study-xxx.md，spec-opt 治理迭代日志使用 YYYYMMDDhhmmss-governance-xxx.md，并同步目录边界、文档索引和隐私脱敏规则。` |
