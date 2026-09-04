---
title: release-propose 下一步调整 Trace
created_at: 2026-08-31 08:35:48
updated_at: 2026-08-31 08:35:48
---

# Trace

## 需求来源

- 用户反馈：`/release-propose <version>` 后默认下一步不应是 `/release-status <version>`，而应进入 `/release-prepare <version>`。

## 变更链路

- Change：`make-release-propose-next-step-prepare`
- Sprint：`sprint-029`
- 类型：纯治理 Change
- product_data_collection_observability：not_applicable
- affected_layers：无
- N/A 原因：只调整命令技能和发布治理文案，不修改 API、DB、Web、小程序请求封装、日志审计、行为埋点或 Task Trace。

## 证据

- `/release-propose` 技能当前 Output 仍指向 `/release-status <version>`。
- `rules/release.md` 当前流程图仍为 propose → status → prepare。
