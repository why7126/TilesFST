---
change_id: add-spec-opt-governance-command
title: 新增规范优化命令 spec-opt
status: proposed
created_at: 2026-08-06 13:46:00
updated_at: 2026-08-06 13:46:00
---

# 提案

## 背景

项目近期多次发生规范体系优化：新增或修改 `.agents/skills` 命令、更新 `rules/`、同步 `AGENTS.md` 和 `docs/README.md`、补充校验脚本。此类工作跨越多个治理入口，但目前缺少一个专门命令来约束范围、同步文档和校验，容易出现只改技能、不改规则或入口文档的断层。

## 目标

- 新增 `/spec-opt` 命令，作为“项目治理规范优化”的专用入口。
- `/spec-opt` 允许直接创建或复用 OpenSpec Change。
- `/spec-opt` 仅服务治理规范，不触碰业务运行时代码。
- 支持新增/修改 `.agents/skills` 命令、`rules/` 文档、`docs/` 文档、`scripts/` 治理脚本。
- 强制规范优化后同步相关入口和索引文档，包括 `AGENTS.md`、`rules/`、`docs/`、`scripts/` 相关说明。
- 保持命令完成输出契约：提供去重后的「下一步」与「待用户决策/处理」。

## 非目标

- 不修改 `src/` 业务代码。
- 不处理产品功能、接口、数据库、Web、小程序或管理端运行时需求。
- 不绕过 OpenSpec Change 直接开发治理能力。
- 不直接修改 `openspec/specs/` 正式规格。
- 不自动创建 REQ/BUG 或推进 Sprint 状态。

## 能力范围

### 新增能力

无。

### 修改能力

- `agent-workflow-tooling`：新增 `/spec-opt` 规范优化命令的行为边界、文档同步要求和校验要求。

## 影响范围

- `.agents/skills/spec-opt/SKILL.md`。
- `AGENTS.md` 命令入口和命令族速查。
- `rules/agent-context-budget.md` 及规范优化相关规则。
- `docs/README.md` 或相关 docs 索引。
- `scripts/validate-agent-context-budget.py` 或新增/修改的治理校验脚本。
- OpenSpec Change 文档与语言校验。

不影响 API、数据库、Orval、Docker Compose、Web、小程序和管理端运行时。
