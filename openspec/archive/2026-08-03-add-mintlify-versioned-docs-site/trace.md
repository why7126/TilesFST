---
change_id: add-mintlify-versioned-docs-site
status: proposed
created_at: 2026-08-03 18:45:00
updated_at: 2026-08-03 19:40:00
source_requirement: REQ-0094-mintlify-versioned-docs-directory
source_sprint: sprint-018
source_requirement_path: issues/requirements/archive/REQ-0094-mintlify-versioned-docs-directory/
change_type: update
related_specs:
  - product-release-management
  - deployment
---

# Change Trace

## 来源

- REQ：`REQ-0094-mintlify-versioned-docs-directory`
- 评审状态：approved
- 评审文件：`issues/requirements/archive/REQ-0094-mintlify-versioned-docs-directory/review.md`
- Sprint：`sprint-018`

## 影响范围

```yaml
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
  release: true
  deployment: true
  docker_compose: true
  environment_variables: true
  media_assets: true
orval_required: false
docker_compose_validation_required: true
```

## 决策摘要

- `releases/vX.Y.Z/usage-docs/` 保留为全量发布快照和 manifest 事实源。
- 新增 `mintlify/` 作为站点源目录，承载多版本导航、`latest`、公告投影和共享截图资产。
- 截图集中到 `mintlify/assets/screenshots/`，release manifest 记录引用、hash 和复用依据。
- Mintlify Compose 服务使用 `docs-site` profile，不作为默认业务服务依赖。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-03 18:45:00 | `/req-opsx` | 基于 REQ-0094 创建 OpenSpec Change，并生成 proposal、design、delta specs、tasks 与 trace。 |
| 2026-08-03 18:55:00 | `/sprint-propose sprint-018` | Change 纳入 `sprint-018` 正式范围，满足后续 `/opsx-apply` 迭代纳入门禁。 |
| 2026-08-03 19:25:00 | `/opsx-apply` | 完成 `mintlify/` 目录、release→site 投影、共享截图 manifest、docs-site Compose profile、目录/usage docs/release 校验和测试。验证：py_compile、OpenSpec language、OpenSpec strict、directory structure、docker compose config、v0.3.3 usage docs、pytest 29 passed。`validate-release.py --release-dir releases/v0.3.3 --stage publish` 因本 Change 修改 `.env.example` 与部署文档触发历史镜像 input hash drift，按发布规范记录为后续产品版本需重新 `/image-prepare`、`/image-build`，不回写旧发布证据。 |
| 2026-08-03 19:40:00 | `/opsx-modify` | 验收返修：补齐历史 usage docs 数据迁移。新增 `--project-existing` 投影入口，并执行 `v0.3.3` 迁移，生成 `mintlify/docs/v0.3.3/`、`mintlify/docs/latest/`、公告投影和 12 个共享截图资产；`usage-docs/manifest.json` 已记录 `site_projection` 与截图 hash / site_asset / reuse_reason。 |
