## Context

REQ-0052 来源于 sprint-008 复盘中“小程序设备验收残留散落”的问题。现有小程序 spec 已要求首页、分类、搜索、商品列表、SKU 详情和全局自定义导航栏在微信真实环境中关注安全区、状态栏、原生胶囊、fixed header 遮挡、触控区域和 320 到 430 pt 视口；但这些验收证据没有统一模板承接。

本 Change 是文档/治理型能力，目标是建立可复制的 `miniapp_device_evidence` 模板和引用规则。它不直接修改 `src/miniapp/`，也不新增自动化截图工具链或真机云测能力。

## Goals / Non-Goals

**Goals:**

- 在长期标准文档中定义小程序 DevTools/真机验收 evidence 模板。
- 让 evidence 能按页面、场景、视口、设备和证据来源分层记录。
- 让 `required`、`passed`、`failed`、`blocked`、`not_applicable`、`follow_up` 六类状态可被后续 REQ、Change 和 Sprint 复用。
- 明确没有 DevTools 或真机 evidence 时，不得在 Sprint 验收、release note 或 Change trace 中写成“设备验收已完成”。
- 引用 `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` 中小程序设备验收独立 Gate 的复盘经验。

**Non-Goals:**

- 不修改小程序页面、组件、样式、路由、API 调用或编译链。
- 不新增 Playwright、小程序自动化、真机云测、截图采集或设备矩阵执行平台。
- 不回填全部历史 Sprint 或历史 Change 的 DevTools/真机 evidence。
- 不修改后端 API、数据库、Orval、Docker Compose、MinIO 或环境变量。
- 不自动创建 follow-up REQ/BUG；若后续发现缺口，只输出可 capture 的标准文案，除非用户明确授权自动 capture。

## Decisions

### D1. 新建独立 capability

将能力建为 `miniapp-device-evidence-template`，而不是修改 `miniapp-home`、`miniapp-global-custom-navigation-bar`、`testing` 或 `agent-workflow-tooling`。

原因：REQ-0052 是跨小程序页面的验收治理模板，既不是单个页面能力，也不是测试框架本身。独立 capability 可以让后续多个小程序 Change 引用同一事实源，避免页面 spec 互相复制模板内容。

### D2. 模板文档沉淀到 docs/standards

实现阶段优先新增 `docs/standards/miniapp-device-evidence-template.md`，并在 Change trace 或 acceptance 中引用该路径。

原因：`docs/standards/` 是治理细则和可复用标准的归属位置；REQ-0052 也明确建议该路径。OpenSpec spec 负责定义系统必须具备的模板能力，长期文档负责承载可复制 YAML 和 Markdown 表格。

### D3. evidence 来源必须分层

模板必须区分静态测试、脚本/单元测试、DevTools 预览、真机验收、N/A 和 follow-up。

原因：静态测试只能证明文件、配置或规则存在；DevTools 只能证明开发者工具环境中的加载和模拟器布局；真机验收才证明指定设备上的真实安全区、触控和微信版本表现。混用结论会直接影响 Sprint 验收和发布说明可信度。

### D4. UI Explore Gate 判定

本 Change 影响小程序验收治理，不提供可见 Web UI，也不存在 `prototype/web/`。因此不触发 Web UI Explore Gate，不选择 CSS Port / Tailwind DS / Asset 策略。

### Conflict Resolution

- 原型：REQ-0052 无 `prototype/web/`、`prototype/miniapp/` 或 PNG Golden Reference。
- 最高优先级证据：REQ 六件套和 `review.md` 条件通过项。
- 与既有 spec 的关系：不修改现有小程序页面 spec；把首页运行入口、导航栏安全区、fixed header、触控区域等作为模板示例和后续引用对象。
- 与 REQ-0039 的关系：复用 evidence 字段、N/A reason 和 remaining risk 思路，但不复用 Web 管理端七层 gate；小程序模板聚焦 DevTools 与真机设备证据。

## Risks / Trade-offs

- [Risk] 只新增模板但后续 Change 不引用，设备验收仍然散落。 → Mitigation: tasks 要求在文档中给出 REQ acceptance、OpenSpec tasks、Change trace、Sprint acceptance-report 和 release note 的引用示例。
- [Risk] 模板字段过重，导致实际验收人员不愿填写。 → Mitigation: 同时提供 YAML 结构和 Markdown 表格，字段短而可复制，允许 N/A、blocked 和 follow_up 说明原因。
- [Risk] 文档模板被误解为自动化能力。 → Mitigation: proposal、design、spec 和 tasks 均明确不新增自动化截图、真机云测或小程序运行时代码。
- [Risk] 截图或录屏证据泄露敏感信息。 → Mitigation: spec 要求只记录仓库相对路径或稳定 artifact 引用，并明确禁止 token、Cookie、密钥、DSN、真实客户数据和本机绝对路径。

## Migration Plan

1. 新增长期标准文档 `docs/standards/miniapp-device-evidence-template.md`。
2. 在文档中提供 `miniapp_device_evidence` YAML 示例、Markdown 表格示例、状态说明和引用位置。
3. 在 Change trace 或 acceptance 中记录本 Change 对 DevTools/真机验收的 N/A 结论：本 Change 只新增模板文档，不修改小程序运行时代码。
4. 补充轻量校验，确认标准文档存在、关键字段存在、敏感信息禁止项存在。
5. 后续小程序 Change 按风险引用模板，逐条记录 DevTools/真机 evidence 或 N/A/follow_up。

## Open Questions

- 无阻塞问题。是否回填历史 evidence、是否引入自动化截图或真机云测，均应另立 REQ 或 Change。
