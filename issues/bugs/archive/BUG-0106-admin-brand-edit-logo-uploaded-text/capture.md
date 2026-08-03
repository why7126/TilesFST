---
bug_id: BUG-0106-admin-brand-edit-logo-uploaded-text
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 12:50:57
severity_hint: low
environment: admin-brand-edit-dialog
related_requirement: null
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 管理后台品牌编辑弹窗已存在，Logo 旁展示冗余“已上传Logo”文案与当前界面预期不一致，是既有 UI 展示偏差，属于 BUG。
---

# 现象

管理后台品牌编辑弹窗中，品牌 Logo 旁边显示了不需要的 `已上传Logo` 文案。

# 复现步骤

1. 登录管理后台。
2. 进入品牌列表。
3. 打开任一已上传 Logo 的品牌编辑弹窗。
4. 查看品牌 Logo 区域旁的提示文案。

# 期望 vs 实际

- 期望：品牌 Logo 旁不显示 `已上传Logo` 文案，仅保留必要的图片预览、上传或替换控件。
- 实际：Logo 旁显示冗余文案，造成界面噪音。

# 影响范围

- 管理后台品牌编辑弹窗。
- 品牌 Logo 上传、预览与替换区域。

# 初步线索

- 需要检查品牌编辑表单中 Logo 上传组件的成功状态提示。
- 修复时应保留必要的错误提示、上传中状态和可访问标签。

# 建议验收或复现要点

- [ ] 品牌编辑弹窗 Logo 旁不再显示 `已上传Logo` 文案。
- [ ] 已上传 Logo 图片仍正常预览。
- [ ] 替换、删除或重新上传 Logo 的交互保持正常。
- [ ] 上传失败、格式不支持等错误提示仍可见。

# 附件

- 暂无。
