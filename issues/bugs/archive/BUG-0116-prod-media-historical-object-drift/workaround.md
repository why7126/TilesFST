---
bug_id: BUG-0116-prod-media-historical-object-drift
title: 生产历史媒体对象与缩略图存在规范漂移临时规避
severity: high
created_at: 2026-08-04 10:43:35
updated_at: 2026-08-04 10:43:35
---

# 生产历史媒体对象与缩略图存在规范漂移临时规避

## 临时规避结论

本缺陷没有可替代正式修复的前端或配置级临时规避。历史对象 key、数据库引用和对象存储缩略图需要受控批处理修复，不能通过端侧继续回退原图或手工改 URL 作为闭环。

## 可接受的临时措施

- 在正式修复前，端侧继续通过后端受控 `/media/{object_key}` 或等价媒体代理读取对象，不直连未授权对象存储。
- 对缺失同目录 `.thumb` 的媒体，若后端读取存在原图回退能力，可短期保持展示可用，但必须记录为性能和治理风险，不得视为修复完成。
- 生产批处理前必须先执行 dry-run，输出 SKU 暂存主图数量、缺失原图数量、缺失缩略图数量、同 size / 同 bytes 缩略图数量、证书图片 files 前缀数量和失败原因摘要。
- 批处理前必须完成生产数据库和对象存储备份，确认对象存储 provider、bucket、endpoint、权限和执行窗口。
- 如果生产对象存储不可读或外部数据库连接不可用，应将修复阻塞记录为 `blocked`，等待环境恢复后重跑 dry-run。

## 不允许的规避方式

- 不允许在前端、小程序或管理端硬编码对象存储公网 URL。
- 不允许把 PDF 或其他文档类证书迁移到 `images/default/brand-certificates/`。
- 不允许直接批量替换 `files/default/brand-certificates/` 前缀而不按 MIME/扩展名分流。
- 不允许只更新数据库 `object_key` 而不确认对象存储中目标 object 存在。
- 不允许只生成缩略图 key 字符串而不写入真实轻量 thumbnail object。
- 不允许在验收记录中输出生产密钥、数据库 DSN、Authorization header、Cookie、`.env` 内容、本机绝对路径或真实客户数据。

## 返修触发

出现以下任一情况时，应停止 apply 并进入返修或补充修复设计：

- dry-run 发现对象存储中原图大量缺失，无法安全迁移或生成缩略图。
- SKU 暂存 迁移后仍有公开 SKU 主图引用 `images/default/tiles/staging/`。
- 品牌 Logo 或证书图片缩略图回填后仍存在同 bytes 缩略图。
- 图片类证书迁移后仍有 JPG、PNG、WebP 留在 `files/default/brand-certificates/`。
- PDF 或文档类证书被误迁移到 `images/`。
- 管理端、店主 Web 或小程序通过 `/media/{object_key}` 读取失败。
