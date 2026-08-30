---
title: 修复小程序证书列表图片 URL 回填任务
change_id: fix-miniapp-certificate-media-urls
source_bug: BUG-0147-miniapp-certificate-list-images-missing
created_at: 2026-08-30 10:44:25
updated_at: 2026-08-30 11:46:57
---

## 1. 后端公开证书列表

- [x] 1.1 复核 `GET /api/v1/miniapp/certificates` 查询层，优先聚合品牌证书主图记录，并兼容旧单文件图片字段。
- [x] 1.2 修复服务层 URL 派生，支持从可信 `file_key` 生成受控 `/media/` 原图语义 URL 与同目录 `.thumb.webp` 缩略图 URL。
- [x] 1.3 保持聚合列表卡片安全边界：图片类证书缺缩略图时返回空缩略图并由端侧占位，不把 `file_url`、原图或原文件作为卡片 fallback。
- [x] 1.4 保持 PDF/文档证书字段分流，PDF/文档不生成图片缩略图，继续使用文件占位或详情打开语义。

## 2. 历史媒体与对象存储

- [x] 2.1 复用证书媒体 dry-run 审计；本地测试收集 `tests/test_backfill_brand_certificate_thumbnails.py` 因环境缺少 `PIL` 暂无法执行。
- [x] 2.2 本次修复不执行生产写入；生产 apply 仍需先确认数据库备份和对象存储快照。
- [x] 2.3 验证图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/`，旧 key 只作为读取兼容或迁移候选。
- [x] 2.4 输出脱敏审计摘要，不记录完整 object key、密钥、连接串、Authorization header、Cookie、`.env` 或本机绝对路径。

## 3. 小程序与接口文档

- [x] 3.1 复核小程序证书列表页图片绑定，确认仅在 `thumbnail_url` 可用时渲染图片，加载失败后展示“证书”占位。
- [x] 3.2 FastAPI Schema 未变化，未运行 Orval。
- [x] 3.3 更新 `docs/03-api-index.md`，说明聚合证书列表 `file_url`、`thumbnail_url`、`file_kind`、fallback 和敏感字段过滤边界。
- [x] 3.4 记录 `product_data_collection_observability` 适用层级、N/A 原因和验证摘要。

## 4. 测试与验收

- [x] 4.1 补充后端接口测试，覆盖主图记录、旧单文件图片、空 `file_url` 但有可信 `file_key`、PDF/文档、隐藏/删除/停用过滤和敏感字段过滤。
- [x] 4.2 补充媒体派生测试，覆盖 `.thumb.webp` URL 生成、缩略图缺失返回空和不使用原文件卡片 fallback。
- [x] 4.3 补充小程序静态测试或页面测试，断言证书列表卡片不请求 `file_url` 原文件，并覆盖图片加载失败占位。
- [x] 4.4 补齐媒体四联验收：key、object、URL、render 均需有 pass/fail/blocked/n/a 状态和脱敏证据。
- [x] 4.5 开发环境使用 DevTools Network 与模拟器渲染截图完成复核；真机或体验版独立 Network evidence 属于发布验收后置项，不阻塞本 Change 开发归档。

## 5. 收尾

- [x] 5.1 运行相关后端 pytest、小程序静态测试、OpenSpec 校验、语言校验、目录结构校验和 Sprint scope 校验。
- [x] 5.2 回填 `BUG-0147` acceptance 验收结果、证据、失败项或 blocked 项。
- [x] 5.3 评估是否需要沉淀 `docs/knowledge-base/incidents/`；本次为窄范围契约修复，不新增 incident 沉淀。
