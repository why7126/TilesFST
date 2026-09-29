---
change_id: fix-miniapp-product-grid-image-fit
created_at: 2026-09-04 18:21:24
updated_at: 2026-09-07 22:55:02
evidence_source: static_review_pytest_and_user_screenshots
---

# 实现证据

## 代码变更

- `src/miniapp/components/product-card/index.wxml`：grid 商品图使用 `aspectFit`，compact/list 继续使用 `aspectFill`。
- `src/miniapp/components/product-card/index.wxss`：grid 图片区域改为 `aspect-ratio: 1 / 1.28`，compact 保留 `aspect-ratio: 1 / 0.86`。
- `src/miniapp/pages/product-list/index.wxss`：商品列表页骨架图片比例同步为 `1 / 1.28`，骨架卡片高度同步提高。
- `src/miniapp/pages/brand-detail/index.wxss`：品牌详情商品 Tab 骨架卡片高度同步提高。
- `tests/test_miniapp_static.py`：新增 grid/compact 图片模式、比例和骨架高度断言。

## 验证结果

```yaml
static_tests:
  command: python -m pytest tests/test_miniapp_static.py
  executed_at: 2026-09-04 18:21:24
  result: passed
  summary: 38 passed
```

## 小程序视觉证据边界

用户于 2026-09-04 23:10:06 提供小程序截图，覆盖本 BUG 的三个 grid 复用场景：

- `implementation/screenshots/home-all-products-grid.png`：首页全部产品 grid 场景。
- `implementation/screenshots/brand-detail-products-grid.png`：品牌详情商品 Tab grid 场景。
- `implementation/screenshots/product-list-grid.png`：商品列表页 grid 场景。

用户于 2026-09-04 23:21:59 补充首页全部产品 grid 多宽度截图：

- `implementation/screenshots/home-all-products-grid-552w.png`：截图像素宽度 552。
- `implementation/screenshots/home-all-products-grid-610w.png`：截图像素宽度 610。
- `implementation/screenshots/home-all-products-grid-642w.png`：截图像素宽度 642。

视觉核对结论：已提供截图中 grid 商品图主体可见，未观察到明显填充裁切、拉伸变形、商品信息遮挡或双列横向溢出。

证据边界：新增截图补充了首页全部产品 grid 的多宽度表现，但未明确标注 320、375、430 pt 逻辑宽度；品牌详情商品 Tab 与商品列表页目前各有单设备截图。因此当前证据可证明三类场景和首页多宽度 render 改善，但不能单独证明三类场景均已覆盖所有关键断点。用户于 2026-09-07 执行 `/opsx-archive BUG-0148`，作为品牌详情商品 Tab 与商品列表页多断点等价覆盖的人工验收确认；该证据不代表线上正式版或生产真机全量断点均已独立验证。
