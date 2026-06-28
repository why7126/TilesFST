---
bug_id: BUG-0030-banner-list-ui-inconsistency
review_id: REV-BUG-0030-001
status: approved
reviewed_at: 2026-06-28 16:18:11
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0030-banner-list-ui-inconsistency` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0030-banner-list-ui-inconsistency
```

建议修复 Change：

```text
fix-banner-admin-ui
```

（可与 BUG-0031–0036 合并为单一 fix change。）

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 `section-head`、`table-toolbar`、`banner-pagination` 与 REQ-0016 原型 port 偏差；与用户管理页代码对比一致。 |
| 严重等级合理 | 通过 | `medium` 合理；为可见 UI 一致性问题，不阻断 Banner CRUD、筛选、上下线。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-009 覆盖标题/toolbar 移除、分页 DOM、AC-021 delta、纯前端范围与 Vitest。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change，参照 BUG-0027 修复模式即可。 |

## 3. 批准理由

1. 根因与 BUG-0009、BUG-0027 同构：CSS Port 未对齐已验收管理端分页黄金参考，修复路径清晰。
2. 修复面集中：`BannerManagementPage.tsx` section-head / table-toolbar / 分页 DOM + 清理 `banner-management.css` 冗余规则，无 API/DB 变更。
3. REQ-0016 AC-021 与列表一致性冲突已在 acceptance AC-009 明确 delta 消化路径。
4. workaround 已说明功能可继续运营，但不消除 Design System 一致性债务。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-admin-ui` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 删除 `section-head` 与 `table-toolbar`（含 `table-count`）；删除规则保留于 disabled 按钮 `title`。
2. 分页 DOM 对齐 `UserManagementPage`（`page-summary` + `page-buttons` + `page-size-wrap`）。
3. 删除 `banner-pagination`、`banner-page-left` 等非标准类名与 CSS。
4. SHOULD 补充 `BannerManagementPage` Vitest 分页结构断言。
5. `/bug-opsx` delta spec MUST MODIFIED 消化 REQ-0016 AC-021 左侧范围文案要求。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0030-banner-list-ui-inconsistency`（建议与 BUG-0031–0036 一并 opsx 合并 change）。
2. 修复完成后 `/opsx-apply` → 按 AC-001/AC-003 与用户管理页并排验收 → `/opsx-archive`。
