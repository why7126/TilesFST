---
note: workflow-sync — workflow-sync 自动同步 — 4/4 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-020
title: Sprint 020 管理端图片密集列表缩略图优化
status: completed
lifecycle_stage: archive
created_at: 2026-08-05 09:55:00
updated_at: 2026-08-06 08:30:00
---

# Sprint 020 管理端图片密集列表缩略图优化

## 1. 目标

本 Sprint 聚焦管理端媒体展示与媒体治理连续能力：一方面将管理端图片密集列表的图片资源选择统一为“列表优先缩略图，详情/编辑/预览继续使用原图”；另一方面新增全局缩略图体积上限策略，并收敛小程序残留电话与剪贴板隐私接口能力，确保提审隐私声明与真实产品口径一致。

Sprint 目标编号列表：

- REQ-0098-admin-media-list-thumbnails
- BUG-0117-miniapp-privacy-clipboard-phone-drift
- REQ-0099-global-thumbnail-size-limit
- optimize-admin-media-list-thumbnails

### REQ-0098-admin-media-list-thumbnails 要点

- SKU 列表响应新增 `main_image_thumbnail_url`。
- Banner 列表响应新增 `image_thumbnail_url`。
- SKU/Banner 列表优先加载缩略图，缺失或失败时 fallback 到原图或既有占位。
- 品牌/证书列表复核缩略图优先策略。
- 同步 OpenAPI、Orval、测试与管理端列表横切验收。

### BUG-0117-miniapp-privacy-clipboard-phone-drift 要点

- 移除小程序提交包中的 `wx.makePhoneCall` 与 `wx.setClipboardData` 残留路径。
- 收敛 `GET /api/v1/miniapp/home` 门店服务动作，不再暴露电话或复制微信号能力。
- 证书详情文件打开失败时使用稳定错误提示，不再复制文件 URL。
- 同步 OpenSpec、README、API 文档、静态测试与后端测试口径。

### REQ-0099-global-thumbnail-size-limit 要点

- 管理后台系统设置「媒体与存储」新增全局缩略图体积上限配置，默认不限制。
- 后端缩略图生成保持 `xxx.webp -> xxx.thumb.webp` 命名和 URL 推导约定，仅调整生成内容大小/质量。
- 配置对 SKU、品牌、证书、Banner 等所有后端生成缩略图链路生效。
- 配置变更默认只影响增量生成；历史对象通过维护作业显式 dry-run/apply 重生成。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0098-admin-media-list-thumbnails | 管理端图片密集列表使用缩略图展示 | done | 3 人天 | archived `optimize-admin-media-list-thumbnails`（2026-08-05 09:55:00） |
| REQ | REQ-0100-mintlify-docs-site-ia-content-experience | Mintlify 文档站信息架构与内容体验优化 | done | 3 人天 | archived `improve-mintlify-docs-site`（2026-08-05 23:29:59） |
| REQ | REQ-0099-global-thumbnail-size-limit | 全局缩略图生成支持可配置体积上限 | done | 5 人天 | archived `update-global-thumbnail-size-limit`（2026-08-05 23:33:54） |
| BUG | BUG-0117-miniapp-privacy-clipboard-phone-drift | 小程序残留电话与剪贴板隐私接口能力导致提审隐私声明不匹配 | done | 3 人天 | archived `fix-miniapp-privacy-interface-drift`（2026-08-05 18:02:03） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0098 | 管理端图片密集列表使用缩略图展示 | P1 | done | archived `optimize-admin-media-list-thumbnails`（2026-08-05 09:55:00） |
| REQ-0100 | Mintlify 文档站信息架构与内容体验优化 | P1 | done | archived `improve-mintlify-docs-site`（2026-08-05 23:29:59） |
| REQ-0099 | 全局缩略图生成支持可配置体积上限 | P1 | done | archived `update-global-thumbnail-size-limit`（2026-08-05 23:33:54） |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0117 | 小程序残留电话与剪贴板隐私接口能力导致提审隐私声明不匹配 | high | done | archived `fix-miniapp-privacy-interface-drift`（2026-08-05 18:02:03） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `optimize-admin-media-list-thumbnails` | REQ-0098-admin-media-list-thumbnails | archived | archived `optimize-admin-media-list-thumbnails`（2026-08-05 09:55:00） |
| `fix-miniapp-privacy-interface-drift` | BUG-0117-miniapp-privacy-clipboard-phone-drift | archived | archived `fix-miniapp-privacy-interface-drift`（2026-08-05 18:02:03） |
| `improve-mintlify-docs-site` | REQ-0100-mintlify-docs-site-ia-content-experience | archived | archived `improve-mintlify-docs-site`（2026-08-05 23:29:59） |
| `update-global-thumbnail-size-limit` | REQ-0099-global-thumbnail-size-limit | archived | archived `update-global-thumbnail-size-limit`（2026-08-05 23:33:54） |
<!-- workflow-sync:scope-changes:end -->

REQ：`REQ-0098`、`REQ-0100`、`REQ-0099` 已纳入正式范围；BUG：`BUG-0117` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 4 个范围项关联 Change，另有 0 个纯 Change；0 archived，0 applied，1 in_progress，3 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 指标 | 值 |
|---|---:|
| 开发 | 2 |
| 测试 | 1 |
| 容量 | 30 人天 |
| 估算 | 14 SP / 14 人天 |
| 容量占用 | 46.67% |
| fix 缓冲 | 16 人天 |

容量门禁：Pass。当前范围低于容量上限，且保留 16 人天 fix 缓冲。

