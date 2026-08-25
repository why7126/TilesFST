---
purpose: 缺陷（BUG）生命周期、状态机、目录与评审门禁
source: 项目团队 + AI v2 定稿
update_method: 命令族变更时同步更新
updated_at: 2026-08-24 16:35:51
---

# 缺陷管理规范

## 1. 目录

```text
issues/bugs/
├── _registry.yaml
├── README.md
├── plan/                      # 规划中并完成评审
│   └── BUG-NNNN-slug/
├── review/                    # 已评审通过，修复/验收中，未 OpenSpec archive
│   └── BUG-NNNN-slug/
├── archive/                   # 已修复并归档
│   └── BUG-NNNN-slug/
└── BUG-NNNN-slug/             # [遗留] 扁平路径，deprecated；勿新建
```

单条 BUG 目录内文件：

```text
BUG-NNNN-slug/
├── capture.md
├── bug.md
├── root-cause.md
├── workaround.md
├── acceptance.md
├── trace.md
├── review.md
├── logs/
└── screenshots/
```

**新建 MUST** 使用 `issues/bugs/plan/BUG-NNNN-slug/`。阶段含义、迁移时机见 `rules/issues-lifecycle.md`。

禁止在 `docs/bugs/` 存放缺陷记录。

## 2. 状态机

| status | 含义 |
|--------|------|
| `captured` | 已记录 |
| `exploring` | 复现/影响分析中 |
| `draft` | 仅有 bug.md |
| `enriching` | 缺陷包补齐中 |
| `pending_review` | 待评审 |
| `approved` | **确认修复**（推荐先 `/sprint-propose`，再 `/bug-opsx`） |
| `rejected` | 非缺陷/误报 |
| `wont_fix` | 不修 |
| `deferred` | 延后 |
| `in_sprint` | 已纳入迭代 |
| `done` | 已修复验收 |

**事实源**：`trace.md` 的 `status`；`bug.md` frontmatter **MUST** 通过 Workflow Sync 同步。`acceptance.md` MUST 使用 `acceptance_status` 或 `## 验收结果回填` 表达验收结论，避免与 BUG 主状态混淆。

## 3. 命令与阶段

| 命令 | 产出 |
|------|------|
| `/capture` | 类型未决时自动分类；BUG 部分同 `/bug-capture`（见 §3.2） |
| `/bug-capture` | capture.md、trace 壳（可一次输入多条，按 §3.1 评估拆分） |

### 3.2 `/capture` 与 bug-capture

用户不确定输入是需求还是缺陷时使用 `/capture`。AI **MUST** 先分类再落盘：判为缺陷的条目遵循 §3.1 拆分规则，产出与 `/bug-capture` 相同，且 frontmatter 含 `captured_via: capture`、`classification_rationale`。一条消息可同时产生 REQ 与 BUG。

### 3.1 `/bug-capture` 多条输入与拆分

用户可能在一条消息中描述多个缺陷。AI **MUST** 先评估再落盘：

- **拆分**：不同界面/层级、缺陷类型、修复面、严重度、交付优先级，或用户显式并列枚举 → 每条独立 `BUG-NNNN-slug/`。
- **合并**：同一页面/弹窗且一次修复可闭环，或同一根因不可分割 → 单条 BUG；回复中一句话说明不拆理由。
- **禁止** umbrella BUG（总记录 + 子 bullet）；每条 MUST 可独立走 explore → opsx → archive。
- 创建多条时，`next_id` 连续递增；Workflow Sync 对**每条**执行 `bug.capture`。
| `/bug-explore` | 默认无文件 |
| `/bug-generate` | bug.md |
| `/bug-complete` | root-cause、workaround、acceptance、trace |
| `/bug-review` | review.md、status；无 flag 默认 approved |
| `/sprint-propose` | iterations/change/sprint-* |
| `/bug-opsx` | openspec/changes/fix-* |

## 4. 门禁

### 4.1 评审门禁（统一，MUST）

与 `rules/requirement-management.md` §4.1 一致。BUG `trace.md` `status ∈ { approved, in_sprint }` 后方可：

- 纳入 Sprint 规划（评审后优先：`/sprint-propose`）
- 创建或回填修复 Change（Sprint 后：`/bug-opsx`）
- `/sprint-apply`

`/bug-review BUG-xxxx` 无 flag 时默认评审通过并进入 `approved`；拒绝、延后或不修复必须显式使用 `--reject`、`--defer` 或 `--wont-fix`。

默认 approve 或显式 `--approve` 前，目标 BUG `root-cause.md` MUST 满足 `root_cause_status: confirmed` 且 confirmed 根因具备可定位证据链。若 `root_cause_status` 为 `unknown`、`hypothesis`、`probable`，或缺少 `root-cause.md` / `root_cause_status`，`/bug-review` MUST 阻断 approve，并提示先 `/bug-complete <BUG-id>` 补齐证据或改用 `--defer`、`--reject`、`--wont-fix`。

