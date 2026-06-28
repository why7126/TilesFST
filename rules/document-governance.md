---
purpose: 文档治理规范
content: 规范 docs、issues、iterations、openspec 的生成、更新、同步与归档规则
source: AI自动生成初稿，项目团队确认
update_method: 研发流程变化时由AI辅助更新，人工Review后合并
created_at: 2026-06-13 00:00:00
updated_at: 2026-06-27 08:30:00
note: AI执行任何需求、BUG、技术改造前必须读取；本文件优先级高于普通文档说明
---

# 文档治理规范

## 1. 总原则

本项目采用以下唯一研发链路：

```text
需求 / BUG / 技术改造
↓
issues/
↓
iterations/
↓
openspec/changes/
↓
src/ + tests/
↓
docs/ 同步
↓
openspec/specs/ 合并
↓
openspec/archive/ 归档
```

AI Agent 不允许直接从用户一句话跳到代码实现。除简单拼写、注释、格式化、无行为变化的小修外，均应先判断是否需要创建或更新 OpenSpec Change。

## 2. docs 目录生成与更新逻辑

`docs/` 用于沉淀产品、架构、部署、接口、数据库、兼容性和治理细则。

### 2.0 目录分层（MUST）

```text
docs/
├── 00–07-*.md          # 层 1：主索引文档（有序号，阅读顺序）
├── standards/          # 层 2：治理细则（无序号）
├── knowledge-base/     # 层 3：故障/事故沉淀
└── README.md           # 总导航
```

| 层级 | 命名 | 示例 |
|------|------|------|
| 主文档 | `docs/NN-topic.md` | `03-api-index.md` |
| 治理细则 | `docs/standards/<topic>.md` | `standards/error-codes.md` |
| 知识库 | `docs/knowledge-base/**` | `incidents/*.md` |

- **禁止**在 `docs/` 根目录新增无序号治理 MD（应放入 `standards/`）。
- 需求、BUG、迭代 **不得**放入 `docs/`（见 `issues/`、`iterations/`）。

### 2.1 生成时机

AI 在以下场景必须创建或更新 `docs/`：

| 场景 | 必须更新的文档 |
|---|---|
| 新产品/新模块 | `docs/00-product-overview.md`（需求正文在 `issues/requirements/`） |
| 架构变化 | `docs/01-architecture.md` |
| Docker Compose、环境变量、服务端口变化 | `docs/02-deployment.md` |
| API 新增、删除、参数变化 | `docs/03-api-index.md`；细则同步 `docs/standards/api-governance.md` 等 |
| SQLite 表结构、字段、索引、迁移变化 | `docs/04-database-design.md` |
| Web/小程序/浏览器/MinIO/SQLite兼容结论变化 | `docs/05-compatibility-matrix.md` |
| API 治理/错误码/鉴权/上传规范变更 | `docs/standards/*.md` |
| 测试治理/覆盖率规范变更 | `docs/standards/testing-governance.md` 等 |
| 故障知识沉淀 | `docs/knowledge-base/incidents/` |
| Sprint 迭代经验复盘 | `docs/knowledge-base/retrospectives/`（`/sprint-exps`） |
| BUG 分析 | `issues/bugs/`（非 `docs/bugs/`） |
| 迭代计划变化 | `iterations/{change|archive}/sprint-xxx/`（非 `docs/iterations/`） |

### 2.2 更新方式

- AI 可以生成初稿和同步变更。
- 涉及产品范围、验收标准、架构边界、上线策略的内容必须人工确认。
- AI 更新文档时必须保留 Obsidian YAML Frontmatter。
- 文档中不确定内容必须标注为 `待确认`，不能编造。

### 2.3 时间记录格式（MUST）

所有文档中的**时间属性字段** MUST 精确到秒，统一使用 **24 小时制**：

```text
YYYY-MM-DD HH:mm:ss
```

> 说明：规范中的 `HH` 表示 24 小时制小时（00–23），与口语中的「hh:mm:ss」含义一致；禁止使用仅日期（`YYYY-MM-DD`）、毫秒时间戳或无时区说明的 ISO-8601 混写（除非引用外部原文并在旁注项目标准时间）。

适用范围包括但不限于：

