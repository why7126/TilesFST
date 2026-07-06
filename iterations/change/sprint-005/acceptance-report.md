---
note: workflow-sync — 1/4 Change 已 archive；0 applied；待人工 sign-off
created_at: 2026-07-04 22:30:20
updated_at: 2026-07-06 16:06:23
title: Sprint 005 验收报告
purpose: 记录 Sprint 005 验收结果与遗留项（模板）
content: 基于 REQ-0030 acceptance.md、BUG-0057 acceptance.md、BUG-0058 acceptance.md 与 BUG-0059 acceptance.md
source: /sprint-propose REQ-0030；/sprint-propose BUG-0057 纳入 sprint-005；/sprint-propose BUG-0058 纳入 sprint-005；/sprint-propose BUG-0059 纳入 sprint-005
update_method: Sprint 验收完成后更新
owner: 产品负责人
status: draft
---

# Sprint 005 验收报告

## 验收概况

| 字段 | 内容 |
|---|---|
| Sprint | sprint-005 |
| 关联需求 | REQ-0030-api-docs-swagger-policy-checklist |
| 关联 BUG | BUG-0057-api-governance-tags-known-debt；BUG-0058-workflow-sync-check-time-drift-idempotency；BUG-0059-user-password-copy-not-working |
| 关联 Change | REQ-0030: `update-api-docs-swagger-policy-checklist`；BUG-0057: `fix-api-governance-route-tags-known-debt`；BUG-0058: `fix-workflow-sync-check-time-drift-idempotency`；BUG-0059: `fix-user-password-copy-not-working` |
| 计划验收日期 | 2026-07-18 22:30:20 |
| 验收结论 | 待验收 |
| 验收人 | 待填写 |

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

本 Sprint 不触发 `admin-list` / `admin-form` / `media-upload` 横切 AC；BUG-0059 涉及管理端弹窗修复，触发 `admin-modal` 横切 AC。

### 管理端弹窗横切验收

> 来源：`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`

- [ ] 弹窗 TSX 不新增 `modal-card` 与专属类双挂载，避免宽度 CSS 层叠回归。
- [ ] 一次性密码结果弹窗在 1440 视口下宽度与现有用户管理弹窗基线一致。
- [ ] 矮视口下弹窗 body scroll、关闭按钮和主操作按钮仍可访问。
- [ ] 复制成功/失败提示不造成弹窗明显布局抖动。
- [ ] 测试导入相关 CSS 时不会因层叠顺序导致弹窗宽度断言漂移。

## BUG-0057 回归验收

> 来源：`issues/bugs/review/BUG-0057-api-governance-tags-known-debt/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-api-governance-route-tags-known-debt` proposed

### route tag 单一事实源

- [ ] AC-001 后端 API route tags 仅保留一个事实源。
- [ ] AC-001 同一 operation 不再同时出现 router-level tag 与 decorator-level tag 合并后的双 tag。
- [ ] AC-001 `auth`、`profile`、`uploads` 等路由不再生成重复 tag，例如 `["auth", "auth"]`。

### OpenAPI tag 命名统一

- [ ] AC-002 最终 OpenAPI 中每个 operation 的 `tags` 数量为 1。
- [ ] AC-002 tag 使用统一命名体系，建议为 kebab-case。
- [ ] AC-002 不再出现 `Admin Brands`、`Admin Tile SKUs` 等展示名 tag 与技术名 tag 并存。

### API governance 校验补强

- [ ] AC-003 `scripts/validate-api-standard.py` 增加最终 OpenAPI operation tags 校验。
- [ ] AC-003 校验覆盖多 tag、重复 tag、非 kebab-case tag。
- [ ] AC-003 构造或保留回归测试，证明上述异常会导致校验失败。

### OpenAPI / Orval 同步

- [ ] AC-004 重新导出 `src/web/openapi.json`。
- [ ] AC-004 如生成物变化，运行 Orval 并同步 `src/web/src/shared/api/generated.ts`。
- [ ] AC-004 确认管理端接口文档页面的 tag 展示不再受重复/双轨 tags 影响。

### 回归验证

- [ ] AC-005 `python scripts/validate-api-standard.py` 通过。
- [ ] AC-005 OpenAPI operation tags 统计结果满足：多 tag operation 为 0，重复 tag operation 为 0，非 kebab-case tag operation 为 0。
- [ ] AC-005 不改变 API 路径、请求参数、响应结构或错误码语义。

## BUG-0058 回归验收

> 来源：`issues/bugs/review/BUG-0058-workflow-sync-check-time-drift-idempotency/acceptance.md`  
> 状态：in_sprint；OpenSpec Change `fix-workflow-sync-check-time-drift-idempotency` proposed

### 归档时间稳定来源

- [ ] AC-001 archived Change 渲染到 Sprint Scope 表时，不使用 issue trace 或 change trace frontmatter `updated_at` 作为归档时间事实源。
- [ ] AC-001 归档时间优先使用 lifecycle、变更记录或归档目录日期等稳定来源。

### Markdown frontmatter 幂等

- [ ] AC-002 workflow-sync 处理 Markdown 且渲染结果与原文一致时，不刷新 frontmatter `updated_at`。
- [ ] AC-002 普通同步后再次执行 `--check` 保持 no delta。

### workflow-sync check 幂等

- [ ] AC-003 连续执行两次 `python scripts/sync-workflow-status.py --check`，第二次返回 0。
- [ ] AC-003 不报告 `iterations/archive/sprint-004/sprint.md` 仅时间字段 drift。

### 回归测试

- [ ] AC-004 自动化测试覆盖 issue trace `updated_at` 晚于真实归档记录的场景。
- [ ] AC-004 自动化测试覆盖无正文变化时 `persist_markdown` 不 touch `updated_at`。


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

## 验收遗留项

| 项目 | 状态 | 处理建议 |
|---|---|---|
| REQ-0030 Change | proposed | 执行 `/opsx-apply update-api-docs-swagger-policy-checklist` |
| BUG 修复 Change | proposed | 执行 `/opsx-apply fix-api-governance-route-tags-known-debt` |
| BUG-0058 Change | proposed | 执行 `/opsx-apply fix-workflow-sync-check-time-drift-idempotency` |
| BUG-0059 Change | proposed | 执行 `/opsx-apply fix-user-password-copy-not-working` |
| Docker Compose 验证 | 待定 | 若只更新文档/checklist可 N/A；若改代理配置则必须执行 |
