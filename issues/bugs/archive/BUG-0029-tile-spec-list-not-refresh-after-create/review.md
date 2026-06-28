---
bug_id: BUG-0029-tile-spec-list-not-refresh-after-create
review_id: REV-BUG-0029-001
status: approved
reviewed_at: 2026-06-28 13:28:00
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0029-tile-spec-list-not-refresh-after-create` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0029-tile-spec-list-not-refresh-after-create
```

建议修复 Change：

```text
fix-tile-spec-list-refresh-after-create
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 `TileSpecManagementPage` 中 `onSuccess={setNotice}` 未调用 `loadSpecs()`；与同页启停/删除路径及 Brand/Category/SKU 页对比一致。 |
| 严重等级合理 | 通过 | `high` 合理；阻断规格 CRUD 操作闭环，运营无法即时确认保存结果，影响 REQ-0009 核心验收。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-009 覆盖新增/编辑刷新、summary 同步、筛选场景、启停删除回归、纯前端范围与可选 Vitest。 |
| 是否需 hotfix 路径 | 不需要 | 非安全/数据损坏问题；修复为前端单处回调，常规 `fix-*` Change 即可，可与 BUG-0027/0028 评估合并 scope。 |

## 3. 批准理由

1. 根因明确且修复路径清晰：对齐 `BrandManagementPage` 的 `onSuccess` 模式（Toast + `loadSpecs()`），预期 3 行改动。
2. 后端 API 与持久化正常，属纯前端 state 同步遗漏，无接口/DB 变更风险。
3. 同页启停/删除已正确刷新，证明 `loadSpecs()` 基础设施完备，修复范围极小。
4. workaround（F5 / 点查询）可临时运营，但不消除重复提交与效率损失，应优先修复。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-tile-spec-list-refresh-after-create` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 修改 `TileSpecManagementPage.tsx`：`TileSpecFormModal` 的 `onSuccess` 回调同时执行 `setNotice(message)` 与 `void loadSpecs()`。
2. MUST NOT 修改 `TileSpecFormModal` 保存逻辑、API、schema 或 Orval 生成物。
3. 可选：补充 Vitest 断言保存 success 后列表加载函数被调用。
4. 修复后手工验证：新增后列表 + 4 指标卡即时更新；编辑排序/备注后行内同步；启停/删除行为无回归。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0029-tile-spec-list-not-refresh-after-create` 创建 OpenSpec change。
2. 可与 BUG-0027、BUG-0028 评估是否合并为单一 `fix-tile-spec-admin-ui` change（tasks 分列 scope）。
3. 修复完成后 `/opsx-apply` → 按 AC-001～AC-003 验收 → `/opsx-archive`。
