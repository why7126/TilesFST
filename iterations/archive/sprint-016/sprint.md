---
note: workflow-sync — workflow-sync 自动同步 — 3/3 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-016
title: Sprint 016 管理端 SKU 列表排序优化与媒体主图缩略图修复
status: completed
lifecycle_stage: archive
created_at: 2026-08-01 07:31:37
updated_at: 2026-08-01 08:30:46
owner: product
---

# Sprint 016 管理端 SKU 列表排序优化与媒体主图缩略图修复

## 1. Sprint 目标

本 Sprint 聚焦管理端 SKU 列表默认排序优化与公开商品主图/缩略图修复：列表先按是否上架排序，未上架 SKU 优先；未上架组内按创建时间倒序；已上架组内按发布时间倒序。同时修复公开商品主图对象 key 长期停留在 `images/default/tiles/pending/...` 的问题，并修复缩略图文件与原图大小一致的问题，确保商品主图与缩略图在绑定 SKU 后归入商品目录、真实降尺寸，并具备可迁移、可审计、可回归的媒体链路。

正式范围：

- `REQ-0087-admin-sku-list-sort-optimization`
- `BUG-0099-public-sku-main-image-key-pending-path`
- `BUG-0100-thumbnail-size-equals-original`

### REQ-0087-admin-sku-list-sort-optimization 要点

- 管理端 SKU 列表默认排序必须先展示未上架 SKU，再展示已上架 SKU。
- 未上架 SKU 内部按创建时间降序排列。
- 已上架 SKU 内部按发布时间降序排列。
- 筛选、分页、搜索、上下架操作和素材展示不因排序规则调整而回归。
- 若列表接口排序契约发生变化，必须同步 API 文档、OpenAPI、Orval 和前后端测试。

### BUG-0099-public-sku-main-image-key-pending-path 要点

- 公开商品主图不得在发布后继续使用 `images/default/tiles/pending/...` 暂存路径。
- 新建 SKU、编辑 SKU 图片、发布 SKU 或等价绑定流程必须将主图对象 key 规范到商品目录。
- 缩略图必须随原图进入同一商品目录，并生成真正小于原图的缩略图尺寸策略。
- 历史 pending 主图需要提供 dry-run/apply/idempotent 迁移能力，并保留旧对象回滚窗口。
- 验收必须覆盖对象存在、URL 可访问、小程序渲染和审计脚本口径。

### BUG-0100-thumbnail-size-equals-original 要点

- `media_type=tile-sku` 的缩略图不得继续只是复制原图字节或保持原始像素尺寸。
- 新上传 SKU 主图时必须生成真实缩小后的 `.thumb.*` 对象，并保持公开图片字段与 URL 可用。
- 历史已生成但与原图同尺寸或字节一致的 `.thumb` 对象需要支持审计与可幂等再生成。
- 缩略图策略必须覆盖 JPEG、PNG、WebP 等主要输入格式，并处理小图、透明 PNG、异常图片等边界。
- 验收必须覆盖缩略图像素尺寸小于原图、对象大小合理下降、URL 可访问和小程序渲染不回归。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0087-admin-sku-list-sort-optimization | 管理端 SKU 列表排序优化 | done | 3 人天 | archived `update-admin-sku-list-sort-optimization`（2026-08-01 08:05:03） |
| BUG | BUG-0099-public-sku-main-image-key-pending-path | 公开商品主图对象 key 仍停留在 pending 暂存路径 | done | 5 人天 | archived `fix-public-sku-main-image-pending-path`（2026-08-01 07:43:29） |
| BUG | BUG-0100-thumbnail-size-equals-original | 缩略图尺寸与原图一致导致加载优化失效 | done | 5 人天 | archived `fix-media-thumbnail-generation`（2026-08-01 08:28:07） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0087 | 管理端 SKU 列表排序优化 | P1 | done | archived `update-admin-sku-list-sort-optimization`（2026-08-01 08:05:03） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0099 | 公开商品主图对象 key 仍停留在 pending 暂存路径 | high | done | archived `fix-public-sku-main-image-pending-path`（2026-08-01 07:43:29） |
| BUG-0100 | 缩略图尺寸与原图一致导致加载优化失效 | high | done | archived `fix-media-thumbnail-generation`（2026-08-01 08:28:07） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `update-admin-sku-list-sort-optimization` | REQ-0087-admin-sku-list-sort-optimization | archived | archived `update-admin-sku-list-sort-optimization`（2026-08-01 08:05:03） |
| `fix-public-sku-main-image-pending-path` | BUG-0099-public-sku-main-image-key-pending-path | archived | archived `fix-public-sku-main-image-pending-path`（2026-08-01 07:43:29） |
| `fix-media-thumbnail-generation` | BUG-0100-thumbnail-size-equals-original | archived | archived `fix-media-thumbnail-generation`（2026-08-01 08:28:07） |
<!-- workflow-sync:scope-changes:end -->

