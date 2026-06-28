---
name: /sprint-propose
id: sprint-propose
category: Workflow
description: 提议并创建新 Sprint 迭代规划（四件套），类似 /opsx-propose 面向整迭代
---

根据当前项目中的需求（Requirement）、缺陷（Bug）和 OpenSpec Change，**提议并创建**新的 Sprint（迭代）规划。与 `/opsx-propose` 对标：单 Change 用 opsx，**整迭代**用 sprint。

**Input**：

- `sprint-003` — 指定 Sprint ID（推荐）
- 或自然语言描述本迭代目标（如「下一 Sprint 做品牌+类目+登录增强」），由 Agent 推导 `sprint-xxx` 编号

可选 flags：

| Flag | 含义 |
|------|------|
| `--req REQ-xxxx,...` | 仅纳入列出的需求 |
| `--change add-*,...` | 仅纳入列出的 Change |
| `--duration 2w` | 迭代周期（默认 2 周） |
| `--dry-run` | 只输出提议范围与估算，不写文件 |

**Output**：`iterations/change/sprint-xxx/` 四件套 + 各 REQ/BUG/Change trace 更新 + 提示下一步 `/sprint-explore` 或 `/sprint-apply`。

---

## 前置关系

```text
issues/requirements/** 、issues/bugs/** 、openspec/changes/**
        │
        ▼
/sprint-propose [sprint-xxx]     ← 本文：创建迭代规划
        │
        ├─ /sprint-explore         ← 范围/依赖/容量探讨（可选）
        ├─ /req-opsx / /bug-opsx       ← 缺 Change 时补建
        ├─ /sprint-apply           ← 开发
        └─ /sprint-archive         ← 迭代结束批量归档
```

---

