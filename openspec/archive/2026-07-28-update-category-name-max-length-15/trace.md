---
change_id: update-category-name-max-length-15
status: proposed
type: update
created_at: 2026-07-28 00:20:23
updated_at: 2026-07-28 00:24:49
source_requirement: REQ-0077-category-name-max-length-15
source_requirement_path: issues/requirements/archive/REQ-0077-category-name-max-length-15/
iteration: sprint-013
---

# Change Trace

## 来源

| 类型 | ID | 路径 |
|---|---|---|
| REQ | REQ-0077-category-name-max-length-15 | `issues/requirements/archive/REQ-0077-category-name-max-length-15/` |

## 影响分析

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: true
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - tile-category-management
change_type: update
expected_openspec_change: update-category-name-max-length-15
```

## Readiness Report

| 项 | 结论 |
|---|---|
| REQ 状态 | approved |
| 文档完整度 | Ready |
| requirement.md | 已存在 |
| user-stories.md | 已存在 |
| business-flow.md | 已存在 |
| acceptance.md | 已存在，含 8 条 AC-XCUT |
| prototype/web | 已存在 HTML + context，PNG 待导出但非阻塞 |

## Conflict Report

| 优先级 | 来源 | 结论 |
|---|---|---|
| 1 | HTML | `prototype/web/category-name-max-length-15.html` 定义 15 字符成功态、16 字符错误态与列表/树展示样例 |
| 2 | PNG | 未导出，后续实现可补截图 |
| 3 | context | `prototype-context.md` 要求复用 CategoryFormModal、列表模板、toast、confirm |
| 4 | acceptance | 功能 AC 与横切 AC 已转入 tasks 和 design |
| 5 | ui-design | 使用 semantic token 与管理端 modal/list best-practice |
| 6 | specs | 现有 data model 最大 30 字符，与 15 字符业务输入上限不冲突 |

## UI / PNG Checklist

- [ ] 实现后补充或记录 1440px 管理端弹窗 computed width 证据。
- [ ] 实现后补充或记录 720px 以下矮视口弹窗滚动证据。
- [ ] 实现后补充或记录管理端类目列表 / 类目树 15 字符展示证据。
- [ ] 实现后补充或记录小程序与 Web 展示端 15 字符布局回归证据。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-28 00:20:23 | `/req-opsx` | 基于 REQ-0077 创建 OpenSpec Change proposal/design/spec/tasks/trace |
| 2026-07-28 00:24:49 | `/sprint-propose` | 纳入 `sprint-013` 正式范围 |
