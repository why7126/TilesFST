---
bug_id: BUG-0025-change-password-toggle-button-misalignment
status: pending_review
created_at: 2026-06-28 12:57:00
updated_at: 2026-06-28 12:57:00
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断密码修改功能，切换按钮仍可点击：

1. **忽略按钮位置漂移**：出现错误提示后，「显示/隐藏」按钮可能下沉，但仍可正常切换密码可见性。
2. **修正输入后错误消失**：清除错误或重新填写使 `error-text` 卸载后，按钮位置自动恢复居中。
3. **使用浏览器自动填充**：若已保存密码，可依赖浏览器填充减少手动切换可见性的需要。

## 2. 操作规避

无配置、脚本或后端变更可规避布局错位；需等待前端 fix change 合并。

## 3. 风险说明

上述规避无法消除：

- 错误状态下按钮视觉错位，降低界面专业感与信任度。
- 与 BUG-0024 叠加时，用户同时面对「错误挂错字段」与「按钮错位」，改密体验更差。

仍建议进入 `/bug-review BUG-0025 --approve`，通过 `fix-change-password-modal-errors` OpenSpec Change 修复布局。
