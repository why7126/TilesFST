---
title: release-propose 默认下一步调整为 release-prepare
created_at: 2026-08-31 08:35:48
updated_at: 2026-08-31 08:35:48
---

# Proposal

## 背景

`/release-propose <version>` 的职责是创建或更新发布计划。发布计划创建后，主线下一步应进入 `/release-prepare <version>`，由 prepare 阶段完成版本源同步、公告准备、usage docs 决策和发布前门禁证据补齐。

当前技能和发布流程图仍把 `/release-status <version>` 作为 propose 后默认下一步，容易让操作者误以为 status 是准备阶段前的必经步骤。

## 变更目标

- 将 `/release-propose <version>` 的默认下一步调整为 `/release-prepare <version>`。
- 明确 `/release-status <version>` 是只读状态面板和阻塞排查入口，可按需运行，但不替代 prepare。
- 保留 release-status 对当前阶段、默认 upgrade 路径和 blocker 分类的只读汇总能力。

## 非目标

- 不修改 release metadata schema。
- 不修改 release validator 的状态计算逻辑。
- 不修改业务 `src/`。
