---
note: workflow-sync — workflow-sync 自动同步 — 11/13 Change archived；0 applied；2 进行中；Sprint `active`
title: sprint-029 规划
created_at: 2026-08-30 15:36:34
updated_at: 2026-09-11 09:19:27
---

# sprint-029 规划

## 1. 目标

### Sprint 目标编号列表

- REQ-0135-authorized-cos-direct-upload
- enforce-product-version-release-gates
- simplify-single-release-target-governance
- automate-product-version-release-prepare
- make-release-propose-next-step-prepare
- converge-release-prepare-automation
- deactivate-environment-tiered-evidence-gates
- rename-evidence-source-specs
- define-connector-directory-boundaries
- REQ-0132-workbuddy-custom-connector
- BUG-0148-miniapp-product-list-card-image-fit
- REQ-0133-miniapp-price-red-display
- REQ-0134-miniapp-public-page-sharing

### enforce-product-version-release-gates 要点

强化发布流程产品版本号门禁，避免后续 release 在 Web 或小程序用户可见版本号未对齐时进入发布确认。

### simplify-single-release-target-governance 要点

收敛发布治理为单一项目发布语义，移除 development / production 发布目标分支、生产环境专属门禁和升级计划目标环境后缀。

### automate-product-version-release-prepare 要点

将 `PRODUCT_VERSION` 同步自动化前移到 `/release-prepare`，发布确认只校验不写版本，`/image-prepare` 前强制版本源已对齐。

### make-release-propose-next-step-prepare 要点

将 `/release-propose` 默认下一步调整为 `/release-prepare`，`/release-status` 仅作为只读状态面板和阻塞排查入口。

### converge-release-prepare-automation 要点

收敛发布准备自动化策略：`/release-propose` 默认声明公告、usage docs 与升级路径决策，`/release-prepare` 统一生成和校验，`/release-publish` 只确认。

### deactivate-environment-tiered-evidence-gates 要点

将环境分层 evidence 从默认 workflow 阻断门禁降级为手动证据来源诊断工具，保留脚本能力但不再自动应用。

### rename-evidence-source-specs 要点

将正式 OpenSpec 中旧环境分层、生产证据后置与强脚本门禁标题收敛为证据来源声明、证明边界和手动诊断语义。

### define-connector-directory-boundaries 要点

明确 WorkBuddy 等外部连接器目录边界：`src/mcp/<connector>/` 承载 MCP 运行时代码，`connectors/<connector>/` 承载 manifest、`mcp.json`、外部 Skill、图标和打包说明。

### REQ-0132-workbuddy-custom-connector 要点

纳入腾讯 WorkBuddy 自定义连接器支持：第一阶段建设本地 stdio MCP + Skill 只读 PoC，覆盖 SKU 搜索、商品详情、品牌/类目查询、目录摘要和管理端写操作 dry-run；第二阶段扩展 HTTPS 远程 MCP、企业鉴权审计、真实写操作和媒体上传。

### BUG-0148-miniapp-product-list-card-image-fit 要点

修复小程序商品列表 grid 卡片图片区偏低、图片填充裁切导致整图无法完整展示的问题，仅覆盖商品列表页、品牌详情商品 Tab 和首页全部产品等复用 `density="grid"` 商品卡片的场景；不扩展 compact/list、详情轮播、API、数据库、对象存储或缩略图生成范围。

### REQ-0133-miniapp-price-red-display 要点

统一小程序有效金额红色与无价、失效状态中性色，覆盖共享卡片、详情主价格、推荐及收藏；保留品牌金和既有页面布局。P2，M／3人天；HTML局部原型已提供，PNG与最终色值、实际样式和视觉证据由后续Change承接。已关联 `update-miniapp-price-red-display`；下一步 `/opsx-apply REQ-0133-miniapp-price-red-display`。

### REQ-0134-miniapp-public-page-sharing 要点

P1，L／5人天（实现3、回归与证据2）。补齐11页朋友和朋友圈分享、安全参数与完整筛选恢复、发现页JS同步及事件语义；复用原生菜单，不新增布局。29条验收未执行，需求已评审，关联Change `add-miniapp-public-page-sharing` 已创建并回填，待 `/opsx-apply REQ-0134-miniapp-public-page-sharing`。

