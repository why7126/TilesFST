---
change_id: add-miniapp-certificate-list-page
type: add
status: applied
created_at: 2026-07-20 00:06:31
updated_at: 2026-07-20 10:22:00
source_requirement: REQ-0057-certificate-list-page
iteration: sprint-009
related_requirements:
  - REQ-0057-certificate-list-page
  - REQ-0038-brand-certificate-management
  - REQ-0048-miniapp-global-custom-navigation-bar
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: true
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
prototype_refs:
  - issues/requirements/archive/REQ-0057-certificate-list-page/prototype/miniapp/context.md
  - issues/requirements/archive/REQ-0057-certificate-list-page/prototype/miniapp/certificate-list-page.html
---

# Change Trace

## 来源

- REQ：`REQ-0057-certificate-list-page`
- 命令：`/req-opsx REQ-0057-certificate-list-page`
- Change：`add-miniapp-certificate-list-page`

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| requirement.md | ready |
| user-stories.md | ready |
| business-flow.md | ready |
| acceptance.md | ready |
| trace.md | ready |
| prototype | ready，HTML/context 已提供，PNG 待后续 evidence |
| readiness | Ready |

## Impact

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: true
capabilities:
  new:
    - miniapp-certificate-list-page
  modified: []
```

## Conflict Report

| 来源 | 决议 |
|---|---|
| HTML prototype | 作为页面信息架构、视觉密度和卡片布局最高参考 |
| PNG | 暂未导出，不阻塞 proposed；实现阶段补 DevTools 或设计截图 evidence |
| context.md | 作为组件结构、状态机和视觉约束参考 |
| acceptance.md | 作为功能、安全、UI 和 API 验收事实源 |
| ui-design.md | 提供深色高端视觉、低圆角、品牌金和移动端可读性约束 |
| existing specs | `miniapp-home` 曾明确证书聚合页不进入首页首期，本 Change 新增独立能力消化该后续范围 |

## PNG / Evidence Checklist

- [x] DevTools 320 pt evidence（follow_up，见 `implementation/miniapp-certificate-list-evidence.md`）
- [x] DevTools 375 pt evidence（follow_up，见 `implementation/miniapp-certificate-list-evidence.md`）
- [x] DevTools 430 pt evidence（follow_up，见 `implementation/miniapp-certificate-list-evidence.md`）
- [x] 真机 evidence 或 blocked/follow_up 说明（blocked，见 `implementation/miniapp-certificate-list-evidence.md`）

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 10:22:00 | /opsx-apply follow-up | 按用户反馈移除证书列表搜索/筛选，改为一行 2 个证书卡片且卡片文本仅展示证书名称、品牌名称、证书类型 |
| 2026-07-20 09:57:03 | /opsx-apply | 完成公开证书列表 API、小程序证书 Tab、OpenAPI/Orval、测试与 evidence 记录 |
| 2026-07-20 08:25:00 | /sprint-propose | 纳入 sprint-009 正式范围 |
| 2026-07-20 00:06:31 | /req-opsx | 创建 OpenSpec Change 并生成 proposal/design/spec/tasks |
