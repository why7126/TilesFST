---
name: "Sprint: Exps"
description: Sprint 经验复盘 - 总结整迭代流程、需求、开发与质量经验，沉淀到 docs/knowledge-base
category: Workflow
tags: [workflow]
---

对指定 Sprint 进行**整迭代经验复盘**，从流程、需求设计、开发质量、可复用抽象等维度提炼可行动结论，并写入 `docs/knowledge-base/`。**不写业务代码**，不修改 `src/`。

与 `/sprint-explore` 对标：`sprint-explore` 用于**迭代前/中**探讨范围与风险；`sprint-exps` 用于**迭代末/归档后**总结经验并沉淀知识。

**推荐时机**：`/sprint-archive` 完成后，或 Sprint 主体开发结束、验收报告基本齐备时。

---

**Input**：

- `sprint-002` — 必填；或可推断唯一 `in_progress` / 最近 `completed` Sprint
- 自然语言补充：「重点看 UI 类 BUG 重复问题」「流程上 req-review 是否太晚」

可选 flags：

| Flag | 含义 |
|------|------|
| `--dry-run` | 只输出 Experience Analysis Report，不写 knowledge-base |
| `--focus process\|req\|dev\|reuse\|quality` | 聚焦某一维度（默认全维度） |
| `--skip-best-practices` | 不生成/更新 `best-practices/` 横切条目 |
| `--include-deferred` | 纳入 sprint.md「延后项（待评审）」一并分析 |

**Output**：

1. **Experience Analysis Report**（回复用户）
2. `docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md`（主复盘文档）
3. 必要时追加 `docs/knowledge-base/best-practices/*.md` 或 `incidents/*.md`
4. 更新 `docs/knowledge-base/README.md` 索引
5. 在 `iterations/<sprint-id>/sprint.md` 追加「经验复盘」链接（若该节不存在则创建）

**禁止**：修改 `src/`、勾选 change `tasks.md`、执行 apply/archive、直接改 `rules/`（仅 **建议** 规则变更并列入行动项）。

---

## Step 0 — 必须读取

```text
AGENTS.md
rules/document-governance.md
rules/requirement-management.md
rules/bug-management.md
rules/ui-design.md          # UI 类 BUG 聚类时
docs/knowledge-base/README.md
```

```text
iterations/<sprint-id>/sprint.yaml
iterations/<sprint-id>/sprint.md
iterations/<sprint-id>/acceptance-report.md
iterations/<sprint-id>/release-note.md
```

对 `sprint.yaml` 中每个 `requirements[]`、`bugs[]`、`changes[]`：

```text
issues/requirements/REQ-xxxx/trace.md
issues/requirements/REQ-xxxx/review.md
issues/requirements/REQ-xxxx/acceptance.md     # 若存在
issues/requirements/REQ-xxxx/requirement.md  # 若存在
issues/bugs/BUG-xxxx/trace.md
issues/bugs/BUG-xxxx/root-cause.md           # 若存在
issues/bugs/BUG-xxxx/review.md               # 若存在
openspec/changes/<change-id>/tasks.md        # 或 archive 下对应目录
openspec/changes/archive/*/trace.md          # 已归档 change
```

```bash
openspec list --json
```

---

## Step 1 — 构建 Sprint 事实基线（MUST）

汇总只读数据，形成 **Sprint Fact Sheet**（内部分析用，写入复盘文档 §概况）：

| 维度 | 采集项 |
|------|--------|
| 范围 | REQ/BUG/Change 数量、完成/归档比例、延后项 |
| 容量 | `estimated_story_points`、`estimated_person_days` vs 实际体感（从 trace 时间戳推断） |
| 流程 | 各 REQ/BUG lifecycle 时间线：capture → review → opsx → apply → archive |
| 质量 | BUG 按类型/模块/严重度聚类；fix-* 与 add-* 比例 |
| 文档 | 缺 prototype/acceptance、review 滞后、opsx 前文档不全的 REQ |
| 技术债 | tasks 遗留 `- [ ]`、acceptance-report pending、已知 workaround |

**Experience Analysis Report** 须先输出此 Fact Sheet 摘要表。

---

## Step 2 — 多维度经验分析（MUST）

按下列维度逐项分析；无证据的推断 MUST 标 **待确认**，不得编造。

