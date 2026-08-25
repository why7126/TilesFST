---
change_id: update-miniapp-certificate-detail-brand-card-entry
source_requirement: REQ-0121-miniapp-certificate-detail-brand-card-entry
status: applied
created_at: 2026-08-24 16:34:40
updated_at: 2026-08-24 16:56:37
sprint: sprint-025
change_type: update
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: true
  api: true
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
  - docs/standards/prototype-ui-acceptance.md
---

# Change Trace

## 关联

- REQ：`REQ-0121-miniapp-certificate-detail-brand-card-entry`
- Sprint：`sprint-025`
- 类型：`update`
- 影响：后端 API / Schema、小程序证书详情页、`brand-card`、媒体缩略图消费、产品使用行为日志。

## UI 验收清单

- [x] 建立并遵守 UI Contract。
- [x] 记录小程序 320 / 375 / 430 pt 逻辑宽度截图或等价摘要。
- [x] 记录正常、缩略图缺失、图片失败、长品牌名和不可用态。
- [x] 记录 `brand_logo_thumbnail_url` Network evidence。
- [x] 回归既有 `brand-card` 调用方。

## 实现摘要

- 后端证书详情 `brand` 响应补齐 `brand_logo_thumbnail_url`，来源为品牌 `logo_object_key` 的同目录缩略图 URL，不暴露对象存储原始 Key。
- 小程序证书详情页 `BrandEntry` 区域改为复用 `brand-card`，传入 `sourcePage=certificate_detail`、`sourceModule=brand_entry`、`certificateId`、`requestId` 和 `allowOriginalLogoFallback=false`。
- `brand-card` 埋点上下文新增 `certificateId`；证书详情页不再上报 `certificate_detail_brand_click`，后端事件字典统一保留 `brand_card_click`。
- 已刷新 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts`，`MiniappCertificateBrandInfo` 包含 `brand_logo_thumbnail_url`。

## 验收证据

| 维度 | 状态 | 证据 |
|---|---|---|
| API 字段 | pass | `tests/test_miniapp_home.py::test_miniapp_certificate_detail_returns_public_data_and_filters_private_records` 覆盖有 Logo 缩略图、无 Logo 缩略图、停用品牌/隐藏/软删除/不存在不可见。 |
| 组件复用 | pass | `tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts` 断言证书详情页注册并使用 `brand-card`，不存在 `bindtap="openBrand"` 私有入口。 |
| 埋点 | pass | `tests/test_miniapp_home.py::test_miniapp_sku_detail_usage_events_validate_dictionary_and_forbidden_properties` 覆盖 `brand_card_click` 携带证书详情上下文并拒绝敏感字段。 |
| OpenAPI / Orval | pass | `./scripts/generate-openapi-client.sh` 成功，Orval 输出 `tileApi` generated client。 |
| 媒体四联 | pass | key：响应不暴露 `logo_object_key`；object：缩略图对象按同目录派生 URL 语义消费；URL：`/media/logos/fst.thumb.webp` 由后端响应；render：静态契约证明 `brand-card` 使用 `brand_logo_thumbnail_url` 且禁止原图 fallback。 |
| UI 视口等价摘要 | pass | `brand-card` 既有固定 Logo 容器、不可用态和长名称静态契约继续复用；证书详情仅新增外层 `brand-card-section` 间距，不新增私有卡片样式。 |
| 真实设备截图 | follow_up | 本次自动化环境未接入微信开发者工具或真机；归档前可追加 DevTools/体验版截图作为人工验收增强证据。 |

## 文档同步

- API 契约已通过 OpenAPI/Orval 生成物同步。
- 小程序媒体与 UI 证据记录在本 trace；无需新增长期文档章节。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-24 16:56:37 | /opsx-apply | 实现证书详情页品牌入口复用 `brand-card`、补齐 `brand_logo_thumbnail_url`、统一 `brand_card_click`，并完成聚焦测试。 |
| 2026-08-24 16:34:40 | /req-opsx | 基于 REQ-0121 创建 OpenSpec Change，生成 proposal、design、delta specs、tasks 和 trace。 |