- YAML Frontmatter 中的 `created_at`、`updated_at` 及创建、更新、归档、评审、发布时间。
- `issues/requirements/`、`issues/bugs/` 中的 `lifecycle`、变更记录、评审记录。
- `iterations/` 中的 Sprint 起止时间、里程碑、验收与发布记录。
- `openspec/changes/`、`openspec/specs/`、archive trace 中的创建、应用、同步、归档记录。
- `docs/`、`rules/`、`README` 中描述历史事件、更新时间或治理动作的字段与表格。

除外规则：

- 纯目录名、文件名、版本号、需求/BUG 编号中的日期片段 MAY 保持既有命名规则。
- 引用外部标准、第三方原文或历史原始记录时 MAY 保留原格式，但 MUST 在新增项目内记录时补充本项目标准时间。
- 若未特别声明时区，默认使用项目本地时区 `Asia/Shanghai`。

### 2.4 AI 自动生成 Markdown 元数据（MUST）

凡由 AI Agent 或 workflow 命令**新建**的 Markdown 文档（含 YAML Frontmatter），Frontmatter **MUST** 包含：

```yaml
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
```

**更新规则：**

| 动作 | `created_at` | `updated_at` |
|------|--------------|--------------|
| 新建 | 设为当前时间 | 设为当前时间 |
| 任意后续修改 | **不得修改** | **MUST** 更新为当前时间 |

**适用范围（自动生成 / AI 维护）：**

| 目录 | 示例 |
|------|------|
| `issues/requirements/` | `capture.md`、`requirement.md`、`trace.md`、`acceptance.md` … |
| `issues/bugs/` | `capture.md`、`bug.md`、`trace.md` … |
| `iterations/` | `sprint.md`、`release-note.md`、`acceptance-report.md` |
| `openspec/changes/` | `proposal.md`、`design.md`、`tasks.md`、`trace.md` … |
| `openspec/specs/` | 归档合并后的 spec（AI 写入时） |
| `docs/` | AI 新建或同步更新的长期文档 |
| `rules/` | AI 辅助更新的治理规范 |

**Legacy 字段映射（逐步废弃，新文档 MUST NOT 使用）：**

| 旧字段 | 替代 |
|--------|------|
| `recorded_at` | `created_at` |
| 仅 `update_method` 无时间 | 补充 `updated_at` |

`python scripts/sync-workflow-status.py` 在写入衍生文档时会自动补全 / 刷新 `created_at` 与 `updated_at`（见 `rules/document-governance.md` §6.1）。

**Frontmatter 最小模板：**

```yaml
---
title: 文档标题
purpose: 一句话用途
created_at: YYYY-MM-DD HH:mm:ss
updated_at: YYYY-MM-DD HH:mm:ss
owner: 角色或负责人
status: draft
---
```

## 3. issues 目录生成与更新逻辑

`issues/` 是原始需求与 BUG 池，不等同于开发任务。生命周期阶段目录（`plan` / `review` / `archive`）见 **`rules/issues-lifecycle.md`**。

### 3.1 新需求

新需求 MUST 创建目录（**禁止** 在 `issues/requirements/` 根下新建扁平 `REQ-*`）：

```text
issues/requirements/plan/REQ-xxxx-slug/
├── capture.md
├── trace.md
└── …
```

必填内容：

```yaml
需求编号:
需求来源:
目标用户:
业务价值:
需求描述:
优先级:
状态:
关联迭代:
关联OpenSpec Change:
验收要点:
备注:
```

### 3.2 新 BUG

新 BUG MUST 创建目录（**禁止** 在 `issues/bugs/` 根下新建扁平 `BUG-*`）：

```text
issues/bugs/plan/BUG-xxxx-slug/
├── capture.md
├── trace.md
└── …
```

必填内容：

```yaml
BUG编号:
发现来源:
严重程度:
影响范围:
复现步骤:
实际结果:
期望结果:
日志/截图:
状态:
关联迭代:
关联OpenSpec Change:
回归测试:
备注:
```

### 3.3 状态流转

推荐状态：

```text
Open → Triaged → In Progress → Resolved → Closed
```

AI 在 Change 创建、开发完成、验收完成时必须同步更新 Issue 状态。

## 4. iterations 目录生成与更新逻辑

`iterations/` 用于管理研发迭代范围，不存放具体实现细节。阶段目录见 `rules/iterations-lifecycle.md`。

