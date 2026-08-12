---
change_id: update-miniapp-recall-pinned-product-badge
status: applied
created_at: 2026-08-08 09:36:33
updated_at: 2026-08-08 10:25:00
---

# 提案：小程序召回置顶商品展示“置顶”标识

## 背景与动机

`REQ-0103` 已让小程序普通商品列表和搜索 SKU 结果支持召回置顶排序，但用户只能看到排序变化，无法识别哪些商品是被业务策略优先展示的商品。`REQ-0104` 要求对当前列表中实际生效的召回置顶商品展示固定“置顶”标识，同时保持新品商品列表和热销商品列表没有置顶逻辑、不展示置顶标识。

## 变更内容

- 在小程序公开商品卡片响应中补充“当前列表实际生效召回置顶”的展示状态字段。
- 小程序商品卡片根据后端字段展示固定文案“置顶”，不根据排序位置自行推断。
- 普通商品列表和搜索 SKU 结果中实际生效的置顶商品展示标识；非置顶商品不展示。
- 新品商品列表、热销商品列表、搜索实时联想、收藏列表不展示“置顶”标识。
- 补充后端 API、Pydantic Schema、OpenAPI/Orval、小程序类型、后端测试和小程序静态测试。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `miniapp-product-list-page`：商品列表公开数据接口与商品卡片展示需要表达和渲染召回置顶标识。
- `miniapp-search`：搜索 SKU 结果复用公开 SKU 卡片时需要展示实际生效的“置顶”标识，并保持搜索实时联想不展示。

## 影响范围

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - miniapp-product-list-page
    - miniapp-search
```

- 后端：复用 `REQ-0103` 已有召回置顶配置与排序判断，向公开商品卡片响应映射展示字段。
- API：`MiniappProductCard` 预计新增布尔字段，字段语义为“当前列表实际生效的召回置顶展示状态”。
- 小程序：商品卡片角标优先级调整，普通列表和搜索 SKU 结果展示“置顶”。
- 数据库：不新增表或字段，复用既有召回置顶字段。
- 测试：覆盖普通列表、搜索 SKU、新品榜、热销榜、缺省字段兼容和分页合并稳定性。