## 4. 里程碑

| 阶段 | 目标日期 | 说明 |
|---|---|---|
| 规划确认 | 2026-08-19 09:00:00 | 确认 REQ-0098 与 Change 范围、API/Orval 影响 |
| 实现完成 | 2026-08-26 18:00:00 | 完成后端字段、前端展示、OpenAPI/Orval 与测试 |
| 验收完成 | 2026-09-01 18:00:00 | 完成 URL/render、管理端列表横切验收和回归测试 |
| Sprint 收尾 | 2026-09-02 18:00:00 | 准备归档与发布说明 |

## 5. 风险

| 风险 | 等级 | 缓解 |
|---|---|---|
| 缩略图字段新增后 Orval 未同步 | medium | tasks 中强制 OpenAPI/Orval 与前端类型同步 |
| 列表 fallback 处理不一致 | medium | 复用 REQ-0095 image adapter 检查口径，并补前端测试 |
| 媒体验收证据分散 | medium | acceptance 要求 URL/render 证据，复用 sprint-019 复盘经验 |
| 全局缩略图体积上限可能影响清晰度 | medium | 默认不限制；仅在配置上限时通过质量递减生成，并保留 `.thumb` URL 规则与历史显式维护入口 |
| 小程序隐私接口残留未清干净 | high | BUG-0117 acceptance 强制静态扫描 `wx.makePhoneCall` / `wx.setClipboardData`，并要求提审隐私声明复核 |

## 6. 知识库承接

| 来源 | 承接点 |
|---|---|
| docs/knowledge-base/retrospectives/sprint-019-retrospective.md | 媒体验收需要 URL/render 证据；管理端列表字段 adapter 检查表应继续接入页面验收 |
| docs/knowledge-base/best-practices/admin-list-page-consistency.md | 管理端列表分页、toast、confirm、操作列和筛选区不应因图片展示调整回归 |
| docs/knowledge-base/best-practices/admin-form-page-consistency.md | 系统设置页仅保留单一保存 CTA，恢复默认/dirty 切换使用 DS modal |
| docs/knowledge-base/best-practices/admin-media-upload-chain.md | 媒体上传链路继续走后端鉴权和对象存储适配层，不前端直连存储 |

## 7. 横切预防清单

| 标签 | 适用范围 | Gate |
|---|---|---|
| admin-list | SKU、Banner、品牌、证书列表 | 分页 DOM、fixed toast、DS confirm、无 `window.confirm`、操作列布局不回归 |
| admin-form | 系统设置「媒体与存储」Tab | 单一保存按钮、fixed toast、DS confirm、无布局抖动 |
| media-upload | SKU、品牌、证书、Banner 缩略图生成与维护作业 | `.thumb` key 规则稳定；体积上限只改变生成内容；历史重生成必须显式 dry-run/apply |
| miniapp-privacy | 小程序门店服务、证书详情文件失败兜底 | 提交包不含电话/剪贴板隐私接口，提审口径与产品能力一致 |

## 8. 依赖树

```text
REQ-0098-admin-media-list-thumbnails
└── optimize-admin-media-list-thumbnails
    ├── tile-sku-management delta spec
    ├── banner-management delta spec
    ├── OpenAPI / Orval
    └── backend + web admin tests

BUG-0117-miniapp-privacy-clipboard-phone-drift
└── fix-miniapp-privacy-interface-drift
    ├── miniapp runtime entry cleanup
    ├── backend home service/schema contract cleanup
    ├── OpenSpec / README / API docs
    └── miniapp static + backend tests

REQ-0099-global-thumbnail-size-limit
└── update-global-thumbnail-size-limit
    ├── system-settings delta spec
    ├── object-storage thumbnail generation policy
    ├── prod-media-maintenance-jobs historical regeneration option
    └── backend + admin web + Orval tests
```

## 9. 发布计划

- 本 Sprint 不单独定义产品版本号。
- 若合入发布版本，需在 release note 中说明管理端 SKU/Banner 列表图片加载体验优化。
- 若合入媒体治理版本，需说明缩略图体积上限默认不限制，启用后仅影响新生成缩略图，历史缩略图需维护作业显式重生成。
- 若合入小程序提审版本，需说明已移除电话与剪贴板隐私接口残留，支持“未采集用户隐私”口径复核。

## 10. 关联文档

- `issues/requirements/archive/REQ-0098-admin-media-list-thumbnails/`
- `issues/requirements/archive/REQ-0099-global-thumbnail-size-limit/`
- `issues/bugs/archive/BUG-0117-miniapp-privacy-clipboard-phone-drift/`
- `openspec/archive/2026-08-05-optimize-admin-media-list-thumbnails/`
- `openspec/archive/2026-08-05-update-global-thumbnail-size-limit/`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`

## 11. 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-05 17:55:13 | `/sprint-propose` | 追加 REQ-0099 到 sprint-020，估算 5 SP / 5 人天 |
| 2026-08-05 10:21:44 | `/sprint-propose` | 追加 BUG-0117 到 sprint-020，估算 3 SP / 3 人天 |
| 2026-08-05 09:55:00 | `/sprint-propose` | 创建 sprint-020 并纳入 REQ-0098 与 Change |
| 2026-08-06 08:21:16 | `/sprint-archive` | 4/4 Change 已归档；readiness、stale scan 与 issue archive promote 门禁通过；目录准备 change → archive |
| 2026-08-06 08:30:00 | `/sprint-exps` | 生成 Sprint 020 复盘：`docs/knowledge-base/retrospectives/sprint-020-retrospective.md` |