### 2.1 迭代流程（Process）

| 检查点 | 示例问题 |
|--------|----------|
| 规划合理性 | 容量是否过载？并行 change 是否导致 archive 顺序问题？ |
| 门禁有效性 | 未评审项是否误入 Sprint？review 是否过晚导致返工？ |
| 命令链顺畅度 | capture → opsx → apply → archive 哪段卡点最多？ |
| 依赖与顺序 | fix-* 是否因父 add-* 未 archive 阻塞？ |
| workflow-sync | 文档漂移是否曾发生？ |
| 优化建议 | 下一 Sprint 应调整的 propose/apply/archive 策略 |

### 2.2 需求与设计（Requirements & Design）

| 检查点 | 示例问题 |
|--------|----------|
| PRD 质量 | requirement.md 是否过粗导致开发期大量 fix-*？ |
| 原型优先级 | 缺 HTML/PNG 是否引发 UI 类 BUG 集群？ |
| acceptance 可测性 | AC 是否可自动化？是否过晚补齐？ |
| 拆分粒度 | REQ 是否过大/过小？parent_requirement 使用是否合理？ |
| 评审深度 | review.md 是否捕获了后续 BUG 本可预见的问题？ |
| 文档模板 | capture/complete 哪些字段应前置必填？ |

### 2.3 开发与质量（Development & Quality）

| 检查点 | 示例问题 |
|--------|----------|
| 重复 BUG 模式 | 同类 UI 不一致（列表分页、弹窗副标题、overflow）如何避免？ |
| 根因聚类 | MinIO/上传/登录重启类是否应上升为 incident 或 best-practice？ |
| 测试覆盖 | 哪些 BUG 本可被 vitest/pytest/E2E 拦截？ |
| OpenSpec tasks | tasks 是否缺 PNG 并排、Orval、Docker 验证等 recurring 项？ |
| 归档质量 | delta spec MODIFIED 标题冲突、trace 未更新等 |

### 2.4 可复用抽象（Reuse & Components）

| 检查点 | 示例问题 |
|--------|----------|
| 页面模板 | 多个管理端列表是否应对齐 `AdminListPage`？ |
| 复合组件 | 弹窗、上传、分页是否应提取 shared 组件？ |
| Design System | 重复 fix 是否说明 DS 缺组件或验收页未覆盖？ |
| API/后端模式 | CRUD、启停、软删是否可抽象基类或代码生成？ |
| 文档/命令 | 是否应新增 checklist 或扩展 `rules/`（仅建议，不直接改） |

---

## Step 3 — 聚类与优先级（MUST）

将发现归类：

| 类型 | 处置 |
|------|------|
| **Sprint 特有问题** | 写入 `retrospectives/<sprint-id>-retrospective.md` |
| **跨 Sprint 可复用** | 写入或更新 `best-practices/<topic>.md` |
| **生产/环境事故级** | 评估 `incidents/<topic>.md`（与 bug-opsx 沉淀标准一致） |
| **流程/规范变更** | 列入行动项，建议走 REQ 或团队确认后改 `rules/` |
| **组件/技术债** | 列入行动项，建议 `/req-capture` 或 `/bug-capture` |

行动项 MUST 含：**优先级**（P0/P1/P2）、**负责人建议**、**下一命令**（如 `/req-capture`、`/build-design-system`）。

---

## Step 4 — 写入 knowledge-base（除非 `--dry-run`）

### 4.1 主文档：`retrospectives/<sprint-id>-retrospective.md`

```markdown
---
sprint_id: sprint-002
title: Sprint 002 迭代经验复盘
status: draft
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
owner: product
related_iteration: iterations/sprint-002/
related_requirements:
  - REQ-xxxx
related_bugs:
  - BUG-xxxx
related_changes:
  - add-xxx
source: /sprint-exps
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 002 迭代经验复盘

## 1. 迭代概况
（Fact Sheet：范围、完成度、容量、时间线）

## 2. 流程复盘
（§2.1 结论：做得好的 / 问题 / 优化建议）

## 3. 需求与设计
（§2.2 结论）

## 4. 开发与质量
（§2.3 结论；重复 BUG 表）

## 5. 可复用抽象
（§2.4 结论；组件/模板建议表）

## 6. 行动项
| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| A-001 | P1 | … | /req-capture … | open |

## 7. 知识库沉淀清单
| 文件 | 操作 | 说明 |
|------|------|------|
| best-practices/admin-list-consistency.md | 新建 | UI 列表对齐 |

## 8. 变更记录
| 时间 | 说明 |
|------|------|
| YYYY-MM-DD HH:mm:ss | 初稿（/sprint-exps） |
```

