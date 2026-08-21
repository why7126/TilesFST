---
note: workflow-sync — workflow-sync 自动同步 — 0/1 Change archived；1 applied；Sprint `planning`
created_at: 2026-08-21 18:43:30
updated_at: 2026-08-21 22:13:10
---

# sprint-025 规划

## 1. 目标

### Sprint 目标编号列表

- REQ-0114-version-deployment-upgrade-rollback-governance

### REQ-0114-version-deployment-upgrade-rollback-governance 要点

建立版本部署升级与回滚治理能力，补齐 `from_version -> to_version` 升级路径对象、部署支持级别、首次部署计划、相邻升级与回滚计划、跨版本升级与回滚计划、env diff、数据库升级验证和回滚证据模型。能力以规范、脚本、命令技能和发布文档为主，不建设可视化升级平台，也不自动执行生产升级或修改真实生产 env。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0114-version-deployment-upgrade-rollback-governance | 版本部署升级与回滚治理能力 | in_sprint | 5 人天 | apply 24/24；待 archive `add-version-deployment-upgrade-rollback-governance` |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0114 | 版本部署升级与回滚治理能力 | P1 | in_sprint | apply 24/24；待 archive `add-version-deployment-upgrade-rollback-governance` |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-version-deployment-upgrade-rollback-governance` | REQ-0114-version-deployment-upgrade-rollback-governance | applied | apply 24/24；待 archive `add-version-deployment-upgrade-rollback-governance` |
<!-- workflow-sync:scope-changes:end -->

REQ：REQ-0114 已纳入正式范围；BUG：无；Change：待 `/req-opsx REQ-0114-version-deployment-upgrade-rollback-governance` 创建并由 Workflow Sync 回填。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 5 SP / 5 人天 |
| 容量占用 | 16.67% |
| fix 缓冲 | 25 人天 / 83.33% |

容量门禁通过。`project.yaml` 未提供显式 Sprint 容量，沿用历史 Sprint 已确认容量基线：2 dev + 1 tester / 30 人天。

## 4. 里程碑

| 阶段 | 目标 |
|---|---|
| OpenSpec | 基于 REQ-0114 创建 `add-version-deployment-upgrade-rollback-governance` Change，明确规范、脚本、命令和文档影响范围。 |
| 实现 | 补齐 upgrade 计划与校验入口、升级路径事实模型、env diff、DB 证据和回滚证据输出。 |
| 验证 | 通过脚本单测、Workflow Sync、OpenSpec 校验、发布/镜像/部署相关 dry-run 或 smoke 证据。 |
| 归档 | Change apply 后验收 AC，完成 `/opsx-archive` 与 Sprint 收尾。 |

## 5. 风险

- 跨版本升级不能仅凭幂等迁移代码宣称 supported，必须以 release 事实源、演练、DB drift/smoke、env diff 和回滚证据驱动支持级别。
- 历史版本 release 事实源可能不完整，必须保留 `verified`、`reconstructed`、`partial` 等可信度标记。
- upgrade 命令不得自动修改真实生产 env、不得自动执行生产升级、不得自动执行写入型 DB 或对象存储维护任务。
- Git tag、release.json、image manifest、PRODUCT_VERSION 和部署 env 的版本关系需要明确定义，避免事实源漂移。

## 6. 知识库承接

- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：治理命令演进也要走 OpenSpec Change，不应绕过 Sprint Inclusion Gate；本 Sprint 的 upgrade 命令与规范扩展必须按 REQ → Sprint → Change → Apply → Archive 闭环。
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：中间态文案和旧状态词会在收尾时造成 stale scan 风险；Sprint 文档和验收说明需要持续以当前事实为准。
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：跨项目或跨版本治理学习必须落为当前项目规范、脚本、技能和验证证据，不停留在探索结论。

## 7. 横切预防清单

- 发布治理证据：版本事实源、image manifest、env diff、DB drift/smoke、回滚证据必须可追溯。
- 安全输出：升级计划和回滚证据不得包含真实 `.env`、密钥、连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。
- 生产边界：命令只能生成计划和校验结果，不自动执行生产升级或写入型维护任务。
- 上下文预算：跨版本分析先定位版本范围和影响摘要，不默认全量展开历史归档、生成物、大日志或镜像 manifest 全文。
- UI 横切：不适用，本 Sprint 当前范围不包含管理端 CRUD、弹窗、媒体上传 UI 或小程序 UI。

## 8. 依赖

```text
REQ-0114 approved
  |
  v
/sprint-propose sprint-025 --req REQ-0114
  |
  v
/req-opsx REQ-0114-version-deployment-upgrade-rollback-governance
  |
  v
/opsx-apply add-version-deployment-upgrade-rollback-governance
  |
  v
/opsx-archive add-version-deployment-upgrade-rollback-governance
```

## 9. 发布计划

本 Sprint 可能影响发布治理规范、upgrade 命令、部署文档、发布文档、env diff 与 DB 校验脚本。若实现改动影响发布流程，后续 release 需要执行 `/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build` 与 `/release-publish` 对应门禁。

## 10. 关联文档

- `issues/requirements/review/REQ-0114-version-deployment-upgrade-rollback-governance/requirement.md`
- `issues/requirements/review/REQ-0114-version-deployment-upgrade-rollback-governance/acceptance.md`
- `issues/requirements/review/REQ-0114-version-deployment-upgrade-rollback-governance/trace.md`
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`
