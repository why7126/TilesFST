---
bug_id: BUG-0028-tile-spec-modal-form-layout
review_id: REV-BUG-0028-001
status: approved
reviewed_at: 2026-06-28 13:22:45
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0028-tile-spec-modal-form-layout` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0028-tile-spec-modal-form-layout
```

建议修复 Change（可与 BUG-0027、BUG-0029 合并编排）：

```text
fix-tile-spec-modal-form-layout
```

或合并为：

```text
fix-tile-spec-admin-ui
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 JSX 字段顺序错误与 CSS port 缺 `.textarea { width: 100% }`；截图、原型 HTML 与代码路径一致。 |
| 严重等级合理 | 通过 | `medium` 合理；不阻断 CRUD，属 REQ-0009 弹窗验收与 CSS Port 缺口。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-011 覆盖字段顺序、保持 `{w}×{l}mm`、备注整行、AC-020/046、CRUD 不回归；AC-021 冲突提示为 SHOULD 可选 scope。 |
| 是否需 hotfix 路径 | 不需要 | 纯前端 UI，无数据/安全/阻断风险；常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 根因明确：`TileSpecFormModal.tsx` 字段顺序与 `tile-spec-management.css` 表单控件 port 不完整，非 API 或后端逻辑缺陷。
2. `bug.md` 已修正 capture 中与 REQ-0009 冲突的期望（去掉 mm 后缀不应作为修复目标），验收标准与 FR-006、AC-019、AC-021 对齐。
3. 修复面集中：组件字段重排 + CSS port，预计不涉及后端或数据库变更。
4. 与 BUG-0027（列表 UI）、BUG-0029（创建后刷新）同属 REQ-0009 交付缺口，合并 fix change 可减少重复 touch。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-tile-spec-modal-form-layout` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 调整 `TileSpecFormModal.tsx`：尺寸名称（只读）移至宽/长之后、厚度/排序之前。
2. 在 `tile-spec-management.css` 补 port `.input`/`.textarea` 宽度、备注固定高度与 `resize: none`。
3. **不要**修改 `buildDisplayName()` 去掉 `mm` 后缀。
4. 可选：AC-021 宽长冲突 inline 提示与只读区 help 文案（tasks 中明确 in/out scope）。
5. SHOULD 补充 `TileSpecFormModal` Vitest；MUST 更新 Change trace checklist 第 7–9 项。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0028-tile-spec-modal-form-layout` 创建 OpenSpec change。
2. 可纳入 Sprint（`related_requirement: REQ-0009-tile-spec-management`）。
3. 修复完成后 `/opsx-apply` → AC-009/AC-046 弹窗 HTML 并排验收 → `/opsx-archive`。
