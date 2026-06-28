---
bug_id: BUG-0033-banner-modal-form-layout-overflow
review_id: REV-BUG-0033-001
status: approved
reviewed_at: 2026-06-28 16:18:27
reviewer: ai-agent
decision: approve
severity: high
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0033-banner-modal-form-layout-overflow` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0033-banner-modal-form-layout-overflow
```

建议修复 Change（可与 BUG-0031～0035 合并编排）：

```text
fix-banner-modal-form-layout-overflow
```

或合并为：

```text
fix-banner-modal-ui
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位 modal 缺 flex/scroll 与 `.textarea` CSS port 缺口；与原型 HTML、`BannerFormModal.tsx`、`banner-management.css` 一致。 |
| 严重等级合理 | 通过 | `high` 合理；矮视口下 footer 不可达会阻断 Banner CRUD，非纯视觉问题。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-012 覆盖 scroll、textarea 整行、placeholder、四套 jump_type、视口矩阵、AC-024/051 对齐。 |
| 是否需 hotfix 路径 | 不需要 | 纯前端 CSS port，无数据/安全紧急风险；常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 根因明确：`banner-management.css` 未 port 原型 modal flex/scroll 与 textarea 规则，与 BUG-0011、BUG-0028 同类已验证模式。
2. 与 REQ-0016 **AC-024**（92vh 可滚动）直接冲突；`add-banner-management` trace checklist 未关闭该项。
3. 修复面集中：主要为 `banner-management.css`，预计不涉及 API 或数据库变更。
4. 与 BUG-0031～0035 同属 Banner 弹窗 UI 缺口，合并 fix change 可减少重复 touch。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-form-layout-overflow` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 在 `banner-management.css` 为 `.banner-modal-card` 补 port flex 布局与 `.modal-body { overflow-y: auto }`（参照 `tile-sku-management.css` BUG-0011 模式）。
2. 在 `.banner-form-grid` 作用域补 port `.textarea`：`width: 100%`、`font-size: 12px`、`height: 72px`、`resize: none`、`::placeholder` 颜色。
3. 矮视口下验收四套 `jump_type` 弹窗 footer 可达；更新 Change trace 关闭 AC-024。
4. SHOULD 补充 `BannerFormModal` Vitest（modal-body scroll / textarea 整行）。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0033-banner-modal-form-layout-overflow` 创建 OpenSpec change。
2. 可纳入 Sprint（`related_requirement: REQ-0016-banner-management`）。
3. 修复完成后 `/opsx-apply` → AC-009/AC-051 modal HTML 并排验收 → `/opsx-archive`。
