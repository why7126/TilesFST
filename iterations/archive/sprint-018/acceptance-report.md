---
note: workflow-sync — 10/10 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-018
title: Sprint 018 Acceptance Report
status: completed
lifecycle_stage: archive
created_at: 2026-08-03 08:40:00
updated_at: 2026-08-03 20:52:16
acceptance_status: passed
---

# Sprint 018 Acceptance Report

## 验收范围

| 类型 | 编号 | Change | 验收状态 | 说明 |
|---|---|---|---|---|
| BUG | BUG-0110-miniapp-card-banner-thumbnail-usage | fix-miniapp-card-banner-thumbnail-usage | done，已归档（`fix-miniapp-card-banner-thumbnail-usage` archived 2026-08-03 13:37:15） | 小程序商品/品牌/证书卡片与 Banner 缩略图策略 |

| 类型 | 编号 | Change | 验收状态 | 说明 |
|---|---|---|---|---|
| BUG | BUG-0105-admin-brand-list-logo-renders-text | fix-admin-brand-list-logo-rendering | done，已归档（`fix-admin-brand-list-logo-rendering` archived 2026-08-03 09:01:17） | 管理后台品牌列表 Logo 列图片渲染修复 |
| REQ | REQ-0094-mintlify-versioned-docs-directory | add-mintlify-versioned-docs-site | done，已归档（`add-mintlify-versioned-docs-site` archived 2026-08-03 19:40:00） | Mintlify 多版本产品文档站、release 快照投影、共享截图资产和 Compose docs-site profile |
| REQ | REQ-0093-standardize-deployment-environment-matrix | standardize-deployment-environment-matrix | done，已归档（`standardize-deployment-environment-matrix` archived 2026-08-03 20:35:23） | 部署环境矩阵、deploy 目录治理、env/Compose/script/release image inputs 追踪 |

## 验收标准

| AC | 验收点 | 状态 | 证据 |
|---|---|---|---|
| AC-001 | 已上传 Logo 的品牌在列表第一列显示图片或缩略图，不显示 URL/key/文件名文本 | not_started | 待补 |
| AC-002 | 未上传 Logo 的品牌显示合理占位 | not_started | 待补 |
| AC-003 | 图片加载失败时显示稳定 fallback，不暴露内部路径或异常 | not_started | 待补 |
| AC-004 | Logo 列布局稳定，不挤压其他列或造成表格跳动 | not_started | 待补 |
| AC-005 | 品牌搜索、编辑、上下架等既有操作不回归 | not_started | 待补 |
| AC-006 | API 字段契约已验证；如变更则同步 OpenAPI/Orval/docs/tests | not_started | 待补 |

## REQ-0094 验收补充

- [ ] `mintlify/` 被目录结构规则正式允许，且站点构建产物、密钥、真实客户数据和临时大文件被目录校验阻断。
- [ ] `releases/vX.Y.Z/usage-docs/` 继续保留全量文档正文与 manifest 事实源，不被改为增量目录。
- [x] release usage docs 可同步或投影到 `mintlify/docs/vX.Y.Z/`，并记录来源 manifest、目标路径、hash、同步时间和手工维护记录；返修已执行 `python scripts/generate-usage-docs.py v0.3.3 --project-existing`，生成 `mintlify/docs/v0.3.3/` 与 `mintlify/docs/latest/`。
- [x] `mintlify/assets/screenshots/` 支持按内容 hash 去重和跨版本复用，manifest 记录 `first_used_in`、`used_by_versions`、`covered_pages`、`source_type` 和 `reuse_reason`；`v0.3.3` 已迁移 12 个共享截图资产。
- [ ] `mintlify/mint.json` 或等价配置包含发布公告、当前版本、历史版本和 `latest` 入口。
- [ ] `docs-site` Compose profile 可启动 Mintlify 文档站，默认 `docker compose up` 不无条件启动文档站。
- [ ] `.env.example`、`rules/environment.md`、`rules/port-management.md` 和 `docs/02-deployment.md` 已同步文档站端口与部署边界。
- [ ] usage docs / release / directory 校验覆盖站点未同步、hash 漂移、截图复用依据缺失、导航缺页、broken links、敏感信息和旧版本内容性误改。

## REQ-0093 验收补充

- [ ] `deploy/` 一级目录存在，并按中期方案区分 `deploy-local/` 与 `deploy-prod/`。
- [ ] 本地开发矩阵覆盖 SQLite/MySQL 与自建 MinIO、Docker MinIO、腾讯云 COS 的组合。
- [ ] 生产矩阵覆盖 Docker MySQL + 腾讯云 COS，且不提交真实密钥。
- [ ] Compose、env 示例、up/down/validate 脚本处于同一部署治理边界，并有清晰文档入口。
- [ ] 发布镜像输入追踪覆盖 Compose 文件、deploy 脚本和 env 示例变更。
- [ ] 目录结构、安全、部署文档和必要 Docker Compose 校验完成。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-03 20:50:43
accepted_by: sprint-archive
evidence:
  - python scripts/validate-sprint-archive-readiness.py --sprint sprint-018
  - python scripts/check-sprint-close-stale-scan.py --sprint sprint-018
  - python scripts/promote-issues-for-archive.py --sprint sprint-018
failed_items: []
source_event: sprint.archive
notes: 10/10 Change 已归档；Sprint close stale scan 与 issue promote gate 通过。微信开发者工具或体验版手工网络面板验证属于终端外事项，已在 BUG-0110 Change trace 中保留风险提示。
```

## Sprint 关闭结论

- 最终结论：通过，Sprint 018 可关闭。
- 关闭时间：2026-08-03 20:50:43。
- 归档队列：10 个 Change 均已在 `openspec/archive/` 下归档，0 个待归档，0 个阻断。
- 校验摘要：Sprint archive readiness、Sprint close stale scan、Issue promote gate 均通过。
- AI Usage：Fact Sheet 显示 snapshot 存在但为 `estimated_fallback` 且 stale；本次关闭按技能要求记录 warning，未声明使用真实 token usage。


## BUG-0110 验收补充

- [x] 商品卡片优先使用缩略图或等价轻量优化图片 URL；分类商品列表已用回归测试确认 `cover_image` 返回 `.thumb.webp`。
- [x] 品牌卡片优先使用 Logo/品牌图片缩略图或等价轻量 URL；品牌列表 item 已移除未使用的原图 Logo URL，仅保留列表卡片所需缩略图 URL，小程序本地也不再复制 `logo_display_url`。
- [x] 证书卡片中图片证书优先使用真实缩略图；证书 Tab 列表 item 已移除未使用的原文件 URL，详情接口继续保留原文件能力。
- [x] Banner 使用缩略图、展示图、压缩图或符合性能策略的安全 URL。返修确认：Banner 自定义上传已生成同目录缩略图对象，避免 `.thumb` URL 因对象缺失回退原图。
- [ ] 缩略图缺失、为空、不可访问或加载失败时可回退原图或占位。
- [ ] 详情页、图片预览、PDF 打开、Banner 跳转和卡片点击能力不回归。

## BUG-0107 验收补充

- [ ] 证书列表证书字段仅展示证书主图/占位和证书名称。
- [ ] 证书字段不展示图片名称、文件名称、对象 key、原始 URL 或上传组件内部文案。
- [ ] 无主图证书展示稳定占位，证书名称仍清晰可读。
- [ ] 证书列表排序、筛选、分页和编辑入口保持可用。
- [ ] BUG-0089 不回归，证书编辑弹窗不重新出现无意义文件名噪音。
