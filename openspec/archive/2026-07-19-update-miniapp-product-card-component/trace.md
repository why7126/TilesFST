---
change_id: update-miniapp-product-card-component
type: update
status: proposed
created_at: 2026-07-19 18:09:44
updated_at: 2026-07-19 18:09:44
source_requirement: REQ-0049-miniapp-product-card-component
sprint: sprint-009
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-product-list-page
    - miniapp-search
    - miniapp-home
    - miniapp-sku-detail-page
---

# Trace

```yaml
change_id: update-miniapp-product-card-component
type: update
status: proposed
source_requirement: REQ-0049-miniapp-product-card-component
sprint: sprint-009
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-product-list-page
    - miniapp-search
    - miniapp-home
    - miniapp-sku-detail-page
```

## Requirement Readiness Report

| 项 | 结果 |
|---|---|
| Readiness | ready |
| 门禁状态 | `in_sprint`，且 lifecycle 已记录 approved |
| 六件套 | requirement、user-stories、business-flow、acceptance、trace 均存在 |
| 原型 | `prototype/miniapp/` 存在，含 HTML、PNG、context、interaction |
| 是否可创建 Change | 是 |

## Impact Analysis

```yaml
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new: []
  modified:
    - miniapp-product-list-page
    - miniapp-search
    - miniapp-home
    - miniapp-sku-detail-page
```

## Prototype Conflict Report

| 来源 | 结论 | 处理 |
|---|---|---|
| HTML 原型 | 深色卡片、固定比例图片、品牌金价格、图片失败和不可查看状态明确 | 写入 design D5 与 delta spec |
| PNG Golden Reference | 已存在 `prototype/miniapp/prototype.png`，作为实现验收参考 | 实现阶段补充 DevTools/真机 evidence |
| context.md | 明确 ProductCard 结构、状态和视觉优先级 | 吸收为组件边界 |
| interaction.md | 标签最多 3 个，优先级为规格 > 材质 > 工艺 > 风格 | 吸收为辅助标签规则 |
| acceptance.md | 要求多列表复用、字段兜底、图片占位、跳转、埋点和无交易快捷操作 | 全量覆盖到 spec 与 tasks |

## PNG / Device Evidence Checklist

- [ ] 320px 小屏卡片文字可读。
- [ ] 分类商品列表复用商品卡片。
- [ ] 搜索结果 SKU 列表复用商品卡片。
- [ ] 首页新品、热销或全部产品区复用商品卡片。
- [ ] 图片失败展示统一占位且不影响其他卡片。
- [ ] 不可查看卡片禁用跳转并给出反馈。
- [ ] 卡片内无收藏、分享、询价、购物车、联系客服或在线下单快捷按钮。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 18:09:44 | /req-opsx | 基于 REQ-0049 创建 OpenSpec Change 草案 |
