---
bug_id: BUG-0107-admin-certificate-list-main-image-name-only
title: 管理后台证书列表证书字段额外显示图片或文件名称
severity: low
status: done
owner: null
discovered_at: 2026-08-03 08:13:39
environment: admin-certificate-list
related_requirement: null
related_change: fix-admin-certificate-list-main-image-name-only
created_at: 2026-08-03 08:19:01
updated_at: 2026-08-03 12:02:24
---

# BUG-0107 管理后台证书列表证书字段额外显示图片或文件名称

## 现象

管理后台证书列表中，证书字段除了证书主图和证书名称外，还额外显示图片名称、文件名称、对象文件名或原始 URL 等上传相关信息，造成列表展示噪音。

## 复现步骤

1. 登录管理后台。
2. 进入证书列表。
3. 查看证书字段的展示内容。
4. 观察证书主图和证书名称附近是否显示图片名称、文件名称、对象 key 或原始 URL。

## 期望结果

- 证书字段仅展示证书主图和证书名称。
- 无主图时展示合理占位，但不影响证书名称可读性。
- 列表排序、筛选和编辑入口保持正常。

## 实际结果

- 证书字段额外显示图片名称或文件名称。
- 上传实现细节暴露在列表中，干扰证书信息浏览。

## 影响范围

- 管理后台证书列表。
- 证书字段的主图、证书名称、图片文件名和证书文件名展示逻辑。
- 关联历史缺陷：`BUG-0089-admin-certificate-edit-image-filename-noise`。

## 严重等级说明

严重等级为 `low`。该问题主要影响管理后台证书列表的信息呈现质量和可读性，不阻断核心证书数据维护流程；但若文件名、对象 key 或原始 URL 持续显示，会增加界面噪音并暴露不应面向业务用户的上传细节。
