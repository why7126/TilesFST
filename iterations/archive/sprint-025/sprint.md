---
note: workflow-sync — workflow-sync 自动同步 — 18/18 Change archived；0 applied；Sprint `completed`
created_at: 2026-08-21 18:43:30
updated_at: 2026-08-25 14:51:36
---

# sprint-025 规划

## 1. 目标

### Sprint 目标编号列表

- REQ-0114-version-deployment-upgrade-rollback-governance
- REQ-0115-media-multi-variant-images
- REQ-0116-workflow-opsx-linked-change-backfill
- REQ-0117-media-maintenance-storage-unreachable-summary
- REQ-0118-unified-web-miniapp-image-variant-consumption-matrix
- REQ-0119-admin-display-image-size-limit-setting
- REQ-0120-webp-derived-image-variants
- REQ-0121-miniapp-certificate-detail-brand-card-entry
- REQ-0122-batch-image-processing-runbook
- BUG-0132-miniapp-sku-detail-large-image-cold-load
- BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url
- BUG-0134-miniapp-certificate-detail-display-url
- BUG-0135-miniapp-certificate-card-file-url-fallback
- BUG-0136-workflow-sync-bug-generate-captured-draft
- BUG-0137-miniapp-lightweight-image-variant-consumption
- BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml
- tighten-sprint-propose-active-sprint-governance
- tighten-bug-review-root-cause-confirmed-gate

### REQ-0114-version-deployment-upgrade-rollback-governance 要点

建立版本部署升级与回滚治理能力，补齐 `from_version -> to_version` 升级路径对象、部署支持级别、首次部署计划、相邻升级与回滚计划、跨版本升级与回滚计划、env diff、数据库升级验证和回滚证据模型。能力以规范、脚本、命令技能和发布文档为主，不建设可视化升级平台，也不自动执行生产升级或修改真实生产 env。

### REQ-0115-media-multi-variant-images 要点

建立媒体图片 `thumbnail / display / original` 多规格展示图能力，覆盖上传后派生生成、商品/媒体 API 多规格 URL、小程序列表/详情/预览选择策略、存量图片批量生成 dry-run / apply、对象存储直出签名/缓存/权限边界与后续 CDN 预留。能力涉及后端 media、对象存储、小程序、Web 展示/管理端回显和测试验收；视频转码、多清晰度视频和生产 CDN 正式接入不纳入本期。

### BUG-0132-miniapp-sku-detail-large-image-cold-load 要点

修复小程序商品详情页冷加载存在大图资源导致图片加载耗时过长的问题，优先限制普通展示路径直接请求 1MB 以上原图，补齐 PNG 大图展示版替代、高清原图仅预览加载、首屏外详情图 lazy-load，以及媒体四联和小程序 Network evidence。该 BUG 聚焦已交付详情页性能偏差，不替代 `REQ-0115` 的通用多规格媒体能力建设。

### BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url 要点

修复小程序商品详情页品牌卡缺少 `brand_logo_thumbnail_url` 导致加载原图的问题，补齐商品详情接口品牌 Logo 缩略图字段、小程序详情页品牌数据类型与传递链路，并验证品牌卡普通展示优先请求缩略图。该 BUG 聚焦商品详情页品牌卡媒体性能偏差，不新增通用多规格媒体能力。

### BUG-0134-miniapp-certificate-detail-display-url 要点

修复小程序证书详情页顶部展示缺少 `display_url` 导致退回原图的问题，补齐证书详情接口图片媒体项展示图字段、小程序详情顶部普通展示优先级，并验证图片证书使用 `images/default/brand-certificates/`、PDF/文档证书使用 `files/default/brand-certificates/`。该 BUG 聚焦证书详情页媒体性能偏差，不新增通用多规格媒体能力。

### BUG-0135-miniapp-certificate-card-file-url-fallback 要点

修复小程序证书卡缺缩略图时 fallback 到 `file_url` 原文件的问题，统一品牌详情证书卡、证书列表和关联证书摘要的卡片展示策略：有缩略图时用缩略图，缺缩略图或加载失败时展示占位或受控失败态，不在卡片列表场景请求原文件。该 BUG 聚焦证书卡片媒体性能与原文件访问边界，不新增通用多规格媒体能力。

### BUG-0136-workflow-sync-bug-generate-captured-draft 要点

