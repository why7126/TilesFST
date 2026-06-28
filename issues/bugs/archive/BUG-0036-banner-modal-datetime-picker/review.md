---
bug_id: BUG-0036-banner-modal-datetime-picker
review_id: REV-BUG-0036-001
status: approved
reviewed_at: 2026-06-28 16:25:00
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0036-banner-modal-datetime-picker` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0036-banner-modal-datetime-picker
```

建议修复 Change（可与 BUG-0031～0035 合并编排）：

```text
fix-banner-modal-datetime-picker
```

或合并为：

```text
fix-banner-modal-ui
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 稳定复现「时分不可选/交互差」；`root-cause.md` 已定位原生 `datetime-local`、秒硬编码、无 DS DateTime 组件及未对齐 HTML 原型；与 `BannerFormModal.tsx`、`banner-display.ts` 一致。 |
| 严重等级合理 | 通过 | `medium` 合理；削弱精确配置生效窗口但不阻断无有效期保存；修复需前端组件化，工作量大于纯 CSS。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-013 覆盖 DateTime 交互、单字段区间形态、ISO 提交、回填、列表展示、time_status、四套 jump_type、AC-027/051 对齐；已裁定 HTML 原型优先于 capture 秒级 UI。 |
| 是否需 hotfix 路径 | 不需要 | 新功能验收缺口、无数据/安全紧急风险；常规 `fix-*` Change，宜与 Banner 弹窗 UI 簇合并。 |

## 3. 批准理由

1. 根因明确：依赖 `datetime-local` 且项目无 DateTime 复合组件；提交/回填逻辑固化秒值，与运营配置需求及 prototype HTML 不一致。
2. 与 REQ-0016 **AC-027**（有效期公共字段）、**AC-051**（modal HTML 并排）直接冲突；后端 ISO 校验已就绪，修复面集中在前端。
3. `acceptance.md` 已按 prototype HTML 裁定单字段区间 `YYYY-MM-DD HH:mm 至 …` 与分钟精度，避免与 capture 秒级表述长期歧义。
4. 与 BUG-0031～0035 同属 `BannerFormModal` UI 缺口，合并 `fix-banner-modal-ui` 可降低回归成本。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-datetime-picker` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 替换 `BannerFormModal` 中裸 `datetime-local`：Popover + 日期/时分选择或受控区间输入，对齐 `rules/ui-design.md` semantic token。
2. UI 改为 **单字段**「有效期」区间展示（对齐 `banner-management-modal-*.html`）；提交仍映射 `valid_from` / `valid_to` ISO。
3. 统一 `formatBannerDateTime` 与弹窗展示；秒策略：开始 `00`、结束 `59`（acceptance AC-004）。
4. SHOULD 补充 Vitest（区间解析、ISO 提交、回填）；更新 Change trace 关闭 AC-027 有效期项。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0036-banner-modal-datetime-picker` 创建 OpenSpec change。
2. 可纳入 Sprint（`related_requirement: REQ-0016-banner-management`）。
3. 修复完成后 `/opsx-apply` → AC-011 modal HTML 并排验收 → `/opsx-archive`。
