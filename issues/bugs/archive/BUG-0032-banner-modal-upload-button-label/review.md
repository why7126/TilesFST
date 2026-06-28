---
bug_id: BUG-0032-banner-modal-upload-button-label
review_id: REV-BUG-0032-001
status: approved
reviewed_at: 2026-06-28 16:18:19
reviewer: ai-agent
decision: approve
severity: low
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0032-banner-modal-upload-button-label` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0032-banner-modal-upload-button-label
```

建议修复 Change：

```text
fix-banner-modal-upload-button-label
```

或与 BUG-0031/0033–0036 合并为 `fix-banner-modal-ui`。

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`root-cause.md` 已定位硬编码文案、`sr-only` 泄漏「浏览…」、上传状态未绑定按钮；与 `BrandFormModal` 代码对比一致。 |
| 严重等级合理 | 通过 | `low` 合理；纯 UI/文案问题，上传与保存功能正常。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖选择/更换/上传中、`hidden` input、AC-032/AC-045 无回归、Brand 模式对齐与 Vitest。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change 即可。 |

## 3. 批准理由

1. 根因清晰：实现未复用 Sprint-002 已验收的品牌 Logo 上传模式（BUG-0004 修复后基准）。
2. 修复面集中：`BannerFormModal.tsx` 单文件为主，无 API/DB/Orval 变更。
3. acceptance 已裁定文案以管理端一致性（选择/更换/上传中）为准，原型冲突可在 fix change delta spec MODIFIED。
4. workaround 确认功能可继续运营，但不消除管理端上传控件一致性债务。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-banner-modal-upload-button-label` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. 动态按钮文案：`上传中` / `更换` / `选择`（对齐 `BrandFormModal`）。
2. `<input type="file">` 改用 `hidden`，上传中 `disabled`。
3. `onChange` 后重置 `input.value`，支持重复选同一文件。
4. SHOULD 补充 `BannerFormModal.test.tsx`（参考 `BrandFormModal.test.tsx`）。
5. MUST NOT 变更上传 API、MinIO 链路或 Banner 业务逻辑。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0032-banner-modal-upload-button-label` 创建 OpenSpec change。
2. 评估与 BUG-0031（同上传区标题）、BUG-0033–0036 合并为单一 `fix-banner-modal-ui` change。
3. 修复完成后 `/opsx-apply` → 按 AC-001/AC-004 与品牌 Logo 上传并排验收 → `/opsx-archive`。
