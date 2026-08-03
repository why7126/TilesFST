---
sprint_id: sprint-018
title: Sprint 018 Release Note
status: published
lifecycle_stage: archive
created_at: 2026-08-03 08:40:00
updated_at: 2026-08-03 20:50:43
---

# Sprint 018 Release Note

> 发布状态：published。Sprint 018 已于 2026-08-03 20:50:43 完成归档关闭，10/10 Change 已归档。

## 发布摘要

本 Sprint 计划修复管理后台品牌列表 Logo 列显示异常：已上传 Logo 的品牌应展示图片或缩略图，不再显示 URL、对象 key、文件名或普通文本字段值。

本 Sprint 追加纳入 Mintlify 多版本产品文档站治理：新增 `mintlify/` 作为文档站源目录，保留 `releases/<version>/usage-docs/` 为发布事实源，并支持共享截图资产、`latest` 指针和 Docker Compose 可选文档站服务。

本 Sprint 追加纳入部署环境矩阵标准化：统一 `deploy/`、`deploy-local/`、`deploy-prod` 边界，明确 SQLite/MySQL 与 MinIO/COS 的本地组合、生产 Docker MySQL + 腾讯云 COS 组合，以及 Compose/env/script 的中期治理入口。

## 用户可见变化

| 范围 | 变化 |
|---|---|
| 管理后台品牌列表 | Logo 列展示品牌 Logo 图片或缩略图 |
| 管理后台品牌列表 | 未上传 Logo 或加载失败时显示稳定占位 |
| 管理后台品牌列表 | 品牌搜索、编辑入口、上下架和分页保持可用 |
| 产品使用文档站 | 支持按版本浏览产品使用文档和发布公告 |
| 本地/演示部署 | 可通过 Compose profile 启动 Mintlify 文档站预览 |
| 部署治理 | 统一本地开发与生产部署环境矩阵、env 示例、Compose 入口和 up/down/validate 脚本策略 |

## 技术影响

| 项 | 结论 |
|---|---|
| API | 默认不变；若实现发现字段契约缺失则同步 OpenAPI/Orval/docs/tests |
| DB | 不变 |
| Web 管理端 | 影响品牌列表 Logo 列 |
| 小程序 | 不影响 |
| Docker Compose | 默认不需要 |
| Docker Compose | REQ-0094 需要新增可选 docs-site profile，默认业务启动不依赖该服务 |
| Docker Compose | REQ-0093 影响 Compose 管理边界、env 示例和部署脚本入口；实现时需验证配置解析或等价脚本校验 |

## 发布风险

- 若后端响应字段与前端渲染字段不一致，Logo 可能仍无法显示。
- 若 fallback 状态缺失，图片加载失败时可能出现破图或布局跳动。
- 若 API Schema 发生变化但未同步 Orval，前端类型和运行时契约可能漂移。
- 若 deploy 目录迁移缺少兼容说明，现有 Docker Compose 命令入口可能短期不可用。
- 若 env 示例边界不清，可能误提交真实密钥、数据库文件或对象存储凭据。

## 验收要求

发布前必须按 `BUG-0105` AC-001 至 AC-006 完成回归，并记录是否需要 Orval。

REQ-0094 发布前必须按需求 AC-001 至 AC-025 和 AC-NF-001 至 AC-NF-008 验证 `releases/` 与 `mintlify/` 职责边界、站点同步、共享截图 manifest、公开安全、Compose profile 和部署文档。

REQ-0093 发布前必须按需求验收标准验证 `deploy/` 目录、local/prod 环境矩阵、env 示例、Compose/脚本入口、部署文档、安全边界和发布镜像输入追踪。

## REQ-0093 补充范围

- `REQ-0093-standardize-deployment-environment-matrix` / `standardize-deployment-environment-matrix`：建立部署环境矩阵、`deploy/` 目录治理、local/prod env 示例和 Docker Compose 脚本入口。
- 默认不新增后端 API、数据库、Web 管理端业务 UI、小程序入口或 Orval 生成。
- 若实现触及 Compose、端口、环境变量或发布镜像输入，必须同步 `.env.example`、`rules/environment.md`、`docs/02-deployment.md`、`docs/08-production-image-release.md` 和相关校验脚本。

## REQ-0094 补充范围

- `REQ-0094-mintlify-versioned-docs-directory` / `add-mintlify-versioned-docs-site`：建立 Mintlify 多版本产品文档站源目录、release 快照投影、共享截图资产和 Docker Compose 可选文档站服务。
- 默认不新增后端 API、数据库、Web 管理端业务 UI、小程序入口或 Orval 生成。
- 若实现触及 Compose、端口或环境变量，必须同步 `.env.example`、`rules/environment.md`、`rules/port-management.md` 和 `docs/02-deployment.md`。


## BUG-0110 补充范围

- `BUG-0110-miniapp-card-banner-thumbnail-usage` / `fix-miniapp-card-banner-thumbnail-usage`：小程序商品卡片、品牌卡片、证书卡片和 Banner 优先使用缩略图或符合性能策略的轻量展示图。
- 若新增或调整公开响应字段，需要同步 OpenAPI、Orval、docs 和 tests。

## BUG-0107 补充范围

- `BUG-0107-admin-certificate-list-main-image-name-only` / `fix-admin-certificate-list-main-image-name-only`：管理后台品牌证书列表证书字段仅展示证书主图/占位和证书名称。
- 证书字段不得显示图片名称、文件名称、对象 key、原始 URL 或上传控件内部文案。
- 默认不改变 API、数据库、Orval、小程序、Docker Compose 或对象存储策略。
