---
bug_id: BUG-0043-system-settings-duplicate-save-buttons
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
---

# 临时规避方案

## 1. 可用性规避

1. **任选其一保存**：页头与底部「保存设置」行为完全相同，点击任一即可 PATCH。
2. **建议固定使用底部按钮**：与「取消 / 恢复默认」同区，操作链更清晰。

## 2. 操作规避

无后端或配置规避。

## 3. 风险说明

双 CTA 造成视觉冗余；页头按钮与 save-tip（BUG-0047）不在同一视觉区。建议 `/bug-review BUG-0043 --approve` 后修复。