### REQ-0135-authorized-cos-direct-upload 要点

P1，XXL／13人天，完整覆盖视频与图片/附件两阶段。先完成后端授权、持久会话、视频分片、确认和正式对象保护，再完成图片派生及全部既有入口。REQ-0136读取签名刷新不纳入本次范围。review.md C-001～004在对应阶段实现前关闭，C-005在UI实施及交付时完成；Change待创建。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0132-workbuddy-custom-connector | 腾讯 WorkBuddy 自定义连接器支持 | in_sprint | 5 人天 | in_progress 42/44；`add-workbuddy-custom-connector` |
| REQ | REQ-0133-miniapp-price-red-display | 小程序有效价格统一红色展示 | done | 3 人天 | archived `update-miniapp-price-red-display`（2026-09-05 23:04:16） |
| REQ | REQ-0134-miniapp-public-page-sharing | 小程序公开内容页朋友及朋友圈分享 | done | 5 人天 | archived `add-miniapp-public-page-sharing`（2026-09-05 22:30:01） |
| REQ | REQ-0135-authorized-cos-direct-upload | 后端授权的 COS 媒体直传与上传确认 | in_sprint | 13 人天 | in_progress 21/22；`add-authorized-cos-direct-upload` |
| BUG | BUG-0148-miniapp-product-list-card-image-fit | 小程序商品列表 grid 卡片图片无法完整显示 | done | 1 人天 | archived `fix-miniapp-product-grid-image-fit`（2026-09-07 22:55:02） |
| Change | enforce-product-version-release-gates | enforce product version release gates | archived | 1 人天 | archived `enforce-product-version-release-gates`（2026-08-30 23:59:59） |
| Change | simplify-single-release-target-governance | simplify single release target governance | archived | 1 人天 | archived `simplify-single-release-target-governance`（2026-08-30 23:59:59） |
| Change | automate-product-version-release-prepare | automate product version release prepare | archived | 1 人天 | archived `automate-product-version-release-prepare`（2026-08-30 23:59:59） |
| Change | make-release-propose-next-step-prepare | make release propose next step prepare | archived | 1 人天 | archived `make-release-propose-next-step-prepare`（2026-08-31 23:59:59） |
| Change | converge-release-prepare-automation | converge release prepare automation | archived | 1 人天 | archived `converge-release-prepare-automation`（2026-08-31 09:17:22） |
| Change | deactivate-environment-tiered-evidence-gates | deactivate environment tiered evidence gates | archived | 1 人天 | archived `deactivate-environment-tiered-evidence-gates`（2026-08-31 10:31:39） |
| Change | rename-evidence-source-specs | rename evidence source specs | archived | 1 人天 | archived `rename-evidence-source-specs`（2026-08-31 14:06:32） |
| Change | define-connector-directory-boundaries | define connector directory boundaries | archived | 1 人天 | archived `define-connector-directory-boundaries`（2026-09-04 23:59:59） |

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0132 | 腾讯 WorkBuddy 自定义连接器支持 | P1 | in_sprint | in_progress 42/44；`add-workbuddy-custom-connector` |
| REQ-0133 | 小程序有效价格统一红色展示 | P2 | done | archived `update-miniapp-price-red-display`（2026-09-05 23:04:16） |
| REQ-0134 | 小程序公开内容页朋友及朋友圈分享 | P1 | done | archived `add-miniapp-public-page-sharing`（2026-09-05 22:30:01） |
| REQ-0135 | 后端授权的 COS 媒体直传与上传确认 | P1 | in_sprint | in_progress 21/22；`add-authorized-cos-direct-upload` |
<!-- workflow-sync:scope-requirements:end -->

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0148 | 小程序商品列表 grid 卡片图片无法完整显示 | medium | done | archived `fix-miniapp-product-grid-image-fit`（2026-09-07 22:55:02） |
<!-- workflow-sync:scope-bugs:end -->

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `enforce-product-version-release-gates` | — | archived | archived `enforce-product-version-release-gates`（2026-08-30 23:59:59） |
| `simplify-single-release-target-governance` | — | archived | archived `simplify-single-release-target-governance`（2026-08-30 23:59:59） |
| `automate-product-version-release-prepare` | — | archived | archived `automate-product-version-release-prepare`（2026-08-30 23:59:59） |
| `make-release-propose-next-step-prepare` | — | archived | archived `make-release-propose-next-step-prepare`（2026-08-31 23:59:59） |
| `converge-release-prepare-automation` | — | archived | archived `converge-release-prepare-automation`（2026-08-31 09:17:22） |
| `deactivate-environment-tiered-evidence-gates` | — | archived | archived `deactivate-environment-tiered-evidence-gates`（2026-08-31 10:31:39） |
| `rename-evidence-source-specs` | — | archived | archived `rename-evidence-source-specs`（2026-08-31 14:06:32） |
| `define-connector-directory-boundaries` | — | archived | archived `define-connector-directory-boundaries`（2026-09-04 23:59:59） |
| `add-workbuddy-custom-connector` | REQ-0132-workbuddy-custom-connector | in_progress | in_progress 42/44；`add-workbuddy-custom-connector` |
| `fix-miniapp-product-grid-image-fit` | BUG-0148-miniapp-product-list-card-image-fit | archived | archived `fix-miniapp-product-grid-image-fit`（2026-09-07 22:55:02） |
| `update-miniapp-price-red-display` | REQ-0133-miniapp-price-red-display | archived | archived `update-miniapp-price-red-display`（2026-09-05 23:04:16） |
| `add-miniapp-public-page-sharing` | REQ-0134-miniapp-public-page-sharing | archived | archived `add-miniapp-public-page-sharing`（2026-09-05 22:30:01） |
| `add-authorized-cos-direct-upload` | REQ-0135-authorized-cos-direct-upload | in_progress | in_progress 21/22；`add-authorized-cos-direct-upload` |
<!-- workflow-sync:scope-changes:end -->

