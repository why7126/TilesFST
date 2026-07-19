---
title: 原型上下文
purpose: REQ-0039 XL 管理端页面分层验收模板原型说明
content: 模板预览目标、结构与非目标
source: requirement.md
owner: product
status: draft
created_at: 2026-07-16 09:06:14
updated_at: 2026-07-16 09:06:14
---

# 原型上下文

本 REQ 不交付实际管理端业务页面。原型用于展示“分层验收模板”作为文档/工具页面时的结构，帮助评审确认 gate 分组、状态字段和 N/A 记录方式。

## 目标

- 展示 DB/API/上传/Orval/Web/Docker/UI 七层 gate。
- 展示每层 gate 的状态、owner、evidence、N/A reason 字段。
- 展示横切 UI gate 与知识库引用。
- 保持管理端工作型信息密度，便于复制为 Markdown 表格或验收报告。

## 非目标

- 不作为最终 Web 管理端页面实现稿。
- 不要求 PNG Golden Reference。
- 不要求接入真实数据、交互或路由。
- 不替代后续 `docs/standards/` 模板文档。

## 视觉优先级

```text
1. acceptance.md 的 gate 结构
2. requirement.md 的范围和功能要求
3. rules/ui-design.md 管理端工作型界面约束
4. docs/knowledge-base best-practices 横切 AC
```

PNG 状态：待导出，非阻塞。
