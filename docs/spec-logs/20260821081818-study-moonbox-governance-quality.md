---
purpose: MoonBox 治理质量学习应用报告
content: 记录证据化根因、命令执行复盘、UI 返修截图对照、Workflow Sync next 推导复核和治理脚本门禁矩阵的采纳结果
source: /spec-study apply MoonBox 候选项
update_method: 同一次 MoonBox 治理质量学习应用的验证结果或修正继续更新本文
created_at: 2026-08-21 08:18:18
updated_at: 2026-08-21 08:18:18
---

# MoonBox 治理质量学习应用报告

## 学习对象与模式

- 学习对象：ProjectMoonBox。
- 学习模式：`/spec-study apply MoonBox 候选项`。
- 执行时间：2026-08-21 08:18:18。
- 应用 Change：`apply-moonbox-governance-quality-learnings`。
- 承载 Sprint：`sprint-024`。

## 学习到的治理能力

- 证据化根因分析：根因状态区分 `unknown`、`hypothesis`、`probable`、`confirmed`，confirmed 必须绑定证据链。
- 命令执行复盘 Hook：workflow 命令结束后报告链路状态、问题证据、规范优化建议和 follow-up 自动创建状态。
- UI 返修截图逐项对照：附件截图、标注图、原型截图或实际截图反馈需要先建立对照表，再返修。
- Workflow Sync next 推导复核：REQ/BUG 回填 Change 后必须刷新当前态看板下一步，避免派生态漂移。
- 治理脚本门禁矩阵：按触达范围选择最小相关校验，不默认全量运行无关测试。

## 已采纳内容

| 内容 | 采纳原因 |
|---|---|
| 证据化根因分析规则与轻量校验脚本 | 补强 BUG、返修和问题排查链路，减少无证据确认根因。 |
| 命令执行复盘 Hook | 让 workflow 命令完成时显式暴露链路问题和可沉淀改进点。 |
| UI 返修截图逐项对照 | 降低 UI 返修直接动手导致的证据遗漏和反复返工。 |
| Workflow Sync next 推导复核 | 防止 `req.opsx` / `bug.opsx` 后当前态看板继续提示旧下一步。 |
| 治理脚本门禁矩阵 | 帮助后续命令选择最小相关验证并说明业务测试不适用原因。 |

## 未采纳内容

| 内容 | 未采纳原因 |
|---|---|
| MoonBox 轻量 Mintlify 模式 | 本项目已有更完整的 release / usage-docs / mintlify 版本化边界，不适合反向降级。 |
| MoonBox 业务 `src/` 实现与部署矩阵 | 本次为纯治理学习应用，禁止修改业务实现、API、DB、Orval 或 Docker 拓扑。 |
| 原样复制 MoonBox 长脚本或长规范 | 按本项目语境改写为短规则、短引用和轻量校验脚本。 |

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `openspec/changes/apply-moonbox-governance-quality-learnings/` | 承载本次学习应用的 proposal、design、tasks 和 delta spec。 |
| `iterations/change/sprint-024/` | 将纯治理 Change 纳入 Sprint scope，满足 apply 门禁。 |
| `rules/root-cause-evidence.md` | 新增证据化根因分析治理规则。 |
| `scripts/validate-root-cause-evidence.py` | 新增轻量根因证据校验脚本。 |
| `docs/standards/command-execution-order.md` | 新增命令执行顺序与治理脚本门禁矩阵。 |
| `.agents/skills/workflow-sync/SKILL.md` | 接入命令执行复盘 Hook、root-cause evidence gate 和 next 推导漂移要求。 |
| `.agents/skills/opsx-apply/SKILL.md`、`.agents/skills/opsx-modify/SKILL.md`、`.agents/skills/bug-complete/SKILL.md`、`.agents/skills/explore/SKILL.md` | 接入根因证据和 UI 返修截图对照要求。 |
| `rules/bug-management.md`、`rules/testing.md`、`rules/ui-design.md` | 同步 BUG、测试和 UI 门禁。 |
| `docs/standards/prototype-ui-acceptance.md` | 补充 UI 返修截图逐项对照表。 |
| `AGENTS.md`、`docs/README.md` | 同步入口路由、红线和文档索引。 |
| `docs/spec-logs/CHANGELOG.md`、本文 | 登记本次跨项目学习应用。 |

## 影响评估

- API：不影响。
- 数据库：不影响。
- Web：不修改业务页面；后续 UI 返修流程增加截图对照门禁。
- 小程序：不修改小程序代码；后续小程序 UI 返修可复用证据门禁。
- 管理端：不修改业务实现；后续管理端 UI 返修需先完成截图对照。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：新增治理脚本校验；业务测试不适用。

## 校验命令和结果

- 通过：`python scripts/validate-root-cause-evidence.py --change apply-moonbox-governance-quality-learnings --json`；未发现 linked BUG，根因证据校验不适用。
- 通过：`python scripts/validate-agent-context-budget.py`
- 通过：`python scripts/validate-openspec-language.py`
- 通过：`python scripts/validate-directory-structure.py`
- 通过：`openspec validate apply-moonbox-governance-quality-learnings`
- 首次未通过后已修复：`python scripts/validate-sprint-scope.py sprint-024 --item apply-moonbox-governance-quality-learnings`；补齐 `sprint.md` 目标编号列表和 workflow-sync changes 表后通过。
- 通过：`python scripts/sync-workflow-status.py --event opsx.apply --change apply-moonbox-governance-quality-learnings --sprint auto`；解析到 `sprint-024`，更新 2 项，错误 0。
- 通过：`python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change apply-moonbox-governance-quality-learnings --sprint sprint-024 --json`；`usage_mode: actual`，`command_run_count: 1`，`warning_count: 0`。
- 通过：`scripts/archive-change.sh apply-moonbox-governance-quality-learnings`；正式 spec 新增 5 条 Requirement，归档到 `openspec/archive/2026-08-21-apply-moonbox-governance-quality-learnings/`。
- 通过：归档后 `python scripts/validate-openspec-language.py`、`python scripts/validate-directory-structure.py`、`python scripts/validate-archive-evidence.py --change apply-moonbox-governance-quality-learnings --archive-path openspec/archive/2026-08-21-apply-moonbox-governance-quality-learnings`。
- 通过：`python scripts/sync-workflow-status.py --event opsx.archive --change apply-moonbox-governance-quality-learnings --sprint auto`；解析到 `sprint-024`，更新 2 项，错误 0。
- 通过：`python scripts/promote-issues-for-archive.py --change apply-moonbox-governance-quality-learnings --reason "/opsx-archive apply-moonbox-governance-quality-learnings"`；无可迁移 Issue。
- 通过：`python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.archive --change apply-moonbox-governance-quality-learnings --sprint sprint-024 --json`；`usage_mode: actual`，`command_run_count: 1`，`warning_count: 0`。
- 通过：聚焦 diff 复核，本次新增/修改集中在治理资产；未新增修改业务 `src/` 文件。

## 学习对象只读保护结果

对 ProjectMoonBox 仅执行只读扫描、片段读取和 Git 状态查询；未在学习对象路径中执行写入、安装、生成、格式化、迁移、测试修复、清理、提交、切换分支或修改 Git 状态的操作。学习对象本身存在既有未提交变更，本次未处理。

## 后续建议

- 后续可把 `validate-root-cause-evidence.py` 扩展为更严格的 BUG archive readiness 门禁。
- 后续可为 Workflow Sync next 推导漂移增加聚焦单元测试，覆盖 REQ 与 BUG 两条链路。
