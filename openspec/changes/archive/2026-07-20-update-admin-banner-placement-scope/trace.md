---
change_id: update-admin-banner-placement-scope
change_type: update
status: applied
created_at: 2026-07-20 18:55:00
updated_at: 2026-07-20 22:51:30
source_requirement: REQ-0062-admin-banner-placement-scope
related_requirements:
  - REQ-0016-banner-management
  - REQ-0060-brand-list-page
iteration: sprint-009
---

# Change Trace

## 来源

- REQ：`issues/requirements/archive/REQ-0062-admin-banner-placement-scope/`
- 父需求：`REQ-0016-banner-management`
- 关联需求：`REQ-0060-brand-list-page`

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| status | in_sprint |
| readiness | Ready |
| documents | capture、requirement、user-stories、business-flow、acceptance、review、prototype/web |
| knowledge-base gate | Pass |
| cross-cutting tags | admin-list, admin-modal, media-upload |

## Impact

```yaml
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: true
  storage: true
  api: true
capabilities:
  new: []
  modified:
    - banner-management
    - web-client
    - miniapp-home
    - database
```

## Conflict Report

| Source | Priority | Decision |
|---|---:|---|
| prototype/web/prototype.html | 1 | 作为管理端 Banner 页面结构参考，不做全新 CSS Port |
| prototype/web/context.md | 2 | 保留展示端单项、展示位置两项、旧数据删除后不编辑旧 Banner |
| acceptance.md | 3 | 作为功能、API/DB/Orval、UI 和横切 AC 事实源 |
| rules/ui-design.md | 4 | 管理端复用 DS token、列表/弹窗/上传 best-practice |
| openspec/specs/banner-management | 5 | 被本 Change 修改；旧多端配置由 REQ-0062 收敛 |
| add-brand-list-page design | related | 其临时复用首页轮播的实现说明需被本 Change 后续 apply 修正 |

## PNG / Visual Checklist

- [ ] 管理端 Banner 列表 1440x1024 对齐现有页面密度和用户管理分页 DOM。
- [ ] Banner 弹窗 Computed width 符合 Banner/SKU 大弹窗基准。
- [ ] 展示端单项和展示位置双项在移动/窄视口下不造成筛选区重叠。
- [ ] Banner 图片上传同会话即时回显。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 22:51:30 | `/opsx-apply` | 补充 Banner 跳转类型“品牌详情”，同步 `brand_id`、品牌 Logo 取图、小程序品牌详情跳转、OpenAPI/Orval、docs 和聚焦测试 |
| 2026-07-20 20:01:35 | `/opsx-apply` | 实现完成并通过聚焦后端测试、前端测试、OpenAPI/Orval 生成、OpenSpec strict 校验，状态 applied |
| 2026-07-20 19:11:31 | `/sprint-propose` | 纳入 `sprint-009`，满足后续 `/opsx-apply update-admin-banner-placement-scope` 的 Sprint 门禁前置条件 |
| 2026-07-20 18:55:00 | `/req-opsx` | 从 REQ-0062 创建 OpenSpec Change，状态 proposed |
