---
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-30 15:36:34
---

# 提案

## 背景

发布 v1.2.2 时发现 `PRODUCT_VERSION` 与发布对象版本曾不一致，但既有 release validator 允许通过 `version_change_rationale` 放行，导致发布确认阶段没有强制阻断用户可见版本号漂移。

本变更将产品版本号一致性从“可解释偏差”收紧为发布硬门禁，覆盖 Web shared 版本源与小程序版本源，并明确版本号变更会使镜像输入失效，需要重新执行镜像准备和镜像构建。

## 变更内容

- `release-prepare` 必须校验 Web 与小程序 `PRODUCT_VERSION` 均等于目标发布版本。
- `release-publish` 在任一用户可见版本号不一致时必须阻断，不允许通过 rationale 发布。
- `scripts/validate-release.py` 增加 shared、小程序 TS 和小程序 JS 版本源一致性校验。
- 发布状态将产品版本号不一致归类为 prepare 阶段证据缺口，并给出更新版本源后重跑 `/image-prepare` 与 `/image-build` 的补救路径。
- 更新发布相关技能说明、发布规则、上下文预算摘要、AGENTS 入口摘要和治理日志。

## 能力范围

### 新增能力

- 无。

### 修改能力

- `product-release-management`: 发布准备与发布确认必须强制校验用户可见产品版本源一致。
- `agent-workflow-tooling`: release 命令输出与状态面板必须提示版本源变更后的镜像重跑要求。

## 影响范围

- 影响治理脚本、脚本测试、规则文档、命令技能和 OpenSpec delta spec。
- 不修改后端 API、数据库 schema、Web、小程序或管理端业务实现。
- 不需要 OpenAPI / Orval。
- 不需要 Docker Compose 验证。
