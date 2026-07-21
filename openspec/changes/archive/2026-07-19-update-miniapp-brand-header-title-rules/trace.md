---
change_id: update-miniapp-brand-header-title-rules
type: update
status: proposed
source_requirement: REQ-0050-miniapp-brand-header-page-title-rules
iteration: sprint-009
created_at: 2026-07-19 18:14:48
updated_at: 2026-07-19 20:47:02
---

# Trace

```yaml
change_id: update-miniapp-brand-header-title-rules
type: update
status: proposed
source_requirement: REQ-0050-miniapp-brand-header-page-title-rules
iteration: sprint-009
capabilities:
  new: []
  modified:
    - miniapp-global-custom-navigation-bar
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
workflow_event: req.opsx
```

## 来源

| 类型 | 路径 |
|---|---|
| REQ trace | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/trace.md` |
| REQ requirement | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/requirement.md` |
| REQ acceptance | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/acceptance.md` |
| 原型 HTML | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/prototype/miniapp/brand-header-title-rules.html` |
| 原型上下文 | `issues/requirements/archive/REQ-0050-miniapp-brand-header-page-title-rules/prototype/miniapp/context.md` |

## Conflict Report

| 冲突点 | 决议 |
|---|---|
| 既有 spec 允许非首页展示品牌短标题或等价页面识别信息 | 本 Change 收窄为非首页只展示一行页面标题。 |
| 既有 spec 要求首页品牌 Logo、门店名称和品牌副文案稳定展示 | 本 Change 固定首页两行文案为 `菲尚特瓷砖馆` 与 `质感空间，由砖而生`。 |
| HTML 原型只展示首页、搜索页、商品详情页 | acceptance 覆盖 search、category、product-list、tile-detail、favorites、certificates、store-info，以 acceptance 为范围事实源。 |
| 原型中虚线胶囊用于标注避让区 | 实现不得自绘分享、关闭或系统胶囊。 |

## PNG Checklist

| 项 | 状态 | 说明 |
|---|---|---|
| PNG Golden Reference | pending | 当前仅有 HTML 原型与 context；后续实现或验收时导出 / 截图。 |
| 320 pt | done | 用户确认已完成微信开发者工具验收：返回按钮、标题和右侧胶囊避让区无重叠，内容不遮挡。 |
| 375 pt | done | 用户确认已完成微信开发者工具验收：返回按钮、标题和右侧胶囊避让区无重叠，内容不遮挡。 |
| 430 pt | done | 用户确认已完成微信开发者工具验收：返回按钮、标题和右侧胶囊避让区无重叠，内容不遮挡。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 18:14:48 | /req-opsx REQ-0050 | 创建 OpenSpec Change，生成 proposal、design、delta spec、tasks 和 trace。 |
| 2026-07-19 20:47:02 | /opsx-apply update-miniapp-brand-header-title-rules | 用户确认微信开发者工具完成 320、375、430 pt 宽度验收，补齐设备 evidence 并完成 tasks。 |
