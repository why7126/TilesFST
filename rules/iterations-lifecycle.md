---
purpose: iterations Sprint 生命周期阶段目录规范
content: change / archive 两阶段目录职责、准入条件、迁移时机与路径解析
source: 项目团队确认
update_method: Sprint 流程或目录边界变化时同步更新
created_at: 2026-06-27 23:45:00
updated_at: 2026-08-07 09:20:34
note: 与 issues plan/review/archive 互补；机器索引仍为 sprint.yaml
---

# iterations 生命周期阶段目录

## 1. 目标

在 `iterations/` 下，用 **change / archive** 两目录表达 Sprint 在「迭代进行中 → 归档闭环」中的物理位置，与 `sprint.yaml` 的 `status` 互补：

- **status**：逻辑状态机（`planning`、`in_progress`、`completed`）
- **lifecycle_stage**（物理目录）：`change` | `archive`

## 2. 目录结构（MUST）

```text
iterations/
├── README.md
├── change/                    # 未归档：规划中或开发中
│   └── sprint-xxx/
│       ├── sprint.yaml
│       ├── sprint.md
│       ├── release-note.md
│       └── acceptance-report.md
└── archive/                   # 已完成归档
    └── sprint-xxx/
        └── （同上四件套）
```

- 每个 `sprint-xxx/` 目录 **MUST** 仅存在于 `change/` 或 `archive/` 之一（不得多份拷贝）。
- 阶段子目录内 **禁止** 再嵌套 `change/archive`。
- 四件套规范见 `rules/document-governance.md` §4.1。
- Sprint ID **MUST** 使用 `sprint-xxx` 三位数字递增格式，例如 `sprint-022`；不得使用日期、主题词或混合命名作为 Sprint ID。

### 2.1 Sprint 自动编号（MUST）

- 当当前没有 `iterations/change/sprint-xxx/` 进行中迭代，且命令需要为 active Change 自动创建 Sprint 时，系统 MAY 自动创建下一个 Sprint。
- 自动创建时 MUST 扫描 `iterations/archive/` 与 `iterations/change/` 下符合 `sprint-[0-9]{3}` 的目录和 `sprint.yaml:sprint_id`，取最大编号加一；例如最新归档为 `sprint-021` 且无进行中迭代时，新建 Sprint MUST 为 `sprint-022`。
- 自动创建 Sprint MUST 落在 `iterations/change/sprint-xxx/`，四件套中的 `sprint_id`、标题、路径引用、Workflow Sync、AI Usage 和校验命令 MUST 使用同一个规范编号。
- 如果已存在 `iterations/change/sprint-xxx/` 进行中迭代，MUST 优先复用或要求用户明确选择；不得默认另建并行 Sprint。
- 若发现新建 Sprint 使用了非规范名称，MUST 立即重命名为自动编号结果，并同步所有引用与校验记录。

### 2.2 遗留扁平路径（兼容）

历史 Sprint 可能仍在：

```text
iterations/sprint-xxx/   # 遗留，deprecated
```

- 工具链 **SHOULD** 继续可读遗留路径（见 `scripts/workflow_sync/collect.py` 的 `resolve_sprint_dir()`）。
- 新建 Sprint **MUST** 落在 `change/` 下，**MUST NOT** 在 `iterations/` 根下新建 `sprint-*`。
- 批量迁移时使用 `scripts/migrate-iterations-lifecycle-stage.py`。

## 3. 两阶段定义

| 阶段目录 | 含义 | 典型 sprint.yaml `status` |
|---|---|---|
| **change** | **未归档**：迭代规划、开发、验收进行中 | `planning`、`in_progress` |
| **archive** | **已完成归档**：Sprint 内 Change 已全部 `/opsx-archive`，迭代验收与发布说明已收尾 | `completed` |

## 3.1 Sprint 容量门禁（MUST）

`/sprint-propose` 在生成正式四件套或更新 REQ/BUG/Change trace 前 MUST 计算候选范围的容量占用率：

```text
capacity_usage = estimated_person_days / capacity_person_days
```

