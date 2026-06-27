---
bug_id: BUG-0015-admin-list-status-tips-layout-shift
status: captured
created_at: 2026-06-27 12:03:34
updated_at: 2026-06-27 12:03:34
severity_hint: medium
environment: local|docker
related_requirement: REQ-0005-brand-management
related_bug: BUG-0003-brand-image-display-layout-shift
captured_via: capture
classification_rationale: 品牌/用户列表状态变更后顶部 Tips 推挤主体内容，与 BUG-0003 同类布局抖动问题；用户列表未覆盖或品牌页回归，属既有交互规范下的偏差。
---

# 现象

在品牌列表页、用户列表页执行状态变更操作（如启用/停用、上架/下架、冻结/解冻、删除等）后，页面顶部会临时新增一行 Tips 提示，数秒后自动消失。Tips 的出现与消失会推挤列表、筛选区或指标卡等主体内容，造成整页上下波动，影响连续操作体验。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖品牌」列表页或「用户管理」列表页。
3. 对任意一行执行状态变更操作（如停用品牌、冻结用户等）。
4. 观察页面顶部是否出现一行 Tips。
5. 等待 Tips 自动消失（约数秒）。
6. 对比 Tips 出现前后、消失前后，页面主体内容是否发生明显上下位移。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 状态变更反馈 Tips MUST 使用非占位文档流模式（如 fixed/overlay toast），出现与消失 MUST NOT 推挤页面主体内容。 |
| **实际** | Tips 作为文档流节点插入页面顶部，出现/消失时导致整页上下波动。 |

# 附件

- 暂无截图。
- 历史相关：`BUG-0003-brand-image-display-layout-shift`（品牌页曾修复，现仍复现或用户列表未覆盖）。
