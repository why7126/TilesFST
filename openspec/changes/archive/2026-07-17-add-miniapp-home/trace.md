---
change_id: add-miniapp-home
type: add
status: applied
created_at: 2026-07-16 09:40:45
updated_at: 2026-07-16 10:46:52
source_requirement: REQ-0041-miniapp-home
source_requirement_path: issues/requirements/archive/REQ-0041-miniapp-home/
iteration: sprint-008
---

# Trace

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| REQ | `REQ-0041-miniapp-home` | 已评审通过的微信小程序首页需求 |
| PRD | `issues/requirements/archive/REQ-0041-miniapp-home/requirement.md` | 范围、功能要求、数据字段和状态块 |
| Acceptance | `issues/requirements/archive/REQ-0041-miniapp-home/acceptance.md` | 功能、范围、UI、状态、API/数据/安全、测试 AC |
| Prototype | `issues/requirements/archive/REQ-0041-miniapp-home/prototype/miniapp/` | HTML、PNG、context 与 Logo |

## 影响分析

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: true
  storage: true
  api: true
capabilities:
  new:
    - miniapp-home
  modified:
    - product-usage-logging
```

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| status | approved |
| requirement.md | present |
| user-stories.md | present |
| business-flow.md | present |
| acceptance.md | present |
| trace.md | present |
| prototype/miniapp | present |
| readiness | Ready |

## Conflict Report

| 来源 | 冲突 / 差异 | 处理 |
|---|---|---|
| `prototype.html` / `prototype.png` | 原型含收藏心形与收藏 Tab | 以 acceptance 为准：本期不实现收藏，隐藏、移除或置为非交互展示 |
| `prototype.html` / `prototype.png` | 原型联系门店提示较轻量 | 本期已纳入咨询功能，至少实现一种可用咨询方式 |
| acceptance | 分享、咨询、热销统计纳入本期 | specs/tasks 已纳入 API、统计、测试和范围控制 |

## PNG / Prototype Checklist

- [ ] 首页视觉对齐 `prototype/miniapp/prototype.png`
- [ ] HTML 原型结构优先于 PNG 细节
- [ ] 收藏入口按范围控制移除/隐藏/禁用
- [ ] 375x812 与 390x844 视口验收
- [ ] 320 到 430 pt 宽度无横向滚动和重叠

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-16 09:40:45 | /req-opsx | 从 REQ-0041 创建 add-miniapp-home OpenSpec Change |
| 2026-07-16 10:21:50 | /sprint-propose | 纳入 sprint-008 正式范围 |
| 2026-07-16 10:46:52 | /opsx-apply | 实现小程序首页首期闭环，状态更新为 applied |
