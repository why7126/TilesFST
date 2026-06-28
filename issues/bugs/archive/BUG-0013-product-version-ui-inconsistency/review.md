---
bug_id: BUG-0013-product-version-ui-inconsistency
review_id: REV-BUG-0013-001
status: approved
reviewed_at: 2026-06-27 11:00:42
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0013-product-version-ui-inconsistency` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0013-product-version-ui-inconsistency
```

建议修复 Change：

```text
fix-product-version-ui-inconsistency
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | `capture.md` / `bug.md` 给出稳定复现路径与用户截图；`root-cause.md` 已定位 `ProductVersionBadge` ad-hoc 实现、未复用 DS `Badge`、admin shell 样式混用及视觉验收门禁缺失。 |
| 严重等级合理 | 通过 | `medium` 合理；版本文案与常量展示正确，不阻断登录/导航；但 REQ-0010 AC-006/AC-013/AC-015 视觉项未达标，影响原型与 DS 一致性。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-009 覆盖 pill 形态、DS token、原型并排、双端一致、a11y、纯前端范围、Vitest 样式断言及 REQ-0010 视觉 AC 闭环。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；可通过常规 `fix-*` Change 修复，与 `add-product-version-display` 补丁路径一致。 |

## 3. 批准理由

1. REQ-0010 功能已交付，本 BUG 为视觉验收缺口，与「已实现需求 + fix-* 补丁」模式一致（类 BUG-0009）。
2. 根因与修复面集中：`ProductVersionBadge`（或 `Badge` variant）+ 可选 `admin-home.css` pill 兜底；不涉及 API/DB/Orval。
3. 有明确 Golden Reference、原型 HTML 与用户截图作为验收基准。
4. workaround 已说明功能可用，但 REQ-0010 视觉 AC 须通过 fix Change 正式闭环。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-product-version-ui-inconsistency` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 重构 `ProductVersionBadge` 为 `Badge` 组件 variant 扩展，对齐 `rules/ui-design.md` §8 与原型 `.version-pill` 语义。
2. 管理端 brand-head 确保 pill 在 admin shell 背景下边框/背景/弱化文字可辨识。
3. 店主端 `Sidebar` 共用同一组件，双端视觉一致。
4. fix Change `tasks.md` 含 admin/catalog 原型 + Golden Reference PNG 并排 checklist；Vitest 断言 pill 关键 class。
5. MUST NOT 变更 `PRODUCT_VERSION` 维护策略或 API/DB。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0013-product-version-ui-inconsistency` 创建 `fix-product-version-ui-inconsistency`。
2. 建议与 REQ-0010 同 Sprint 规划（父需求 `in_sprint`）。
3. 修复完成后 `/opsx-apply` → 原型并排验收 → `/opsx-archive`。
