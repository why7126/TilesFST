---
bug_id: BUG-0131-miniapp-sku-detail-carousel-original-image-height
acceptance_status: passed
created_at: 2026-08-21 13:08:22
updated_at: 2026-08-21 14:44:50
source_change: fix-miniapp-sku-detail-carousel-original-image-height
source_sprint: sprint-024
---

# 验收标准

## 回归 AC

| 编号 | 验收项 | 状态 | 证据要求 |
|---|---|---|---|
| AC-0131-01 | 商品详情页轮播首屏图片不再优先使用小尺寸 `.thumb` 作为大图展示资源，可使用原图或详情级展示图。 | passed | 后端接口断言、小程序 WXML/TS 绑定断言、Network evidence 已覆盖。 |
| AC-0131-02 | 点击图片预览仍使用原图或等价高清预览 URL。 | passed | 小程序静态测试覆盖预览 URL 语义。 |
| AC-0131-03 | 商品列表、商品卡片、推荐位和 Banner 仍保留 `.thumb`，不引入列表加载性能回退。 | passed | 后端列表接口测试、卡片/推荐位静态测试已覆盖。 |
| AC-0131-04 | 轮播高度从固定 `680rpx` 调整为更适合瓷砖详情展示的比例，覆盖 320 到 430px 逻辑宽度视口。 | passed | 关键视口样式断言已覆盖。 |
| AC-0131-05 | 首屏仍能露出商品名称或关键商品信息，不因媒体区变高导致商品信息完全被挤出。 | passed | 小程序页面结构与高度上限断言已覆盖。 |
| AC-0131-06 | 正式规格、测试断言和媒体四联验收同步更新。 | passed | OpenSpec delta、测试通过摘要、四联验收记录已闭环。 |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0131-miniapp-sku-detail-carousel-original-image-height |
| 标题 | 小程序商品详情页轮播图清晰度不足且高度偏小 |
| 严重等级 | medium |
| 影响范围 | 小程序商品详情页 / 后端 SKU 详情接口媒体 URL 语义 / 测试与规格 |
| 复现入口 | 微信小程序商品详情页顶部轮播，示例 SKU `M612X07` |
| 受影响端 | miniapp / backend |
| 环境 | miniapp-devtools / miniapp-device / prod-like |
| 媒体类型 | image / thumbnail |
| 业务资源 | 商品详情页 SKU 图片，使用脱敏资源描述，不记录真实 object key |
| 修复前实际结果 | 详情页首屏轮播使用 `.thumb` 展示图，用户截图中纹理、边缘和展板文字发糊；轮播高度固定 `680rpx`。 |
| 修复后期望结果 | 详情页首屏使用原图或详情级展示图；点击预览仍高清；列表和卡片仍使用 `.thumb`；轮播高度更适合瓷砖详情且首屏商品信息仍可见。 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | passed | 自动化已确认响应不暴露 raw object key；脱敏原图 key 与 `.thumb` key 关系摘要作为发布前补证建议保留。 | 不记录真实密钥或未脱敏路径。 |
| object | waived | 示例 SKU 原图与 `.thumb` 的 MIME、像素尺寸、bytes 对比未连接对象存储审计；当前修复以 URL 语义和端侧渲染为闭环证据。 | 若 `.thumb` 与原图关系异常或原图本身低清，在发布验收中说明边界。 |
| URL | pass | 后端聚焦测试确认 SKU 详情图片 `media[].url` 为 `/media/tiles/1.webp`、`preview_url` 为 `/media/tiles/1.webp`，`cover_image` 和列表卡片仍为 `.thumb.webp`。 | 若后续引入详情级展示图字段，需保持预览和列表缩略图断言。 |
| render | waived | 小程序静态测试和样式断言覆盖轮播高度、详情展示 URL 与首屏信息露出；真机或体验版截图作为发布前补证建议保留。 | Release 前补充 render evidence；若无法补证，在发布验收中记录豁免说明。 |

### 非 pass 记录

- key：passed；原因：自动化可证明未暴露 raw object key，脱敏 key 关系证据作为发布前补证建议保留。
- object：waived；原因：示例 SKU 原图与 `.thumb` 的尺寸、体积和 MIME 摘要依赖对象存储审计，当前 Sprint 以 URL 语义和端侧渲染证据闭环。
- URL：pass；证据：后端聚焦测试和小程序静态测试已覆盖详情展示 URL、预览 URL、列表 `.thumb` 和媒体绑定。
- render：waived；原因：当前以静态测试和样式断言闭环，修复后 DevTools、真机或体验版 evidence 转为发布前补证建议。

## 小程序 evidence 要求

- 修复前截图：用户补充截图显示 SKU `M612X07` 商品详情页首屏图片发糊，商品名称和价格仍在首屏露出。
- 修复后必须补充：至少一张 320 到 430px 逻辑宽度范围内的首屏截图，证明图片清晰度改善且商品名称或关键商品信息仍可见。
- 如使用真机或体验版，记录设备类型、微信版本或 DevTools 版本摘要，不记录本机绝对路径、用户隐私或真实客户数据。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-21 14:44:50
accepted_by: workflow-sync
source_change: fix-miniapp-sku-detail-carousel-original-image-height
source_sprint: sprint-024
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

