---
note: workflow-sync — 7/8 Change 已 archive；0 applied；待人工 sign-off
created_at: 2026-07-04 22:30:20
updated_at: 2026-07-10 08:50:39
title: Sprint 005 验收报告
purpose: 记录 Sprint 005 验收结果与遗留项（模板）
content: 基于 REQ-0029 acceptance.md、REQ-0030 acceptance.md、BUG-0056 acceptance.md、BUG-0057 acceptance.md、BUG-0058 acceptance.md、BUG-0059 acceptance.md、BUG-0060 acceptance.md 与 BUG-0061 acceptance.md
source: /sprint-propose REQ-0030；/sprint-propose REQ-0029 纳入 sprint-005；/sprint-propose BUG-0056 纳入 sprint-005；/sprint-propose BUG-0057 纳入 sprint-005；/sprint-propose BUG-0058 纳入 sprint-005；/sprint-propose BUG-0059 纳入 sprint-005；/sprint-propose BUG-0060 纳入 sprint-005；/sprint-propose BUG-0061 纳入 sprint-005
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: draft
---

# Sprint 005 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-005 |
| 关联需求 | REQ-0029-admin-list-foundation-components；REQ-0030-api-docs-swagger-policy-checklist |
| 关联 BUG | BUG-0056-sprint-archive-incomplete-tasks-gate；BUG-0057-api-governance-tags-known-debt；BUG-0058-workflow-sync-check-time-drift-idempotency；BUG-0059-user-password-copy-not-working；BUG-0060-audit-log-request-id-copy-error；BUG-0061-change-password-policy-error-message-unclear |
| 关联 Change | REQ-0029: `add-admin-list-foundation-components`；REQ-0030: `update-api-docs-swagger-policy-checklist`；BUG-0056: `fix-sprint-archive-incomplete-tasks-gate`；BUG-0057: `fix-api-governance-route-tags-known-debt`；BUG-0058: `fix-workflow-sync-check-time-drift-idempotency`；BUG-0059: `fix-user-password-copy-not-working`；BUG-0060: `fix-audit-log-request-id-copy-error`；BUG-0061: `fix-change-password-policy-error-message` |
| 计划验收日期 | 2026-07-18 22:30:20 |
| 验收结论 | 待验收 |
| 验收人 | 待填写 |

## REQ-0029 功能验收

> 来源：`issues/requirements/archive/REQ-0029-admin-list-foundation-components/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `add-admin-list-foundation-components` proposed

### MetricCard / MetricCardGrid

- [ ] AC-001 MUST 提供 `MetricCard` 或等价组件，用于管理端列表页指标摘要。
- [ ] AC-002 `MetricCard` MUST 稳定输出 `.metric-card`、`.metric-label`、`.metric-value`、`.metric-desc`。
- [ ] AC-003 `MetricCard` MUST 支持 `label`、`value`、`description` 基础字段。
- [ ] AC-004 `MetricCard` MUST 对空值、加载中或未返回数据提供统一展示策略。
- [ ] AC-005 `MetricCard` SHOULD 支持 danger / 异常描述变体，并用于日志审计等异常指标。
- [ ] AC-007 MUST 提供 `MetricCardGrid` 或等价容器，减少页面重复书写 `summary-grid`。
- [ ] AC-008 `MetricCardGrid` MUST 支持 2、3、4 个指标卡布局。
- [ ] AC-009 `MetricCardGrid` MUST 支持 `aria-label` 标识指标区域。
- [ ] AC-010 指标卡容器替换后 MUST 不造成 hero、filter、table 的纵向位移。

### 分页窗口与页面接入

- [ ] AC-012 MUST 将分页窗口算法沉淀到共享工具或管理端共享层，禁止新页面继续从页面局部复制算法。
- [ ] AC-013 分页窗口工具默认 MUST 最多展示 5 个页码。
- [ ] AC-015 分页窗口工具 MUST 对 `currentPage < 1`、`currentPage > totalPages`、`totalPages < 1`、`maxVisible < 1` 做兜底。
- [ ] AC-018 管理端列表页分页 MUST 保留 `.page-summary`。
- [ ] AC-019 管理端列表页分页 MUST 保留 `.page-right`。
- [ ] AC-020 管理端列表页分页 MUST 保留 `.page-buttons`。
- [ ] AC-021 管理端列表页分页 MUST 保留 `.page-size-wrap`。
- [ ] AC-024 首批接入页面 MUST 从 `TileSkuManagementPage`、`LogAuditPage`、`ApiDocsPage`、`BrandManagementPage` 中选择 2–3 个。
- [ ] AC-026 首批页面替换后 MUST 保持原有筛选、分页状态、空态、权限逻辑不变。

### 设计系统与测试

- [ ] AC-028 `/design-system` 或管理端设计验收区 MUST 展示 `MetricCard` / `MetricCardGrid` 基础样例。
- [ ] AC-033 MUST 为 `MetricCard` 增加渲染测试，检查 label、value、description 与关键 DOM class。
- [ ] AC-034 MUST 为分页窗口工具增加或迁移单元测试。
- [ ] AC-035 SHOULD 为首批接入页面保留结构测试，检查 `summary-grid`、`metric-card`、`page-summary`、`page-right`、`page-buttons`、`page-size-wrap`。
- [ ] AC-037 本需求 MUST NOT 修改后端分页 API。
- [ ] AC-038 本需求 MUST NOT 修改数据库表结构。
- [ ] AC-039 本需求 MUST NOT 修改 OpenAPI 或触发 Orval。
- [ ] AC-040 本需求 MUST NOT 引入新的颜色 Token 或全局主题变化。

## REQ-0030 功能验收

> 来源：`issues/requirements/review/REQ-0030-api-docs-swagger-policy-checklist/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `update-api-docs-swagger-policy-checklist` proposed