修复 Workflow Sync 对 `bug.generate` 未主动将 `captured` BUG 推进为 `draft` 的问题，确保生成 `bug.md` 后 trace、registry、当前态看板和 `bug.md` frontmatter 状态一致，并覆盖首次生成、重复生成和缺失 `bug.md` 保护场景。该 BUG 聚焦治理工作流状态同步，不涉及业务 API、DB 或 UI。

### BUG-0137-miniapp-lightweight-image-variant-consumption 要点

修复小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段的问题，补齐首页/品牌 Banner 轻量字段契约，禁止品牌 Logo 普通展示 fallback 到 `brand_logo_url` 原图，统一商品详情与证书详情分享图字段优先级，并补齐静态测试与小程序 DevTools Network/render evidence。验收返修需确认首页缺图 fallback 不再请求不存在的 `/assets/tile-placeholder.png`，而是展示视图占位或现有空态。该 BUG 聚焦媒体多规格消费矩阵返修，不新增通用派生图能力。

### BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml 要点

修复 Workflow Sync 写入 REQ trace frontmatter 时可能生成非法 YAML 结构的问题，覆盖 REQ/BUG trace frontmatter 结构化写入、标准 YAML parser 校验、顶层 Issue 状态不被 `openspec_changes[].status` 污染、已知 `REQ-0120` 异常样本修正与聚焦回归测试。该 BUG 聚焦治理工作流脚本缺陷，不涉及业务 API、DB 或 UI。

### REQ-0116-workflow-opsx-linked-change-backfill 要点

增强 `req.opsx` 与 `bug.opsx` 两条 linked Change 自动回填链路，确保 Workflow Sync 在创建或确认 Change 后幂等同步 Issue trace、`requirement.md` / `bug.md` 主文档、REQ/BUG registry 与 Sprint scope。该治理项不涉及业务 API、DB 或 UI，实现阶段需明确多 Change Issue 的 `related_change` 主值选择策略，并补齐 REQ/BUG 两条链路的聚焦测试。

### REQ-0117-media-maintenance-storage-unreachable-summary 要点

增强媒体维护 dry-run 的对象存储不可达快速失败摘要，区分 `STORAGE_UNAVAILABLE` 与对象真实不存在，要求聚合任务在顶层输出 blocked 状态、脱敏环境摘要、受影响任务和建议动作。该 P2 运维增强不新增 UI/API/DB，后续 Change 需同步生产媒体维护 runbook，并补齐对象不可达、对象缺失、聚合阻断和敏感输出保护测试。

### REQ-0118-unified-web-miniapp-image-variant-consumption-matrix 要点

沉淀 Web 与微信小程序图片三规格消费矩阵，统一 `thumbnail`、`display`、`original` 在页面、位置和图对象上的消费规则。该需求只做规范矩阵：微信小程序与 Web 管理端按真实媒体位置梳理，店主 Web 按预留规范处理，非原图目标场景不允许 fallback 到原图；不直接修改 `src/`、API、数据库或对象存储。

### REQ-0119-admin-display-image-size-limit-setting 要点

新增管理端「系统设置 - 媒体与存储」display 图体积目标上限配置，默认值沿用 768KB，并保持与 `media.thumbnail_max_size_kb` 缩略图体积目标独立。后续 Change 需要覆盖系统设置 API、Pydantic Schema、OpenAPI / Orval、管理端设置页、display 派生生成链路、历史对象维护任务读取策略、媒体与对象存储文档和聚焦测试；不改变 `.thumb` / `.display` 同目录 key/URL 模型，不在保存系统设置时自动重建历史对象。

### REQ-0120-webp-derived-image-variants 要点

将新上传 JPEG、PNG、WebP 图片的 `thumbnail` 与 `display` 派生图统一编码为 WebP，同时保留原图上传格式、MIME 和高清预览语义。后续 Change 需要覆盖 WebP 派生 key/MIME 一致性、历史图片 dry-run/apply 补生成、SVG/PDF/GIF/HEIC/TIFF/BMP 首期跳过或 fallback 策略、Web 管理端/店主 Web/小程序优先消费 WebP 派生图，以及媒体五联和小程序四联验收；不强制重建全部历史对象，不引入 AVIF 或前端直连对象存储。

### REQ-0121-miniapp-certificate-detail-brand-card-entry 要点