REQ：2 个已纳入正式范围；BUG：1 个已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：现有Change状态以Scope派生表为准；REQ-0134已关联 `add-miniapp-public-page-sharing`；其他Change关联状态以机器范围及派生表为准。

## 3. 工作量与容量

| 项 | 值 |
|---|---:|
| 容量基线 | 30 人天 |
| 估算 | 35 SP / 35 人天 |
| 容量占用 | 116.67% |
| fix 缓冲 | 0 人天 / 0%（另超容量5人天） |

## 4. 横切预防清单

- `product_data_collection_observability`: applicable。
- `affected_layers`: backend_api、request_logs、task_traces、task_trace_spans、admin_web_indirect、object_storage_indirect、deployment。
- `reason`: REQ-0132 连接器将作为直接 API 调用方访问 ProjectTilesFST，并在第二阶段执行管理端写操作、媒体上传和远程 MCP 服务部署，涉及请求来源识别、工具调用审计、任务链路、错误摘要、环境变量和凭据安全。
- `validation`: Sprint 阶段已承接 REQ-0132 的观测声明；后续 `/opsx-apply` 与实现 Change 必须覆盖直接 API 调用、鉴权越权、dry-run 不写入、真实写操作审计、上传链路、OpenAPI/Orval、Docker/HTTPS 部署和脱敏日志验证。
- `best_practices`: `docs/knowledge-base/best-practices/admin-media-upload-chain.md`；媒体上传在第一阶段仅 dry-run，不执行真实上传，第二阶段真实上传必须沿用后端鉴权和对象存储适配层。
- `BUG-0148 product_data_collection_observability`: n/a；仅调整小程序 grid 商品卡片展示样式和静态用例，不涉及 API、DB、请求封装、日志审计、行为埋点、Task Trace 或对象存储。
- `BUG-0148 media_acceptance`: key/object/URL 为 n/a，渲染验收待 `/opsx-apply BUG-0148-miniapp-product-list-card-image-fit` 与实现阶段通过小程序页面截图或 DevTools 证据补齐。

