---
bug_id: BUG-0047-system-settings-save-tip-layout-shift
status: pending_review
created_at: 2026-06-28 18:35:49
updated_at: 2026-06-28 18:35:49
---

# 临时规避方案

## 1. 可用性规避

1. **忽略页面跳动**：保存已成功，tip 文案仍可读。
2. **快速操作**：tip 自动消失或切换 Tab 后位移恢复。

## 2. 操作规避

无配置规避。

## 3. 风险说明

layout shift 影响专业感，可能使用户误点。建议 `/bug-review BUG-0047 --approve` 后修复。
