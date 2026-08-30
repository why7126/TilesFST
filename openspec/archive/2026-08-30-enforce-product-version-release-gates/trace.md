---
created_at: 2026-08-30 15:36:34
updated_at: 2026-08-30 15:36:34
---

# Trace

```yaml
change_id: enforce-product-version-release-gates
source:
  type: spec-opt
  command: "/spec-opt 强化发布流程产品版本号门禁"
  sprint: sprint-029
root_cause:
  status: confirmed
  summary: release validator 仅检查 shared PRODUCT_VERSION，并允许 version_change_rationale 放行，未覆盖小程序用户可见版本源。
affected_governance:
  - release-prepare
  - release-publish
  - release-status
  - release-propose
  - image-prepare
  - rules/release.md
  - scripts/validate-release.py
product_data_collection_observability:
  applicability: not_applicable
  affected_layers: []
  rationale: 纯发布治理与校验脚本变更，不修改 API、DB、端侧请求封装、日志审计、行为埋点或 Task Trace。
```
