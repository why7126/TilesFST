---
bug_id: BUG-0003-brand-image-display-layout-shift
status: captured
recorded_at: 2026-06-25 20:11:22
severity_hint: high
environment: local|docker
related_requirement: REQ-0005-brand-management
related_change: add-brand-management
related_bugs:
  - BUG-0002-brand-ui-inconsistency
---

# 现象

瓷砖品牌页存在两类用户可见问题：

1. 上传品牌图片后，图片不能正常显示；无论是在品牌列表页，还是在品牌编辑弹窗内，都无法看到已上传图片的正确预览或回显。
2. 当列表页发生状态变更时，页面顶部会新增一行 Tips，几秒后消失；Tips 出现和消失会推挤页面内容，导致整个页面上下波动。

# 复现步骤

1. 以 admin 或 employee 登录管理端。
2. 进入「瓷砖品牌」列表页。
3. 新增或编辑一个品牌，并上传品牌图片/Logo。
4. 保存后返回品牌列表，观察品牌图片展示。
5. 再次打开该品牌编辑弹窗，观察已上传图片是否正常回显。
6. 在品牌列表页执行状态变更操作，例如启用或停用品牌。
7. 观察页面顶部 Tips 出现和几秒后消失时，页面主体内容是否发生上下位移。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 上传成功后，品牌列表页和品牌编辑弹窗 MUST 正常展示已上传图片；状态变更提示 SHOULD 使用不影响布局的固定位置 toast、inline 弱提示或预留空间提示，不应推挤页面主体内容。 |
| **实际** | 上传图片后在品牌列表页和品牌编辑弹窗均不能正常显示；状态变更 Tips 在页面顶部临时插入一行，出现/消失时导致页面上下波动。 |

# 影响范围

- Web 管理端：瓷砖品牌列表页。
- Web 管理端：品牌新增/编辑弹窗。
- 媒体展示：品牌图片/Logo 上传后的预览、回显和列表展示。
- 交互体验：品牌状态变更后的提示反馈引发布局抖动。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | media-display / frontend-ui |
| 严重程度建议 | high |
| 可能修复面 | Web 管理端品牌管理页图片 URL/预览回显逻辑、状态变更反馈组件布局策略 |
| 相关历史 | `BUG-0002-brand-ui-inconsistency` 曾处理品牌页分页与 Logo 控件视觉一致性，本缺陷为上传后显示失败与 Tips 布局波动，建议独立追踪。 |

# 附件

- 暂无截图。
- 参考页面：瓷砖品牌列表页、品牌新增/编辑弹窗。
- 参考规范：`rules/media.md`、`rules/security.md`、`rules/ui-design.md`、`rules/document-governance.md`。
