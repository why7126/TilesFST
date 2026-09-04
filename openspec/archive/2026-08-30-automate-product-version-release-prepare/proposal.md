---
title: PRODUCT_VERSION 发布准备自动同步
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 22:41:57
---

# Proposal: PRODUCT_VERSION 发布准备自动同步

## 背景

当前发布治理已经能在 `release-prepare` 和 `release-publish` 阶段校验 Web 与小程序 `PRODUCT_VERSION` 是否等于发布版本，但更新动作仍容易被理解为人工编辑步骤。上一个 v1.2.2 发布返修说明了这个风险：如果版本源未先对齐，后续 image plan / manifest 的稳定输入也会产生漂移。

## 目标

- `/release-prepare <version>` 在校验前自动同步 Web 与小程序中存在的 `PRODUCT_VERSION` 源到发布版本。
- 自动刷新 `release.json.gates.product_version`、`release.json.product_version_sync` 和公告中可由发布对象推导的版本状态证据。
- `/release-publish` 只做发布确认，不修改 Web 或小程序版本源。
- `/image-prepare` 在版本源未对齐时阻断，并要求先回到 `/release-prepare <version>`。

## 非目标

- 不修改业务逻辑、接口、数据库或页面能力。
- 不把发布确认阶段变成自动改版本阶段。
- 不让 image-prepare 代写 `src/` 版本源。

## 影响范围

- Release / image 相关技能说明。
- Release 规则和上下文预算摘要。
- Release / image validator 脚本与聚焦测试。
- OpenSpec product-release-management delta。
- Sprint scope 和规范工程日志。