### checklist 固定章节与触发范围

- [ ] AC-001 后续 API docs refine、接口文档页模板化或 Swagger 入口调整的 design / acceptance 包含“Swagger Web 代理与生产 Try It Out 策略”检查章节。
- [ ] AC-002 checklist 明确 Swagger 入口调整、Web 代理调整、`/docs` / `/redoc` / `/openapi.json` 路由调整、生产部署说明调整时触发。

### 同源入口与行级深链

- [ ] AC-003 Swagger 主入口使用 `/docs` 或经 design 说明的等价同源 Web 路径，且前端不硬编码后端 host、端口或容器服务名。
- [ ] AC-004 若 API docs 页面提供行级 Swagger 查看，链接使用同源 deep link，且仅对 `included_in_openapi=true` 且存在可用 `operation_id` 的路由启用。
- [ ] AC-005 非 OpenAPI 路由或缺少 `operation_id` 的路由保持可见但不可点击跳转。

### 代理与生产策略

- [ ] AC-006 本地开发环境验证 `/docs`、`/redoc`、`/openapi.json` 可进入后端文档响应或等价响应。
- [ ] AC-007 Docker Web 环境验证 `/docs` 不进入 Web 首页、React Router fallback 或其他非后端文档页面。
- [ ] AC-008 生产等价环境记录 `/docs`、`/redoc`、`/openapi.json` 的反向代理策略或 N/A 原因。
- [ ] AC-009 生产环境 Swagger 文档可见时，`Try It Out` 禁用、隐藏或等价只读。
- [ ] AC-010 OpenSpec design 检查后端 `APP_ENV` 与 Swagger UI 参数策略，生产环境不依赖前端文案单点防护。

### 安全与文档同步

- [ ] AC-011 页面展示调试策略时，文案与实际环境策略一致，生产环境不得展示“可在线调试”等误导信息。
- [ ] AC-012 Swagger 链接、hash、query、localStorage 新键、页面文案和验收记录不包含 Bearer Token、JWT Secret、数据库 DSN、MinIO AccessKey/SecretKey 或真实环境变量值。
- [ ] AC-013 OpenSpec Change 明确是否同步 `docs/03-api-index.md` 与 `docs/standards/api-governance.md`；若不同步，已在 design 或 trace 中说明原因。
- [ ] AC-014 review 可追踪到 Sprint 004 复盘 A-006，并说明该行动项通过 REQ-0030 进入正式需求链路。
- [ ] AC-015 trace / tasks / acceptance 记录本地、Docker、生产等价策略的验证结果；无法自动化时标注人工验证方式。

## 横切 AC

本 Sprint 不触发 `media-upload` 横切 AC；REQ-0029 与 BUG-0060 触发 `admin-list` 横切 AC。BUG-0059 涉及管理端弹窗修复，触发 `admin-modal` 横切 AC。BUG-0061 涉及管理端修改密码弹窗与表单错误提示，额外触发 `admin-modal` 与 `admin-form` 横切 AC。

