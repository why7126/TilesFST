---
requirement_id: REQ-0036-clipboard-helper-best-practice-docs
title: Clipboard helper best-practice 文档业务流程
status: approved
created_at: 2026-07-11 23:47:07
updated_at: 2026-07-11 23:53:49
---

# Business Flow

## 1. 文档沉淀流程

```text
识别 Clipboard helper 调用方经验
    |
    v
汇总 REQ-0032 helper 边界与 Sprint 006 复盘行动项
    |
    v
建立 best-practice 文档
    |
    +-- 调用方文案：success / failed / unavailable / empty
    +-- fallback 策略：手动选择、禁用入口、明确提示
    +-- 敏感值边界：允许 / 谨慎 / 禁止复制
    +-- checklist：代码评审、QA 验证、日志/埋点检查
    |
    v
从 Web README 或知识库索引建立入口
    |
    v
后续新增复制入口时按 checklist 验收
```

## 2. 调用方使用流程

```text
新增复制入口
    |
    v
确认待复制内容是否已授权可见
    |
    +-- 禁止/默认不复制：不提供入口或走专门安全流程
    |
    +-- 谨慎复制：确认业务必要性 + 安全提示 + 不记录原文
    |
    +-- 允许复制：继续接入 helper
            |
            v
        调用 copyTextToClipboard 或等价 helper
            |
            +-- success：展示业务语义成功文案
            +-- failed：提示自动复制失败并触发 fallback
            +-- unavailable：提示浏览器不支持自动复制并触发 fallback
            +-- empty：隐藏/禁用入口或提示内容为空
```

## 3. 文档评审流程

```text
/req-complete
    |
    v
补齐 user-stories / business-flow / acceptance
    |
    v
/req-review --approve
    |
    v
/req-opsx
    |
    v
OpenSpec 确认文档落位、入口链接和验收 checklist
    |
    v
实现阶段新增或更新 best-practice 文档
```

## 4. 与父需求差异

| 维度 | REQ-0032 | REQ-0036 |
|---|---|---|
| 目标 | 沉淀 Clipboard helper 或复制交互最佳实践，实现结构化结果和 fallback 能力 | 建立长期 best-practice 文档，约束调用方文案、fallback 和敏感值边界 |
| 交付物 | helper / 代表场景迁移 / 测试 / 初始使用边界 | 文档、checklist、示例/反例、知识库或 Web README 入口 |
| 验收重点 | 复制能力是否稳定、失败路径是否可用 | 后续调用方是否能按文档一致接入并避免敏感值泄露 |
| UI 原型 | 可涉及列表和弹窗代表场景 | 不新增 UI 原型 |

## 5. 依赖与边界

```text
REQ-0036
├── 依赖
│   ├── REQ-0032-clipboard-copy-helper-best-practice
│   ├── docs/knowledge-base/README.md
│   ├── docs/knowledge-base/retrospectives/sprint-006-retrospective.md
│   ├── rules/security.md
│   └── src/web/README.md（候选入口）
└── 不依赖
    ├── 后端 API
    ├── 数据库表结构
    ├── Orval 生成
    ├── Docker Compose
    ├── 小程序复制 API
    └── 管理端页面原型
```
