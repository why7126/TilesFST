---
bug_id: BUG-0107-admin-certificate-list-main-image-name-only
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 12:02:36
severity_hint: low
environment: admin-certificate-list
related_requirement: null
related_bug: BUG-0089-admin-certificate-edit-image-filename-noise
lifecycle_stage: plan
captured_via: capture
classification_rationale: 管理后台证书列表已存在，证书字段展示了不需要的图片名称或文件名称，是既有列表展示内容不符合预期，属于 BUG。
---

# 现象

管理后台证书列表中，证书字段除了证书主图和证书名称外，还显示了图片名称或文件名称。

# 复现步骤

1. 登录管理后台。
2. 进入证书列表。
3. 查看证书字段的展示内容。
4. 观察是否显示图片名称、文件名称或对象文件名。

# 期望 vs 实际

- 期望：证书字段仅显示证书主图和证书名称。
- 实际：证书字段额外显示图片名称或文件名称，产生信息噪音。

# 影响范围

- 管理后台证书列表。
- 证书主图、证书名称、图片文件名和证书文件名展示逻辑。

# 初步线索

- 需要检查证书列表列渲染是否复用了上传组件的文件名展示。
- 修复时应避免隐藏证书名称或主图加载失败占位。

# 建议验收或复现要点

- [ ] 证书字段只显示证书主图和证书名称。
- [ ] 不显示图片名称、文件名称、对象 key 或原始 URL。
- [ ] 无主图时显示合理占位，不影响证书名称展示。
- [ ] 列表排序、筛选、编辑入口保持正常。

# 附件

- 暂无。
