---
bug_id: BUG-0105-admin-brand-list-logo-renders-text
title: 管理后台品牌列表第一列品牌 Logo 显示为文字
severity: medium
status: done
owner:
discovered_at: 2026-08-03 08:13:39
environment: admin-brand-list
related_requirement:
related_change: fix-admin-brand-list-logo-rendering
created_at: 2026-08-03 08:19:00
updated_at: 2026-08-03 12:50:28
---

# 管理后台品牌列表第一列品牌 Logo 显示为文字

## 现象

管理后台品牌列表第一列的品牌 Logo 未正常渲染为图片，而是显示为文字内容。

## 复现步骤

1. 登录管理后台。
2. 进入品牌列表页面。
3. 查看第一列品牌 Logo。
4. 观察已上传 Logo 的品牌是否显示图片。

## 期望结果

- 已上传 Logo 的品牌在列表第一列显示品牌 Logo 缩略图。
- 未上传 Logo 的品牌显示设计系统内的合理占位状态。
- 图片加载失败时不暴露对象 key、文件名或原始 URL 噪音。

## 实际结果

- 品牌 Logo 显示为文字，未按图片方式渲染。
- 用户无法在品牌列表中直观看到品牌 Logo 视觉信息。

## 影响范围

- 管理后台品牌列表。
- 品牌 Logo 图片 URL、缩略图 URL 或表格图片渲染组件。
- 可能影响品牌信息维护时对 Logo 上传结果的核对效率。

## 严重等级说明

严重等级为 `medium`。该问题不阻断品牌数据维护、搜索、编辑或上下架操作，但会影响管理后台品牌列表的核心视觉识别能力，并可能暴露不应直接展示给用户的图片字段文本。

## 初步线索

- 检查品牌列表列配置是否将 Logo 字段作为普通文本输出。
- 确认后端返回的 Logo 字段、缩略图字段与前端渲染字段是否一致。

## 附件

- 暂无。
