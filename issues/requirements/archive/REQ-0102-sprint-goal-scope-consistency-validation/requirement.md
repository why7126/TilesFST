---
requirement_id: REQ-0102-sprint-goal-scope-consistency-validation
title: Sprint 目标编号列表与 Scope 一致性校验
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-06 11:23:34
updated_at: 2026-08-06 17:17:37
---

# REQ-0102 Sprint 目标编号列表与 Scope 一致性校验

## 1. 需求背景

项目的 Sprint 规划文档采用 `sprint.yaml` 作为机器事实源，`sprint.md` 作为人类阅读入口。`sprint.md` 内既有 `## 1. 目标` 下的「Sprint 目标编号列表」，也有 `## 2. Scope` 主表和 Workflow Sync 派生分组表。

近期发现 `sprint-020` 的 Scope 已包含 `REQ-0100-mintlify-docs-site-ia-content-experience`，但「Sprint 目标编号列表」未列出该编号。现有 `validate-sprint-scope.py` 能确认 `sprint.yaml` 与 `## 2. Scope` 主表、派生分组表一致，因此该类漂移仍会通过校验，影响产品、评审和归档人员快速理解 Sprint 范围。

本需求要求补齐 Sprint 目标编号列表与正式 Scope 的一致性校验，并明确 `/sprint-propose`、Workflow Sync 与 Sprint 四件套在该字段上的责任边界，避免机器范围正确但人读摘要遗漏。

## 2. 目标用户

| 角色 | 核心诉求 |
|---|---|
| 产品负责人 / 项目负责人 | 打开 `sprint.md` 时能快速看到完整目标编号，不被遗漏项误导。 |
| AI / Codex Agent | 在新增或同步 Sprint Scope 后，有明确校验提示，避免漏改目标编号列表。 |
| 评审者 | 能用一条校验命令发现 `sprint.md` 人读摘要与正式 Scope 的差异。 |
| 流程维护者 | 能将一致性规则沉淀到脚本和 Skill，而不是依赖人工肉眼检查。 |

## 3. 需求目标

- 建立「Sprint 目标编号列表」与 Sprint 正式 Scope 的一致性规则。
- 让 `validate-sprint-scope.py` 能发现目标编号列表缺失项，并输出具体缺失编号。
- 明确 `/sprint-propose` 在新增或修正 Scope 时必须同步目标编号列表。
- 明确 Workflow Sync 对目标编号列表的责任边界：至少不能让该漂移逃过最终校验。
- 确保 Sprint 四件套的人读入口与机器事实源保持一致。

## 4. 范围

### 4.1 本期包含

| 范围 | 说明 |
|---|---|
| 目标编号列表解析 | 从 `sprint.md` 的「Sprint 目标编号列表」提取 REQ、BUG 和 Change 编号。 |
| Scope 一致性校验 | 对比 `sprint.yaml` 正式范围、`## 2. Scope` 主表、Workflow Sync 分组表和目标编号列表。 |
| 缺失项提示 | 校验失败时输出具体 Sprint、具体编号、缺失位置和建议修复方向。 |
| `/sprint-propose` 规则同步 | 新增或同步 Scope 时，必须同步更新目标编号列表与对应要点段落。 |
| Workflow Sync 边界说明 | 规则和 Skill 中明确目标编号列表是否由 Workflow Sync 写入，以及校验如何兜底。 |
| Sprint 四件套影响 | 至少覆盖 `sprint.md`，并确认 `acceptance-report.md`、`release-note.md`、`sprint.yaml` 不被错误依赖为人读目标列表。 |
| 回归样例 | 使用 `sprint-020` / `REQ-0100` 漏列场景作为复现或测试样例。 |

### 4.2 本期不包含

| 不包含 | 说明 |
|---|---|
| 大规模历史 Sprint 自动修复 | 本需求优先建立校验与规则；历史批量修复需另行评估或通过后续 Change 明确范围。 |
| 自动重写目标自然语言段落 | 不要求 Workflow Sync 自动改写 `## 1. 目标` 的描述性段落。 |
| 修改业务功能 | 不涉及管理端、店主 Web、微信小程序的业务能力。 |
| API / DB 变更 | 不新增接口、Pydantic Schema、数据库表或 Orval 生成物。 |
| 绕过 OpenSpec 流程 | 后续实现仍必须通过 OpenSpec Change。 |

