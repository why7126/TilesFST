---
change_id: add-spec-opt-governance-command
title: spec-opt 规范优化命令设计
status: proposed
created_at: 2026-08-06 13:46:00
updated_at: 2026-08-06 13:46:00
---

# 设计

## 命令定位

`/spec-opt` 是项目治理规范优化命令，用于新增或修改 AI 命令、规则文档、文档索引和治理脚本。它是可落盘命令，不是只读探索命令。

核心边界：

- 允许直接创建或复用 OpenSpec Change。
- 只服务治理规范，不碰业务运行时代码。
- 可修改 `.agents/skills/`、`rules/`、`docs/`、`scripts/`、`AGENTS.md` 和 active OpenSpec Change。
- 不修改 `src/`、运行时 API、数据库 schema、Web、小程序或管理端业务实现。

## 适用输入

命令可接受自然语言或结构化参数：

```text
/spec-opt 新增 spec-opt 命令
/spec-opt update-command bug-review "优化评审后的下一步提示"
/spec-opt update-rules "命令完成输出契约去重"
/spec-opt update-script validate-agent-context-budget.py "校验 spec-opt 文档同步"
```

## 推荐流程

```text
理解治理优化目标
→ 判断影响范围：skills / rules / docs / scripts / AGENTS / OpenSpec
→ 创建或复用 OpenSpec Change
→ 生成或更新 Change artifacts
→ 修改对应技能、规则、文档和脚本
→ 同步入口文档和索引文档
→ 运行校验
→ 输出下一步与待用户决策/处理
```

## 文档同步矩阵

| 变更类型 | 必须同步 |
|---|---|
| 新增/修改命令 | `.agents/skills/<command>/SKILL.md`、`AGENTS.md`、`rules/agent-context-budget.md`、相关 OpenSpec Change |
| 新增/修改规则 | `rules/*.md`、`AGENTS.md` 读取路由或红线、相关 docs 索引 |
| 新增/修改 docs 规范 | `docs/README.md`、相关 `docs/standards/*.md`、`rules/document-governance.md`（按需） |
| 新增/修改脚本 | `scripts/<name>`、脚本帮助文本或 README、相关规则和技能说明、测试或校验命令 |
| 更新命令输出契约 | 所有受影响 Skill、`rules/agent-context-budget.md`、校验脚本 |

## 门禁与校验

`/spec-opt` 完成前应按影响范围运行：

```bash
python scripts/validate-agent-context-budget.py
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
openspec validate <change-id>
```

如修改脚本，应补充或运行对应脚本级测试；如只修改 Markdown 规范，可记录“不适用业务测试”。

## 输出要求

最终输出必须包含：

```text
下一步：<可直接执行的命令；若没有则写“暂无可推进下一步”>
待用户决策/处理：
- <仍需用户选择、确认、补充或处理的事项；若没有则写“无”>
```

已在「下一步」中给出的命令或动作不得重复写入「待用户决策/处理」。

## 风险与缓解

| 风险 | 缓解 |
|---|---|
| 命令边界过宽，误改业务代码 | 在 Skill 中明确禁止修改 `src/`，并要求输出影响范围 |
| 只改技能未同步入口文档 | 将 `AGENTS.md`、`rules/`、`docs/`、`scripts/` 同步列为 MUST |
| 校验遗漏新增命令 | 扩展 `validate-agent-context-budget.py` 或等价脚本扫描全部 `.agents/skills/*/SKILL.md` |
| 与 `/opsx-propose` 职责重叠 | `/spec-opt` 负责治理规范优化落地，可调用/创建 OpenSpec Change；`/opsx-propose` 仍是通用 Change 创建命令 |
