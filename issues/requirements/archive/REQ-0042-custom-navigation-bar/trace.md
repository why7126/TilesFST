---
requirement_id: REQ-0042-custom-navigation-bar
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-07-17 08:52:22
updated_at: 2026-07-19 11:02:41
lifecycle:
  captured: 2026-07-17 08:52:22
  generated: 2026-07-17 09:22:51
  completed: 2026-07-18 12:55:02
  reviewed: 2026-07-19 09:23:32
  approved: 2026-07-19 09:23:32
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-custom-navigation-bar
    type: update
    status: archived
related_requirements:
  - REQ-0041-miniapp-home
  - REQ-0043-miniapp-home-style-optimization
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0042-custom-navigation-bar
requirement_name: custom-navigation-bar
requirement_type: 小程序 / 首页导航体验
priority: P1
status: done
lifecycle_stage: review
owner: product
source: 用户反馈
target_clients:
  web_admin: 不涉及
  web_catalog: 不涉及
  wechat_miniapp: 本期
parent_requirement: REQ-0041-miniapp-home
related_requirements:
  - REQ-0041-miniapp-home
  - REQ-0043-miniapp-home-style-optimization
related_changes:
  - add-miniapp-custom-navigation-bar
lifecycle:
  captured: 2026-07-17 08:52:22
  generated: 2026-07-17 09:22:51
  completed: 2026-07-18 12:55:02
  reviewed: 2026-07-19 09:23:32
  approved: 2026-07-19 09:23:32
iteration: sprint-008
openspec_changes:
  - change_id: add-miniapp-custom-navigation-bar
    type: update
    status: archived
readiness: Ready
readiness_notes: 评审通过；当前首页搜索框上方品牌展示模块作为自定义导航栏，排除“门店信息”入口，搜索框保持在导航栏下方；右侧分享和关闭使用小程序原生能力。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - prototype/miniapp/context.md
  - prototype/miniapp/prototype.html
expected_openspec_change: add-miniapp-custom-navigation-bar
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-007-retrospective.md
cross_cutting_tags: []
baseline_requirement: REQ-0043-miniapp-home-style-optimization
custom_navigation_scope:
  source_module: src/miniapp/pages/index/index.wxml 中搜索框上方的 brand-header 品牌展示部分
  include:
    - store-logo
    - store-name
    - store-subtitle
    - 原生分享按钮
    - 原生关闭按钮
  exclude:
    - store-link
    - 门店信息入口
    - openStoreInfo 默认点击跳转
  search_box: 保持在自定义导航栏下方
  native_actions: 右侧分享和关闭必须直接使用微信小程序原生能力，不在页面内手绘模拟
scope:
  backend_api: 默认不涉及；仅复用 REQ-0043 首页已有 store / brand 信息。若后续新增或调整接口 contract，必须同步 OpenAPI、Orval、docs 和测试。
  database: 默认不涉及；若后续新增字段，必须同步 SQLite/MySQL 文档、schema / migration 和测试。
  web_admin: 不涉及。
  web_storefront: 不涉及。
  wechat_miniapp: 本期；预计影响首页 brand-header 的信息边界、点击行为、WXML/WXSS/TS；默认不新增页面。
  object_storage: 默认不涉及；Logo 或图片必须使用后端安全 URL 或本地安全资源，不得直连未授权对象存储。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 11:02:11 | lifecycle-stage-migrate | review → archive（/opsx-archive add-miniapp-custom-navigation-bar） |
| 2026-07-19 11:01:08 | /opsx-archive | Change `add-miniapp-custom-navigation-bar` 已归档，状态同步完成。 |
| 2026-07-19 10:08:02 | /opsx-apply | Change `add-miniapp-custom-navigation-bar` apply 完成，待 archive。 |
| 2026-07-19 09:49:14 | /req-opsx | 创建 OpenSpec Change `add-miniapp-custom-navigation-bar`，修改 `miniapp-home` 规格 |
| 2026-07-19 09:30:12 | /req-refine | 按产品补充：自定义导航栏右侧需要分享和关闭两个按钮，直接使用微信小程序原生能力；继续排除门店信息入口 |
| 2026-07-19 09:25:05 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-07-19 09:23:32 | /req-review --approve | 评审通过；同意以 REQ-0043 为视觉与信息架构基准，将 brand-header 品牌展示部分作为自定义导航栏，并排除“门店信息”入口 |
| 2026-07-19 09:16:31 | /req-complete refine | 按产品确认将当前首页搜索框上方品牌展示模块定义为自定义导航栏；排除“门店信息”入口，搜索框保持在导航栏下方 |
| 2026-07-18 13:08:46 | /req-explore refine | 对齐 REQ-0043：首页样式与信息架构以 REQ-0043 为基准；REQ-0042 调整为 custom navigation 兼容门禁，不再强制自定义导航栏 |
| 2026-07-18 12:55:02 | /req-complete | 补齐用户故事、业务流程、验收标准与 miniapp prototype 策略；管理端 knowledge-base 横切标签 N/A，参考 sprint-007 复盘的分层验收与范围控制经验 |
| 2026-07-17 09:22:51 | /req-generate | 生成微信小程序自定义导航栏方案 PRD，状态更新为 draft |
| 2026-07-17 08:52:22 | /capture | 记录微信小程序首页采用自定义导航栏方案 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
- 2026-07-19 11:01:08 workflow-sync：状态同步为 done（Change archived）