- 若容量或估算缺失导致无法计算，MUST 先补齐输入；不得默认通过。
- 当 `estimated_person_days > capacity_person_days * 1.2` 时，MUST 硬阻断正式规划：不得创建 `iterations/change/<sprint>/` 四件套，不得更新 `trace.md` 的 `iteration` 或 Change trace，并提示拆分 Sprint、移出低优先级项或替换范围后重新运行 `/sprint-propose`。
- 当 `capacity_person_days < estimated_person_days <= capacity_person_days * 1.2` 时，MAY 继续生成 Sprint，但 MUST 在 `sprint.md` 记录容量风险、fix 缓冲影响和延后项建议。
- 当 `estimated_person_days <= capacity_person_days` 时，按既有 Review Gate、Readiness Gate 和 Scope 规则继续。
- 已存在 Sprint 追加或修正正式范围时，MUST 先用 `python scripts/add-sprint-scope-item.py --sprint <sprint-id> [--req <REQ-id>|--bug <BUG-id>] [--change <change-id>] ...` 更新 `sprint.yaml` 机器事实源，再运行 Workflow Sync 派生刷新人读文档；不得只手工编辑 `sprint.md`、Issue trace 或 Change trace。
- 已评审但尚未创建 Change 的 REQ/BUG MAY 先通过 `/sprint-propose` 纳入正式 Sprint 范围；此时 `sprint.yaml` MUST 记录对应 `requirements[]` 或 `bugs[]`，并在输出中提示后续 `/req-opsx` 或 `/bug-opsx`。创建 Change 后，Workflow Sync MUST 将 Change 回填到同一 Sprint 的 `changes[]` 与 `scope_estimates[].change`。
- 多个范围项写入同一 `sprint.yaml` 时，MUST 串行执行 `scripts/add-sprint-scope-item.py`。禁止通过并行工具同时追加多个 REQ/BUG/Change 到同一个 Sprint；并发写入可能导致 YAML 旧内容覆盖、重复键或无效 UTF-8 残留。
- `/sprint-propose` 写入或更新范围后，MUST 在 Workflow Sync 成功后运行 `python scripts/validate-sprint-scope.py <sprint-id> [--item <REQ|BUG|change-id>]`，确认新增或更新项同时出现在 `sprint.md` `## 1. 目标` 的 Sprint 目标编号列表、`## 2. Scope` 主表和派生表；该校验失败时必须修复后重跑，不得仅以 `sprint.yaml`、trace 或 Scope 表一致作为完成依据。
- `sprint.md` `## 2. Scope` 主表 MUST 与既有 Sprint 规范保持六列：`类型 | 编号 | 标题 | 状态 | 估算 | 说明`。派生表可按 requirements / bugs / changes 分组，但主表不得用 `范围项` 窄表替代。

## 3.2 opsx-apply 迭代纳入门禁（MUST）

`/opsx-apply <change-id>` 执行前，目标 Change **MUST** 已纳入某个 `sprint-xxx` 正式范围。该规则适用于所有 Change，包括来源于 REQ/BUG 的 Change，以及通过 `/opsx-propose`、`/spec-opt` 或其他治理流程直接创建的非 REQ/BUG Change。

通用门禁：

- `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]` MUST 包含 `<change-id>`。
- `python scripts/sync-workflow-status.py --event opsx.apply --change <change-id> --sprint auto --dry-run` 或等价解析 MUST 能定位到该 Sprint；若报告 sprint skipped / unresolved，MUST 停止 `/opsx-apply`。
- 对非 REQ/BUG Change，`scope_estimates[]` SHOULD 以该 Change 作为独立范围项记录 `change`、估算和纳入理由；不得因无 REQ/BUG 来源而豁免 Sprint Inclusion Gate。

REQ/BUG 关联 Change 的附加门禁：

- 若 Change 关联 REQ，`requirements[]` MUST 包含对应 `REQ-*`；若关联 BUG，`bugs[]` MUST 包含对应 `BUG-*`。
- 关联 REQ/BUG `trace.md` MUST 存在 `iteration: sprint-xxx`，且状态为 `in_sprint` 或后续交付态。
- 若 REQ/BUG 已在 Sprint 中但创建 Change 时 `changes[]` 尚未回填，MUST 先运行对应 `/req-opsx` 或 `/bug-opsx` 的 Workflow Sync，确保 `changes[]` 与 `scope_estimates[].change` 同步后再 apply。
- 若 `/sprint-propose` 声称已纳入 REQ/BUG/Change，但 `/opsx-apply --dry-run` 仍报告 `change <id> not in sprint scope`，根因优先按 `sprint.yaml` 机器事实源缺失处理：重新运行 `scripts/add-sprint-scope-item.py` 或修正其输入，然后再 Workflow Sync 与 scope 校验；不得要求用户重复口头确认同一纳入动作。
- `/req-opsx`、`/bug-opsx`、`/opsx-apply`、`/opsx-archive` 后，Workflow Sync MUST 同步刷新 `sprint.md` 的 `## 2. Scope` 主表状态与说明；当 Change archived 时，对应 REQ/BUG 行 MUST 显示 `done` 与归档 Change，不得继续显示 `approved`、`in_sprint` 或“待创建 Change”。

