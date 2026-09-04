---
title: 单一项目发布治理设计
created_at: 2026-08-30 16:10:00
updated_at: 2026-08-30 22:01:44
---

# Design: 单一项目发布治理

## 决策

发布目标不再是本项目的治理维度。Release validator 统一使用 `project` scope 表示当前项目发布语义，旧 `--target` 参数只作为兼容入口保留，不能改变门禁、状态面板、升级计划文件名或发布确认结果。

## 行为调整

- `release.json` 新对象不再要求 `release_target` 或 `production_deployment`。
- `release-status` 输出 scope、phase、blocking decisions、blocking evidence、follow-ups 和默认升级路径，不再输出 production-only follow-up。
- `upgrade-plan` 生成 `releases/<version>/upgrade-plans/<from>-to-<version>.json`。
- `validate-release.py` 查找默认升级计划时只查无后缀文件。
- `validate-release-upgrade.py` 生成和校验单一项目升级计划，保留旧 `deployment_target` 读取兼容但不作为必填门禁。

## 兼容策略

历史 release 或测试夹具中仍可能出现 `release_target`、`production_release_required`、`deployment_target`、`production_only_pending`。本次调整不要求立即清理历史事实，但 validator 不得因这些字段自动进入生产发布路径，也不得要求 `.production` 计划或 `production_deployment` 证据。

## 风险与验证

主要风险是旧技能或脚本仍给出 `--target production` / `.development.json` 命令，导致后续发布再次分叉。通过全文搜索、聚焦单测、当前 v1.2.2 release status / publish validation、upgrade plan validation、OpenSpec 与目录校验覆盖。
