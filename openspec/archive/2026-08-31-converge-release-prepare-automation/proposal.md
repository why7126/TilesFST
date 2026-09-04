---
created_at: 2026-08-31 09:10:00
updated_at: 2026-08-31 09:10:00
---

# 收敛发布准备自动化策略

## 背景

当前发布命令族已经将 `/release-propose` 的主线下一步调整为 `/release-prepare`，并将产品版本号同步自动化纳入 prepare 阶段。但 release 产物决策仍有残留分散点：usage docs 仍在 prepare 阶段要求人工二次确认，默认升级计划缺失时 status 面板仍倾向提示独立 `/upgrade-plan`，公告是否生成也没有形成“每版必生成或更新”的稳定默认。

这会让一次发布在 propose、prepare、status、upgrade 和 publish 之间产生不必要的人工切换。治理上需要把“发布准备阶段应当自动完成的产物”前移为 `release.json` 中的计划决策，并由 `/release-prepare` 按计划执行。

## 变更范围

- `/release-propose` 默认声明公告必生成或更新、usage docs 默认跳过、默认升级路径包含 `fresh -> <version>` 与上一正式版本到目标版本。
- `/release-propose` 增加 `--usage-docs`、`--no-usage-docs` 和可重复 `--upgrade-from <fresh|version>` 参数契约。
- `/release-prepare` 根据 `release.json` 自动同步 `PRODUCT_VERSION`、生成或更新公告、按需生成和校验 usage docs / Mintlify 投影、生成并校验默认与显式升级计划。
- `/release-status` 保持只读状态面板，缺默认或声明升级计划时把安全修复路径指向 `/release-prepare <version>`。
- `/release-publish` 仅确认发布，不写版本源，不生成主公告，不生成 usage docs，不生成 upgrade plan。
- 同步 `rules/release.md`、上下文预算规则、release 模板、校验脚本和聚焦测试。

## 非目标

- 不修改业务 `src/` 运行时代码。
- 不执行真实 Docker 镜像构建、部署升级、数据库迁移或对象存储写入。
- 不恢复 development / production 发布目标区分。
- 不要求每个版本默认生成 Mintlify 产品使用文档；usage docs 仍默认跳过，只有显式 `--usage-docs` 时生成。

## 验收

- `release.json` 模板和命令契约能表达公告、usage docs 和升级路径决策。
- release status 缺默认升级计划时，下一步指向 `/release-prepare <version>`，而不是把默认主线拆成手工 `/upgrade-plan`。
- usage docs 默认跳过不再表现为 `pending_confirmation` 决策阻塞。
- publish 阶段仍阻断缺失、无效或未校验的必需产物，但不会生成或修正文档/升级计划。