Change：已纳入 1 个需求优化项关联 Change 与 2 个 BUG 修复 Change。执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| developers | 2 |
| testers | 1 |
| capacity_person_days | 30 |
| estimated_story_points | 13 |
| estimated_person_days | 13 |
| capacity_usage | 43.33% |
| fix_buffer_person_days | 17 |
| fix_buffer_ratio | 56.67% |

容量门禁：Pass。`project.yaml` 未提供显式 Sprint 容量，沿用 sprint-015 已确认容量基线 2 dev + 1 tester / 30 人天。本 Sprint 当前纳入 1 个 P1 REQ、2 个 P1/high BUG 与 3 个 Change，估算 13 人天，占用 43.33%，满足容量硬门禁，fix buffer 17 人天 / 56.67%，满足建议缓冲。

## 4. 里程碑

| 阶段 | 目标日期 | 交付 |
|---|---|---|
| 规划确认 | 2026-08-01 07:43:29 | Sprint 四件套、REQ/BUG/Change trace 同步 |
| 实现完成 | 2026-08-07 18:00:00 | 后端 SKU 列表排序、主图路径修复、真实缩略图生成、历史 pending/.thumb 迁移或再生成脚本与前后端/媒体链路测试完成 |
| 验收归档 | 2026-08-15 18:00:00 | Change archive、REQ/BUG archive、验收报告闭环 |

## 5. 风险

| 风险 | 缓解 |
|---|---|
| 已上架和未上架分组排序方向混淆，导致运营仍看不到最新待处理 SKU | 后端测试覆盖未上架优先、未上架 created_at 降序、已上架 published_at 降序三段样例 |
| 上下架后发布时间为空或更新时机不一致，导致已上架组内顺序不稳定 | 明确已上架使用 `published_at` 降序；缺失值处理写入实现任务和测试 |
| 前端页面自行二次排序与后端排序冲突 | 优先以后端列表排序为准；前端测试只断言展示顺序，不引入页面级临时排序 |
| API 排序契约变化后 Orval 或文档未同步 | 如响应或参数语义变化，同步 OpenAPI、Orval、docs/03-api-index.md 与相关测试 |
| 管理端列表布局横切回归 | 复用 admin-list best-practice，验收覆盖分页 DOM、指标卡、筛选下拉、fixed toast、DS confirm/window.confirm |
| pending 主图迁移后对象缺失或 URL 不可访问 | 迁移脚本先 dry-run，再 apply；验收覆盖对象存储存在性、后端媒体 URL、公开接口响应与小程序图片渲染 |
| 缩略图仍与原图同尺寸，无法形成带宽收益 | 明确缩略图最大边/质量策略，测试断言缩略图尺寸小于原图并与原图同商品目录 |
| 图片处理依赖在 Docker 镜像或 CI 环境缺失，导致缩略图生成只在本地可用 | 若新增 Pillow/libwebp 等依赖，同步 Dockerfile、锁文件和测试环境；用后端测试覆盖 JPEG/PNG/WebP 基线 |
| 透明 PNG、小图或异常图片导致缩略图质量下降或生成失败 | 对透明图片保留 alpha，对小图定义跳过或等比压缩策略，对异常图片返回明确错误并保持原图写入不破坏 |

## 6. 知识库承接

| 来源 | 承接动作 |
|---|---|
| `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 管理端 SKU 列表排序调整必须保持筛选区、表格卡片、分页、fixed toast、操作列和重置行为一致性。 |
| `docs/knowledge-base/retrospectives/sprint-015-retrospective.md` | 承接 T-015-002：管理端列表类变更在 apply 前先确认统一筛选下拉基线与目标页面差异，避免排序优化带出筛选 UI 回归。 |
| `docs/knowledge-base/best-practices/admin-media-upload-chain.md` | 媒体修复必须沿上传、API 读取、Nginx/MinIO 暴露、前端/小程序渲染整链路验证。 |
| `docs/knowledge-base/retrospectives/sprint-015-retrospective.md` | 承接 T-015-003：媒体类 BUG 使用“URL 可访问 / 对象存在 / 小程序渲染 / 性能懒加载”四联验收模板。 |
| `docs/knowledge-base/retrospectives/sprint-015-retrospective.md` | 缩略图修复需同时验证性能收益与可访问性，避免仅替换对象路径却未降低体积。 |

## 7. 横切预防清单

- [ ] admin-list：SKU 列表排序调整不改变筛选区、表格卡片、分页 DOM、状态列、素材列、操作列和 fixed toast 行为。
- [ ] sorting：未上架 SKU 必须整体排在已上架 SKU 之前。
- [ ] sorting：未上架 SKU 内按 `created_at` 降序排列。
- [ ] sorting：已上架 SKU 内按 `published_at` 降序排列。
- [ ] API：若 SKU 列表排序契约影响接口说明，必须同步 OpenAPI、Orval 与 API 文档。
- [ ] 测试：后端测试覆盖混合上架状态、同组多条记录、发布时间为空边界。
- [ ] 测试：前端回归覆盖展示顺序、分页、筛选组合和上下架后的列表刷新。
- [ ] media：公开 SKU 主图对象 key 不得保留在 `images/default/tiles/pending/`。
- [ ] media：原图与缩略图均进入商品目录，缩略图尺寸必须小于原图。
- [ ] media：`.thumb.*` 对象不得与原图字节一致，像素尺寸与对象大小需体现真实缩略策略。
- [ ] media：JPEG、PNG、WebP、小图、透明 PNG 与异常图片边界有测试或明确处理策略。
- [ ] migration：历史 pending 主图迁移支持 dry-run、apply、幂等与失败回滚窗口说明。
- [ ] migration：历史同尺寸 `.thumb` 对象审计与再生成支持 dry-run、apply、幂等与失败回滚窗口说明。
- [ ] miniapp：小程序卡片图片可正常加载，审计脚本不再报告 `pending_main_image`。

## 8. 依赖 ASCII 树

```text
REQ-0087-admin-sku-list-sort-optimization
└── update-admin-sku-list-sort-optimization
    ├── 后端 SKU 列表默认排序契约
    ├── 管理端 SKU 列表展示顺序
    ├── 条件 API / OpenAPI / Orval 同步
    └── 后端 pytest / 前端 Vitest / admin-list 横切验收

