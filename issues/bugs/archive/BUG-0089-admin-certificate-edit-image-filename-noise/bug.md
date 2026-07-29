---
bug_id: BUG-0089-admin-certificate-edit-image-filename-noise
title: 管理端证书编辑弹窗图片下方显示无意义文件名
severity: low
status: done
owner:
discovered_at: 2026-07-29 08:08:23
environment: local
related_requirement: REQ-0078-certificate-multiple-images-main-image
related_change: fix-admin-certificate-image-filename-noise
created_at: 2026-07-29 09:07:56
updated_at: 2026-07-29 09:07:56
---

# 现象

管理端品牌证书编辑弹窗中，当证书图片已有内容时，证书图片上传说明“支持 JPG / PNG / WebP，最多 9 张”下方会显示图片文件名。

该文件名已经可以由图片预览、主图标记、删除和设为主图操作承载上下文，不需要额外作为文本列表展示；当前展示会增加弹窗信息噪音。

# 复现步骤

1. 进入管理端品牌证书管理页面。
2. 打开已有证书的编辑弹窗，且该证书已存在至少一张证书图片。
3. 查看“证书图片”区域。
4. 观察“支持 JPG / PNG / WebP，最多 9 张”说明下方是否出现图片文件名。

# 期望 vs 实际

- 期望：证书图片区域只展示图片卡片、主图标记、删除、设为主图、继续添加等必要信息；上传说明下方不展示图片文件名文本列表。
- 实际：当证书图片列表非空时，上传说明下方额外展示 `cover.webp`、`page-2.webp` 等图片文件名。

# 影响范围

- 影响管理端 `/admin/brand-certificates` 新增/编辑品牌证书弹窗的证书图片上传区域。
- 主要影响编辑已有证书的场景；新增证书上传图片后也可能出现同类冗余信息。
- 不影响后端 API、数据库存储、小程序展示、证书图片上传和保存数据本身。

# 严重等级说明

严重等级为 `low`。该问题属于管理端表单 UI 噪音，不阻断证书编辑、图片上传、删除、设主图或保存流程，也不会导致数据错误；但会降低弹窗信息清晰度，建议作为常规修复处理。
