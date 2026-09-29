---
change_id: fix-miniapp-product-grid-image-fit
acceptance_status: passed
created_at: 2026-09-04 18:08:43
updated_at: 2026-09-07 22:55:02
source_bug: BUG-0148-miniapp-product-list-card-image-fit
source_sprint: sprint-029
---

# 验收记录

## 验收范围

- 小程序商品列表页 `density="grid"` 商品卡片。
- 品牌详情商品 Tab 复用的 grid 商品卡片。
- 首页全部产品区域复用的 grid 商品卡片。
- grid 图片比例、完整适配展示、占位背景、骨架屏稳定性和小程序静态测试。

## 不适用范围

- `density="compact"`、`density="list"`、商品详情轮播、图片预览、品牌图、证书图、Banner 图。
- API、DB、Orval、对象存储、媒体 key、媒体 URL、缩略图生成和 Docker Compose。

## 媒体四联验收

| 维度 | 状态 | 证据 | 说明 |
|---|---|---|---|
| key | n/a | `implementation/evidence.md` | 不修改媒体对象 key、前缀、上传或历史映射。 |
| object | n/a | `implementation/evidence.md` | 不修改对象存储对象、MIME、大小、缩略图生成或历史对象。 |
| URL | n/a | `implementation/evidence.md` | 不修改 API、URL 生成、代理路径、签名策略或图片字段优先级。 |
| render | passed | `implementation/evidence.md`；`implementation/screenshots/home-all-products-grid.png`；`implementation/screenshots/brand-detail-products-grid.png`；`implementation/screenshots/product-list-grid.png`；`implementation/screenshots/home-all-products-grid-552w.png`；`implementation/screenshots/home-all-products-grid-610w.png`；`implementation/screenshots/home-all-products-grid-642w.png` | 已补充三类 grid 场景截图，并补充首页全部产品 grid 多宽度截图；当前证据下未见明显裁切、拉伸、遮挡或横向溢出；用户于 2026-09-07 发起归档，作为品牌详情商品 Tab 与商品列表页多断点等价覆盖的人工验收确认。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-09-07 22:55:02
accepted_by: user
evidence:
  - "静态测试：python -m pytest tests/test_miniapp_static.py，38 passed。"
  - "实现证据：openspec/changes/fix-miniapp-product-grid-image-fit/implementation/evidence.md。"
  - "截图证据：首页全部产品 grid、品牌详情商品 Tab grid、商品列表页 grid。"
  - "补充截图：首页全部产品 grid 552/610/642 像素宽度截图。"
  - "人工确认：用户于 2026-09-07 执行 /opsx-archive BUG-0148，确认该 BUG 可归档。"
failed_items: []
notes: 当前截图可支撑三类 grid 场景和首页多宽度 render 改善；品牌详情商品 Tab 与商品列表页未分别提供 320/375/430 pt 标注截图，本次以用户归档确认作为等价人工验收结论。该证据不代表线上正式版或生产真机全量断点均已独立验证。
```