未通过时的修复路径：对 REQ/BUG Change，先运行 `/sprint-propose` 将 REQ/BUG 纳入 `iterations/change/<sprint>/`，再运行对应 `/req-opsx` 或 `/bug-opsx` 创建/回填 Change；对非 REQ/BUG Change，先运行 `/sprint-propose` 或 `python scripts/add-sprint-scope-item.py --sprint <sprint-id> --change <change-id> ...` 将 Change 写入 Sprint scope。完成 Workflow Sync 和 scope 校验后再重新执行 `/opsx-apply`。

## 4. 目录迁移时机（MUST）

AI 在执行下列命令并成功后 **MUST** 移动目录（`git mv` 或等价），并更新 `sprint.yaml` 的 `lifecycle_stage`：

| 事件 | 命令示例 | 自 → 至 |
|---|---|---|
| 新建 Sprint | `/sprint-propose` | — → `change/` |
| 迭代归档闭环 | `/sprint-archive`（`status: completed`） | `change/` → `archive/` |

**不迁移**：

- 仅 `/sprint-explore`、`/sprint-apply` 进行中 → 保留在 `change/`
- 单 Change `/opsx-archive` → Sprint 目录 **不** 单独迁移（整 Sprint 归档时一并迁移）

迁移后 **SHOULD** 运行 `python scripts/sync-workflow-status.py --check`。

## 5. sprint.yaml 字段

阶段目录变更时，在 `sprint.yaml` 中维护：

```yaml
lifecycle_stage: change | archive
```

`status` 与 `lifecycle_stage` **SHOULD** 一致：

- `planning` / `in_progress` → `change`
- `completed` → `archive`

`sprint.md` 的变更记录 **SHOULD** 记录迁移，例如：`change → archive（/sprint-archive）`。

## 6. 路径引用

- 文档与脚本引用时使用完整路径，例如：  
  `iterations/change/sprint-003/` 或 `iterations/archive/sprint-002/`
- Workflow Sync、Sprint 命令 **MUST** 通过 `resolve_sprint_dir()` 解析路径，**禁止** 硬编码仅根目录扁平路径。

## 7. 与 issues / OpenSpec 关系

| 层级 | 职责 |
|---|---|
| `iterations/change/` | 当前或规划中的 Sprint 四件套 |
| `iterations/archive/` | 已结束 Sprint 四件套（历史保留） |
| `issues/*/review/` | 已评审、开发中 REQ/BUG |
| `openspec/changes/` | 进行中的 Change |
| `openspec/archive/` | 已归档 Change |
| `openspec/changes/archive/` | 禁止真实存在；仅 legacy 引用扫描或迁移测试可出现该字符串 |

Sprint 归档 **MUST** 在 `/sprint-archive` 时同步：Change → `openspec/archive/`，关联 REQ/BUG → `issues/*/archive/`（若尚未迁入）。
`/sprint-archive` 完成前 MUST 通过 `python scripts/validate-directory-structure.py`，确保没有真实 `openspec/changes/archive/` 目录残留。

Sprint close / `/sprint-archive` 前 MUST 通过 `python scripts/validate-sprint-archive-readiness.py --sprint <sprint-id>`。该 readiness gate 会同时执行 Sprint close stale scan，阻断四件套中与真实 Issue/Change 生命周期冲突的中间态文案和旧归档路径 `openspec/changes/archive/` canonical 引用。单独排查 stale 文案时 MAY 运行 `python scripts/check-sprint-close-stale-scan.py --sprint <sprint-id>`。

## 8. AI 检查清单

```text
□ 新建 Sprint 是否落在 change/ ？
□ sprint-archive 后是否迁入 archive/ ？
□ sprint.yaml 是否更新 lifecycle_stage ？
□ 路径引用是否使用 change/ 或 archive/ 前缀？
□ 是否确认没有 openspec/changes/archive/ 真实目录？
□ 是否运行 Sprint close stale scan / archive readiness，确认四件套无过期中间态文案？
□ 是否运行 sync-workflow-status.py --check ？
```