BUG-0099-public-sku-main-image-key-pending-path
└── fix-public-sku-main-image-pending-path
    ├── SKU 图片绑定目录规范化
    ├── 原图与缩略图同商品目录写入
    ├── 历史 pending 主图迁移脚本
    └── 对象存储 / URL 可访问 / 小程序渲染 / 审计脚本回归

BUG-0100-thumbnail-size-equals-original
└── fix-media-thumbnail-generation
    ├── 真实缩略图生成策略
    ├── JPEG / PNG / WebP / 小图 / 透明图边界
    ├── 历史同尺寸 .thumb 审计与再生成
    └── 对象存储 / URL 可访问 / 小程序渲染 / 带宽收益回归
```

## 9. 关联文档

- `issues/requirements/archive/REQ-0087-admin-sku-list-sort-optimization/requirement.md`
- `issues/requirements/archive/REQ-0087-admin-sku-list-sort-optimization/acceptance.md`
- `issues/requirements/archive/REQ-0087-admin-sku-list-sort-optimization/trace.md`
- `openspec/archive/2026-08-01-update-admin-sku-list-sort-optimization/proposal.md`
- `openspec/archive/2026-08-01-update-admin-sku-list-sort-optimization/design.md`
- `openspec/archive/2026-08-01-update-admin-sku-list-sort-optimization/tasks.md`
- `issues/bugs/archive/BUG-0099-public-sku-main-image-key-pending-path/bug.md`
- `issues/bugs/archive/BUG-0099-public-sku-main-image-key-pending-path/root-cause.md`
- `issues/bugs/archive/BUG-0099-public-sku-main-image-key-pending-path/acceptance.md`
- `issues/bugs/archive/BUG-0099-public-sku-main-image-key-pending-path/trace.md`
- `openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/proposal.md`
- `openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/design.md`
- `openspec/archive/2026-08-01-fix-public-sku-main-image-pending-path/tasks.md`
- `issues/bugs/archive/BUG-0100-thumbnail-size-equals-original/bug.md`
- `issues/bugs/archive/BUG-0100-thumbnail-size-equals-original/root-cause.md`
- `issues/bugs/archive/BUG-0100-thumbnail-size-equals-original/acceptance.md`
- `issues/bugs/archive/BUG-0100-thumbnail-size-equals-original/trace.md`
- `openspec/archive/2026-08-01-fix-media-thumbnail-generation/proposal.md`
- `openspec/archive/2026-08-01-fix-media-thumbnail-generation/design.md`
- `openspec/archive/2026-08-01-fix-media-thumbnail-generation/tasks.md`

## 10. 延后项

无。

## 11. 关闭记录

- 2026-08-01 08:28:07：`/sprint-archive sprint-016` readiness 通过，3/3 Change 已归档，REQ/BUG 均已进入 archive 阶段，Sprint 状态更新为 `completed`，生命周期阶段更新为 `archive`。
- AI usage：当前 Sprint snapshot 为 `estimated_fallback` 且 stale；未提供本地 session JSONL，关闭报告仅保留估算 fallback 警告。建议后续运行 `python scripts/extract-ai-usage.py --session-jsonl <local-session.jsonl> --sprint sprint-016 --json` 刷新真实用量。

## 12. 经验复盘

- 2026-08-01 09:37:42：`/sprint-exps sprint-016` 生成复盘文档 `docs/knowledge-base/retrospectives/sprint-016-retrospective.md`，沉淀媒体五联验收、archive trace gate、close stale scan 与 AI usage snapshot fresh gate 行动项。
