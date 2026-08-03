---
title: 小程序商品卡片缩略图 URL 回归
purpose: 沉淀商品卡片图片性能优化后返回不可访问缩略图 URL 的事故经验
content: BUG-0094 媒体 URL 契约、pending 主图、同路径缩略图和历史回填经验
source: BUG-0094-miniapp-list-images-not-loading-after-speed-fix
update_method: 小程序商品卡片图片、缩略图生成或对象存储回填策略变化时更新
owner: 小程序与媒体链路负责人
status: draft
created_at: 2026-07-31 15:58:29
updated_at: 2026-07-31 15:58:29
---

# 小程序商品卡片缩略图 URL 回归

## 事故摘要

`BUG-0092` 为提升小程序商品卡片图片加载速度，引入列表缩略图优先策略；`BUG-0094` 证明该策略在历史 pending 主图数据上不完整：生产公开 SKU 主图存在 `images/default/tiles/pending/<uuid>.jpg`，原图对象存在，但接口返回的 `/media/thumbnails/default/tiles/pending/<uuid>.jpg` 对应对象不存在，真机商品卡片进入“暂无图片”兜底。

## 预防规则

- 列表性能优化不得只改变 URL 形态，必须验证目标媒体 URL 可通过 `/media/{object_key}` 受控读取。
- 商品列表缩略图应与原图同目录、文件名差异化，例如 `<uuid>.thumb.jpg`。
- `thumbnails/` 前缀仅作为历史兼容读取或迁移来源，不作为 pending 主图最终写入策略。
- 缩略图缺失时，后端媒体读取层应回退同目录原图；列表接口不得返回已知不可访问 URL。
- 历史数据必须有 dry-run 审计与可重入回填，输出公开 SKU、无主图、pending 主图、原图缺失、缩略图缺失、成功数、失败数和失败原因摘要。

## 验收提醒

- 小程序首页、商品列表、搜索结果和品牌详情商品区都要复用同一 `cover_image` 语义。
- 保留商品卡片 `lazy-load` 或等价延迟加载，避免恢复图片展示后回退到首屏外图片全量请求。
- 真机或体验版 Network 证据应检查实际请求路径，不只检查接口字段是否非空。
- 审计和回填日志不得输出密钥、Authorization header、Cookie、`.env` 内容或本机路径。
