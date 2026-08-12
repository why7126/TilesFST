---
purpose: ProjectMoonBox 治理学习应用报告
content: 记录日志优先 spec-study、git-check、原型 UI 验收、Issue 当前态看板和引导式反馈契约的采纳结果
source: /spec-study ProjectMoonBox apply 全部候选项
update_method: 同一次 ProjectMoonBox 治理学习应用的验证结果或修正继续更新本文
created_at: 2026-08-10 23:28:57
updated_at: 2026-08-10 23:28:57
---

# ProjectMoonBox 治理学习应用报告

## 学习对象

- 学习对象：ProjectMoonBox。
- 学习模式：auto。
- 执行时间：2026-08-10 23:28:57。
- 应用 Change：`openspec/changes/apply-projectmoonbox-governance-learnings/`。
- Sprint：`sprint-022`。

## 学习到的治理能力

- 日志优先学习：先以学习对象 `docs/spec-logs/CHANGELOG.md` 作为治理演进地图，再按主题补读单次日志和真实治理资产。
- Git 安全检测：新增推送前 staged/tracked 安全扫描，覆盖真实 env、运行时数据、大文件、密钥、连接串和本机绝对路径。
- 原型驱动 UI 验收：用 UI Contract、Skeleton、1440px 视觉证据、computed style、Mock/API 边界和最终一致性检查约束带 prototype 的 UI Change。
- Issue 当前态看板：在 REQ/BUG 根目录维护每个 Issue 一行的当前态索引，但不替代机器事实源。
- 引导式反馈契约：命令需要用户选择时优先使用原生交互卡片，不支持时降级为文本结构化选项。

## 已采纳内容

| 内容 | 采纳原因 |
|---|---|
| `/spec-study` 日志优先学习顺序 | 降低跨项目学习上下文消耗，并减少盲扫规则、技能和脚本的概率。 |
| `/git-check` 技能与脚本 | 补足推送前安全门禁，贴合本项目 `.env`、MinIO、运行时数据和本机路径红线。 |
| 原型驱动 UI 验收标准 | 本项目 Web、管理端、小程序均有视觉一致性风险，适合用证据化门禁前移。 |
| Issue 当前态看板索引 | 提供目录级扫描入口，同时保持 `_registry.yaml`、`trace.md`、Sprint 和 OpenSpec 为事实源。 |
| 引导式反馈契约 | 让命令在需要用户决策时更收敛，减少大段开放式追问。 |

## 未采纳内容

| 内容 | 未采纳原因 |
|---|---|
| ProjectMoonBox 的 S3/MySQL 完整部署矩阵 | 本项目已有 MinIO 单桶、腾讯 COS 生产 Compose、小程序和视频资产治理边界，原样迁移会扩大范围。 |
| 学习对象业务 `src/` 实现与测试 | 本次仅应用治理资产，禁止修改业务实现。 |
| 自动让 Workflow Sync 写 Issue 当前态看板 | 一次性改动状态机风险较高，先落规则和索引文件，后续可单独治理自动化。 |

## 更新文件

| 文件 | 修改原因 |
|---|---|
| `openspec/changes/apply-projectmoonbox-governance-learnings/` | 承载本次纯治理学习应用的 proposal、design、tasks、trace 和 delta spec。 |
| `iterations/change/sprint-022/sprint.yaml` | 将纯治理 Change 纳入 Sprint scope，满足 apply 门禁。 |
| `.agents/skills/spec-study/SKILL.md` | 增加日志优先学习顺序和漂移风险标注。 |
| `.agents/skills/git-check/SKILL.md` | 新增推送前安全检测命令入口。 |
| `.agents/skills/req-opsx/SKILL.md`、`.agents/skills/opsx-apply/SKILL.md`、`.agents/skills/opsx-modify/SKILL.md`、`.agents/skills/opsx-archive/SKILL.md` | 接入原型驱动 UI 验收门禁。 |
| `scripts/git-check.py` | 新增 staged/tracked 安全扫描脚本。 |
| `scripts/validate-agent-context-budget.py` | 将 `git-check` 纳入命令技能校验。 |
| `AGENTS.md`、`rules/agent-context-budget.md`、`rules/security.md`、`rules/ui-design.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、`rules/directory-structure.md` | 同步全局入口、上下文预算、安全、UI、Issue 生命周期、文档和目录边界。 |
| `docs/standards/prototype-ui-acceptance.md`、`docs/README.md` | 新增原型 UI 验收标准并同步文档索引。 |
| `issues/requirements/CHANGELOG.md`、`issues/bugs/CHANGELOG.md` | 新增 REQ/BUG 当前态看板索引。 |
| `docs/spec-logs/CHANGELOG.md`、本文 | 记录本次跨项目学习应用。 |

## 影响说明

- API：不影响。
- 数据库：不影响。
- Web：不修改业务 UI；后续带 prototype 的 Web UI Change 需遵守新增门禁。
- 小程序：不修改小程序代码；后续带 prototype 的小程序 UI Change 需提供对应视觉证据。
- 管理端：不修改业务代码；后续管理端 UI Change 需补齐 UI Contract 与视觉证据。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：新增治理脚本校验；业务测试不适用。

## 校验命令和结果

- 通过：`python scripts/validate-agent-context-budget.py`
- 通过：`python scripts/validate-openspec-language.py`
- 通过：`python scripts/validate-directory-structure.py`
- 通过：`openspec validate apply-projectmoonbox-governance-learnings`
- 通过：`python scripts/validate-sprint-scope.py sprint-022 --item apply-projectmoonbox-governance-learnings`
- 通过：`python scripts/git-check.py`
- 通过：`python scripts/sync-workflow-status.py --event opsx.apply --change apply-projectmoonbox-governance-learnings --sprint auto`
- 通过：`python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change apply-projectmoonbox-governance-learnings --sprint sprint-022 --json`

## 学习对象只读保护

对 ProjectMoonBox 仅执行只读扫描和片段读取命令；未在学习对象路径中执行写入、安装、生成、格式化、迁移、清理、提交、切换分支或修改 Git 状态的操作。学习对象本身存在既有 dirty/untracked 状态，本次不处理。

## 后续建议

- 后续可将 Issue 当前态看板行刷新自动化纳入 Workflow Sync。
- 后续可将 UI Contract 与截图证据检查沉淀为 `/opsx-archive` 前自动校验。