## 5. 核心概念

### 5.1 Sprint 正式 Scope

Sprint 正式 Scope 以 `sprint.yaml` 中的 `requirements`、`bugs`、`changes` 和 `scope_estimates` 为机器事实源，并由 Workflow Sync 派生到 `sprint.md` 的 `## 2. Scope` 主表及分组表。

### 5.2 Sprint 目标编号列表

Sprint 目标编号列表指 `sprint.md` `## 1. 目标` 下用于人读速览的一组编号列表。该列表不是机器事实源，但必须覆盖正式 Scope 中纳入 Sprint 的 REQ、BUG 和必要 Change，避免读者误判 Sprint 范围。

### 5.3 对应要点段落

对应要点段落指 `## 1. 目标` 下以范围项编号命名的说明段落，例如 `### REQ-0098-... 要点`。当目标编号列表新增 REQ/BUG 时，应同步存在可读要点，除非规则明确该类项无需要点。

## 6. 功能要求

### FR-001 目标编号列表必须覆盖正式 Scope

- 系统 MUST 校验 `sprint.md` 的 Sprint 目标编号列表包含 `sprint.yaml.requirements` 中的每个 REQ。
- 系统 MUST 校验目标编号列表包含 `sprint.yaml.bugs` 中的每个 BUG。
- 系统 SHOULD 校验目标编号列表包含未通过 REQ/BUG 间接表达的纯 Change。
- 对已通过 REQ/BUG 关联表达的 Change，系统 MAY 不强制在目标编号列表中重复列出 Change ID，但规则必须明确。
- 校验 MUST 支持完整 ID 与短编号的等价判断，例如 `REQ-0100-mintlify-docs-site-ia-content-experience` 与 `REQ-0100`。

### FR-002 缺失项必须给出具体失败信息

- 当 Scope 中的编号未出现在目标编号列表时，校验 MUST 失败。
- 失败信息 MUST 包含 Sprint ID、缺失编号和缺失位置。
- 推荐失败文案形如：`REQ-0100-mintlify-docs-site-ia-content-experience missing from sprint.md Sprint target id list`。
- 若同时缺失多个编号，校验 MUST 分条输出所有缺失项。
- 若目标编号列表不存在或格式不可解析，校验 MUST 提示列表缺失或格式异常，而不是静默跳过。

### FR-003 `/sprint-propose` 必须同步目标编号列表

- `/sprint-propose` 在新建 Sprint 时 MUST 生成完整目标编号列表。
- `/sprint-propose` 在已有 Sprint 中追加或修正正式 Scope 时 MUST 同步更新目标编号列表。
- 同步目标编号列表时 SHOULD 同步新增或更新对应要点段落。
- 多个范围项追加到同一 Sprint 时，目标编号列表更新 MUST 与 `sprint.yaml` 写入顺序保持一致，避免覆盖或重复。
- `/sprint-propose` 结束前 MUST 运行增强后的 `validate-sprint-scope.py`，并确保目标编号列表校验通过。

### FR-004 Workflow Sync 必须明确责任边界

- Workflow Sync 规则 MUST 明确 `## 2. Scope` 主表和分组表由 Workflow Sync 派生维护。
- Workflow Sync 规则 MUST 明确「Sprint 目标编号列表」是否由 Workflow Sync 自动维护。
- 如果 Workflow Sync 不维护目标编号列表，则最终校验 MUST 能发现目标编号列表与 Scope 不一致。
- 如果后续决定由 Workflow Sync 维护目标编号列表，则必须保证幂等、保留人写目标说明，并避免覆盖自然语言背景。
- 无论采用哪种方案，Sprint 同步成功不应让目标编号遗漏风险沉默通过。

### FR-005 `validate-sprint-scope.py` 必须覆盖目标编号列表

- `validate-sprint-scope.py <sprint-id>` MUST 同时检查 Scope 主表、Workflow Sync 分组表和目标编号列表。
- `--item <id>` 聚焦校验时 MUST 对该项执行目标编号列表检查。
- 校验 SHOULD 支持 archived 与 active Sprint 路径，不限定 `iterations/change`。
- 校验 SHOULD 避免误把 `## 2. Scope` 或后续章节中的编号当作目标编号列表证据。
- 校验成功路径保持摘要输出；失败路径输出具体缺失项。

