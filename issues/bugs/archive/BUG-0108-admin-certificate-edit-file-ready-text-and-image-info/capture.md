---
bug_id: BUG-0108-admin-certificate-edit-file-ready-text-and-image-info
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 12:52:14
severity_hint: medium
environment: admin-certificate-edit-dialog
related_requirement: null
related_bug: BUG-0089-admin-certificate-edit-image-filename-noise
lifecycle_stage: plan
captured_via: capture
classification_rationale: 管理后台证书编辑弹窗已存在，PDF/兼容文件提示文案冗余且图片信息不能正常显示，属于同一弹窗内既有文件与图片信息展示能力偏差，归为一个 BUG。
---

# 现象

管理后台证书编辑弹窗中，PDF/兼容文件区域显示不需要的 `证书文件已就绪` 文案；同时图片信息全部不能正常显示。

# 复现步骤

1. 登录管理后台。
2. 进入证书列表。
3. 打开任一已有证书的编辑弹窗。
4. 查看 PDF/兼容文件区域和图片信息区域。

# 期望 vs 实际

- 期望：PDF/兼容文件区域不显示 `证书文件已就绪` 文案；图片信息应正常显示已有图片、主图状态和必要操作。
- 实际：PDF/兼容文件区域显示冗余文案；图片信息无法正常显示。

# 影响范围

- 管理后台证书编辑弹窗。
- 证书文件预览/状态提示。
- 证书图片列表、主图、图片信息展示与编辑。

# 初步线索

- 需要检查证书编辑表单初始化时文件字段与图片字段的数据映射。
- 需要确认图片数组、主图标识、缩略图 URL 与原图 URL 是否在编辑弹窗中被正确消费。
- 修复时应保留上传失败、文件缺失或格式不兼容等必要错误提示。

# 建议验收或复现要点

- [ ] PDF/兼容文件区域不再显示 `证书文件已就绪` 文案。
- [ ] 编辑已有证书时，图片信息正常显示。
- [ ] 主图状态、图片预览、替换或删除操作正常。
- [ ] 新增图片、保存后再次打开编辑弹窗，图片信息仍正确回显。
- [ ] 不显示对象 key、原始文件名或无意义文件名噪音。

# 附件

- 暂无。
