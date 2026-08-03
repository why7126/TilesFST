---
requirement_id: REQ-0094-mintlify-versioned-docs-directory
title: Mintlify 多版本产品文档目录与站点浏览 - 用户故事
created_at: 2026-08-03 18:30:03
updated_at: 2026-08-03 18:35:14
owner: product
---

# 用户故事

## US-001 公开读者切换版本文档

作为店主、客户或公开访客，我希望在 Mintlify 文档站中一次性浏览当前版本和历史版本产品使用文档，以便确认自己正在阅读与系统版本一致的操作说明。

验收要点：

- 文档站存在清晰的产品使用文档版本入口。
- 每个版本页面明确展示或可追溯到目标版本号。
- `latest` 入口指向一个已发布且可用的全量文档版本。
- 缺少 usage docs 的历史版本不展示空页面，而是说明仅公告可用或该版本未生成使用文档。

## US-002 发布负责人保留 release 快照事实源

作为产品负责人或项目负责人，我希望 `releases/vX.Y.Z/usage-docs/` 继续作为发布文档事实源和快照，以便发布审计、历史回溯和站点投影都有稳定依据。

验收要点：

- `releases/vX.Y.Z/usage-docs/` 保留全量文档正文和 manifest。
- `manifest.json` 记录页面、截图引用、hash、来源、覆盖页面和同步状态。
- `mintlify/` 中的同版本页面可以追溯到对应 release 快照。
- 不允许绕过 release 快照直接把站点目录当作唯一事实源。

## US-003 开发维护站点目录同步

作为开发人员，我希望 usage docs 生成、更新和校验命令能把 release 快照同步或投影到 `mintlify/`，以便文档站目录、导航和 release manifest 保持一致。

验收要点：

- 生成或更新当前版本 usage docs 后，可同步或投影到 `mintlify/docs/<version>/`。
- Mintlify 配置能包含当前版本、历史版本、公告和 `latest` 入口。
- 校验命令能发现站点目录未同步、页面 hash 漂移、导航缺页和 broken links。
- 命令输出保持摘要化，明确 pass、warning、blocker 和下一步。

## US-004 文档维护者管理共享截图资产

作为文档维护者，我希望系统截图集中存放在 `mintlify/assets/screenshots/` 并按内容 hash 去重，以便多个版本复用相同截图，减少仓库体积和重复维护。

验收要点：

- `releases/vX.Y.Z/usage-docs/` 默认不直接存放大体积截图文件。
- 共享截图文件名包含内容 hash 和语义名称。
- manifest 记录截图资产的 `content_hash`、`first_used_in`、`used_by_versions`、`covered_pages`、`source_type` 和 `reuse_reason`。
- 当界面、字段、流程或权限边界变化时，必须新增截图而不是复用旧截图。

## US-005 实施和支持人员使用稳定链接

作为实施或客户支持人员，我希望每个发布版本都有稳定的站点路径，以便培训、交付和问题排查时可以发送与客户系统版本一致的文档链接。

验收要点：

- `mintlify/docs/vX.Y.Z/` 为版本固定路径，不随最新版本发布而改变语义。
- `latest` 有明确目标版本，且可追溯。
- 历史版本页面不得被新版本文档语义覆盖。
- 文档站路径避免暴露内部 OpenSpec、Sprint、Issue 或未评审状态。

## US-006 评审者确认目录治理和安全边界

作为评审者，我希望新增 `mintlify/` 一级目录前完成目录治理、文档治理和公开安全规则同步，以便不会绕过 OpenSpec 红线或公开敏感信息。

验收要点：

- 新增 `mintlify/` 前必须通过 OpenSpec Change 更新目录边界。
- `AGENTS.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`rules/release.md`、`releases/README.md` 同步说明职责边界。
- validator 能扫描 `mintlify/` 和 release manifest 中的敏感信息。
- 不公开真实客户数据、密钥、数据库连接串、Authorization header、Cookie、本地绝对路径和生产私有域名。

## US-007 部署人员通过 Docker Compose 启动文档站

作为部署或演示环境维护人员，我希望 Docker Compose 能通过明确 profile 启动 Mintlify 文档站服务，以便本地预览、演示部署或受控生产部署时可以同时访问业务系统和产品文档站。

验收要点：

- Mintlify 服务通过 `docs-site` 或等价 profile 启动，不影响默认 backend/web/minio 部署。
- 文档站服务使用 `mintlify/` 目录和 `mintlify/mint.json` 配置。
- 宿主机端口通过 `.env.example` 变量配置，不硬编码在多个文件中。
- 部署文档说明本地/演示/生产下启用 Compose 内文档站服务与外部 Mintlify/静态托管的取舍。
- 生产发布若包含该服务，必须纳入 Docker Compose 验证、发布门禁和镜像构建证据。