若文件已存在：**追加** §8 变更记录，更新 `updated_at`，合并新行动项（不删除人工编辑内容）。

### 4.2 横切 best-practices / incidents

- 仅当结论**跨 Sprint 可复用**且复盘文档 §7 已列出时创建/更新
- 遵循既有 frontmatter 与时间格式（`rules/document-governance.md` §2.3–§2.4）
- **不得**与 `issues/bugs/` 重复整份 BUG 文档；知识库写**模式与预防**，BUG 目录写**个案**

### 4.3 更新索引

`docs/knowledge-base/README.md` 的目录说明中 MUST 包含 `retrospectives/`，并追加本 Sprint 复盘链接。

### 4.4 回链迭代文档

在 `iterations/<sprint-id>/sprint.md` 末尾（或 §经验复盘）追加：

```markdown
## 经验复盘

- 文档：[`docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md`](../../docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md)
- 生成：YYYY-MM-DD HH:mm:ss（/sprint-exps）
```

---

## Step 5 — 输出 Experience Analysis Report（MUST）

```markdown
## Sprint Experience Analysis Report

**Sprint:** sprint-002
**Mode:** exps | dry-run
**Focus:** all | process | …

### Fact Sheet
| 指标 | 值 |
|------|-----|
| REQ | 11（done 10） |
| BUG | 10（done 9） |
| Change archived | 20/21 |
...

### 关键发现（Top 5）
1. …
2. …

### 重复 BUG / 模式
| 模式 | 次数 | 关联 BUG | 预防建议 |
|------|------|----------|----------|

### 可复用抽象机会
| 机会 | 涉及 REQ/页面 | 建议 |
|------|---------------|------|

### 行动项摘要
| ID | P | 描述 | 下一步 |
|----|---|------|--------|

### 已写入 knowledge-base
- retrospectives/sprint-002-retrospective.md
- best-practices/…（若有）

### 建议人工 Review
- [ ] 复盘 status: draft → published
- [ ] 确认行动项负责人与优先级
- [ ] 评估是否创建新 REQ 落实组件抽象
```

---

## Guardrails

| 规则 | 说明 |
|------|------|
| 证据优先 | 结论 MUST 引用 trace、root-cause、tasks、acceptance 等路径 |
| 不编造 | 无数据则标待确认 |
| 不替代 issues | 新需求/缺陷走 `/capture` 或 req/bug-capture，不在复盘里当工单 |
| 不改 rules 自动 | 规则变更仅作行动项建议 |
| 不写 src | 组件抽象只记录建议，实现走 OpenSpec |
| dry-run | `--dry-run` 不得写任何文件 |
| 时间格式 | `YYYY-MM-DD HH:mm:ss`（Asia/Shanghai） |

---

## 与相邻命令的分工

| 命令 | 时机 | 产出 |
|------|------|------|
| `/sprint-explore` | 迭代前/中 | 范围、依赖、风险探讨（可无文件） |
| `/sprint-apply` | 迭代中 | 代码实现 |
| `/sprint-archive` | 迭代末 | Change 归档、Sprint 关闭 |
| **`/sprint-exps`** | **归档后/验收期** | **knowledge-base 经验沉淀** |

推荐链：`/sprint-archive` → **`/sprint-exps`** → 下一 `/sprint-propose` 参考行动项。

---

## 示例

```text
/sprint-exps sprint-002
/sprint-exps sprint-002 --dry-run
/sprint-exps sprint-002 --focus dev
/sprint-exps sprint-002 --focus reuse
```

---

## 参考

- 迭代归档：`.cursor/commands/sprint-archive.md`
- 知识库：`docs/knowledge-base/README.md`
- 文档治理：`rules/document-governance.md` §2.0、§2.1
- BUG incident 沉淀：`rules/bug-management.md`
