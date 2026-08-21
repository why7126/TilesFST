---
requirement_id: REQ-0112-admin-list-column-pagination-consistency-contract
created_at: 2026-08-12 14:29:16
updated_at: 2026-08-12 14:29:16
owner: product
source: requirement.md
---

# Business Flow

## 1. 范围与依赖

```text
Sprint 022 复盘 T-002
  ↓
REQ-0112 列展示与分页一致性契约
  ├─ Banner 管理列表
  ├─ 日志审计列表
  ├─ 用户管理列表
  ├─ Design System / AdminListPage 契约
  ├─ 前端测试
  └─ docs/knowledge-base best-practices
```

## 2. 设计与实现流程

```text
确认首批页面
  ↓
盘点现有列/分页/API
  ↓
定义契约
  ├─ nowrap 默认
  ├─ 有效期例外
  ├─ sticky 操作列
  ├─ 分页 DOM
  └─ 后端真实分页
  ↓
OpenSpec design 决策
  ├─ 共享 class / template prop
  ├─ API 是否变化
  ├─ Orval 是否需要
  └─ 测试策略
  ↓
代表页面实现与回归
  ↓
knowledge-base 回填
```

## 3. 用户操作流程

```text
用户进入管理端列表
  ↓
查看总数、筛选与分页
  ↓
扫描表头和主要字段
  ├─ 普通字段单行截断
  └─ 有效期列按例外双行展示
  ↓
横向滚动或窄屏查看更多列
  ↓
操作列保持可达
  ↓
执行编辑/状态变更/删除
  ├─ 危险操作进入 DS confirm modal
  └─ 结果以 fixed toast 反馈
```

## 4. 与 REQ-0095 的差异

| 需求 | 治理对象 | 本需求关系 |
|---|---|---|
| REQ-0095 | image/name/fallback 字段语义 adapter | 已归档，作为字段展示语义基础。 |
| REQ-0112 | 列宽、换行、sticky 操作列、分页 DOM、真实分页 | 补齐列表布局与分页契约，不重复字段语义 adapter。 |

## 5. 知识库引用

| 标签 | 引用文档 | 复用方式 |
|---|---|---|
| admin-list | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` | 转化为 acceptance 横切 AC，并在后续 design 中作为 apply 前 gate。 |
| sprint-022-retrospective | `docs/knowledge-base/retrospectives/sprint-022-retrospective.md` | 来源行动项 T-002，确认本需求的复发模式和首批范围。 |
