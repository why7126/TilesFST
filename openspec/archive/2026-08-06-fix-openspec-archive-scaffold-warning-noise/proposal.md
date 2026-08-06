---
change_id: fix-openspec-archive-scaffold-warning-noise
title: 吸收 OpenSpec 归档英文脚手架兼容 warning 噪音
status: applied
source_bug: BUG-0119-openspec-archive-scaffold-warning-noise
created_at: 2026-08-06 10:39:32
updated_at: 2026-08-06 10:54:33
---

# 提案

## 背景

BUG-0119 记录了 OpenSpec 归档完成后反复输出固定非阻塞提示的问题：上游 OpenSpec CLI 会提示 `proposal.md` 缺少英文 `## Why` / `## What Changes`，但项目规则要求 OpenSpec Change 文档中文优先，且不得为了消除 CLI 兼容提示回填英文脚手架标题。

当前归档封装层已经能让该 warning 不阻断归档，但最终结论仍重复展示固定说明，容易让验收者误以为归档存在未解决问题。

## 目标

- 在 `/opsx-archive` 和底层归档封装脚本中吸收已知 OpenSpec CLI 英文脚手架兼容 warning。
- 当该 warning 是唯一 stderr 且项目中文语言校验通过时，最终归档结论不再重复提示固定说明。
- 保留真实错误、未知 stderr、目录结构错误和中文语言校验失败的阻断或 warning 输出。
- 通过脚本级测试覆盖静默吸收、未知 stderr 暴露和语言校验失败三类路径。

## 非目标

- 不修改后端 API、数据库 schema、Web、小程序或管理端运行时行为。
- 不变更 OpenSpec CLI 上游行为。
- 不要求 Change 文档新增英文 `## Why` / `## What Changes` 标题。
- 不修改 `openspec/specs/` 正式规格，归档阶段再合并 delta。

## 影响范围

- `scripts/archive-change.sh` 或其调用的归档封装逻辑。
- `.agents/skills/opsx-archive/SKILL.md` 的成功输出口径，若实现需要同步说明。
- 脚本级测试与 OpenSpec 语言校验。

## 回滚方案

若过滤规则误吞真实 stderr，可回滚本 Change 对归档脚本 warning 分类逻辑的修改，恢复所有 OpenSpec CLI stderr 在最终说明中的展示；同时保留新增测试中的未知 stderr 场景作为回归证据，重新调整匹配规则后再应用。
