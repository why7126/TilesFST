---
title: PRODUCT_VERSION 发布准备自动同步 Trace
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 22:41:57
---

# Trace

## 需求来源

- 用户反馈：发布过程中不希望再由人工编辑文档或版本源来更新版本号。
- 探索结论：版本号应在 `/release-prepare <version>` 自动同步，且必须早于 `/image-prepare` 和 `/image-build`。

## 变更链路

- Change：`automate-product-version-release-prepare`
- Sprint：`sprint-029`
- 类型：纯治理 Change
- product_data_collection_observability：not_applicable
- affected_layers：无
- N/A 原因：不修改 API、DB、Web、小程序请求封装、日志审计、行为埋点或 Task Trace。

## 证据

- Release validator 增加 `--sync-product-version`。
- Image validator 增加版本源未对齐 blocker。
- Release / image 技能与发布规则同步。
- 聚焦测试覆盖自动同步与前置阻断。
