---
bug_id: BUG-0026-change-password-cancel-confirm-redundant
status: pending_review
created_at: 2026-06-28 13:06:10
updated_at: 2026-06-28 13:06:10
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断密码修改功能，当前可继续使用：

1. **接受二次确认**：在浏览器原生对话框中点击「确定」即可关闭弹窗（多一次点击）。
2. **清空后再关**：若需避免 confirm，可先清空三个密码字段再点击「取消」——字段均为空时不会触发 confirm（体验较差，不推荐作为常规操作）。

## 2. 操作规避

无配置、环境变量或后端开关可关闭 dirty confirm；须等待前端 fix change 合并。

## 3. 风险说明

上述规避仅减少摩擦，无法消除：

- 「取消」语义与二次确认矛盾，降低管理端表单操作一致性。
- 原生 `window.confirm` 样式不可控，与 Design System 不一致。
- 与 BUG-0024/0025 同弹窗叠加时，改密整体 UX 进一步下降。

仍建议进入 `/bug-review BUG-0026 --approve`，通过 `fix-change-password-modal-errors`（或等价 fix-* Change）移除多余 confirm，并同步 OpenSpec delta。
