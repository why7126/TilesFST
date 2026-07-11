---
requirement_id: REQ-0032-clipboard-copy-helper-best-practice
title: Clipboard 复制交互沉淀共享 helper 或 best-practice 业务流程
status: archived
created_at: 2026-07-11 16:04:55
updated_at: 2026-07-11 20:10:50
---

# Business Flow

## 1. 总体流程

```text
用户点击复制
    |
    v
调用方读取待复制文本
    |
    v
copyTextToClipboard(text, options)
    |
    +-- text 为空/空白 ---------> 返回 empty
    |
    +-- Clipboard API 不存在 ---> 调用 fallbackSelect? -> 返回 unavailable
    |
    +-- writeText 成功 ---------> 返回 success
    |
    +-- writeText 失败 ---------> 调用 fallbackSelect? -> 返回 failed
    |
    v
调用方根据结果展示业务语义反馈
    |
    +-- success：可执行业务埋点
    +-- failed/unavailable：提示手动复制
    +-- empty：隐藏入口或提示内容为空
```

## 2. 日志审计 request_id 场景

```text
日志审计列表行
    |
    +-- request_id 为空：不展示复制按钮，或点击后提示当前日志没有 request_id
    |
    +-- request_id 有值：点击复制 request_id
            |
            v
        共享 helper 尝试复制
            |
            +-- success：展示 request_id 已复制 + 保留 copy_request_id 埋点
            +-- failed/unavailable：展示打开详情手动复制指引
```

## 3. 重置密码弹窗场景

```text
随机密码已生成弹窗
    |
    v
管理员点击复制密码
    |
    v
共享 helper 尝试复制 password
    |
    +-- success：弹窗内状态提示密码已复制
    |
    +-- failed/unavailable：
            |
            +-- fallbackSelect 聚焦并选中密码输入框
            +-- 弹窗内状态提示 Command/Ctrl + C 手动复制
```

## 4. 与父需求差异

| 维度 | REQ-0000-build-design-system | REQ-0032 |
|---|---|---|
| 目标 | 建立整体 Design System、token 与组件规则 | 沉淀 Clipboard 复制交互的共享能力与验收口径 |
| 范围 | 全局 UI/组件治理 | Web 管理端复制 helper、反馈约定、fallback 与测试 |
| 输出 | Design token、组件、规范、验收页 | helper 需求、用户故事、流程、AC、prototype 策略 |
| 风险 | 视觉与组件体系不一致 | 复制失败路径遗漏、文案漂移、敏感信息泄露 |

## 5. 依赖与边界

```text
REQ-0032
├── 依赖
│   ├── rules/ui-design.md
│   ├── docs/knowledge-base/best-practices/admin-list-page-consistency.md
│   ├── docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
│   ├── src/web/src/pages/admin/LogAuditPage.tsx
│   └── src/web/src/features/admin/components/ResetPasswordDialog.tsx
└── 不依赖
    ├── 后端 API
    ├── 数据库表结构
    ├── Orval 生成
    ├── MinIO / 上传链路
    └── 小程序复制 API
```
