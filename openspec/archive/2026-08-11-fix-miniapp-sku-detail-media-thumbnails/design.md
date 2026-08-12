---
change_id: fix-miniapp-sku-detail-media-thumbnails
status: proposed
created_at: 2026-08-07 22:55:00
updated_at: 2026-08-07 22:55:00
source_bug: BUG-0125-miniapp-sku-detail-media-original-load
---

# 设计说明

## 根因

详情页媒体契约没有区分首屏展示图、原图预览图、视频 URL 和视频封面 URL。后端 SKU 详情服务仍把图片 `url` 与 `preview_url` 都设为原图，小程序详情页也直接使用 `item.url` 渲染首屏大图。列表型入口已有 `.thumb` 缩略图策略，但详情页未复用。

## 修复方案

1. 后端 SKU 详情媒体构造增加展示/预览分层：
   - 图片媒体 `url` 或等价展示字段优先返回同目录 `.thumb` URL。
   - 图片媒体 `preview_url` 返回原图 URL。
   - 兜底主图场景同样遵守缩略图展示、原图预览。
2. 视频媒体保持 `url` 为视频受控 URL：
   - `cover_url` 优先使用主图缩略图。
   - 主图缩略图缺失时允许通过 `/media/{thumb_key}` 回退原图，但验收必须记录该风险。
3. 小程序详情页渲染：
   - 首屏 `<image>` 使用展示 URL。
   - `previewImage` 使用 `preview_url || url`，确保预览清晰。
   - 分享图可优先用已有分享图/封面策略，但不得暴露 object key。
4. 测试与文档：
   - 后端测试更新 SKU 详情媒体断言。
   - 小程序静态测试覆盖详情页首屏字段绑定和视频封面字段。
   - API 文档补充 SKU 详情媒体字段语义。
   - acceptance 回填媒体四联验收。

## 风险与约束

- `.thumb` 对象存在不等于真实轻量缩略图，验收必须检查对象大小、像素或 bytes 差异。
- 若历史 SKU 缺少缩略图，后端 `/media/{object_key}` 缺失回退可避免破图，但性能收益不足，需记录历史对象维护建议。
- 本修复会改变小程序公开接口字段语义和后端测试断言，属于 API 行为变更；需要同步 API 文档。小程序不使用 Orval，管理端 Web Orval 不受直接影响。

## 验证计划

- 运行后端 SKU 详情接口相关 pytest。
- 运行小程序静态测试。
- 运行 OpenSpec 校验和语言校验。
- 使用微信 DevTools 或真机记录详情页 Network evidence。
