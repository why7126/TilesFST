---
purpose: add-miniapp-home 实现证据
content: 记录 API、DB、小程序、测试、Orval 与范围控制验收结果
source: /opsx-apply add-miniapp-home
created_at: 2026-07-16 10:21:50
updated_at: 2026-07-16 10:21:50
---

# add-miniapp-home 实现证据

## API / 数据

| 项 | 结果 |
|---|---|
| 首页聚合接口 | `GET /api/v1/miniapp/home`，返回门店摘要、Banner、快捷入口、服务区、新品和热销商品 |
| 搜索接口 | `GET /api/v1/miniapp/products`，支持 `keyword`、`filter_type`、`filter_value`、`section` |
| 商品详情接口 | `GET /api/v1/miniapp/products/{product_id}`，仅返回公开商品字段 |
| 行为事件 | `product_detail_view`、`home_share`、`product_share`、`home_contact_click`、`product_contact_click` 已加入事件字典 |
| 热销排序 | 复用 `usage_events`，详情访问、分享、咨询作为辅助排序；无事件时按更新时间/ID 降级 |
| DB schema | 未新增表；复用 `tiles`、`tile_images`、`banners`、`usage_events` |
| Orval | 已运行 `./scripts/generate-openapi-client.sh` |

公开响应不包含 `remark`、后台状态、库存管理字段、raw object key、Authorization、Cookie 或原始手机号。

## 小程序

| 页面 | 结果 |
|---|---|
| `pages/index/index` | 首页首屏、搜索、Banner、快捷入口、新品、热销、品牌服务、加载/错误/空态 |
| `pages/search/index` | 搜索页与快捷筛选结果 |
| `pages/tile-detail/index` | 商品详情、分享、咨询、详情访问埋点 |
| `pages/store-info/index` | 门店摘要与咨询入口 |
| TabBar | 首页、分类、找砖、我的；无收藏 Tab |

## 范围控制

| 不做项 | 结果 |
|---|---|
| 收藏按钮 / 收藏状态 / 收藏列表 / 收藏统计 | 未实现；静态测试覆盖 `favorite` / `收藏` 缺失 |
| 预约表单 | 未实现；静态测试覆盖 `appointment` / `预约` 缺失 |
| 到店询价规则 | 未实现；价格缺失时仅展示 `到店咨询` |
| 快捷入口后台配置 / 服务入口后台配置 | 未实现；快捷入口为固定默认入口 |
| 复杂用户画像 | 未实现 |
| 收藏驱动热销算法 | 未实现；热销只使用 usage events 和时间/排序降级 |

## 测试与验证

| 命令 | 结果 |
|---|---|
| `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py` | 7 passed |

布局验证采用小程序静态 smoke 方式记录：

- `app.json` 覆盖首页、搜索、商品详情、门店信息和 TabBar。
- 首页、搜索、详情、门店页主按钮/卡片设置 `min-height: 88rpx` 或更高，满足 44pt 触控目标。
- 详情页底部操作栏使用 `env(safe-area-inset-bottom)` 预留安全区。
- 页面样式使用固定宽度约束、`overflow: hidden`、省略和 grid/flex 布局，覆盖 320-430 pt 宽度的无横向滚动/重叠风险。

Docker Compose 验证：N/A。本次未修改代理、环境变量、Nginx、对象存储或容器网络边界。