### 管理端列表横切验收

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`

- [ ] 日志审计页复制成功/失败/兜底反馈使用 fixed toast 或等价固定层，不引起 hero、表格或分页纵向位移。
- [ ] REQ-0029 首批接入页面的指标摘要 DOM 使用 `article.metric-card` + `.metric-label` + `.metric-value` + `.metric-desc`。
- [ ] REQ-0029 首批接入页面的分页 DOM 使用左侧 `.page-summary` 与右侧 `.page-right` 页码 + 每页条数。
- [ ] REQ-0029 分页窗口最多展示 5 个页码，且页面结构测试覆盖 `.page-buttons` 与 `.page-size-wrap`。
- [ ] 日志审计页分页 DOM、表格卡片和 sticky action column 不因复制修复回归。
- [ ] `request_id` 复制按钮保留在带有完整 `request_id` 的日志行中；无 `request_id` 的行不展示复制按钮。

### 管理端弹窗横切验收

> 来源：`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`

- [ ] 弹窗 TSX 不新增 `modal-card` 与专属类双挂载，避免宽度 CSS 层叠回归。
- [ ] 一次性密码结果弹窗在 1440 视口下宽度与现有用户管理弹窗基线一致。
- [ ] 矮视口下弹窗 body scroll、关闭按钮和主操作按钮仍可访问。
- [ ] 复制成功/失败提示不造成弹窗明显布局抖动。
- [ ] 测试导入相关 CSS 时不会因层叠顺序导致弹窗宽度断言漂移。
- [ ] 修改密码弹窗错误提示不造成弹窗布局抖动。
- [ ] 修改密码弹窗仍保留可访问的错误提示区域与关闭能力。

### 管理端表单横切验收

> 来源：`docs/knowledge-base/best-practices/admin-form-page-consistency.md`

- [ ] 修改密码失败反馈不得使用 `window.alert` 或原生浏览器弹窗。
- [ ] 成功/失败反馈不得引发表单区域明显位移。
- [ ] 错误提示应归属到对应字段或表单可理解区域，避免用户误判操作对象。

## BUG-0056 回归验收

> 来源：`issues/bugs/archive/BUG-0056-sprint-archive-incomplete-tasks-gate/acceptance.md`  
> 状态：done；OpenSpec Change `fix-sprint-archive-incomplete-tasks-gate` archived

### 默认阻断未完成 tasks

- [ ] AC-001 Sprint 的任一 Change `tasks.md` 存在 `- [ ]` 时，归档前置校验返回非零退出码。
- [ ] AC-001 报告明确列出 Change ID 与未完成任务数。

### 已归档 Change 仍可发现未完成项

- [ ] AC-002 Sprint 已在 `iterations/archive/` 且对应 archived Change 的 `tasks.md` 仍有未完成项时，校验脚本继续报告 blocked。
- [ ] AC-002 校验不得因为 Change 已在 archive 目录而跳过 tasks 检查。

### 完成状态通过

- [ ] AC-003 Sprint 内所有 Change 的 `tasks.md` 均为 `- [x]` 时，校验脚本返回 0。
- [ ] AC-003 报告 verdict 为 PASS。

### 命令文档强制使用校验脚本

- [ ] AC-004 Codex `source-command-sprint-archive` skill MUST 要求先运行 readiness 校验脚本。
- [ ] AC-004 默认 blocked verdict MUST 停止归档、停止 Sprint close、停止 issue promote。

## BUG-0057 回归验收

> 来源：`issues/bugs/archive/BUG-0057-api-governance-tags-known-debt/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-api-governance-route-tags-known-debt` proposed

### route tag 单一事实源

- [x] AC-001 后端 API route tags 仅保留一个事实源。
- [x] AC-001 同一 operation 不再同时出现 router-level tag 与 decorator-level tag 合并后的双 tag。
- [x] AC-001 `auth`、`profile`、`uploads` 等路由不再生成重复 tag，例如 `["auth", "auth"]`。

### OpenAPI tag 命名统一

- [x] AC-002 最终 OpenAPI 中每个 operation 的 `tags` 数量为 1。
- [x] AC-002 tag 使用统一命名体系，建议为 kebab-case。
- [x] AC-002 不再出现 `Admin Brands`、`Admin Tile SKUs` 等展示名 tag 与技术名 tag 并存。

### API governance 校验补强

- [x] AC-003 `scripts/validate-api-standard.py` 增加最终 OpenAPI operation tags 校验。
- [x] AC-003 校验覆盖多 tag、重复 tag、非 kebab-case tag。
- [x] AC-003 构造或保留回归测试，证明上述异常会导致校验失败。

### OpenAPI / Orval 同步

- [x] AC-004 重新导出 `src/web/openapi.json`。
- [x] AC-004 如生成物变化，运行 Orval 并同步 `src/web/src/shared/api/generated.ts`。
- [x] AC-004 确认管理端接口文档页面的 tag 展示不再受重复/双轨 tags 影响。

### 回归验证

- [x] AC-005 `python scripts/validate-api-standard.py` 通过。
- [x] AC-005 OpenAPI operation tags 统计结果满足：多 tag operation 为 0，重复 tag operation 为 0，非 kebab-case tag operation 为 0。
- [x] AC-005 不改变 API 路径、请求参数、响应结构或错误码语义。

## BUG-0058 回归验收

> 来源：`issues/bugs/archive/BUG-0058-workflow-sync-check-time-drift-idempotency/acceptance.md`  
> 状态：applied，待归档；OpenSpec Change `fix-workflow-sync-check-time-drift-idempotency` applied

### 归档时间稳定来源

- [x] AC-001 archived Change 渲染到 Sprint Scope 表时，不使用 issue trace 或 change trace frontmatter `updated_at` 作为归档时间事实源。
- [x] AC-001 归档时间优先使用 lifecycle、变更记录或归档目录日期等稳定来源。

### Markdown frontmatter 幂等

- [x] AC-002 workflow-sync 处理 Markdown 且渲染结果与原文一致时，不刷新 frontmatter `updated_at`。
- [x] AC-002 普通同步后再次执行 `--check` 保持 no delta。

### workflow-sync check 幂等

- [x] AC-003 连续执行两次 `python scripts/sync-workflow-status.py --check`，第二次返回 0。
- [x] AC-003 不报告 `iterations/archive/sprint-004/sprint.md` 仅时间字段 drift。

### 回归测试

- [x] AC-004 自动化测试覆盖 issue trace `updated_at` 晚于真实归档记录的场景。
- [x] AC-004 自动化测试覆盖无正文变化时 `persist_markdown` 不 touch `updated_at`。


## BUG-0059 回归验收

> 来源：`issues/bugs/archive/BUG-0059-user-password-copy-not-working/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-user-password-copy-not-working` proposed

### 创建用户后可复制初始密码

- [ ] AC-001 创建新用户成功后，一次性初始密码弹窗展示。
- [ ] AC-001 点击「复制密码」后，剪贴板内容与弹窗展示的完整 `initial_password` 一致。
- [ ] AC-001 页面展示复制成功反馈。

### 重置密码后可复制新随机密码

- [ ] AC-002 重置密码成功后，一次性随机密码弹窗展示。
- [ ] AC-002 点击「复制密码」后，剪贴板内容与弹窗展示的完整 `password` 一致。
- [ ] AC-002 页面展示复制成功反馈。

### 剪贴板失败 fallback

- [ ] AC-003 Clipboard API 不存在、权限被拒绝或 `writeText` 失败时，页面不得静默失败。
- [ ] AC-003 页面展示失败提示或手动复制指引。
- [ ] AC-003 尽可能选中一次性密码文本，帮助管理员手动复制。

### 一次性密码安全边界

- [ ] AC-004 弹窗继续提示「关闭后不可再次查看」或等价风险说明。
- [ ] AC-004 不新增再次查询一次性明文密码的接口或入口。
- [ ] AC-007 不修改用户管理 API 请求路径、响应字段或错误码。
- [ ] AC-007 不修改数据库 schema。
- [ ] AC-007 不将一次性明文密码持久化到数据库、日志、审计事件或长期文档。

### 链路与测试

- [ ] AC-005 创建用户成功 Toast、重置密码成功 Toast、用户列表刷新行为不回归。
- [ ] AC-005 受保护账号的重置密码按钮仍置灰，不绕过既有权限边界。
- [ ] AC-006 新增或更新 `ResetPasswordDialog` 前端测试。
- [ ] AC-006 测试覆盖复制成功路径，并断言 `navigator.clipboard.writeText` 使用当前展示密码调用。
- [ ] AC-006 测试覆盖复制失败路径，并断言失败提示或手动复制指引。
- [ ] AC-006 SHOULD 覆盖 Clipboard API 不存在时的 fallback 行为。

## BUG-0060 回归验收

> 来源：`issues/bugs/archive/BUG-0060-audit-log-request-id-copy-error/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-audit-log-request-id-copy-error` proposed

### request_id 复制成功路径

- [ ] AC-001 管理员打开日志审计页后，带有 `request_id` 的日志记录仍展示复制按钮。
- [ ] AC-002 点击复制按钮且 Clipboard API 可用时，完整 `request_id` 写入剪贴板。
- [ ] AC-003 复制成功后展示固定位置成功反馈，不造成表格、分页或页面内容纵向位移。

### 剪贴板失败 fallback

- [ ] AC-004 当 Clipboard API 不存在时，页面不抛出运行时错误，并给出手动复制指引或等价兜底。
- [ ] AC-005 当 `writeText` 被浏览器拒绝或返回失败时，页面不抛出未捕获错误，并给出手动复制指引或等价兜底。
- [ ] AC-006 无 `request_id` 的日志记录不展示复制按钮；若通过函数防御触发空值复制，提示“当前日志没有 request_id”或等价文案。

### 埋点与回归测试

- [ ] AC-007 复制成功时可上报 `copy_request_id` 使用行为事件；复制失败或兜底路径不得误报成功复制。
- [ ] AC-008 修复后日志审计页既有筛选、分页、详情抽屉和日志列表渲染测试保持通过。
- [ ] 测试覆盖 Clipboard API 成功、API 不存在、`writeText` reject 和空 `request_id` 防御。

## BUG-0061 回归验收

> 来源：`issues/bugs/archive/BUG-0061-change-password-policy-error-message-unclear/acceptance.md`
> 状态：in_sprint；OpenSpec Change `fix-change-password-policy-error-message` applied

### 具体策略失败提示

- [x] AC-001 长度不足时展示“至少需要 N 位字符”或等价文案，且 N 与当前有效策略一致。
- [x] AC-002 缺少大写字母时明确提示“需要包含大写字母”或等价文案。
- [x] AC-003 缺少小写字母时明确提示“需要包含小写字母”或等价文案。
- [x] AC-004 缺少数字时明确提示“需要包含数字”或等价文案。
- [x] AC-005 缺少特殊字符时明确提示“需要包含特殊字符”或等价文案。

### 既有错误无回归

- [x] AC-006 弱密码继续展示“密码过于常见，请更换”或等价文案。
- [x] AC-007 新密码与原密码相同继续展示“新密码不能与原密码相同”或等价文案。
- [x] AC-010 原密码错误、限流与受保护账号提示不误显示为密码策略失败。

### 动态策略与契约同步

- [x] AC-008 修改密码弹窗规则展示与当前有效策略一致，不固定展示旧规则。
- [x] AC-009 API 返回可被前端识别的具体失败信息；若变更响应结构，已同步 OpenAPI、Orval、`docs/03-api-index.md` 与错误码/治理文档。
- [x] AC-011 后端与前端测试覆盖具体失败原因和既有路径无回归。
- [x] AC-012 修复不放宽密码策略、不绕过后端校验、不记录或持久化明文密码。

## 验收遗留项

| 项目 | 状态 | 处理建议 |
|---|---|---|
| REQ-0029 Change | proposed | 执行 `/opsx-apply add-admin-list-foundation-components` |
| REQ-0030 Change | proposed | 执行 `/opsx-apply update-api-docs-swagger-policy-checklist` |
| BUG-0056 Change | archived | 已归档至 `openspec/changes/archive/2026-07-09-fix-sprint-archive-incomplete-tasks-gate/` |
| BUG 修复 Change | proposed | 执行 `/opsx-apply fix-api-governance-route-tags-known-debt` |
| BUG-0058 Change | applied | 已完成 `/opsx-apply fix-workflow-sync-check-time-drift-idempotency`；待归档 |
| BUG-0059 Change | proposed | 执行 `/opsx-apply fix-user-password-copy-not-working` |
| BUG-0060 Change | proposed | 执行 `/opsx-apply fix-audit-log-request-id-copy-error` |
| BUG-0061 Change | applied | 已实现并完成后端/前端回归、OpenAPI/Orval、Web build、OpenSpec strict 与目录结构校验 |
| Docker Compose 验证 | 待定 | 若只更新文档/checklist可 N/A；若改代理配置则必须执行 |