收敛小程序证书详情页所属品牌入口，复用既有 `brand-card` 组件，补齐证书详情 `brand` 数据中的 `brand_logo_thumbnail_url`，并统一品牌入口点击埋点为 `brand_card_click`。后续 Change 需要明确证书详情接口或页面适配层的品牌缩略图字段来源、品牌入口跳转参数、埋点参数、既有 `brand-card` 调用方回归，以及小程序媒体四联证据；不重做证书详情页整体结构，不新增通用图片派生能力。

### REQ-0122-batch-image-processing-runbook 要点

新增批量图片处理 Runbook，覆盖图片转换脚本说明、`thumb/display` 派生生成、缩略图专项重建、对象 key 迁移、生产执行步骤、安全门禁和验收证据模板，并明确长期技术文档 `docs/` 与版本使用文档快照 `releases/vX.Y.Z/usage-docs/` 两者都需要投影。后续 Change 需要确认脚本清单、未实现能力标注、生产可回滚级别、首个绑定版本和媒体上传横切 AC；不直接改源码/API/DB/对象存储，不执行生产任务。

### tighten-sprint-propose-active-sprint-governance 要点

收紧 `/sprint-propose` 的 active Sprint 默认选择、连续编号、容量硬阻断引导和归档冻结治理：未指定 Sprint 时按 active Sprint 数量选择或阻断；显式新建 Sprint 必须是最大编号加一；保留 `100%~120%` 容量风险通过区间；Sprint 归档后关联 REQ、BUG、Change 与四件套默认冻结，普通研发命令不得反向改写。

### tighten-bug-review-root-cause-confirmed-gate 要点

