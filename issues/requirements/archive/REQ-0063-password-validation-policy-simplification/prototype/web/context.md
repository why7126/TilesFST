---
requirement_id: REQ-0063-password-validation-policy-simplification
title: 密码校验规则简化 - Web 原型说明
status: pending_review
owner: product
created_at: 2026-07-20 19:53:30
updated_at: 2026-07-20 19:53:30
---

# Web 原型说明

## 目标

本需求不新增独立页面，仅调整管理端既有密码输入区域的规则提示、字段校验和错误文案。原型用于说明修改密码弹窗和其他管理端密码表单的提示位置与状态，不作为全新视觉稿。

## 适用界面

- 修改本人密码弹窗：继承 `REQ-0015-password-change` 的 520px 居中弹窗。
- 创建用户/重置密码表单：在新密码字段附近展示同一规则提示。

## UI 要点

- 新密码字段下方展示规则说明：`密码需为 5-32 位，并同时包含英文字符和数字。`
- 字段级错误出现在字段下方，优先提示具体失败原因。
- 满足项可使用成功态；未满足项使用弱提示或错误态，具体视觉由 Design System 决定。
- 弹窗 footer 保持取消 / 保存修改的既有结构。
- 不新增顶部 notice，不用全局 Toast 替代字段级错误。

## 原型文件

- `password-policy-hints.html`：轻量 HTML 原型，用于说明字段提示布局。
- PNG 暂不导出；后续如进入 OpenSpec Change 并涉及 UI 变更，可按 HTML 截图生成验收图。
