## Context

`REQ-0062-admin-banner-placement-scope` 已评审通过，目标是将 Banner 管理从多端运营位收敛为小程序两个轮播位：首页轮播和品牌列表页轮播。当前正式 `banner-management` spec 仍允许 `WEB_HOME`、`MINIAPP_HOME`、`TOPIC` 三个展示端；前端 `banner-display.ts` 也暴露 Web 首页、小程序首页、专题页选项；小程序首页仓库固定读取 `MINIAPP_HOME + MINIAPP_HOME_CAROUSEL`。

相关依赖：

- `REQ-0016-banner-management`：父需求，提供 Banner 管理数据模型、API、页面、弹窗和图片上传。
- `REQ-0060-brand-list-page` / `add-brand-list-page`：品牌列表页需要独立轮播来源；当前该 Change 尚未归档，曾临时复用 `MINIAPP_HOME_CAROUSEL`。
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`

原型与验收优先级：

```text
issues/requirements/archive/REQ-0062-admin-banner-placement-scope/prototype/web/prototype.html
  > prototype/web/context.md
  > acceptance.md
  > rules/ui-design.md
  > openspec/specs
```

Conflict Resolution:

- 原 `banner-management` spec 允许 Web 首页和专题页；REQ-0062 明确删除旧数据并收敛为小程序，因此本 Change 以 REQ-0062 为准。
- `add-brand-list-page` 实现说明曾选择复用 `MINIAPP_HOME_CAROUSEL`；本 Change 要求品牌列表页改用独立 `MINIAPP_BRAND_LIST_CAROUSEL`，后续 apply 时必须同步调整。
- Web 原型只表达结构策略，不作为全新 CSS Port；实现应复用现有 Banner 管理页和 DS/已有组件。

## Goals / Non-Goals

**Goals:**

- 管理端 Banner 展示端文案和可选范围只保留“小程序”。
- 展示位置只保留“首页轮播”和“品牌列表页轮播”。
- 删除旧 Banner 业务记录，不做长期兼容保留。
- 后端校验、数据库约束、前端选项和小程序查询保持一致。
- 小程序首页与品牌列表页使用独立轮播位置。
- 保留并回归 Banner 图片上传、弹窗宽度、列表分页和 fixed toast 横切质量 gate。

**Non-Goals:**

- 不新增 Banner 表。
- 不新增 Web 首页 Banner 展示能力。
- 不维护专题页 Banner。
- 不新增点击统计报表、拖拽排序或多租户投放位。
- 不物理删除 MinIO 对象作为本 Change 必做项。

## Decisions

### D1. 展示端沿用存储枚举 `MINIAPP_HOME`，管理端文案显示“小程序”

为了减少数据库字段含义迁移成本，本 Change 采用最小破坏策略：保留 `display_client=MINIAPP_HOME` 作为小程序展示端的存储值，但 UI 文案、API 文档和验收均表达为“小程序”。后端不再接受 `WEB_HOME`、`TOPIC` 或其他非小程序展示端。

备选方案：

- 新增 `display_client=MINIAPP` 并迁移所有小程序 Banner。语义更干净，但会扩大数据库迁移、历史数据映射和兼容测试范围；当前 REQ 的核心是范围收敛和位置拆分，首期不采用。

### D2. 新增 `MINIAPP_BRAND_LIST_CAROUSEL` 展示位置

在 `MINIAPP_HOME` 下允许两个位置：

- `MINIAPP_HOME_CAROUSEL`：首页轮播
- `MINIAPP_BRAND_LIST_CAROUSEL`：品牌列表页轮播

这能满足“展示端只有小程序、展示位置有两项”的产品语义，同时让首页和品牌列表页查询数据隔离。

备选方案：

- 品牌列表页继续复用首页轮播。实现简单，但违反 REQ-0062 的独立位置目标，也会让两个页面内容混用。
- 新建品牌轮播表。扩展性强，但和 Banner 管理父需求重复，不采用。

### D3. 旧数据删除通过迁移完成，删除记录不删除媒体对象

迁移应删除不在新范围内的 Banner 业务记录，并记录删除数量。删除条件至少覆盖：

- `display_client != 'MINIAPP_HOME'`
- `position NOT IN ('MINIAPP_HOME_CAROUSEL', 'MINIAPP_BRAND_LIST_CAROUSEL')`

迁移不得物理删除 `/media` 或 MinIO 对象。对象是否清理由后续运维策略处理，避免误删被 SKU、品牌或其他业务复用的素材。

### D4. 管理端复用现有 Banner 管理页，不做全新 CSS Port

`prototype/web/prototype.html` 是结构说明。实现应复用现有 `/admin/banners`、`BannerFormModal`、分页、MetricCard、fixed toast、DS confirm 和上传控件，只调整选项、默认值、文案和测试。CSS 变更只限必要适配，并继续使用 semantic token。

### D5. OpenAPI / Orval / docs / tests 作为同一交付面

展示端和展示位置影响 API 请求体、响应体、前端类型、数据库约束和小程序查询。实现完成前必须同步 OpenAPI、Orval、API 文档、数据库文档和测试，不能只改前端选项。

## Risks / Trade-offs

- [Risk] 存储枚举仍叫 `MINIAPP_HOME`，和管理端文案“小程序”存在语义差异。  
  Mitigation: 在 design、API 文档和代码常量中注明 `MINIAPP_HOME` 是兼容存储值；UI 文案统一显示“小程序”。

- [Risk] 旧数据删除不可逆，误删会影响回滚。  
  Mitigation: 迁移前记录删除条件和删除数量；应用前可通过数据库备份或迁移 dry-run 输出确认。回滚策略以数据库备份恢复为主，不自动重建旧记录。

- [Risk] `add-brand-list-page` 仍在进行中，可能继续读取首页轮播。  
  Mitigation: 本 Change tasks 必须包含品牌列表页轮播查询改造，并在 Workflow/Sprint 编排时注意与 `add-brand-list-page` 的先后关系。

- [Risk] 只改前端选项会被绕过 API 保存旧枚举。  
  Mitigation: 后端 Pydantic/Service 校验和数据库测试必须覆盖旧枚举拒绝。

- [Risk] Banner 图片上传回归。  
  Mitigation: 保留 `admin-media-upload-chain` 的 AC-XCUT，Docker `:3000` 边界上传需要验收。

## Migration Plan

1. 增加或调整 Banner 展示位置常量，允许 `MINIAPP_HOME_CAROUSEL` 与 `MINIAPP_BRAND_LIST_CAROUSEL`。
2. 增加数据迁移：删除不在小程序两个位置范围内的 Banner 业务记录，并记录删除数量。
3. 调整后端 Banner 校验、列表默认范围和 summary 统计。
4. 调整小程序首页查询只读首页轮播；品牌列表页查询只读品牌列表页轮播。
5. 调整 Web 管理端选项、默认值、文案和测试。
6. 同步 OpenAPI、Orval、API 文档、数据库文档和测试。

Rollback 策略：

- 代码回滚可恢复旧枚举逻辑，但已删除业务记录需通过数据库备份恢复。
- 本 Change 不自动恢复旧 Banner 数据；生产执行前必须确认备份或导出。

## Open Questions

- [Resolved] 展示端存储枚举首期沿用 `MINIAPP_HOME`，UI 文案显示“小程序”。
- [Resolved] 品牌列表页轮播使用新位置 `MINIAPP_BRAND_LIST_CAROUSEL`。
- [Resolved] 旧 Banner 业务记录删除，不物理删除 MinIO 对象。
- [Pending Apply] 与 `add-brand-list-page` 的实现先后关系需在 Sprint 编排中确认。
