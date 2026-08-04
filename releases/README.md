---
title: 产品版本发布目录
purpose: 说明产品版本发布对象、Mintlify 公告源文件和发布校验材料的目录边界
created_at: 2026-07-02 14:56:58
updated_at: 2026-08-03 19:10:00
owner: product
status: draft
---

# 产品版本发布目录

`releases/` 用于承载对外产品版本发布材料。一个产品版本可以合并多个 Sprint，并追踪关联 REQ、BUG 和 OpenSpec Change。

## 目录结构

```text
releases/
├── README.md
├── templates/
│   ├── release.json
│   └── announcement.mdx
└── vX.Y.Z/
    ├── release.json
    ├── announcement.mdx
    └── usage-docs/        # 仅确认需要生成或更新产品使用文档时存在
        ├── manifest.json
        ├── overview.mdx
        ├── admin/
        └── miniapp/
```

`mintlify/` 是独立的公开文档站源目录，用于承载 Mintlify 配置、多版本文档投影、`latest` 指针、公告投影和共享截图资产。`releases/` 继续作为发布对象和使用文档事实源。

## 文件职责

| 文件 | 职责 |
|---|---|
| `release.json` | 机器可读产品发布对象，记录版本、范围、门禁、影响、升级与回滚 |
| `announcement.mdx` | Mintlify 公开公告源文件 |
| `usage-docs/manifest.json` | 当前版本产品使用文档事实源，记录页面、来源、覆盖、人工维护和自动化策略 |
| `usage-docs/**/*.mdx` | 当前版本公开产品使用文档页面；会同步或投影到 `mintlify/docs/vX.Y.Z/` |

## 产品使用文档

产品使用文档通过 `releases/vX.Y.Z/usage-docs/` 按版本维护，但不是每个版本都必须生成。发版准备时先确认：

- 需要生成：运行 `/usage-docs-generate <version>` 或底层 `scripts/generate-usage-docs.py <version>`，生成 `usage-docs/**` 和 `manifest.json`，再运行 `/usage-docs-validate <version>`。
- 需要更新：运行 `/usage-docs-update <version>`，默认只更新当前版本相关页面；旧版本内容性更正必须有明确授权并写入 manifest。
- 不需要生成或更新：运行 `scripts/generate-usage-docs.py <version> --skip --rationale "<原因>" --confirmed-by "<确认来源>"` 或等价流程，只更新 `release.json` 的 `usage_docs.status=skipped` 与 `usage_docs_preview=na`，不创建空 `usage-docs/`。
- 尚未确认：记录 `usage_docs.status=pending_confirmation`，发布准备和发布确认不得伪造 generated。

生成当前版本时，若存在前一个已生成 usage docs 的版本，当前版本必须继承前版完整页面集合，再按本版本发布范围补充说明。自动选择来源版本时 MUST 只从具备 `usage-docs/manifest.json` 的历史版本中按 SemVer 语义选择小于当前版本的最近版本；相邻上一版本未生成 usage docs 时继续向更早版本查找，不得使用字符串字典序。不得只生成模板页或只保留当前版本新增/变更页面。

`域名/docs` 的真实访问由 Mintlify base path、Cloudflare/Vercel/CDN rewrite、Nginx 反向代理或等价方案承载；本仓库只维护源文件和部署边界说明，不提交外部账号、DNS、生产私有域名、密钥或凭据。

当 `usage_docs.status=generated` 时，release 快照会同步或投影到：

```text
mintlify/docs/vX.Y.Z/
mintlify/docs/latest/
mintlify/releases/vX.Y.Z/announcement.mdx
mintlify/assets/screenshots/
```

截图集中在 `mintlify/assets/screenshots/` 并按内容 hash 命名；`usage-docs/manifest.json` 记录 `site_asset`、hash、来源、覆盖页面、复用版本和复用依据。`releases/vX.Y.Z/usage-docs/assets/` 不得存在。不同版本复用同一截图时，必须确认界面、字段、操作入口、数据状态和权限边界未发生影响用户理解的变化。

## 发布门禁

发布前必须校验：

- OpenSpec Change 已 archive。
- 测试按范围执行并记录。
- API 变更已同步 OpenAPI / Orval。
- Docker Compose 与部署文档已同步。
- 数据库迁移、数据库文档和回滚说明已同步。
- `.env.example` 与相邻注释已同步。
- `src/shared/product-version.ts` 的 `PRODUCT_VERSION` 与发布对象版本一致，或记录不更新原因。
- Mintlify build / preview 或等价校验通过。
- 产品使用文档生成决策已记录：generated 需 `usage_docs_preview=pass`；skipped 需 `usage_docs_preview=na` 并记录理由；pending_confirmation 阻断发布。
- `mintlify/` 站点投影、`latest` 指针、公告投影、共享截图 hash、导航和公开安全校验通过。

## 边界

- 不替代 `iterations/` Sprint 四件套。
- 不替代 `issues/` 需求与 BUG 文档。
- 不替代 `openspec/changes/` 或 `openspec/specs/`。
- 不存放运行时生成站点、真实客户数据、密钥、数据库连接串或不可公开运维信息。
- `usage-docs/` 只包含公开产品使用说明、功能入口、操作注意事项和版本差异；内部运维、API、数据库、对象存储凭据、生产私有域名或敏感配置不得混入。
- 不把 `mintlify/` 作为 release 唯一事实源；历史版本内容性更正仍必须回到 release 快照和 manifest 留痕。