收紧 `/bug-review` 默认 approve 与显式 `--approve` 前的根因 confirmed 门禁：目标 BUG 必须满足 `root_cause_status: confirmed` 且证据链可定位；`unknown`、`hypothesis`、`probable`、缺少 `root-cause.md` 或缺少根因状态均阻断 approve。该治理项只修改规则、命令技能、根因证据校验脚本、聚焦测试与治理日志，不触碰业务 `src/`。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0114-version-deployment-upgrade-rollback-governance | 版本部署升级与回滚治理能力 | done | 5 人天 | archived `add-version-deployment-upgrade-rollback-governance`（2026-08-22 20:06:55） |
| REQ | REQ-0115-media-multi-variant-images | 媒体图片多规格展示图能力 | done | 5 人天 | archived `add-media-multi-variant-images`（2026-08-22 18:22:44） |
| REQ | REQ-0116-workflow-opsx-linked-change-backfill | 增强 opsx linked Change 自动回填 | done | 1 人天 | archived `update-workflow-opsx-linked-change-backfill`（2026-08-22 14:57:30） |
| REQ | REQ-0117-media-maintenance-storage-unreachable-summary | 媒体维护 dry-run 增加对象存储不可达快速摘要 | done | 1 人天 | archived `improve-media-maintenance-storage-unreachable-summary`（2026-08-22 19:37:21） |
| REQ | REQ-0118-unified-web-miniapp-image-variant-consumption-matrix | 统一 Web 与小程序图片三规格消费矩阵 | done | 1 人天 | archived `update-media-image-variant-consumption-matrix`（2026-08-22 21:31:33） |
| REQ | REQ-0119-admin-display-image-size-limit-setting | 管理端媒体与存储新增 display 图体积目标上限配置 | done | 3 人天 | archived `add-admin-display-image-size-limit-setting`（2026-08-22 22:18:00） |
| REQ | REQ-0120-webp-derived-image-variants | 图片上传生成 WebP 展示图和缩略图 | done | 3 人天 | archived `add-webp-derived-image-variants`（2026-08-25 14:18:06） |
| REQ | REQ-0121-miniapp-certificate-detail-brand-card-entry | 小程序证书详情页品牌入口复用 brand-card | done | 1 人天 | archived `update-miniapp-certificate-detail-brand-card-entry`（2026-08-24 16:56:37） |
| REQ | REQ-0122-batch-image-processing-runbook | 批量图片处理 Runbook | done | 3 人天 | archived `add-batch-image-processing-runbook`（2026-08-25 11:18:08） |
| BUG | BUG-0132-miniapp-sku-detail-large-image-cold-load | 小程序商品详情页冷加载存在大图资源导致图片加载耗时过长 | done | 3 人天 | archived `fix-miniapp-sku-detail-large-image-cold-load`（2026-08-22 19:56:51） |
| BUG | BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | 小程序商品详情页品牌卡缺少 brand_logo_thumbnail_url 导致加载原图 | done | 1 人天 | archived `fix-miniapp-sku-detail-brand-logo-thumbnail-url`（2026-08-22 21:37:04） |
| BUG | BUG-0134-miniapp-certificate-detail-display-url | 小程序证书详情页顶部展示缺少 display_url 导致退回原图 | done | 1 人天 | archived `fix-miniapp-certificate-detail-display-url`（2026-08-24 14:30:46） |
| BUG | BUG-0135-miniapp-certificate-card-file-url-fallback | 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件 | done | 1 人天 | archived `fix-miniapp-certificate-card-file-url-fallback`（2026-08-22 21:30:50） |
| BUG | BUG-0136-workflow-sync-bug-generate-captured-draft | Workflow Sync 对 bug.generate 未主动从 captured 推进 draft | done | 1 人天 | archived `fix-workflow-sync-bug-generate-status-transition`（2026-08-22 21:47:46） |
| BUG | BUG-0137-miniapp-lightweight-image-variant-consumption | 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段 | done | 3 人天 | archived `fix-miniapp-lightweight-image-variant-consumption`（2026-08-25 09:03:03） |
| BUG | BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | Workflow Sync 写入 REQ trace frontmatter 时可能生成非法 YAML 结构 | done | 1 人天 | archived `fix-workflow-sync-trace-frontmatter-invalid-yaml`（2026-08-25 10:23:18） |
| Change | tighten-sprint-propose-active-sprint-governance | tighten sprint propose active sprint governance | archived | 0.5 人天 | archived `tighten-sprint-propose-active-sprint-governance`（2026-08-22 14:12:50） |
| Change | tighten-bug-review-root-cause-confirmed-gate | tighten bug review root cause confirmed gate | archived | 0.5 人天 | archived `tighten-bug-review-root-cause-confirmed-gate`（2026-08-24 16:40:37） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0114 | 版本部署升级与回滚治理能力 | P1 | done | archived `add-version-deployment-upgrade-rollback-governance`（2026-08-22 20:06:55） |
| REQ-0115 | 媒体图片多规格展示图能力 | P1 | done | archived `add-media-multi-variant-images`（2026-08-22 18:22:44） |
| REQ-0116 | 增强 opsx linked Change 自动回填 | P1 | done | archived `update-workflow-opsx-linked-change-backfill`（2026-08-22 14:57:30） |
| REQ-0117 | 媒体维护 dry-run 增加对象存储不可达快速摘要 | P2 | done | archived `improve-media-maintenance-storage-unreachable-summary`（2026-08-22 19:37:21） |
| REQ-0118 | 统一 Web 与小程序图片三规格消费矩阵 | P1 | done | archived `update-media-image-variant-consumption-matrix`（2026-08-22 21:31:33） |
| REQ-0119 | 管理端媒体与存储新增 display 图体积目标上限配置 | P1 | done | archived `add-admin-display-image-size-limit-setting`（2026-08-22 22:18:00） |
| REQ-0120 | 图片上传生成 WebP 展示图和缩略图 | P1 | done | archived `add-webp-derived-image-variants`（2026-08-25 14:18:06） |
| REQ-0121 | 小程序证书详情页品牌入口复用 brand-card | P1 | done | archived `update-miniapp-certificate-detail-brand-card-entry`（2026-08-24 16:56:37） |
| REQ-0122 | 批量图片处理 Runbook | P1 | done | archived `add-batch-image-processing-runbook`（2026-08-25 11:18:08） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0132 | 小程序商品详情页冷加载存在大图资源导致图片加载耗时过长 | high | done | archived `fix-miniapp-sku-detail-large-image-cold-load`（2026-08-22 19:56:51） |
| BUG-0133 | 小程序商品详情页品牌卡缺少 brand_logo_thumbnail_url 导致加载原图 | high | done | archived `fix-miniapp-sku-detail-brand-logo-thumbnail-url`（2026-08-22 21:37:04） |
| BUG-0134 | 小程序证书详情页顶部展示缺少 display_url 导致退回原图 | high | done | archived `fix-miniapp-certificate-detail-display-url`（2026-08-24 14:30:46） |
| BUG-0135 | 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件 | high | done | archived `fix-miniapp-certificate-card-file-url-fallback`（2026-08-22 21:30:50） |
| BUG-0136 | Workflow Sync 对 bug.generate 未主动从 captured 推进 draft | medium | done | archived `fix-workflow-sync-bug-generate-status-transition`（2026-08-22 21:47:46） |
| BUG-0137 | 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段 | high | done | archived `fix-miniapp-lightweight-image-variant-consumption`（2026-08-25 09:03:03） |
| BUG-0138 | Workflow Sync 写入 REQ trace frontmatter 时可能生成非法 YAML 结构 | medium | done | archived `fix-workflow-sync-trace-frontmatter-invalid-yaml`（2026-08-25 10:23:18） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-version-deployment-upgrade-rollback-governance` | REQ-0114-version-deployment-upgrade-rollback-governance | archived | archived `add-version-deployment-upgrade-rollback-governance`（2026-08-22 20:06:55） |
| `add-media-multi-variant-images` | REQ-0115-media-multi-variant-images | archived | archived `add-media-multi-variant-images`（2026-08-22 18:22:44） |
| `tighten-sprint-propose-active-sprint-governance` | — | archived | archived `tighten-sprint-propose-active-sprint-governance`（2026-08-22 14:12:50） |
| `fix-miniapp-sku-detail-large-image-cold-load` | BUG-0132-miniapp-sku-detail-large-image-cold-load | archived | archived `fix-miniapp-sku-detail-large-image-cold-load`（2026-08-22 19:56:51） |
| `update-workflow-opsx-linked-change-backfill` | REQ-0116-workflow-opsx-linked-change-backfill | archived | archived `update-workflow-opsx-linked-change-backfill`（2026-08-22 14:57:30） |
| `improve-media-maintenance-storage-unreachable-summary` | REQ-0117-media-maintenance-storage-unreachable-summary | archived | archived `improve-media-maintenance-storage-unreachable-summary`（2026-08-22 19:37:21） |
| `update-media-image-variant-consumption-matrix` | REQ-0118-unified-web-miniapp-image-variant-consumption-matrix | archived | archived `update-media-image-variant-consumption-matrix`（2026-08-22 21:31:33） |
| `fix-miniapp-sku-detail-brand-logo-thumbnail-url` | BUG-0133-miniapp-sku-detail-brand-logo-thumbnail-url | archived | archived `fix-miniapp-sku-detail-brand-logo-thumbnail-url`（2026-08-22 21:37:04） |
| `fix-miniapp-certificate-detail-display-url` | BUG-0134-miniapp-certificate-detail-display-url | archived | archived `fix-miniapp-certificate-detail-display-url`（2026-08-24 14:30:46） |
| `fix-miniapp-certificate-card-file-url-fallback` | BUG-0135-miniapp-certificate-card-file-url-fallback | archived | archived `fix-miniapp-certificate-card-file-url-fallback`（2026-08-22 21:30:50） |
| `fix-workflow-sync-bug-generate-status-transition` | BUG-0136-workflow-sync-bug-generate-captured-draft | archived | archived `fix-workflow-sync-bug-generate-status-transition`（2026-08-22 21:47:46） |
| `add-admin-display-image-size-limit-setting` | REQ-0119-admin-display-image-size-limit-setting | archived | archived `add-admin-display-image-size-limit-setting`（2026-08-22 22:18:00） |
| `add-webp-derived-image-variants` | REQ-0120-webp-derived-image-variants | archived | archived `add-webp-derived-image-variants`（2026-08-25 14:18:06） |
| `update-miniapp-certificate-detail-brand-card-entry` | REQ-0121-miniapp-certificate-detail-brand-card-entry | archived | archived `update-miniapp-certificate-detail-brand-card-entry`（2026-08-24 16:56:37） |
| `tighten-bug-review-root-cause-confirmed-gate` | — | archived | archived `tighten-bug-review-root-cause-confirmed-gate`（2026-08-24 16:40:37） |
| `fix-miniapp-lightweight-image-variant-consumption` | BUG-0137-miniapp-lightweight-image-variant-consumption | archived | archived `fix-miniapp-lightweight-image-variant-consumption`（2026-08-25 09:03:03） |
| `add-batch-image-processing-runbook` | REQ-0122-batch-image-processing-runbook | archived | archived `add-batch-image-processing-runbook`（2026-08-25 11:18:08） |
| `fix-workflow-sync-trace-frontmatter-invalid-yaml` | BUG-0138-workflow-sync-trace-frontmatter-invalid-yaml | archived | archived `fix-workflow-sync-trace-frontmatter-invalid-yaml`（2026-08-25 10:23:18） |
<!-- workflow-sync:scope-changes:end -->

REQ：REQ-0114、REQ-0115、REQ-0117、REQ-0118、REQ-0119、REQ-0120、REQ-0121、REQ-0122 已纳入正式范围；BUG：BUG-0132、BUG-0133、BUG-0134、BUG-0135、BUG-0136、BUG-0137、BUG-0138 已纳入正式范围；Change：REQ-0114、REQ-0115、REQ-0117、REQ-0118、REQ-0119、REQ-0120、REQ-0121、REQ-0122、BUG-0132、BUG-0133、BUG-0134、BUG-0135、BUG-0136、BUG-0137 与 BUG-0138 已创建 OpenSpec Change 并由 Workflow Sync 回填。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 35 SP / 35 人天 |
| 容量占用 | 116.67% |
| fix 缓冲 | 0 人天 / 0% |

容量门禁风险通过。`project.yaml` 未提供显式 Sprint 容量，沿用历史 Sprint 已确认容量基线：2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 9 个 REQ、7 个 BUG 与 2 个治理 Change，估算 35 人天，占用 116.67%，处于 100%~120% 风险通过区间，fix 缓冲为 0。后续不得继续追加非紧急范围，应优先归档已完成项或拆分到 sprint-026。

## 4. 里程碑

| 阶段 | 目标 |
|---|---|
| OpenSpec | 基于 REQ-0114、REQ-0115、REQ-0116、REQ-0117、REQ-0118、REQ-0119、REQ-0120、REQ-0121、REQ-0122、BUG-0132、BUG-0133、BUG-0134、BUG-0135、BUG-0136 与 BUG-0137 创建对应 Change，明确规范、脚本、媒体服务、对象存储、小程序、系统设置、WebP 派生图、brand-card 复用、批量图片处理 Runbook、文档投影和 Workflow Sync 影响范围。 |
| 实现 | 补齐 upgrade 计划与校验入口；补齐媒体多规格生成、存量批量生成、对象存储直出能力；新增 display 图体积目标系统设置；将 thumbnail/display 派生图统一为 WebP 并保留原图格式；修复商品详情页冷加载大图问题、品牌卡 Logo 原图回退问题、证书详情顶部原图回退问题、证书卡缺缩略图原文件 fallback 问题和 `bug.generate` 状态推进问题；增强 opsx linked Change 回填同步；增加媒体维护 dry-run 对象存储不可达快速摘要；沉淀 Web 与小程序图片三规格消费矩阵；收敛证书详情页所属品牌入口复用 `brand-card` 并统一 `brand_card_click`；新增批量图片处理 Runbook 与 docs / usage-docs 投影策略。 |
| 验证 | 通过脚本单测、Workflow Sync、OpenSpec 校验、发布/镜像/部署 dry-run 或 smoke、媒体五联、小程序 Network evidence、BUG-0132、BUG-0133、BUG-0134、BUG-0135、BUG-0136 与 BUG-0137 回归验收、REQ/BUG opsx linked Change 幂等测试、对象存储不可达/对象缺失分类和敏感输出保护测试、REQ-0118 消费矩阵验收、REQ-0119 系统设置 API/管理端 UI/display 生成配置验收、REQ-0120 WebP key/object/URL/render/benefit 验收、REQ-0121 brand-card 展示/跳转/埋点/缩略图四联验收，以及 REQ-0122 Runbook 双投影、安全门禁和批处理验收模板检查。 |
| 归档 | Change apply 后验收 AC，完成 `/opsx-archive` 与 Sprint 收尾。 |

## 5. 风险

- 跨版本升级不能仅凭幂等迁移代码宣称 supported，必须以 release 事实源、演练、DB drift/smoke、env diff 和回滚证据驱动支持级别。
- 历史版本 release 事实源可能不完整，必须保留 `verified`、`reconstructed`、`partial` 等可信度标记。
- upgrade 命令不得自动修改真实生产 env、不得自动执行生产升级、不得自动执行写入型 DB 或对象存储维护任务。
- Git tag、release.json、image manifest、PRODUCT_VERSION 和部署 env 的版本关系需要明确定义，避免事实源漂移。
- 媒体多规格图不能只验证对象存在，必须同时证明 key、object、URL、render 和资源体积/耗时收益。
- 存量图片批量生成属于写入型维护能力，必须先 dry-run、脱敏输出并明确 apply 授权、幂等和失败回滚边界。
- 对象存储直出必须保持签名、缓存、公开范围和后端代理 fallback 清晰，不得让前端直连未授权对象存储。
- 媒体维护 dry-run 的对象存储不可达摘要必须区分基础设施不可达与对象真实缺失，避免误导 apply 判断。
- 图片三规格消费矩阵只沉淀规范，不应在同一 Change 中夹带 Web 或小程序实现修复；实现偏离需要后续拆分。
- 非原图目标场景不得 fallback 到原图，后续修正规格字段时需要避免把历史兜底当作性能通过证据。
- REQ-0119 追加后 fix 缓冲降至 21.67%，低于建议的 30%；若 Sprint 继续追加范围，必须重新计算容量并优先拆分或延后低优先级项。
- display 图体积目标配置不得与缩略图体积目标混用，避免列表图和详情图互相伤害性能或清晰度。
- REQ-0120 追加后 fix 缓冲降至 11.67%，虽未触发容量硬阻断，但后续不宜继续追加非阻断功能范围。
- WebP 派生图必须保持 key 扩展名、MIME 与对象内容一致；特殊格式跳过或 fallback 需要有可定位日志和验收记录。
- REQ-0121 追加后 fix 缓冲降至 8.33%，虽未触发容量硬阻断，但 sprint-025 已不适合继续追加非紧急范围；后续普通新增项应拆分到 sprint-026。
- 证书详情页品牌入口收敛必须避免与 BUG-0133、BUG-0134 的媒体修复重复或冲突，后续 Change 设计需明确字段来源、组件边界和验收证据归属。
- REQ-0122 追加后容量占用升至 113.33%，仍未触发 120% 硬阻断，但 fix 缓冲为 0；后续不得继续追加非紧急范围。
- 批量图片处理 Runbook 容易把未实现脚本写成生产可执行步骤，后续 Change 必须先盘点现有脚本、待改造脚本和待新增脚本，并明确未实现能力标注。
- Runbook 双投影必须保持 `docs/` 长期事实源与 `releases/vX.Y.Z/usage-docs/` 版本快照边界，避免版本快照反向覆盖长期技术文档或改写旧版本历史语义。

## 6. 知识库承接

- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：治理命令演进也要走 OpenSpec Change，不应绕过 Sprint Inclusion Gate；本 Sprint 的 upgrade 命令与规范扩展必须按 REQ → Sprint → Change → Apply → Archive 闭环。
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：中间态文案和旧状态词会在收尾时造成 stale scan 风险；Sprint 文档和验收说明需要持续以当前事实为准。
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`：跨项目或跨版本治理学习必须落为当前项目规范、脚本、技能和验证证据，不停留在探索结论。
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`：媒体上传必须覆盖状态机、同会话回显、Docker Web `:3000` 边界、object key 与受控 URL 一致性。
- `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`：小程序媒体性能必须覆盖 key、object、URL、render 四联，并补 DevTools、体验版或真机 Network evidence。
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：后续若基于 REQ-0118 修正管理端列表媒体列，必须保持分页 DOM、toast、confirm 和列展示契约。
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`：后续若基于 REQ-0118 修正管理端弹窗回显，必须避免 `modal-card` 与专属类并存并补 computed width 验收。
- `docs/knowledge-base/retrospectives/sprint-022-retrospective.md`：BUG-0125 / BUG-0126 证明“有缩略图对象”不等于页面真的使用缩略图，验收需记录端上实际请求与渲染。

