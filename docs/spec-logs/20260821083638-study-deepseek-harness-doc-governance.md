---
purpose: deepseek-harness 文档治理学习应用报告
content: 文档事实唯一归属、治理决策记录、文档表达卫生、最小相关验证和防御性模式模板
source: /spec-study apply deepseek-harness 候选项
update_method: 同一学习应用流程的验证结果或修正更新本文档
created_at: 2026-08-21 08:36:38
updated_at: 2026-08-21 08:46:50
---

# deepseek-harness 文档治理学习应用报告

## 学习对象与模式

- 学习对象：`https://github.com/deepseek-ai/deepseek-harness`
- 学习模式：Phase 1 远端只读学习，Phase 2 经用户确认后应用候选项。
- 执行时间：2026-08-21 08:36:38，时区 `Asia/Shanghai`。

## 学习到的治理能力

- 文档事实唯一归属：入口摘要与详细规则分离，降低长期文档漂移。
- 治理决策记录轻量化：记录采纳原因、未采纳原因、替代方案、验证责任和后续触发条件。
- 文档 slop / CoT 泄漏审计：发现会话推理、临时草稿、review 对话、不可解析引用和未脱敏路径。
- 最小相关验证选择：按 diff scope 和触达面选择证据，不重复运行未受影响的检查。
- 防御性模式知识库模板：把个案问题沉淀为可复用预防规则和验证方式。

## 已采纳内容和采纳原因

| 内容 | 采纳原因 | 落地位置 |
|---|---|---|
| 文档事实唯一归属 | 本项目入口、规则、技能和 spec-log 已较多，需减少重复规则漂移 | `rules/document-governance.md`、`AGENTS.md`、`docs/README.md` |
| 治理决策记录字段 | 让治理变更可解释、可复核，不只留下文件清单 | `rules/document-governance.md`、`.agents/skills/spec-study/SKILL.md`、`.agents/skills/spec-opt/SKILL.md` |
| 文档表达卫生审计 | 给长期文档提供轻量审计入口，降低会话残留风险 | `docs/standards/document-prose-hygiene.md`、`scripts/validate-doc-prose-hygiene.py` |
| 最小相关验证选择 | 与现有命令门禁矩阵互补，避免无意义重复验证 | `docs/standards/command-execution-order.md` |
| 防御性模式模板 | 将复盘经验转成可执行预防规则 | `docs/knowledge-base/best-practices/defensive-pattern-template.md` |

## 未采纳内容和原因

- 未引入学习对象的 `.agents/notes/` 目录树：本项目当前唯一 AI 工具入口是 `.agents/skills/`，恢复新入口会扩大目录边界。
- 未复制学习对象源码、脚本长文或插件体系：本次只迁移治理原则，避免跨项目结构耦合。
- 未引入 Node 测试体系：本项目治理脚本以 Python 为主，轻量校验脚本更贴合现有验证链。

## 替代方案或取舍

- 用 `docs/spec-logs/` 的学习报告和治理日志承载决策字段，替代新增 Agent Note 目录。
- 用启发式 Python 扫描提供 warning 级信号，替代自动删除或强制失败，避免误删有效事实。
- 用防御性模式模板补充知识库，而不是把事故叙事复制成长期规范。

## 验证责任和后续触发条件

- 验证责任：修改长期文档、规则、技能说明或知识库的命令负责运行聚焦文档卫生校验；OpenSpec、目录和 Sprint 门禁仍由对应 workflow 命令负责。
- 后续触发条件：若文档卫生脚本 warning 长期噪声过多，应通过独立治理 Change 调整 pattern、allowlist 或目标范围。

## 更新文件清单

| 文件 | 修改原因 |
|---|---|
| `AGENTS.md` | 增加文档治理读取路由和长期文档表达红线 |
| `rules/document-governance.md` | 补充事实唯一归属和治理决策字段 |
| `docs/standards/command-execution-order.md` | 补充 diff scope 与最小相关验证选择规则 |
| `docs/standards/document-prose-hygiene.md` | 新增文档 slop / CoT 泄漏审计标准 |
| `scripts/validate-doc-prose-hygiene.py` | 新增长期文档表达卫生轻量校验脚本 |
| `docs/knowledge-base/best-practices/defensive-pattern-template.md` | 新增防御性模式知识库模板 |
| `docs/README.md`、`docs/knowledge-base/README.md` | 同步文档索引 |
| `.agents/skills/spec-study/SKILL.md`、`.agents/skills/spec-opt/SKILL.md` | 补充应用阶段与治理优化阶段的文档卫生要求 |
| `openspec/changes/apply-deepseek-harness-doc-governance-learnings/` | 记录 Change proposal、design、tasks 和 delta spec |
| `iterations/change/sprint-024/` | 将纯治理 Change 纳入 Sprint scope |
| `docs/spec-logs/CHANGELOG.md` | 登记规范工程变更历史 |

## 影响范围

- API：不影响。
- 数据库：不影响。
- Web：不影响业务实现。
- 小程序：不影响。
- 管理端：不影响。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：新增治理脚本级校验；业务测试不适用。

## 校验命令和结果

- `python scripts/validate-doc-prose-hygiene.py <focused-paths> --json`：通过执行，返回 warning 15 条；命中项为规则正文中的规范性用语和启发式历史叙事词，未作为 blocker。
- `python -m py_compile scripts/validate-doc-prose-hygiene.py`：通过。
- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `openspec validate apply-deepseek-harness-doc-governance-learnings`：通过。
- `python scripts/validate-sprint-scope.py sprint-024 --item apply-deepseek-harness-doc-governance-learnings`：通过。
- `python scripts/sync-workflow-status.py --event opsx.apply --change apply-deepseek-harness-doc-governance-learnings --sprint auto`：通过，解析 Sprint 为 `sprint-024`，Errors 0。
- `python scripts/extract-ai-usage.py --post-command-hook --workflow-event opsx.apply --change apply-deepseek-harness-doc-governance-learnings --sprint sprint-024 --json`：通过，`status=ok`，`warning_count=0`。

`git diff --name-only -- src` 显示工作区存在前置业务 `src/` 改动；本次学习应用触达文件集中在治理资产、OpenSpec Change、Sprint 记录、spec-log 和治理脚本，未新增或修改业务 `src/` 文件。

## 学习对象只读保护结果

学习对象通过远端只读网页与仓库文件视图读取；未克隆、未安装依赖、未运行写入命令，未修改学习对象任何文件或仓库状态。

## 后续建议

- 文档卫生脚本先作为 warning 级检查使用；积累误报后再决定是否加入更强门禁。
- 未来 BUG 或返修复盘若发现可复用预防规则，优先用防御性模式模板沉淀，而不是复制完整事故报告。
