---
bug_id: BUG-0007-brand-logo-not-displayed-after-storage-fix
title: 对象存储修复后品牌 Logo 仍不显示
severity: high
status: in_sprint
owner: product
discovered_at: 2026-06-26 14:51:17
environment: local|docker
related_requirement: REQ-0005-brand-management
related_change: fix-brand-logo-display-after-storage-fix
---

# 缺陷说明

## 1. 现象

对象存储写入问题修复后，品牌列表页以及品牌编辑页仍没有正常显示品牌 Logo 图片。

用户反馈当前表现为：

- 品牌列表页 Logo 未显示。
- 品牌编辑弹窗 Logo 未显示。
- 对象存储问题已经修复后，前端展示仍未恢复。

## 2. 复现步骤

1. 启动本地或 Docker 环境。
2. 确认对象存储上传链路已修复并可写入 MinIO。
3. 进入管理端 `/admin/brands`。
4. 查看品牌列表中的 Logo 展示。
5. 打开品牌编辑弹窗，查看 Logo 回显。

## 3. 期望结果

品牌列表页和品牌编辑弹窗都应能展示已上传的品牌 Logo 图片。

## 4. 实际结果

品牌列表页和品牌编辑弹窗仍未显示 Logo 图片。

## 5. 影响范围

| 范围 | 影响 |
|---|---|
| Web 管理端品牌列表 | 品牌 Logo 无法作为品牌识别信息展示 |
| Web 管理端品牌编辑弹窗 | 已上传 Logo 无法正常回显，影响编辑确认 |
| 品牌管理验收 | `REQ-0005-brand-management` 中 Logo 上传、展示、回显相关验收存在风险 |
| 媒体访问链路 | 可能暴露对象 key、媒体 URL、后端受控读取或前端绑定问题 |

## 6. 严重等级说明

严重等级暂定为 `high`。

原因：

- 品牌 Logo 是品牌管理核心展示字段。
- 列表页和编辑页同时不可见，说明不是单一页面空态问题。
- 该问题发生在对象存储写入问题修复之后，可能影响媒体访问链路的闭环验收。

## 7. 关联信息

| 类型 | 编号 | 说明 |
|---|---|---|
| 父需求 | `REQ-0005-brand-management` | 品牌管理能力 |
| 相关 BUG | `BUG-0003-brand-image-display-layout-shift` | 曾修复品牌 Logo 展示与提示布局问题 |
| 相关 BUG | `BUG-0006-object-storage-upload-not-minio` | 对象存储写入链路问题 |
