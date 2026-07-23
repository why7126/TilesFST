---
change_id: add-miniapp-wechat-share-pages
type: add
status: proposed
created_at: 2026-07-21 14:44:56
updated_at: 2026-07-21 22:57:26
iteration: sprint-010
source_requirement: REQ-0064-miniapp-wechat-share-pages
source_requirement_path: issues/requirements/archive/REQ-0064-miniapp-wechat-share-pages/
related_requirements:
  - REQ-0041-miniapp-home
  - REQ-0044-miniapp-sku-detail-page
  - REQ-0047-product-list-common-component-application
  - REQ-0048-miniapp-global-custom-navigation-bar
  - REQ-0053-miniapp-custom-navigation-best-practice
  - REQ-0058-brand-detail-home-page
affected_capabilities:
  - miniapp-home
  - miniapp-sku-detail-page
  - miniapp-product-list-page
  - miniapp-brand-detail-home-page
  - miniapp-global-custom-navigation-bar
  - miniapp-device-evidence-template
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-009-retrospective.md
impact:
  backend: not_expected
  web: not_affected
  miniapp: affected
  admin: not_affected
  database: not_expected
  storage: existing_public_or_local_fallback_only
  api: not_expected
  orval: not_expected
  docker_compose: not_required
device_evidence:
  devtools_320_375_430: required
  real_device: required_or_follow_up
  static_test_boundary: must_not_be_reported_as_real_device
---

# Trace

## Requirement Readiness Report

| 项目 | 结论 |
|---|---|
| REQ status | approved |
| requirement.md | present |
| user-stories.md | present |
| business-flow.md | present |
| acceptance.md | present |
| trace.md | present |
| prototype strategy | present: `prototype/miniapp/context.md` |
| readiness | Ready |

## Impact Analysis

```yaml
impact:
  backend: not_expected
  web: not_affected
  miniapp: affected
  admin: not_affected
  database: not_expected
  storage: existing_public_or_local_fallback_only
  api: not_expected
capabilities:
  new: []
  modified:
    - miniapp-home
    - miniapp-sku-detail-page
    - miniapp-product-list-page
    - miniapp-brand-detail-home-page
    - miniapp-global-custom-navigation-bar
    - miniapp-device-evidence-template
change_type: add
```

## Conflict Report

| Source | Result |
|---|---|
| `prototype/web/` | N/A，REQ 无 Web prototype。 |
| `prototype/miniapp/context.md` | 使用小程序原生分享入口，不新增自绘分享 UI。 |
| `acceptance.md` | 已覆盖 4 页面 × 2 分享渠道、参数保留、埋点、设备 evidence 和安全边界。 |
| `rules/ui-design.md` | 不新增 Web UI；小程序继续沿用深色品牌风格。 |

结论：无 HTML / PNG 冲突。实现阶段以 `prototype/miniapp/context.md`、acceptance 和 delta specs 为准。

## PNG / Device Evidence Checklist

- DevTools 320 / 375 / 430 pt 或等价静态视口 evidence：required。
- 真机 evidence：required；无法执行时必须标记 `blocked` 或 `follow_up`。
- 静态测试通过不得写作 DevTools 或真机通过。
- Evidence 不得记录本机绝对路径、token、Cookie、Authorization header、`.env`、真实客户数据或 MinIO 凭据。

## Implementation Evidence

| 项目 | 结论 |
|---|---|
| 分享页面矩阵 | 首页、SKU 详情页、商品列表页、品牌详情页均补齐 `onShareAppMessage` 与 `onShareTimeline`。 |
| 运行入口同步 | 四个目标页面同目录 `.ts` 与微信开发者工具实际加载 `.js` 已同步分享逻辑。 |
| 商品列表参数 | 分享 query 使用 `categoryId`、`categoryLevel`、`categoryName`、`brandId`、`keyword`、`section`、`sourcePage` 白名单并编码。 |
| 埋点 | `home_share`、`sku_share_click`、`product_list_share_click`、`brand_detail_share_click` 均为 best-effort；失败不阻断分享。 |
| API / DB / Orval | 未新增接口、响应字段、数据库表或字段；无需 Orval。 |
| Evidence | `implementation/share-evidence.md` 记录 static_review、320/375/430 pt 等价静态视口检查与 real_device_follow_up。 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-21 22:57:26 | /opsx-apply | 实现四页面微信朋友/朋友圈分享、运行 `.js` 同步、静态测试与 evidence；真机验收标记 follow_up。 |
| 2026-07-21 14:59:21 | /sprint-propose sprint-010 | 纳入 sprint-010 正式迭代范围；保持 proposed，等待 `/opsx-apply add-miniapp-wechat-share-pages`。 |
| 2026-07-21 14:44:56 | /req-opsx | 从 REQ-0064 创建 OpenSpec Change，状态 proposed。 |
