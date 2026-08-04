---
requirement_id: REQ-0088-versioned-product-usage-docs
status: done
lifecycle_stage: archive
priority: P1
created_at: 2026-08-01 08:10:11
updated_at: 2026-08-04 09:30:26
lifecycle:
  captured: 2026-08-01 08:10:11
  generated: 2026-08-01 08:18:25
  completed: 2026-08-01 08:24:50
  reviewed: 2026-08-01 09:53:42
  approved: 2026-08-01 09:53:42
iteration: sprint-017
openspec_changes:
  - change_id: add-versioned-product-usage-docs
    type: add
    status: archived
related_requirements: []
---

# 需求追踪

## 基本信息

```yaml
requirement_id: REQ-0088-versioned-product-usage-docs
requirement_name: versioned-product-usage-docs
requirement_type: 发布治理 / 产品使用文档 / Mintlify
priority: P1
status: done
owner: product
source: /capture
target_clients:
  web_admin: 不直接影响运行时；产品文档需覆盖管理端操作说明
  web_catalog: 不直接影响运行时；如后续上线店主 Web，需覆盖公开浏览说明
  wechat_miniapp: 不直接影响运行时；产品文档需覆盖小程序使用说明
related_requirements: []
related_changes:
  - add-versioned-product-usage-docs
lifecycle:
  captured: 2026-08-01 08:10:11
  generated: 2026-08-01 08:18:25
  completed: 2026-08-01 08:24:50
  reviewed: 2026-08-01 09:53:42
  approved: 2026-08-01 09:53:42
iteration: sprint-017
openspec_changes:
  - change_id: add-versioned-product-usage-docs
    type: add
    status: archived
readiness: Ready
readiness_notes: 已补齐 requirement、user-stories、business-flow、acceptance 与 trace，并根据用户反馈明确产品文档不是每个版本都自动生成，需在 release-prepare 阶段先确认是否生成或更新；本 REQ 为发布治理 / 产品使用文档 / Mintlify 能力，不涉及管理端 CRUD UI、表单、弹窗或媒体上传，Knowledge-base UI 横切 AC 判定为 N/A。
documents:
  - capture.md
  - requirement.md
  - user-stories.md
  - business-flow.md
  - acceptance.md
  - review.md
expected_openspec_change: add-versioned-product-usage-docs
knowledge_base_refs:
  - docs/knowledge-base/retrospectives/sprint-015-retrospective.md
cross_cutting_tags:
  - release-governance
  - documentation
  - mintlify
knowledge_base_summary: sprint-015 复盘提示发布前 checklist 需集中补证，小程序设备 evidence 应前移到 release-prepare，归档/发布文档需避免未闭环的中间阶段语义残留；本 REQ 已将 usage docs 生成决策确认、usage_docs_preview gate、旧版本维护策略、公开安全扫描和发布文档中间态扫描纳入验收。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-02 17:59:18 | lifecycle-stage-migrate | review → archive（/opsx-archive add-versioned-product-usage-docs） |
| 2026-08-02 17:58:38 | /opsx-archive | Change `add-versioned-product-usage-docs` 已归档，状态同步完成。 |
| 2026-08-01 11:56:22 | /opsx-modify | Change `add-versioned-product-usage-docs` 验收返修已同步；后续已于 2026-08-02 17:58:38 归档闭环。 |
| 2026-08-01 11:15:00 | /opsx-apply | Change `add-versioned-product-usage-docs` 当时完成 apply；后续已于 2026-08-02 17:58:38 归档闭环。 |
| 2026-08-01 10:35:08 | /sprint-propose sprint-017 | REQ-0088 纳入 `sprint-017` 正式范围；关联 Change `add-versioned-product-usage-docs` 纳入同一 Sprint，后续已归档闭环。 |
| 2026-08-01 10:30:19 | /req-opsx | 修正 Workflow Sync 派生残留：REQ 当时尚未纳入 Sprint；Change `add-versioned-product-usage-docs` 后续已归档闭环。 |
| 2026-08-01 09:53:42 | /req-opsx | 创建 OpenSpec Change `add-versioned-product-usage-docs`；后续已归档闭环。 |
| 2026-08-01 09:54:15 | lifecycle-stage-migrate | plan → review（/req-review --approve） |
| 2026-08-01 09:53:42 | /req-review --approve | 需求评审通过，状态更新为 approved，准备迁移 plan → review。 |
| 2026-08-01 08:27:24 | /req-complete | 根据用户反馈修正产品文档生成策略：不是每个版本都生成，release-prepare 必须先确认是否需要生成或更新。 |
| 2026-08-01 08:24:50 | /req-complete | 补齐 user-stories、business-flow、acceptance；Knowledge-base gate 判定为 N/A（无 UI 横切标签），状态更新为 pending_review。 |
| 2026-08-01 08:18:25 | /req-generate | 生成 requirement.md，状态更新为 draft。 |
| 2026-08-01 08:10:11 | /capture | 记录版本化产品使用文档生成、更新、发布门禁与旧版本维护策略需求。 |

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0111-usage-docs-previous-version-semver-sort | medium | done | fix-usage-docs-previous-version-semver-sort | usage docs 前置版本候选使用字符串排序可能选错版本 |