## 7. 横切预防清单

- 发布治理证据：版本事实源、image manifest、env diff、DB drift/smoke、回滚证据必须可追溯。
- 安全输出：升级计划和回滚证据不得包含真实 `.env`、密钥、连接串、Authorization header、Cookie、本机绝对路径或真实客户数据。
- 生产边界：命令只能生成计划和校验结果，不自动执行生产升级或写入型维护任务。
- 上下文预算：跨版本分析先定位版本范围和影响摘要，不默认全量展开历史归档、生成物、大日志或镜像 manifest 全文。
- 媒体上传横切：上传或派生生成入口必须覆盖 `idle -> uploading -> done / failed`、同会话即时回显、Docker Web `:3000` 边界文件验收和对象存储标准前缀。
- 小程序媒体横切：列表、详情、预览必须分别验证 `thumbnail_url`、`display_url`、`original_url` 的 Network evidence、fallback 和 lazy-load。
- 图片规格矩阵横切：列表/卡片/推荐位使用 `thumbnail`，详情普通展示使用 `display`，预览/下载/保真查看使用 `original`；非原图目标场景不允许原图 fallback。
- 管理端表单横切：REQ-0119 实现时必须保持系统设置页单一 footer 保存 CTA、DS modal 恢复默认/dirty 确认、fixed toast 无 layout shift。
- display 配置横切：REQ-0119 实现时必须验证 `media.display_max_size_kb` 或等价字段与 `media.thumbnail_max_size_kb` 独立，并记录新上传 `.display` 的 key/object/URL/render evidence。
- WebP 派生横切：REQ-0120 实现时必须验证原图格式保留、`.thumb.webp` / `.display.webp` 或等价 key、`image/webp` MIME、多端优先消费派生 URL 和历史补生成 dry-run/apply 幂等证据。
- Runbook 横切：REQ-0122 实现时必须覆盖图片转换、thumb/display 派生、缩略图重建、对象 key 迁移、生产执行、安全门禁和验收证据模板，并区分 docs 长期事实源与 release usage-docs 快照投影。
- UI 横切：REQ-0115 如进入管理端上传状态或小程序展示改造，后续 Change 必须补 UI Contract、关键交互和截图证据。

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