### 4.1 新迭代目录

新迭代 **MUST** 使用三位编号目录 `iterations/change/sprint-xxx/`，并通过 **`/sprint-propose`** 或等价流程创建 **以下四件套**（缺一不可）：

```text
iterations/change/sprint-xxx/
├── sprint.yaml          # 机器可读索引（MUST）
├── sprint.md            # 人类可读说明
├── release-note.md      # 发布说明初稿
└── acceptance-report.md # 验收报告模板
```

迭代归档（`/sprint-archive`）后 **MUST** 将目录迁入 `iterations/archive/sprint-xxx/`。

#### sprint.yaml（MUST）

`sprint.yaml` 是迭代的**结构化事实源**，供 AI、脚本与 trace 引用；`sprint.md` 为其人类可读展开。

**MUST** 包含字段：

```yaml
sprint_id: sprint-xxx
status: planning | in_progress | completed
lifecycle_stage: change | archive
start_date: YYYY-MM-DD HH:mm:ss
end_date: YYYY-MM-DD HH:mm:ss

capacity:
  developers: <int>
  testers: <int>

requirements:   # issues/requirements 目录名，如 REQ-0001-user-login
bugs:           # issues/bugs 目录名，无则 []
changes:        # openspec change id，如 add-user-login

estimated_story_points: <int>
estimated_person_days: <number>
```

创建新迭代时 **MUST** 同步生成 `sprint.yaml`；范围变更（需求/BUG/Change 进出迭代、状态、日期、估算）时 **MUST** 同时更新 `sprint.yaml` 与 `sprint.md`。

### 4.2 更新时机

| 场景 | 必须更新 |
|---|---|
| 新迭代创建 | `sprint.yaml`、`sprint.md`、`release-note.md`、`acceptance-report.md`（四件套） |
| 需求进入迭代 | `sprint.yaml`、`sprint.md` |
| 需求移出迭代 | `sprint.yaml`、`sprint.md` |
| Change 创建或纳入 | `sprint.yaml`、`sprint.md`；REQ/BUG 须 **approved** 或 **in_sprint**（须先完成 `/req-review` / `/bug-review`） |
| Change 完成 / 归档 | `sprint.yaml`（status）、`sprint.md`、`release-note.md`、`acceptance-report.md` |
| 发现风险 | `sprint.md`（风险章节） |
| Sprint 结束 | `sprint.yaml`（`status: completed`）、`acceptance-report.md` |

## 5. openspec 目录生成与更新逻辑

`openspec/` 是系统行为事实源。

### 5.1 specs 与 changes 的边界

- `openspec/specs/`：当前已生效能力，不允许在开发中直接修改。
- `openspec/changes/`：开发中的需求、BUG修复、技术改造。
- `openspec/archive/`：已完成并验收的历史变更。

### 5.2 何时必须创建 Change

满足任一条件必须创建 `openspec/changes/<change-id>/`：

- 新功能。
- BUG 修复导致系统行为变化。
- API 变更。
- 数据库结构变化。
- 权限或角色变化。
- Docker Compose、部署方式、环境变量变化。
- Web/小程序/管理端交互变化。
- 文件上传、MinIO对象存储策略变化。
- 影响测试、验收、发布的技术改造。

### 5.3 Change 必备结构

```text
openspec/changes/<change-id>/
├── proposal.md
├── design.md
├── tasks.md
├── trace.md
├── acceptance.md
├── test-plan.md
├── specs/
└── implementation/
```

### 5.4 归档规则

验收通过后：

1. 将 `changes/<change-id>/specs/*` 合并到 `openspec/specs/*`。
2. 更新 `issues/` 状态为 Closed。
3. 更新 `iterations/{change|archive}/*/sprint.yaml`、`sprint.md`、`release-note.md` 和 `acceptance-report.md`。
4. 将 Change 移动到 `openspec/archive/YYYY-MM/<change-id>/`。

AI 不得删除归档内容。

## 6. 文档自动同步矩阵

