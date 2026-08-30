---
title: 修复小程序证书列表图片 URL 回填设计
change_id: fix-miniapp-certificate-media-urls
source_bug: BUG-0147-miniapp-certificate-list-images-missing
created_at: 2026-08-30 10:44:25
updated_at: 2026-08-30 10:44:25
---

# 根因与目标

根因已在 `BUG-0147` 中确认为数据契约缺口：公开证书列表 API 能识别图片类证书，但列表聚合链路只依赖 `record.file_url` 推导 `thumbnail_url`，当生产历史记录 `file_url` 为空、主图记录未被聚合或 key 前缀不匹配时，图片类证书返回 `thumbnail_url: null`。小程序端按规范不使用 `file_url` 原文件兜底，因此全部显示占位。

本 Change 目标是让图片类证书列表项在存在可信媒体来源时返回真实轻量缩略图，同时保留卡片不拉原文件、公开接口不暴露敏感字段和历史对象修复可审计的边界。

# 修复方案

## 后端列表聚合

- 查询层优先选择 `brand_certificate_images` 的唯一主图；没有主图时按既有排序选择可公开图片记录；最后才兼容旧单文件图片字段。
- URL 派生以可信 `file_key` 为优先来源，支持 `images/default/brand-certificates/` 标准前缀和已保存的完整旧 key 读取兼容。
- 对图片类证书生成同目录 `.thumb.webp` 缩略图 URL；当缩略图对象缺失或无法确认时返回 `thumbnail_url: null`，并让端侧继续展示占位。
- 聚合列表继续默认返回 `file_url: null` 或仅保留预览语义需要的受控 URL，不得让卡片图片字段 fallback 到原图或原文件。

## 历史媒体回填

- 修复阶段先对生产或等价数据执行 dry-run，统计图片证书、PDF/文档证书、空 URL、非标准 key、缺 `.thumb.webp`、object 缺失和可幂等补齐数量。
- 需要写入时，apply 必须在备份确认后执行，并输出成功、失败、跳过、重试候选和失败分类脱敏摘要。
- 二次 dry-run 或 audit 必须证明幂等，且不得默认删除旧对象。

## 小程序渲染

- 证书列表页保持现有安全策略：`file_kind == "image"` 且 `thumbnail_url` 非空才渲染图片。
- 图片加载失败继续进入“证书”占位，不二次请求 `file_url`、`original_url` 或 raw object URL。
- 验收需要小程序 DevTools、真机或体验版截图 / Network evidence；无法真机时标注 blocked 或 follow-up。

## 产品数据采集与链路观测

- 直接 API 请求必须进入 `request_logs`，路径模板覆盖 `/api/v1/miniapp/certificates`，错误摘要和元数据不得包含完整 object key、Authorization header、Cookie、`.env` 或本机路径。
- 小程序列表页已有浏览和加载失败行为事件时，修复不得破坏 `requestId` 透传和证书图片加载失败事件。
- 若新增或调整媒体回填维护命令，该命令属于 `maintenance_jobs`，应记录脱敏执行摘要；批量 apply 或多步骤任务应接入 Task Trace 或说明 N/A 原因。

# 测试策略

- 后端接口测试覆盖图片证书主图记录、旧单文件图片、空 `file_url` 但有可信 `file_key`、PDF/文档证书、隐藏/删除/停用过滤和敏感字段过滤。
- 媒体 URL 测试覆盖 `.thumb.webp` 派生规则、非标准 key 兼容、缩略图缺失返回空和原文件不进入卡片字段。
- 小程序静态测试或页面测试覆盖证书列表只绑定 `thumbnail_url`、图片失败占位和不 fallback 到 `file_url`。
- 媒体四联验收覆盖 key、object、URL、render；生产证据只保留脱敏摘要。

# 风险与取舍

- 不在本 Change 中新增 CDN 正式接入、证书详情页视觉改版或管理端上传交互重构。
- 不把 `files/default/brand-certificates/` 下的图片直接视为正确状态；可读兼容与标准化迁移分开记录。
- 不以 HTTP 200 单点证明修复完成，必须结合 MIME、`x-media-fallback` 或等价响应头、接口字段和端侧渲染证据。
