---
created_at: 2026-08-30 10:25:00
updated_at: 2026-08-30 11:13:00
---

# 提案：新增发布状态决策面板

## 摘要

为 release / image / upgrade 工作流新增只读发布状态决策面板。面板汇总当前发布目标、阶段、阻塞决策、阻塞证据、非阻塞生产 follow-up 和精确下一条命令，但不新增发布编排命令。

## 动机

现有发布工作流已经具备必要门禁，但操作者需要在 `/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build`、`/upgrade-plan`、`/upgrade-validate` 和 `/release-publish` 之间自行推断状态。尤其当仅生产环境可取得的证据出现在开发发布工作中时，流程容易显得嘈杂。

## 范围

- 新增 `/release-status <version>` 命令技能，并由只读脚本支撑。
- 定义统一的发布 blocker 分类契约。
- 为发布目标展示默认升级路径命令。
- 明确镜像 stable input 覆盖运行时、构建和部署输入，不覆盖发布证据叙述文档。
- 更新 release 规则、agent context budget 规则、相关技能、发布校验器和 spec log。

## 非目标

- 不新增 `/release-orchestrate` 或任何自动多步骤发布命令。
- 不执行部署、生产升级、数据库迁移或对象存储写入任务。
- 不修改 `src/` 下的业务运行时代码。
