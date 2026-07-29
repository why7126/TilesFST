---
bug_id: BUG-0089-admin-certificate-edit-image-filename-noise
status: done
created_at: 2026-07-29 08:08:23
updated_at: 2026-07-29 09:07:56
severity_hint: low
environment: local
related_requirement:
related_bug:
---

# 现象

管理端证书编辑弹窗中，当证书图片已有内容时，在“支持 JPG / PNG / WebP，最多 9 张”提示下方会额外显示图片名称。

该图片名称对编辑证书图片没有实际帮助，属于无意义的信息展示。

# 复现步骤

1. 进入管理端证书管理相关页面。
2. 打开已有证书的编辑弹窗。
3. 确认证书图片字段已有图片内容。
4. 查看“支持 JPG / PNG / WebP，最多 9 张”提示下方的信息。

# 期望 vs 实际

- 期望：图片上传说明下方不显示图片文件名，仅保留必要的图片预览、上传、删除等操作信息。
- 实际：图片上传说明下方显示了图片名称，形成无意义的界面噪音。

# 附件

暂无。
