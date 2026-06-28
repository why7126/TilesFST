---
bug_id: BUG-0011-tile-sku-modal-content-overflow
status: captured
recorded_at: 2026-06-27 08:56:54
severity_hint: high
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_change: null
---

# 现象

瓷砖 SKU 新增/编辑弹窗内容高度超出可视区域时，底部表单项（如备注、图片/视频上传区等）被裁切或不可见，弹窗内**未提供垂直滚动条**，用户无法访问完整表单内容。

# 复现步骤

1. 以 admin 登录管理端（建议 1080p 或更小视口，或浏览器窗口非全屏）。
2. 进入「瓷砖SKU」列表页，点击「新增SKU」或「编辑」打开弹窗。
3. 观察弹窗内全部表单字段是否均在可视范围内。
4. 尝试滚动弹窗内容区域，确认是否存在垂直滚动条。
5. 若视口较小或表单字段较多（含图片、视频上传区），确认底部字段是否无法看到或无法操作。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 弹窗固定最大高度；内容区超出时在 Dialog 内部出现垂直滚动条，用户可滚动查看并操作全部字段；页眉（标题/副标题）与页脚（取消/保存）应固定或随 Design System 弹窗规范处理。 |
| **实际** | 内容超出弹窗显示范围，底部字段不可见；缺乏滚动条，无法完成表单填写与提交。 |

# 影响范围

- Web 管理端：瓷砖 SKU 新增/编辑弹窗。
- 关联需求：REQ-0006-tile-sku-management。
- 功能影响：阻塞用户在常规视口下完成 SKU 创建/编辑（尤其含媒体上传区时）。

# 初步分类（待 /bug-generate 确认）

| 判断 | 结论 |
|---|---|
| 缺陷类型 | 功能性 UI 缺陷（可用性/阻塞） |
| 严重程度建议 | high |
| 可能修复面 | 弹窗内容区 `overflow-y-auto`、max-height 约束、Dialog 布局结构 |
| 设计约束 | 对齐管理端其他长表单弹窗滚动行为、`rules/ui-design.md` |

# 附件

- 暂无截图。
- 参考原型：`issues/requirements/archive/REQ-0006-tile-sku-management/prototype/web/tile-sku-create-modal.html`