未评审 BUG **不得**写入 Sprint 四件套正式范围；仅可记入 `sprint.md`「延后项（待评审）」并提示 `/bug-review BUG-xxxx`。

### 4.2 opsx-apply 迭代纳入门禁（统一，MUST）

来源于 BUG 的 OpenSpec Change 在 `/opsx-apply` 前 **MUST** 已正式纳入某个 `sprint-xxx`：

- BUG `trace.md` MUST 满足 `status: in_sprint`（或后续交付态）且 `iteration: sprint-xxx` 非空。
- 对应 `iterations/change|archive/<sprint>/sprint.yaml` MUST 在 `bugs[]` 与 `changes[]` 中包含该 BUG 与 Change。
- 若 BUG 先进入 Sprint、后执行 `/bug-opsx` 创建 Change，Workflow Sync MUST 将新 Change 回填到该 Sprint 的 `changes[]` 与对应 `scope_estimates[].change`；仅有 BUG 在 `bugs[]` 不足以通过 `/opsx-apply` 门禁。
- `/opsx-apply` MUST 先用 `--sprint auto` 或等价检查确认能解析到 Sprint；解析失败时必须停止，提示先执行 `/sprint-propose`。

`approved` 只表示已评审通过；推荐下一步是先 `/sprint-propose` 进入 Sprint 规划，再 `/bug-opsx` 创建 Change 并回填 Sprint scope。不得仅凭 `approved` 直接 `/opsx-apply`。

BUG 来源链路的下一步命令参数 MUST 始终使用原始 `BUG-*`。`/bug-opsx` 创建或确认 linked Change 后，后续 `/opsx-apply` 与 `/opsx-archive` 的可执行下一步必须写成 `/opsx-apply <BUG-id>`、`/opsx-archive <BUG-id>`；内部再由对应 opsx 命令解析到真实 `<change-id>`。

### 4.3 其他门禁

- `/bug-opsx`：推荐入口为已评审后的 `in_sprint`；兼容 `approved` 的追溯/补建 Change 场景，但输出 MUST 提醒若尚未纳入 Sprint，应先 `/sprint-propose`
- Sprint：**P0 BUG** 优先于功能 REQ
- 旧命令 `/bug-to-change` 已删除 → `/bug-opsx`

## 5. 严重等级

```text
blocker | critical | high | medium | low
```

## 6. 知识沉淀

修复后若有复用价值，可更新 `docs/knowledge-base/incidents/`（由 bug-opsx tasks 提醒）。

## 7. 父需求反向追溯

BUG 的 `related_requirement` 不只是单向引用。若 `related_requirement` 非空，AI 在以下阶段 MUST 同步更新父需求 `issues/requirements/<REQ-ID>/trace.md` 的 `## 关联缺陷` 索引表：

- `/bug-complete` 或 `/bug-review` 确认父需求后。
- `/bug-opsx` 创建或确认修复 Change 后。
- BUG 纳入 Sprint、完成 `/opsx-apply`、完成 `/opsx-archive` 或状态变化后。

父需求 trace 中只记录索引级信息：`BUG`、`严重等级`、`状态`、`关联 Change`、`说明`。MUST NOT 在需求 trace 中复制 BUG 复现步骤、根因全文、日志或截图。

`trace.md` 的 `lifecycle` 与 `## 变更记录` 中所有时间记录 MUST 遵守 `rules/document-governance.md` §2.3（`YYYY-MM-DD HH:mm:ss`）。

Frontmatter **MUST** 含 `created_at`、`updated_at`；更新 trace 时刷新 `updated_at`，不得修改 `created_at`。

状态变更后 MUST 运行 `python scripts/sync-workflow-status.py`（见 `rules/document-governance.md` §6.1 与 `.agents/skills/workflow-sync/SKILL.md`）。

状态变化事件（`bug.generate`、`bug.review`、`bug.opsx`、`opsx.apply`、`opsx.archive`、`sprint.archive`）后，Workflow Sync MUST 检查 BUG 顶层子文档：`bug.md` 同步当前主状态；`acceptance.md` 回填 `acceptance_status`、source Change/Sprint、证据入口和失败项结构；`root-cause.md`、`workaround.md`、`review.md` 若状态字段语义不明，应报告 warning/blocker，归档前不得残留未解释的非闭环状态。

BUG `root-cause.md` MUST 遵守 `rules/root-cause-evidence.md`：根因状态区分 `unknown`、`hypothesis`、`probable`、`confirmed`；confirmed 必须记录可定位证据链，证据不足时必须写明人工补证步骤，不得把推测表述为已确认根因。

## 8. 参考命令

`.agents/skills/bug-*/SKILL.md`
