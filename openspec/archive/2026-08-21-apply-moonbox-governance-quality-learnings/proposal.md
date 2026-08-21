## 背景

本项目已在 2026-08-10 应用过 ProjectMoonBox 的基础治理能力，但 MoonBox 后续继续沉淀了证据化根因、命令执行复盘、UI 返修截图对照、Workflow Sync next 推导复核和治理脚本门禁矩阵。当前项目已有相近基础能力，适合做第二轮小范围治理补强，减少 BUG 根因无证据、命令完成后问题未沉淀、UI 返修直接动手和工作流派生态漂移。

## 变更内容

- 新增证据化根因分析规则与轻量校验脚本，要求 BUG、问题排查和验收返修区分根因状态，并为 confirmed 根因绑定证据链。
- 为 workflow 命令补充执行链路复盘 Hook，要求完成输出包含链路状态、问题证据、规范优化建议和 follow-up 自动创建状态。
- 强化 UI 型 `/opsx-modify`：当反馈包含附件截图、标注图、原型截图或实际截图时，返修前必须建立逐项视觉对照表。
- 明确 Workflow Sync next 推导复核：`req.opsx` / `bug.opsx` 回填 Change 后必须刷新当前态看板下一步，避免继续提示旧命令。
- 新增治理脚本门禁矩阵文档，用最小相关验证原则列出不同命令阶段应运行的治理脚本。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `agent-workflow-tooling`：补充 Agent 命令、Workflow Sync、BUG 根因证据、UI 返修和治理脚本门禁的行为要求。

## 影响

- API：不影响。
- 数据库：不影响。
- Web / 小程序 / 管理端：不修改业务实现；后续 UI 返修流程增加证据门禁。
- Orval：不需要。
- Docker Compose：不需要。
- 测试：新增治理校验脚本；业务测试不适用。
- 目录边界：仅触达 `.agents/skills/`、`rules/`、`docs/`、`scripts/`、`openspec/changes/`、`iterations/change/` 和 `docs/spec-logs/`。
