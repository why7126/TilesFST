---
bug_id: BUG-0046-system-settings-reset-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
---

# 临时规避方案

## 1. 可用性规避

1. **继续使用原生 confirm**：功能完整，确认/取消均可完成操作。
2. **避免误触恢复默认**：操作前仔细阅读浏览器对话框文案。

## 2. 操作规避

无替代 UI；无法在不改代码情况下获得 DS modal。

## 3. 风险说明

原生 confirm 样式不可品牌化；与全站不一致。建议 `/bug-review BUG-0046 --approve` 后修复。
