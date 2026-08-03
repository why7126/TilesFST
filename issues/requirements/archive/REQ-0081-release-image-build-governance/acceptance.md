---
requirement_id: REQ-0081-release-image-build-governance
title: 发布镜像准备与构建治理 - 验收标准
status: done
created_at: 2026-07-29 10:07:04
updated_at: 2026-07-29 18:35:04
owner: product
---

# 验收标准

## 功能 AC

- [ ] AC-001：当发布范围包含后端、Web 构建、Dockerfile、Compose、`.env.example`、构建脚本、数据库 schema / migration、API / Orval 或离线镜像交付影响时，系统将 `image_required` 判定为 `true`。
- [ ] AC-002：当 `image_required=false` 时，`release.json` 或 image plan 中必须记录明确 rationale。
- [ ] AC-003：`/image-prepare <version>` 必须读取 `releases/<version>/release.json`，缺失时阻断并提示先完成发布计划。
- [ ] AC-004：`/image-prepare` 必须校验 `PRODUCT_VERSION`、`TILESFST_IMAGE_TAG`、`IMAGE_BUILD_TAG` 与发布版本的一致性，或记录明确差异理由。
- [ ] AC-005：`/image-prepare` 必须校验 `scripts/build-images.env.example` 的常规发版路径只要求修改 `IMAGE_BUILD_TAG`。
- [ ] AC-006：`/image-prepare` 必须生成 `releases/<version>/image-build-plan.json`，包含版本、image_required、image_tag、source_scope、build_env、input_files、input_hashes、database_impact、required_commands 和 blockers。
- [ ] AC-007：`image-build-plan.json` 不得包含真实 `.env` 内容、数据库连接串、密钥、Authorization header、Cookie 或真实客户数据。
- [ ] AC-008：`/image-build <version>` 必须读取有效 `image-build-plan.json`，缺失或过期时不得自行猜测构建输入。
- [ ] AC-009：`/image-build` 必须复用或封装 `scripts/build-images.sh` 完成 backend/web 镜像构建、平台验证、后端依赖验证、Web Nginx 验证、离线包导出和 sha256 生成。
- [ ] AC-010：`/image-build` 必须生成 `releases/<version>/image-manifest.json`，包含版本、image_tag、built_at、platform、backend_image、web_image、tarball、input_hashes、validation 和 source_plan。
- [ ] AC-011：Docker、buildx、网络或基础镜像源不可用时，`/image-build` 必须记录环境阻断和修复建议，不得写入成功证据。
- [ ] AC-012：`/release-prepare` 在 `image_required=true` 时必须要求 `image_prepare` 门禁 pass 或记录 blocker。
- [ ] AC-013：发布目标包含离线镜像包或生产镜像交付时，`/release-prepare` 或 `/release-publish` 必须要求 `image_build` 门禁 pass 或记录 blocker。
- [ ] AC-014：`/release-publish` 必须校验 manifest 的版本、tag、input_hashes 与当前发布输入一致；manifest 缺失、过期或不匹配时必须阻断发布。
- [ ] AC-015：当发布范围涉及数据库 schema 或迁移时，image plan 和 manifest 必须记录 SQLite schema、MySQL schema、迁移脚本、数据库文档和回滚说明相关输入或证据摘要。
- [ ] AC-016：人工外部构建证据只可作为受控替代证据，必须记录来源、校验方式、sha256、风险说明，且不得包含敏感连接串或密钥。
- [ ] AC-017：五个命令的依赖关系必须在 Skill 或规则文档中明确：`/release-propose` → `/release-prepare` → `/image-prepare` → `/image-build` → `/release-publish`。
- [ ] AC-018：`/release-prepare` 不得默认自动执行真实镜像构建；真实构建必须由 `/image-build` 或明确用户确认的等价流程承载。

## 非功能 AC

- [ ] AC-NF-001：构建计划、manifest、发布对象和公告均不得泄露密钥、真实 `.env`、数据库连接串、Authorization header、Cookie 或真实客户数据。
- [ ] AC-NF-002：命令输出应保持摘要化，展示版本、是否需要镜像、计划/manifest 路径、blocker 和下一步命令。
- [ ] AC-NF-003：镜像治理能力必须复用现有 `scripts/build-images.sh`、Dockerfile 和生产 Compose，不破坏既有镜像构建手册。
- [ ] AC-NF-004：输入 hash 漂移、版本不一致、manifest 过期必须作为可阻断门禁，而不是仅作为 warning。
- [ ] AC-NF-005：若实现新增或修改发布、镜像命令 Skill，必须遵守 `rules/agent-context-budget.md`，避免默认全量读取历史归档、生成物或大日志。

## 横切 AC（knowledge-base）

本 REQ 为发布 / 镜像构建 / 命令治理能力，不涉及管理端 CRUD 列表、管理端表单页、管理端弹窗或媒体上传 UI 场景；Knowledge-base UI 横切标签为 N/A，本节不新增 AC-XCUT。
