---
bug_id: BUG-0089-admin-certificate-edit-image-filename-noise
status: done
created_at: 2026-07-29 08:36:14
updated_at: 2026-07-29 09:07:56
review_result: approved
reviewed_at: 2026-07-29 08:36:14
reviewer:
---

# 评审结论

确认修复。

# 评审清单

- [x] 可复现或根因充分
- [x] 严重等级合理
- [x] 回归验收明确
- [x] 无需 hotfix 路径

# 说明

该问题由管理端品牌证书图片上传组件在图片列表非空时额外渲染 `images[].file_name` 文本列表导致，根因明确且影响范围限定在品牌证书新增/编辑弹窗的前端 UI 展示。

严重等级 `low` 合理：不阻断证书编辑、图片上传、删除、设为主图或保存流程，也不影响 API、数据库或小程序展示。验收标准已覆盖编辑回显、新增上传后的文件名不展示，以及图片操作能力不回归。

# 后续动作

- 可进入 `/bug-opsx BUG-0089` 创建修复 Change。
- 可纳入 Sprint 常规修复范围。