- `REQ-0133 product_data_collection_observability`: not_applicable，affected_layers=[]；仅价格展示状态、token及规范调整，不变更API、DB、请求封装、行为采集、请求日志或Task Trace；通过AC-OBS-001至003核对，Orval及Docker为N/A。
- `REQ-0133 cross_cutting_tags`: []；无管理端列表、表单、弹窗及上传标签。沿用AC-PROTOTYPE-001至004验证UI Contract、Skeleton、视觉证据及实际样式，未执行验收不得标为通过。

- `REQ-0134 product_data_collection_observability`: applicable，affected_layers=[miniapp, usage_events]；API、DB、request_logs及保留周期无契约变化，Task Trace因无新后端复杂任务为N/A。AC-018至021覆盖事件语义、脱敏、失败降级和既有请求链路；功能验证未执行，Orval和Docker无需新增验证。
- `REQ-0134 knowledge_base_refs`: miniapp-custom-navigation.md与sprint-028-retrospective.md；承接AC-XCUT-001至005，验证无栈返回、重复进入、胶囊避让、图片真实渲染和证据来源。引用导航实践仍为draft，需求已评审采纳具体AC。

- REQ-0135：`product_data_collection_observability=applicable`；affected_layers=[web_admin, backend_api, request_logs, usage_events, task_traces, task_trace_spans, object_storage]。AC-016～018覆盖端事件、请求与任务阶段、来源区分、脱敏、保留期、API/DB/Orval及Compose；店主端和小程序仅展示回归，新增上传封装N/A。validation：已核对需求声明与24条待执行AC，尚无实现证据。
- REQ-0135：`admin-modal`承接`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`的专属类、1440px computed width及矮视口滚动；`media-upload`承接`docs/knowledge-base/best-practices/admin-media-upload-chain.md`的状态机、即时回显、Web :3000控制链路和历史读取，共6条横切AC。直传主体不经nginx，保留代理路径独立验证边界大小。

## 5. 知识库承接

- 最近复盘：`docs/knowledge-base/retrospectives/sprint-028-retrospective.md`，承接 AI Usage 归因与 workflow evidence 描述需在命令链路中保持明确。
- 命中最佳实践：`docs/knowledge-base/best-practices/admin-media-upload-chain.md`，用于约束后续媒体上传真实写入阶段的鉴权、适配层和证据链。
- 命中最佳实践：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`，用于约束 BUG-0148 实现后的媒体渲染验收边界。

- REQ-0133承接sprint-028环境证据边界经验：静态对比度、HTML Mock、DevTools及真机证据分别声明；AI Usage按默认发现执行，估算回退不冒充实际计量。

- REQ-0134承接分享直达返回和实际卡片渲染证据；sprint-028 open行动项A-028-01（AI用量覆盖）、A-028-02（媒体证据包）、A-028-03（发布面板表达）仅作观察，不自动纳入或创建Issue。采集费用回退不表述为实际用量，开发证据不替代真机接收。

- REQ-0135承接最近sprint-028复盘的媒体四联证据和环境来源边界；A-028-01用量归因、A-028-02证据包、A-028-03发布面板表达继续观察，不新增治理范围或自动创建Issue。两份命中实践仍为draft，按已评审AC执行。

## 6. 依赖 ASCII 树

```text
REQ-0135-authorized-cos-direct-upload（P1，13人天）
└── /req-opsx REQ-0135-authorized-cos-direct-upload（待创建并回填同一Sprint）
    ├── C-001/002/003：授权、确认一致性、参数与验收阈值冻结
    ├── 视频完整闭环 → 安全/竞态/Compose验收
    └── C-004图片选型 → 图片及附件全入口 → C-005视觉与媒体兼容验收

REQ-0134-miniapp-public-page-sharing（P1，5人天）
└── add-miniapp-public-page-sharing（已回填sprint.yaml）
    └── /opsx-apply REQ-0134-miniapp-public-page-sharing
        ├── 参数白名单与客户端版本冻结
        ├── 11页分享、筛选恢复、事件语义及TS/JS同步
        └── 双渠道真机接收与29条验收

