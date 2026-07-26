---
change_id: add-miniapp-sku-detail-page
type: add
status: applied
created_at: 2026-07-18 19:20:46
updated_at: 2026-07-18 19:54:32
source_requirement: REQ-0044-miniapp-sku-detail-page
iteration: sprint-008
related_requirements:
  - REQ-0044-miniapp-sku-detail-page
related_bugs: []
capabilities:
  new:
    - miniapp-sku-detail-page
  modified:
    - product-usage-logging
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: possible
  storage: true
  api: true
prototype:
  type: miniapp
  paths:
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/sku-detail.html
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/prototype-context.md
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/interaction.md
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/sku-detail-main.png
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/sku-detail-preview.png
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/sku-detail-favorite.png
    - issues/requirements/archive/REQ-0044-miniapp-sku-detail-page/prototype/miniapp/sku-detail-share.png
png_checklist:
  - sku-detail-main.png
  - sku-detail-preview.png
  - sku-detail-favorite.png
  - sku-detail-share.png
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
---

# Change Trace

## Readiness

| Gate | Result | Evidence |
|---|---|---|
| Review Gate | PASS | `REQ-0044` status 为 `in_sprint`，已完成 `/req-review --approve` |
| Requirement Readiness | Ready | requirement、user-stories、business-flow、acceptance、review、trace 与 miniapp prototype 齐全 |
| Sprint Gate | PASS | `REQ-0044` 已纳入 `sprint-008`；本 Change 将同步加入 sprint changes |
| UI Explore Gate | N/A | 影响端为微信小程序，不触发 `impact.web` 的 CSS Port / DS / Asset 选择 |
| Knowledge-base Gate | N/A | 不命中管理端 `admin-list`、`admin-form`、`admin-modal`、`media-upload` 横切标签 |

## Impact Analysis

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: possible
  storage: true
  api: true
capabilities:
  new:
    - miniapp-sku-detail-page
  modified:
    - product-usage-logging
```

## Conflict Report

| Source | Decision |
|---|---|
| `miniapp-home` spec 中收藏不进入首页首期 | REQ-0044 明确 SKU 详情页收藏粒度为 SKU，本 Change 将收藏作为 SKU 详情新增能力纳入 |
| HTML / PNG / context 原型 | 作为 SKU 详情页视觉和交互最高参考；实现不得复制 Web 浏览器专属 API |
| 微信真实导航环境 | 不模拟微信系统状态栏、胶囊、分享或关闭按钮 |
| acceptance 不做项 | 购物、询价、库存、订单、支付、优惠券、促销倒计时不得实现 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-18 19:20:46 | /req-opsx | 从 REQ-0044 创建 OpenSpec Change 初稿，新增 miniapp-sku-detail-page 并扩展 product-usage-logging |
| 2026-07-18 19:54:32 | /opsx-apply | 完成 SKU 详情页后端、小程序、DB、OpenAPI/Orval、docs 和测试；`openspec validate add-miniapp-sku-detail-page --strict` 通过，`uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py` 22 passed |
