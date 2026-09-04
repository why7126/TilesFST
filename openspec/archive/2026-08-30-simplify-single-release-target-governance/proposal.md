---
title: 收敛单一项目发布治理
created_at: 2026-08-30 16:10:00
updated_at: 2026-08-30 22:01:44
---

# Proposal: 收敛单一项目发布治理

## 背景

本项目当前不会区分 development / production 发布目标。早前为了分层证据与发布安全引入的 `release_target`、`production_deployment`、`production_only_pending`、升级计划 `.development` / `.production` 文件名后缀，在本项目语境下会制造不必要的双轨发布认知。

## 目标

- 发布治理统一为单一项目发布语义。
- Release / upgrade 命令不再要求或推荐 `--target development|production`。
- `release-publish` 不再存在生产环境专属门禁，只校验当前项目发布事实、用户可见版本号、镜像、升级计划、公告和公开安全。
- 升级计划文件名收敛为 `<from>-to-<to>.json`。
- 历史 `release_target`、`deployment_target`、`production_only_pending` 字段仅作为兼容输入，不再产生额外发布分支或阻塞。

## 非目标

- 不修改业务 `src/`。
- 不执行真实部署、数据库升级、镜像构建或环境变更。
- 不删除历史归档 changelog 中已经发生过的开发/生产分离事实。

## 影响范围

- 发布与升级治理规则。
- Release / upgrade 相关技能说明。
- Release / upgrade validator 和聚焦测试。
- v1.2.2 release 事实源与升级计划命名。
- Sprint scope、OpenSpec delta 和规范工程日志。