REQ-0133-miniapp-price-red-display（P2，3人天）
└── update-miniapp-price-red-display
    └── /opsx-apply REQ-0133-miniapp-price-red-display
        ├── 保留BUG-0148商品卡片图片适配成果
        ├── 价格状态与token、TS/JS同步
        └── 聚焦回归、Skeleton与视觉证据

REQ-0132-workbuddy-custom-connector
└── /opsx-apply REQ-0132-workbuddy-custom-connector
    └── openspec/changes/add-workbuddy-custom-connector
        ├── src/mcp/workbuddy/
        ├── connectors/workbuddy/
        ├── backend API / auth / observability
        └── tests / docs / deployment config

BUG-0148-miniapp-product-list-card-image-fit
└── openspec/changes/fix-miniapp-product-grid-image-fit
    └── /opsx-apply BUG-0148-miniapp-product-list-card-image-fit
        ├── src/miniapp/components/product-card/
        ├── src/miniapp/pages/product-list/
        ├── src/miniapp/pages/brand-detail/
        └── tests/test_miniapp_static.py
```

## 7. 关联文档

- `issues/requirements/review/REQ-0135-authorized-cos-direct-upload/`

- `issues/requirements/archive/REQ-0134-miniapp-public-page-sharing/`

- `issues/requirements/review/REQ-0132-workbuddy-custom-connector/`
- `issues/requirements/archive/REQ-0133-miniapp-price-red-display/`
- `issues/bugs/archive/BUG-0148-miniapp-product-list-card-image-fit/`
- `connectors/README.md`
- `openspec/specs/agent-workflow-tooling/spec.md`

## 8. 里程碑、风险与发布计划

REQ-0133按“需求纳入→创建Change并回填→UI Contract与Skeleton确认→实现及回归→视觉验收→归档”推进，具体日期随实施排期确定。优先完成缺陷项及P1范围；价格优化作为P2实施，当前修复缓冲与容量风险以本节最新REQ-0135规划为准。

共享商品卡片与BUG-0148存在文件重叠，价格样式不得回退grid图片完整显示能力。PNG和色值确认是后续视觉取证项，未完成前不得关闭关联UI验收项；需确保小字号价格对比度≥4.5:1。

发布说明将REQ-0133列为计划范围，验收完成后再纳入产品版本发布流程；本规划不指定产品版本、不执行部署或发布。

REQ-0134里程碑：需求纳入→创建Change并回填→冻结参数及测试版本→实现与聚焦回归→朋友/朋友圈接收验证→归档。先完成缺陷及P1范围，再推进P2价格展示；与REQ-0133触及相同页面时串行整合并联合回归。

容量风险：追加REQ-0135后为35/30人天（116.67%），超容量5人天，剩余fix缓冲0，低于30%建议。已完成范围不因归档从本Sprint累计估算中扣除；不自动移出已纳入项。设备不足可能延迟验收，应保留明确补证记录。REQ-0134仅列为计划交付，验收后再进入产品版本发布，不执行部署。


REQ-0135里程碑按依赖推进：纳入范围→创建Change→关闭阶段一设计条件→视频实现与验收→关闭图片选型条件→图片及附件实现与全入口验收→整体归档。未确定日历承诺，不把当前空end_date解释为可无限扩充容量。

REQ-0135估算分解：授权/会话/确认/稳定对象4人天，视频分片与Web状态2人天，图片派生与多入口3人天，安全/竞态/Compose及展示兼容4人天。若新增估算超过1人天，总量将超过36人天硬线，必须拆分或替换范围；紧急缺陷优先，优先讨论将尚未实施的图片阶段移至下一Sprint，需明确重新规划，不能仅移动文案或提前关闭REQ。当前只做风险记录，不自动创建sprint-030。

REQ-0135发布按媒体类别灰度，可视频先上线，后续图片/附件完成后才可关闭完整REQ；仅列计划交付，未指定产品版本或执行部署。授权、COS跨域和观测需生产证据；图片选型若引入收费服务须先明确授权。
