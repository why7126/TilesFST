---
bug_id: BUG-0031-banner-modal-image-section-label
review_id: REV-BUG-0031-002
status: approved
reviewed_at: 2026-06-28 16:25:05
reviewer: ai-agent
decision: approve
severity: low
hotfix_required: false
related_change: fix-banner-admin-ui
supersedes: REV-BUG-0031-001
---

# 缺陷评审

## 1. 评审结论

`BUG-0031-banner-modal-image-section-label` 评审通过（`/bug-generate` + `/bug-complete` 刷新后复审），状态变更为 `approved`。合并入已有 change **`fix-banner-admin-ui`**（tasks §3.1 移除 `banner-upload-title`）。

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现；`BannerFormModal.tsx` L315–321 + `imageSource` 映射已定位 |
| 严重等级合理 | 通过 | `low` — 纯 UI 冗余，不阻断上传/保存 |
| 回归验收明确 | 通过 | AC-001～008 覆盖各 jump_type / image_source、Brand 对齐、无回归 |
| Hotfix | 不需要 | 无功能/数据/安全风险；常规 fix 并入 `fix-banner-admin-ui` |

## 3. 修复路径

- **Change**：`fix-banner-admin-ui`（已 proposed，含 BUG-0030～0036）
- **关联**：与 BUG-0032 同文件同 tasks §3 修复
- **Next**：若尚未 apply → `/opsx-apply fix-banner-admin-ui`；已 opsx 则直接进入 Sprint apply
