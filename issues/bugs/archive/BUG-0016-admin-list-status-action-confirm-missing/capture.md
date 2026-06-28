---
bug_id: BUG-0016-admin-list-status-action-confirm-missing
status: captured
created_at: 2026-06-27 12:03:34
updated_at: 2026-06-27 12:03:34
severity_hint: medium
environment: local|docker
related_requirement: REQ-0008-brand-status-confirm
related_bug: null
captured_via: capture
classification_rationale: REQ-0008 已交付品牌启停二次确认，但品牌/用户列表多项状态变更（含删除、冻结等）仍缺少确认弹窗；属已有交互规范未完整落地，非新能力需求。
---

# 现象

品牌列表页、用户列表页在执行启用/停用、上架/下架、冻结/解冻、删除等状态变更操作时，缺少二次确认弹窗，点击后直接执行，存在误操作风险，与类目列表启用/停用等已对齐的二次确认交互不一致。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖品牌」列表页，对某行点击「停用」「启用」「删除」等状态类操作。
3. 观察是否在执行前弹出二次确认 Dialog。
4. 进入「用户管理」列表页，对某行点击「冻结」「解冻」「删除」等操作。
5. 观察是否弹出二次确认 Dialog。
6. 对比「瓷砖类目」列表页启用/停用操作是否有二次确认弹窗。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 品牌/用户列表的启用、停用、上架、下架、冻结、解冻、删除等状态变更操作 MUST 在执行前弹出二次确认弹窗，文案与操作类型匹配。 |
| **实际** | 上述操作多数或全部缺少二次确认，点击后直接生效。 |

# 附件

- 暂无截图。
- 参考需求：`REQ-0008-brand-status-confirm`（品牌启停确认已归档，需扩展或补全至用户列表与其余操作类型）。
