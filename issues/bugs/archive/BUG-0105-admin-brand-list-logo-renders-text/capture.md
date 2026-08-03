---
bug_id: BUG-0105-admin-brand-list-logo-renders-text
status: done
created_at: 2026-08-03 08:13:39
updated_at: 2026-08-03 12:50:46
severity_hint: medium
environment: admin-brand-list
related_requirement: null
related_bug: null
lifecycle_stage: plan
captured_via: capture
classification_rationale: 管理后台品牌列表和 Logo 展示能力已存在，第一列未渲染图片而显示文字，是既有媒体展示逻辑异常，属于 BUG。
---

# 现象

管理后台品牌列表第一列的品牌 Logo 未正常显示为图片，而是显示为文字。

# 复现步骤

1. 登录管理后台。
2. 进入品牌列表。
3. 查看第一列品牌 Logo。
4. 观察已上传 Logo 的品牌是否显示图片。

# 期望 vs 实际

- 期望：品牌列表第一列展示品牌 Logo 缩略图或合理占位图。
- 实际：品牌 Logo 显示为文字，未按图片方式渲染。

# 影响范围

- 管理后台品牌列表。
- 品牌 Logo 图片 URL、缩略图 URL 或表格图片渲染组件。

# 初步线索

- 需要检查品牌列表列配置是否把 Logo 字段作为普通文本输出。
- 需要确认后端返回的 Logo 字段、缩略图字段与前端渲染字段是否一致。

# 建议验收或复现要点

- [ ] 已上传 Logo 的品牌在列表第一列显示图片。
- [ ] 未上传 Logo 的品牌显示设计系统内的合理占位状态。
- [ ] 图片加载失败时不暴露对象 key、文件名或原始 URL 噪音。
- [ ] 不影响品牌搜索、编辑、上下架等既有操作。

# 附件

- 暂无。
