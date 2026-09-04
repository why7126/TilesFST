---
title: PRODUCT_VERSION 发布准备自动同步设计
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 22:41:57
---

# Design: PRODUCT_VERSION 发布准备自动同步

## 决策

版本源写入归属 `/release-prepare`，因为它位于 release scope 确认之后、image stable input 固化之前。这样可以让版本号成为镜像计划和 manifest 的稳定输入，而不是发布确认阶段才发现的返修项。

## 行为设计

- `scripts/validate-release.py --sync-product-version` 读取 `releases/<version>/release.json` 的 `version`。
- 同步以下存在的版本源：
  - `src/shared/product-version.ts`
  - `src/miniapp/utils/product-version.ts`
  - `src/miniapp/utils/product-version.js`
- 同步后写入 `release.json.gates.product_version.status=pass` 与 evidence。
- 同步后写入 `release.json.product_version_sync`，记录版本、时间、文件和是否变更。
- 公告只刷新可由 release metadata 推导的版本标题与版本状态提示，不写最终发布确认、tarball sha 或人工 copy edit 内容。
- `release-publish` 继续校验版本一致性，但不写版本源。
- `image-prepare` 发现版本源未对齐时写入 blocker，要求先运行 `/release-prepare <version>`。

## 风险控制

- 自动同步只匹配 `PRODUCT_VERSION = '<version>'` / `"..."` 这类受控赋值，不做任意文本替换。
- `image-prepare` 不代写版本源，避免在镜像流程里产生隐式业务文件变更。
- `release-publish` 不写版本源，避免发布确认阶段改变镜像稳定输入。

## 验证策略

- 单测覆盖 release prepare sync 对三处版本源、release metadata 和公告版本状态的更新。
- 单测覆盖 image prepare 在版本源未对齐时生成 blocker。
- 继续运行 release / image validator、OpenSpec、目录结构、上下文预算、文档卫生、Workflow Sync 和 AI Usage hook。