### FR-006 Sprint 四件套一致性

- `sprint.md` 的目标编号列表、Scope 主表、Workflow Sync 分组表必须表达同一组正式范围。
- `sprint.yaml` 仍是机器事实源，不得以目标编号列表反向覆盖 `sprint.yaml`。
- `acceptance-report.md` 与 `release-note.md` 不需要包含目标编号列表，但其关联范围不得与 `sprint.yaml` 冲突。
- Sprint archive 或 release 相关校验如依赖 Scope，一律以 `sprint.yaml` 和增强校验结果为准。

### FR-007 历史案例复现与测试覆盖

- 测试 MUST 覆盖 `sprint-020` 中 `REQ-0100` 存在于 Scope 但缺失于目标编号列表的场景。
- 测试 MUST 覆盖目标编号列表完整时校验通过。
- 测试 SHOULD 覆盖短编号与完整 ID 混用场景。
- 测试 SHOULD 覆盖 BUG 与纯 Change 的边界策略。
- 若历史 Sprint 不自动修复，测试或文档 MUST 说明预期为“校验发现漂移”，而不是“自动变更历史文档”。

## 7. UI / UE 约束

本需求不新增 Web 管理端、店主 Web 或微信小程序 UI。

`sprint.md` 作为人读文档时应保持可扫描：

- 目标编号列表应使用 Markdown 列表，不引入复杂表格。
- 编号顺序应与正式 Scope 或 Sprint 优先级保持一致。
- 对应要点段落标题应稳定可搜索。
- 不应引入大段说明替代明确编号。

## 8. 数据与接口影响

| 范围 | 影响 |
|---|---|
| SQLite/MySQL | 不涉及表结构或数据迁移。 |
| Pydantic Schema | 不涉及。 |
| OpenAPI/Orval | 不涉及。 |
| 后端运行时 | 不涉及业务后端运行时代码。 |
| Web 管理端 | 不涉及管理端页面代码。 |
| 小程序 | 不涉及。 |
| 店主 Web | 不涉及。 |
| 脚本 / 工作流 | 需要增强 `validate-sprint-scope.py`，并同步 `/sprint-propose` 与 Workflow Sync 规则。 |
| 测试 | 需要补充脚本级回归测试或等价校验用例。 |

## 9. 关联需求与现状参考

| 关联项 | 关系 |
|---|---|
| `iterations/archive/sprint-020/sprint.yaml` | 机器事实源中包含 `REQ-0100`。 |
| `iterations/archive/sprint-020/sprint.md` | Scope 表包含 `REQ-0100`，目标编号列表缺失 `REQ-0100`。 |
| `scripts/validate-sprint-scope.py` | 当前只校验 Scope 主表和 Workflow Sync 分组表，需要扩展。 |
| `.agents/skills/sprint-propose/SKILL.md` | 已要求结束前运行 Scope 校验，需要补齐目标编号列表一致性要求。 |
| `.agents/skills/workflow-sync/SKILL.md` | 已说明目标编号列表不在 sync 范围，需要明确兜底校验或维护策略。 |
| `scripts/workflow_sync/patch.py` | 当前负责渲染 Scope 主表与派生分组表，不负责目标编号列表。 |

## 10. 状态块

```yaml
requirement_id: REQ-0102-sprint-goal-scope-consistency-validation
status: archived
priority: P1
readiness: Ready
parent_requirement: null
terminal: multi
target_clients:
  web_admin: not_included
  web_catalog: not_included
  wechat_miniapp: not_included
api_change_required: false
database_change_required: false
orval_required: false
prototype_required: false
next_step: /req-opsx REQ-0102
notes:
  - 本需求定位为 Sprint 工作流与校验治理，不涉及业务运行时代码。
  - 后续实现应优先让 validate-sprint-scope.py 暴露 sprint-020 / REQ-0100 的遗漏。
  - 是否由 Workflow Sync 自动维护目标编号列表，需要在 OpenSpec design 阶段确认。
  - 已补齐 user-stories、business-flow、acceptance 和 trace，可进入需求评审。
  - 需求已评审通过，可进入 req-opsx 或纳入 Sprint 规划。
```
