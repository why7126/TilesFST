---
created_at: 2026-08-03 19:10:00
updated_at: 2026-08-05 18:40:00
purpose: Mintlify 公开产品文档站源目录说明
---

# Mintlify 文档站源目录

`mintlify/` 承载公开产品文档站源文件、Mintlify 配置、公告投影和可公开截图资产。

- `releases/vX.Y.Z/usage-docs/` 仍是版本产品使用文档事实源和发布快照。
- `mintlify/docs/vX.Y.Z/` 由 release 快照同步或投影生成。
- `mintlify/docs/latest/` 指向最新已发布且 usage docs 站点校验通过的版本。
- `mintlify/assets/screenshots/` 集中存放按内容 hash 命名的共享截图资产。

## 站点配置规则

- `mintlify/docs.json` 是唯一主配置，使用 Mintlify `mint` theme、站点色彩、favicon、版本、tabs 和 groups 组织产品化文档入口。
- `mintlify/mint.json` 已废弃，不得与 `docs.json` 同时作为站点主配置存在。

## 站点投影规则

- release 快照事实源始终是 `releases/vX.Y.Z/usage-docs/manifest.json` 与同目录 MDX；`mintlify/` 只承载公开站点投影。
- `latest` 只允许指向最新已发布、usage docs 已生成、Mintlify 导航和站点 manifest 校验通过的版本。
- `mintlify/docs/vX.Y.Z/` 是固定版本快照，生成后默认冻结；如需人工修正文案，必须在 `mintlify/site-manifest.json` 的 `manual_overrides` 或对应 release manifest 中说明原因、确认人、时间和影响文件。
- 没有 usage docs 的历史版本不得创建空目录或空页面；应在 release 治理记录中说明不可用原因。
- `mintlify/assets/screenshots/` 只放可公开真实系统截图，文件名使用 `sha256-<digest-prefix>-<semantic-name>.<ext>`；页面引用使用 `/assets/screenshots/<file>`。
- 更新 `latest`、导航或截图后，必须同步 `mintlify/site-manifest.json`，并运行 `python scripts/validate-mintlify-site.py`。
- 验收时应优先运行 Mintlify preview；若本地缺少 Mintlify CLI 或网络不可用，必须在验收记录中说明未运行原因，并至少通过静态站点校验。

## 校验边界

站点校验必须覆盖导航缺页、站内 broken links、图片引用、`latest` 指针漂移、site manifest 漂移、`.DS_Store`、构建产物和公开安全敏感模式。

本目录不得存放构建产物、真实客户数据、密钥、数据库连接串、真实 `.env`、Authorization header、Cookie、运行时数据库或不可公开运维信息。
