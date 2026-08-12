---
change_id: fix-miniapp-sku-detail-media-thumbnails
status: proposed
created_at: 2026-08-07 22:55:00
updated_at: 2026-08-07 22:55:00
---

# 测试计划

## 自动化测试

- `tests/test_miniapp_home.py`：覆盖 `GET /api/v1/miniapp/skus/{sku_id}` 中图片展示 URL、预览 URL、视频封面 URL、分享图和推荐卡片不回退。
- `tests/test_miniapp_static.py`：覆盖小程序详情页首屏图片绑定展示 URL、预览绑定原图 URL、视频 poster 兜底。
- 媒体读取测试：覆盖 `.thumb` URL 受控 `/media/{object_key}` 读取和缺失回退。

## 人工或设备验收

- 微信 DevTools 或真机 Network：进入 SKU 详情页后首屏图片请求路径包含 `.thumb`。
- 图片预览：点击图片后预览 URL 使用原图，展示清晰。
- 视频 SKU：视频封面请求缩略图，点击播放仍请求视频 URL。
- 媒体四联：key、object、URL、render 均记录 evidence。

## 回归范围

- 首页新品/热销商品卡片。
- 商品列表和搜索结果商品卡片。
- 品牌详情商品推荐。
- Banner 图片缩略图。