REQ-0115 approved
  |
  v
/sprint-propose sprint-025 --req REQ-0115
  |
  v
/req-opsx REQ-0115-media-multi-variant-images
  |
  v
/opsx-apply REQ-0115
  |
  v
/opsx-archive REQ-0115
```

## 9. 发布计划

本 Sprint 可能影响发布治理规范、upgrade 命令、部署文档、发布文档、env diff、DB 校验脚本、媒体上传/读取接口、小程序媒体加载策略和对象存储访问策略。若实现改动影响发布流程，后续 release 需要执行 `/release-propose`、`/release-prepare`、`/image-prepare`、`/image-build` 与 `/release-publish` 对应门禁；若影响小程序生产体验，还需要执行 `/miniapp-prepare` 或等价发布前检查。

## 10. 关联文档

- `issues/requirements/archive/REQ-0114-version-deployment-upgrade-rollback-governance/requirement.md`
- `issues/requirements/archive/REQ-0114-version-deployment-upgrade-rollback-governance/acceptance.md`
- `issues/requirements/archive/REQ-0114-version-deployment-upgrade-rollback-governance/trace.md`
- `issues/requirements/archive/REQ-0115-media-multi-variant-images/requirement.md`
- `issues/requirements/archive/REQ-0115-media-multi-variant-images/acceptance.md`
- `issues/requirements/archive/REQ-0115-media-multi-variant-images/trace.md`
- `issues/requirements/archive/REQ-0119-admin-display-image-size-limit-setting/requirement.md`
- `issues/requirements/archive/REQ-0119-admin-display-image-size-limit-setting/acceptance.md`
- `issues/requirements/archive/REQ-0119-admin-display-image-size-limit-setting/trace.md`
- `issues/requirements/archive/REQ-0120-webp-derived-image-variants/requirement.md`
- `issues/requirements/archive/REQ-0120-webp-derived-image-variants/acceptance.md`
- `issues/requirements/archive/REQ-0120-webp-derived-image-variants/trace.md`
- `docs/knowledge-base/retrospectives/sprint-024-retrospective.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

## 11. 关闭记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-25 14:45:16 | /sprint-archive sprint-025 | 18/18 Change 已归档；readiness、stale scan 与 issue promote gate 通过；AI usage snapshot 缺失，按 estimated_fallback 警告记录。 |