| 变更类型 | 必须同步 |
|---|---|
| API | `docs/03-api-index.md`、`src/web/orval.config.ts`、前端生成客户端 |
| 数据库 | `docs/04-database-design.md`、`src/backend/migrations/`、测试 |
| Docker | `docker-compose.yml`、`docs/02-deployment.md`、README |
| MinIO | `compatibility/object-storage/minio.md`、后端配置、部署文档 |
| Web页面 | `openspec/changes/*/specs/web-client/spec.md`、PRD或原型 |
| 小程序页面 | `openspec/changes/*/specs/wechat-miniapp/spec.md`、兼容性文档 |
| 管理端 | `openspec/changes/*/specs/tile-admin/spec.md`、权限说明 |
| Change 归档 / Sprint 范围 | `iterations/{change|archive}/sprint-xxx/sprint.yaml`、`sprint.md`、`release-note.md`、`acceptance-report.md` |
| BUG修复 | `issues/bugs/*`、回归测试 |

### 6.1 Workflow 状态同步（MUST）

执行 `req-*`、`bug-*`、`opsx-*`、`sprint-*` 工作流命令后，**MUST** 运行：

```bash
python scripts/sync-workflow-status.py --event <event> [--sprint auto] [--change|--req|--bug <id>]
```

- 脚本路径：`scripts/sync-workflow-status.py`；Skill：`.agents/skills/workflow-sync/SKILL.md`
- 机器维护区：`sprint.md` 中 `<!-- workflow-sync:scope-*:start/end -->` 标记块
- **Scope 表时间格式（MUST）**：`sprint.md` Scope 表中「说明」（REQ/BUG）与「Sprint 目标」（Change）列内嵌的 archived 时间戳 MUST 为 `YYYY-MM-DD HH:mm:ss` 且时分秒 MUST 有实际值（禁止占位 `00:00:00`）；优先取自 archived change `trace.md` 的 `updated_at` / 变更记录、issue `trace.md` 的 `lifecycle.archived`（或 `completed`/`reviewed`/`approved`），回退 archive 目录日期前缀时补 change `updated_at` 的时分秒或 `23:59:59`。
- **里程碑时间格式（MUST）**：`sprint.md` §里程碑 表格「目标日期」列 MUST 使用 `YYYY-MM-DD HH:mm:ss` 且时分秒 MUST 有实际值；`workflow-sync` 将 legacy 仅日期或 `00:00:00` 行规范化为当日 `23:59:59`。
- **Sprint 目标完整性（MUST）**：`sprint.yaml` 中 `requirements` / `bugs` 每一项 MUST 在 `sprint.md` §Sprint 目标 中同步维护 **两处**：（1）顶部编号列表条目；（2）对应 `### REQ-xxxx / BUG-xxxx 要点` 小节。**未评审 REQ/BUG 不得出现在上述两处或 `sprint.yaml`**；仅可列于「延后项（待评审）」。纳入或移出迭代时两处同步更新（workflow-sync **不**自动维护该节，由 `/sprint-propose` 或范围变更命令负责）。
- CI / 本地校验：`python scripts/sync-workflow-status.py --sprint auto --check`
- **禁止** Agent 手工编辑 Scope 表与 `openspec_changes[].status`（sync 失败时修复脚本或 hotfix 后重跑）

| 命令族 | 典型 `--event` |
|--------|----------------|
| req-* | `req.capture` … `req.opsx` |
| bug-* | `bug.capture` … `bug.opsx` |
| opsx-* | `opsx.propose` / `opsx.apply` / `opsx.archive` |
| sprint-* | `sprint.propose` / `sprint.apply` / `sprint.archive` |

## 7. AI 执行顺序

AI 接到任务后必须按以下顺序执行：

```text
1. 阅读 AGENTS.md
2. 阅读 rules/*，特别是 document-governance.md 与 directory-structure.md
3. 阅读 openspec/project.md
4. 判断是否已有 issue
5. 判断是否需要进入 iteration
6. 判断是否需要创建/更新 OpenSpec Change
7. 更新 proposal/design/tasks/spec/test-plan
8. 开发 src/
9. 补充 tests/
10. 同步 docs/
11. 更新 issues 和 iterations
12. 归档或说明尚不可归档
```

## 8. 禁止行为

- 禁止绕过 Issue 与 OpenSpec Change 直接开发需求。
- 禁止只改代码不改文档。
- 禁止直接修改 `openspec/specs/` 作为开发变更。
- 禁止把需求、BUG、迭代、Spec 混在一个文档中。
- 禁止生成无来源、无状态、无验收标准的需求文档。