## Step 0 — 必须读取

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/directory-structure.md
rules/iterations-lifecycle.md
docs/knowledge-base/README.md
```

扫描范围：

```text
project.yaml                    # 若存在：团队容量
issues/requirements/**
issues/bugs/**
openspec/changes/**             # 含 archive/
openspec list --json
iterations/change/**            # 进行中 Sprint
iterations/archive/**           # 已归档 Sprint（编号冲突扫描）
docs/knowledge-base/retrospectives/   # 最近 1~2 个已归档 Sprint 复盘
docs/knowledge-base/best-practices/   # 横切预防清单（若存在）
```

### Step 0.1 — 知识库读库（MUST）

1. 取 `iterations/archive/` 中编号最大的 Sprint → 读取对应 `docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md`。
2. 若存在更早一期复盘，**SHOULD** 一并读取（最多 2 份），用于识别跨 Sprint 复发模式。
3. 提取上一 Sprint **§6 行动项** 中 `status: open` 的条目；输出 **Knowledge Intake Report**（表格：ID / 优先级 / 描述 / 本 Sprint 承接方式）。
4. 扫描本 Sprint 候选 REQ/BUG 类型，标记需引用的 best-practices：

| 范围特征 | MUST 读取 |
|----------|-----------|
| 含管理端**列表页** add-* / 列表 UI fix | `best-practices/admin-list-page-consistency.md` |
| 含管理端**表单/设置页** add-* | `best-practices/admin-form-page-consistency.md` |
| 含管理端**弹窗** add-* / modal fix | `best-practices/admin-modal-width-css-cascade.md` |
| 含**图片/视频/头像**上传 | `best-practices/admin-media-upload-chain.md` |

5. **无上一 Sprint 复盘**时：仍读取 `best-practices/` 索引；在输出中注明「无复盘承接项」。

---

## Step 1 — 输入与编号

1. 若无 Sprint ID：扫描 `iterations/change/` 与 `iterations/archive/` 取最大编号 +1 → `sprint-xxx`。
2. 若 `iterations/change/sprint-xxx/` 或 `iterations/archive/sprint-xxx/` 已存在：询问 **继续填充** 还是 **换编号**。
3. 若用户给自然语言目标：列出候选 REQ/BUG/Change，用 **AskUserQuestion** 确认纳入范围。

---

## Step 2 — 纳入前检查

### 评审门禁（MUST — 无例外）

纳入 Sprint **正式规划** 或执行开发前，REQ/BUG **MUST** 已完成评审：

```text
issues/requirements/<REQ>/trace.md  → status ∈ { approved, in_sprint }
issues/bugs/<BUG>/trace.md        → status ∈ { approved, in_sprint }
```

**未评审**（`draft`、`pending_review`、`captured`、`enriching` 等）时 **MUST**：

| 禁止 | 说明 |
|------|------|
| 写入 `sprint.yaml` | 不得加入 `requirements[]` / `bugs[]` |
| 写入 Sprint 目标 / Scope / 里程碑 / 工作量合计 | 不得出现在 `sprint.md` 正式范围 |
| 写入 release / acceptance 关联范围 | 四件套正式条目 |
| 更新 `trace.md` `iteration` | 不得设为 sprint-xxx |
| `/req-opsx` / `/bug-opsx` / `/sprint-apply` | 不得执行 |

**允许**：仅记入 `sprint.md` §「延后项（待评审）」+ 提示 `/req-review` 或 `/bug-review --approve`。

用户显式要求「纳入 sprint-xxx」时也 **MUST** 先拒绝写入规划；**无**「历史回填 WARN 仍写入 yaml」例外。

若发现既有 Sprint 已含未评审项：**输出 WARN**，将其移出 `sprint.yaml` 与正式 Scope，改入延后项，并提示补评审。

**优先级**：P0 BUG > P0 REQ > P1 …

### Requirement（文档条件）

```text
requirement.md、acceptance.md、trace.md 已存在
status: approved（见上节门禁）
```

**Not Ready** → 不纳入 `sprint.yaml`，写入 sprint.md「延后项」并建议 `/req-complete`。

### Bug

```text
bug.md、root-cause.md、acceptance.md 已存在
状态：Open | Ready
```

### OpenSpec Change

```text
openspec/changes/<id>/ 存在且含 proposal、design、tasks
或用户确认先纳入 REQ，Change 待 `/req-opsx`
```

已 **archive** 的 change **不得**纳入新 Sprint（除非 fix-* 续作，须新建 change）。

---

## Step 3 — 容量与工作量

读取 `project.yaml`（若不存在则默认）：

```yaml
capacity:
  developers: 2
  testers: 1
duration: 2周
```

估算标准（与历史 sprint 一致）：

```text
XS=0.5  S=1  M=3  L=5  XL=8  XXL=13 人天
```

按前端 / 后端 / 测试分列；汇总 `estimated_story_points` 与 `estimated_person_days`。

### 知识库容量门禁（MUST — 来自 Sprint 002/003 复盘）

| 规则 | 阈值 | 超限时 MUST |
|------|------|-------------|
| **add-* 主能力数** | ≤ **6** | 在 `sprint.md` §风险标注；余项移入「延后项」或下一 Sprint |
| **fix 缓冲** | 预留 **≥30%** SP/人天 | 在估算表单独列出 `fix_buffer` 行，不得全部塞满 add-* |
| **UI 横切复发风险** | 每新增 1 个管理端列表/表单/弹窗 add-* | 在 §横切预防清单 增加对应 best-practices 链接 + 1 条风险 |

若上一 Sprint 复盘行动项含 **A-006（容量）** 等 open 项，本 Sprint **MUST** 在 §知识库承接 写明是否采纳及偏差理由。

---

## Step 4 — 优先级、依赖与归组

**优先级**：P0 BUG → P0 REQ → P1 REQ → P2 …

**依赖**（MUST 写入 `sprint.md` §依赖 ASCII 树）：

- 从 requirement 父子关系、change proposal、Admin Shell 等基座推导
- fix-* **MUST** 挂在对应 add-* 之下

**归组**：同一业务域（如 Tile Management）尽量同一 Sprint。

---

## Step 5 — 创建四件套（`--dry-run` 跳过）

目录：

```text
iterations/change/sprint-xxx/
├── sprint.yaml          # MUST 机器可读事实源
├── sprint.md            # 人类可读展开
├── release-note.md      # 发布说明初稿
└── acceptance-report.md # 验收报告模板
```

### sprint.yaml（MUST）

```yaml
sprint_id: sprint-xxx
status: planning          # 启动开发后改为 in_progress
lifecycle_stage: change   # 归档后改为 archive 并迁入 iterations/archive/
start_date: YYYY-MM-DD HH:mm:ss
end_date: YYYY-MM-DD HH:mm:ss

capacity:
  developers: <int>
  testers: <int>

requirements: []          # issues/requirements 目录名
bugs: []
changes: []               # openspec change id

estimated_story_points: <int>
estimated_person_days: <number>
```

### sprint.md（MUST 含）

- Sprint 目标（**MUST** 覆盖 `sprint.yaml` 中全部 `requirements` / `bugs`：**编号列表** + 各 `### REQ/BUG-xxxx 要点` 小节，含严重等级/现象/根因/修复范围/OpenSpec 状态）
- Scope 表（REQ / BUG / Change + 优先级 + 状态；Scope archived 时间戳 MUST `YYYY-MM-DD HH:mm:ss`，由 workflow-sync 维护）
- 工作量估算表（含 **fix 缓冲** 行，若适用）
- 里程碑（「目标日期」列 MUST `YYYY-MM-DD HH:mm:ss`）
- 风险
- **§知识库承接**（MUST）：上一 Sprint open 行动项表格 + 本 Sprint 承接/延后/拒绝及理由
- **§横切预防清单**（MUST）：本 Sprint 涉及的 `docs/knowledge-base/best-practices/*.md` 链接 + 各文档验收 gate 摘要（checkbox 列表，供 apply 前对照）
- **依赖** ASCII 树
- 发布计划
- 关联文档链接（含 knowledge-base 复盘与 best-practices）

### release-note.md / acceptance-report.md

按 `rules/document-governance.md` §4.1 模板生成初稿。四件套 Markdown **MUST** 含 Frontmatter 字段 `created_at`、`updated_at`（`YYYY-MM-DD HH:mm:ss`）；后续任意修改只更新 `updated_at`。

---

## Step 6 — 更新 Trace

对纳入的每项更新：

```text
issues/requirements/*/trace.md   → iteration: sprint-xxx
issues/bugs/*/trace.md
openspec/changes/*/trace.md      # 若 change 已存在
```

---

## Step 7 — 输出

```text
## Sprint Propose 完成

