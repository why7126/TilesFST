---
requirement_id: REQ-0032-clipboard-copy-helper-best-practice
title: Clipboard 复制交互 prototype context
status: pending_review
created_at: 2026-07-11 16:04:55
updated_at: 2026-07-11 16:04:55
---

# Prototype Context

## 目的

本需求不新增完整业务页面原型，prototype 用于表达复制 helper 在两个既有 Web 管理端场景中的交互反馈策略：

- 日志审计列表复制 `request_id`：按钮位于表格行内，反馈以 fixed toast 或现有 `AdminToast` 呈现。
- 重置密码弹窗复制随机密码：按钮位于弹窗页脚，失败时聚焦并选中密码输入框，反馈位于弹窗 body 的 `role="status"` 文案。

## 验收重点

- 自动复制成功、API 不存在、写入失败、手动复制四种状态均可在原型中看到反馈。
- 不新增营销式说明区，不改变管理端暗色旗舰风。
- 不使用裸 Hex；后续实现必须使用 semantic token 或既有 CSS 类。
- PNG 暂不导出，后续 `/req-opsx` 或实现阶段可按需要截图。

## 页面关系

```text
prototype/web/clipboard-copy-helper.html
├── 列表行内复制示例
│   ├── success toast
│   ├── unavailable guidance
│   └── failed guidance
└── 弹窗复制密码示例
    ├── success status
    └── fallback select guidance
```