**Sprint:** sprint-xxx
**Status:** planning
**Requirements:** N
**Changes:** M
**Estimated:** XX SP / YY 人天（含 fix 缓冲 ZZ SP）

**Knowledge Intake:**
- 上一 Sprint 复盘：<sprint-id> | open 行动项：K 条 | 本 Sprint 承接：J 条
- 引用 best-practices：<文件列表>

**Capacity Gate:**
- add-* 数量：A / 6 | fix 缓冲：B% | 超容量风险：是/否

**Artifacts:**
- [x] sprint.yaml
- [x] sprint.md（含 §知识库承接、§横切预防清单）
- [x] release-note.md
- [x] acceptance-report.md

**Next:**
1. `/sprint-explore sprint-xxx` — 探讨依赖/容量/风险（可选）
2. 缺 Change 的 REQ → `/req-opsx REQ-xxxx`（须 approved）；add-* design/tasks MUST 引用 §横切预防清单
3. `/sprint-apply sprint-xxx --dry-run` — 查看开发队列
4. `/sprint-apply sprint-xxx` — 开始开发
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 四件套缺一不可 | 不得只写 sprint.md |
| 不得绕过 OpenSpec | 新能力须先 REQ + Change，再纳入 sprint |
| 编号唯一 | 不覆盖已有 sprint 目录（除非用户确认续写） |
| 容量透明 | 超容量须在 sprint.md 风险表标注 |
| 不得绕过评审门禁 | 未 approved/in_sprint 的 REQ/BUG 不得写入 Sprint 规划或 trace.iteration |
| 知识库必读 | 不得跳过 Step 0.1；无复盘时须在输出注明 |
| 容量门禁 | add-* >6 或 fix 缓冲 <30% 须在风险表显式 WARN，不得静默忽略 |
| 不写 src | 本命令只建迭代文档，实现用 `/sprint-apply` |

---

## 参考

- 原 `create-iteration` 逻辑已合并至本文
- Sprint 治理：`rules/document-governance.md` §4.1
- 知识库：`docs/knowledge-base/README.md`；复盘由 `/sprint-exps` 写入
- 单 Change 提议：`/opsx-propose`
- 开发编排：`/sprint-apply`
- 批量归档：`/sprint-archive`
- 需求横切 AC：`/req-complete`（best-practices checklist）

---

## Final Step — Workflow Sync (MUST)

Read `.agents/skills/workflow-sync/SKILL.md` and run:

```bash
python scripts/sync-workflow-status.py --event sprint.propose --sprint <sprint-id>
```

- Exit code **MUST** be `0` before ending this command.
- Print the **Workflow Sync Report** to the user.
- Do **not** hand-edit `sprint.md` Scope marker blocks (`<!-- workflow-sync:* -->`).
