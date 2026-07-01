---
created_at: 2026-06-29 10:03:38
updated_at: 2026-07-01 08:56:55
title: Sprint 004 迭代说明
purpose: 记录 Sprint 004 目标、范围、Change、工作量与风险
content: 生产环境部署与 MySQL 数据库支持（REQ-0018）+ 管理端超级管理员账号保护（REQ-0019）+ 创建用户校验提示修复（BUG-0050）+ 管理端接口文档菜单与在线调试（REQ-0022）
source: AI 根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: in_progress
note: workflow-sync — workflow-sync 自动同步 — 3/4 Change archived；1 applied；Sprint `in_progress`
---

# Sprint 004

## Sprint 目标

本迭代原主线聚焦 **生产环境部署与 MySQL 数据库支持**，将 TILESFST 从当前本地/demo SQLite 部署能力扩展到 VPS Docker Compose + 外部 MySQL 8.0+ + MinIO 持久化的生产部署路径，同时保持本地 `./scripts/docker-up.sh` SQLite 默认体验不回归。

2026-06-30 追加 **管理端超级管理员账号保护**：以 `ADMIN_USERNAME` 对应账号作为受保护系统账号，禁止管理端编辑、重置密码、冻结、删除及默认策略下本人改密，避免失去系统保底管理员。

2026-06-30 追加 **创建用户校验提示修复**：将已评审 BUG-0050 纳入本 Sprint，修复用户管理弹窗创建用户时用户名长度不足返回默认 422 `detail`、前端只能展示兜底错误的问题。

2026-07-01 追加 **管理端接口文档菜单与在线调试**：将已评审 REQ-0022 纳入本 Sprint，在系统设置下方新增 `/admin/api-docs` 管理端入口，支持管理员查看系统所有接口、Swagger 调试策略与 Orval 方法名映射。

正式纳入范围：

1. **REQ-0018-production-mysql-deployment** — 生产环境部署与 MySQL 数据库支持。
2. **REQ-0019-admin-superuser-protection** — 管理端超级管理员账号保护。
3. **BUG-0050-user-create-validation-message-unclear** — 创建用户校验失败未明确提示具体问题点。
4. **REQ-0022-admin-api-docs-menu** — 管理端接口文档菜单与在线调试。

### REQ-0018-production-mysql-deployment 要点

- **优先级**：P0
- **类型**：基础设施 / 部署 / 数据库
- **范围**：后端双数据库策略、MySQL baseline 初始化、空库管理员 seed、生产 Compose、MinIO 生产持久化、环境变量与部署文档、MySQL 验证路径。
- **不包含**：Compose 内嵌 MySQL、SQLite 到 MySQL 业务数据迁移、高可用、K8s/Helm/Terraform、云厂商专有集成、前端/小程序 UI 改动。
- **OpenSpec**：`add-production-mysql-deployment`（proposed，OpenSpec strict validate 已通过）。
- **验收重点**：生产 `APP_ENV=production` 必须连接 MySQL 并 fail-fast；本地 SQLite 不回归；生产 MinIO 单桶持久化；MySQL 集成验证覆盖 schema init、admin seed、登录或 CRUD；文档和 `.env.example` 同步。

### REQ-0019-admin-superuser-protection 要点

- **优先级**：P1
- **类型**：管理端 / 用户与权限
- **范围**：后端统一识别 `settings.admin_username` 受保护账号；用户列表/详情返回 `is_protected` 与 `protected_reason`；禁止编辑、重置密码、冻结/解冻、删除和默认策略下本人改密；前端用户管理列表禁用受保护账号操作按钮并展示原因。
- **不包含**：新增 `super_admin` / `root` 角色枚举；改变既有 RBAC；移除 `.env` 级运维恢复机制；店主端、小程序改造。
- **OpenSpec**：`update-admin-superuser-protection`（proposed）。
- **验收重点**：后端 403 保护与数据库不变；OpenAPI/Orval 暴露新增字段；错误码登记；用户管理行操作禁用态对齐现有列表页；普通用户操作不回归。

### BUG-0050-user-create-validation-message-unclear 要点

- **严重等级**：medium
- **类型**：管理端 / 用户管理 / 表单校验反馈
- **现象**：创建用户时输入 `abc` 这类小于 4 位用户名，后端返回 FastAPI 默认 422 `detail`，前端无法读取统一 `message`，只能展示兜底失败文案。
- **根因**：`UserCreateRequest.username` 的 Pydantic `min_length=4` 在进入 `validate_username()` 前拦截，业务层中文错误文案没有机会返回；全局异常处理未统一转换请求体验证错误。
- **修复范围**：创建用户 API 的用户名校验错误结构、前端弹窗错误提示展示、用户名其他格式错误与重复用户名回归、合法创建不回归。
- **OpenSpec**：`fix-user-create-validation-message-unclear`（proposed）。
- **验收重点**：`username="abc"` 返回统一 `{ code, message, data }` 且 message 明确；弹窗能定位用户名字段；后端 pytest 与前端组件测试覆盖。

### REQ-0022-admin-api-docs-menu 要点

- **优先级**：P1
- **类型**：管理端 / 接口文档
- **范围**：SYSTEM 分组在「系统设置」下方新增「接口文档」菜单；注册 `/admin/api-docs`；管理员可查看系统全部接口目录、Swagger/OpenAPI 入口、生产 Try It Out 策略与 Orval 生成方法名。
- **系统所有接口定义**：包含 `/api/v1/*`、`/health`、`/media/{object_key:path}` 以及其他未纳入 `/api/v1` 但属于 FastAPI app 的路由。
- **不包含**：接口编辑、Mock、公开接口文档、生产环境 Try It Out、通过管理端修改 OpenAPI/Orval/后端路由、展示密钥或真实环境变量。
- **OpenSpec**：`add-admin-api-docs-menu`（applied，23/23 tasks complete，OpenSpec strict validate 已通过）。
- **验收重点**：仅管理员可访问；生产展示入口但隐藏/禁用 Try It Out；接口目录含非 `/api/v1` 路由；Orval 方法名可定位前端联调；符合管理端列表/表单横切一致性 gate。

## Scope

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0018 | 生产环境部署与 MySQL 数据库支持 | P0 | done | archived `add-production-mysql-deployment`（2026-06-29 16:25:27） |
| REQ-0019 | 管理端超级管理员账号保护 | P1 | done | archived `update-admin-superuser-protection`（2026-06-30 19:07:02） |
| REQ-0022 | 管理端接口文档菜单与在线调试 | P1 | in_sprint | apply 23/23；待 archive `add-admin-api-docs-menu` |
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0050 | 创建用户校验失败未明确提示具体问题点 | medium | done | archived `fix-user-create-validation-message-unclear`（2026-06-30 18:52:07） |
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-production-mysql-deployment` | REQ-0018-production-mysql-deployment | archived | archived `add-production-mysql-deployment`（2026-06-29 16:25:27） |
| `update-admin-superuser-protection` | REQ-0019-admin-superuser-protection | archived | archived `update-admin-superuser-protection`（2026-06-30 19:07:02） |
| `fix-user-create-validation-message-unclear` | REQ-0005-user-management | archived | archived `fix-user-create-validation-message-unclear`（2026-06-30 18:52:07） |
| `add-admin-api-docs-menu` | REQ-0022-admin-api-docs-menu | applied | apply 23/23；待 archive `add-admin-api-docs-menu` |
<!-- workflow-sync:scope-changes:end -->

### 延后项（待评审 / 未纳入本 Sprint）

| 项目 | 状态 | 延后原因 |
|---|---|---|
| REQ-0013-admin-shell-padding-refine | pending_review | 未评审，不得纳入正式规划 |
| Sprint 003 A-002 / A-003 / A-004 对应 UI 抽象 | backlog | 本 Sprint 为基础设施部署，不纳入 UI 模板建设 |
| 系统设置 P1b 登录失败锁定 | backlog | REQ-0017 复盘延后项，需单独 capture/review |

## 工作量估算

| 工作项 | SP | 人天 | 角色 | 说明 |
|---|---:|---:|---|---|
| 数据库配置与 MySQL driver | 4 | 3.0 | 后端 | `APP_ENV` / `DATABASE_URL` / fail-fast / 日志脱敏 |
| Dialect-aware session 与初始化 | 5 | 4.0 | 后端 | SQLite/MySQL engine 分支；MySQL migration 入口 |
| MySQL baseline DDL 与 seed | 5 | 4.0 | 后端 | 表清单、类型映射、管理员 seed |
| 生产 Docker Compose 与 MinIO | 3 | 2.0 | 后端/DevOps | prod compose、外部 MySQL、MinIO volume |
| 文档与环境变量同步 | 2 | 1.5 | 后端/文档 | `.env.example`、deployment、database、rules、README |
| MySQL 集成验证与 smoke | 2 | 1.5 | 测试/后端 | MySQL 8 service/marker、登录/API、媒体读取 |
| Release / archive 预检 | 0 | 0.0 | 全员 | 归入各项验收 |
| REQ-0019 后端保护与错误码 | 3 | 2.0 | 后端 | 受保护账号判定、列表/详情字段、编辑/重置/状态/改密拦截 |
| REQ-0019 管理端用户列表 UI | 2 | 1.5 | 前端 | 操作按钮禁用态、原因提示、普通用户流程回归 |
| REQ-0019 API 文档与 Orval | 1 | 1.0 | 后端/前端 | OpenAPI 字段、错误码文档、Orval 客户端同步 |
| REQ-0019 自动化测试 | 1 | 1.0 | 测试/前端/后端 | pytest + Vitest 覆盖保护和不回归 |
| BUG-0050 校验错误统一与前端提示 | 3 | 2.0 | 后端/前端/测试 | 用户名长度不足统一错误结构、弹窗展示后端 message、pytest + Vitest 回归 |
| REQ-0022 管理端导航与页面框架 | 3 | 2.0 | 前端 | SYSTEM 菜单、`/admin/api-docs` 路由、管理员权限与页面骨架 |
| REQ-0022 接口目录聚合 | 3 | 2.0 | 后端/前端 | 覆盖 `/api/v1/*`、`/health`、`/media/{object_key:path}` 与其他 app routes |
| REQ-0022 Swagger 环境策略 | 3 | 2.0 | 后端/前端 | 非生产允许调试；生产展示入口但隐藏/禁用 Try It Out |
| REQ-0022 Orval 方法名映射 | 3 | 2.0 | 前端/API | 展示 Orval 生成方法名；未生成项显示状态与原因 |
| REQ-0022 测试、文档与验收 | 3 | 3.0 | 测试/文档 | pytest/Vitest/Orval/API 文档/生产策略验收 |
| **fix_buffer** | **10** | **7.0** | 全员 | 原 REQ-0018 缓冲 + REQ-0019 追加缓冲；约 33% |
| **合计** | **58** | **43.0** | — | 3 个已归档 change + 1 个 proposed add-*；追加范围存在排期风险 |

## 里程碑

| 里程碑 | 目标日期 | 验收输出 |
|---|---|---|
| M1 配置与 DB 设计定稿 | 2026-07-01 18:00:00 | `DATABASE_URL` 策略、MySQL driver、`implementation/db.md` 类型映射初版 |
| M2 MySQL baseline + seed | 2026-07-04 18:00:00 | 空 MySQL schema 初始化、管理员登录 smoke |
| M3 生产 Compose + MinIO | 2026-07-08 18:00:00 | `docker-compose.prod.yml`、MinIO 单桶持久化、外部 MySQL runbook |
| M4 测试与文档收口 | 2026-07-11 18:00:00 | SQLite 回归、MySQL 集成验证、部署文档与 env 同步 |
| M5 Sprint 验收 | 2026-07-13 18:00:00 | acceptance-report 勾选、OpenSpec validate、准备 archive |

## 风险

| 风险 | 等级 | 缓解 |
|---|---|---|
| SQLite 最终态到 MySQL baseline 漏表/漏索引 | high | 先汇总 `schema.sql` + migrations；`implementation/db.md` 表清单逐项勾选；MySQL test 覆盖关键表 |
| Repository SQL 存在 SQLite-only 语法 | high | MySQL 集成测试覆盖登录和至少一条 CRUD；必要时按 dialect 分支 |
| 生产 `.env` 使用示例密钥 | high | 文档和 `.env.example` 显式禁止；release checklist 检查 |
| 外部 MySQL 网络/权限问题 | medium | 部署 runbook 加入 8.0+、utf8mb4、DDL+DML、白名单、端口可达检查 |
| workflow-sync 将 REQ 状态标为 `in_sprint` 但 iteration 为空的历史残留 | low | 本 Sprint 创建后写入 `iteration: sprint-004` 并由 workflow-sync 收敛 |
| fix 缓冲被实现任务挤占 | medium | 保留 10 SP / 7.0 人天缓冲；非 P0 新需求默认下一 Sprint |
| 已进入 apply 后追加 REQ-0019 | medium | 本次为用户显式纳入；执行前必须先 `/req-opsx`，且不得重新打开已归档 REQ-0018 |
| 受保护账号前端只做禁用但后端未拦截 | high | 后端作为强制边界；pytest 覆盖编辑、重置、状态、本人改密拒绝 |
| 管理端用户列表 UI 回归 Sprint 002/003 重复问题 | medium | 引用 `admin-list-page-consistency.md`；保留分页 DOM、fixed toast、DS confirm modal |
| 已进入 in_progress 后追加 BUG-0050 | medium | 本次为用户显式纳入；执行前必须先 `/bug-opsx`，并将 fix-* 挂在既有 `add-user-management` 能力之下 |
| 追加后 fix 缓冲低于 30% 门槛 | medium | 当前保留 10 SP / 7.0 人天缓冲；因 BUG-0050 追加后缓冲约 23%，后续非 P0/P1 项默认延后 |
| 用户创建弹窗错误提示可能回归弹窗 CSS/布局问题 | low | 引用 `admin-modal-width-css-cascade.md`；仅调整错误提示，不改弹窗宽度类名与主体布局 |
| 已进入 in_progress 后追加 REQ-0022 | medium | 本次为用户显式纳入；已创建 `add-admin-api-docs-menu`，执行前需确认 change 仍为 proposed 且通过 strict validate |
| REQ-0022 需要覆盖非 `/api/v1` 路由，OpenAPI 可能默认遗漏 | medium | 后端聚合路由时必须显式补充 `/health`、`/media/{object_key:path}` 与其他 app routes；验收用路由清单对照 |
| 生产环境误开放 Swagger Try It Out | high | 以环境变量/构建配置/Swagger UI 参数为强制 gate；生产 smoke 必须验证 Try It Out 不可用 |
| Orval 方法名映射与实际生成文件漂移 | medium | 实现后执行 Orval，并以 `src/web/src/shared/api/generated.ts` 为事实源校验方法名 |
| 追加后 fix 缓冲进一步低于 30% 门槛 | high | 当前 sprint 已 in_progress 且多次追加；REQ-0022 后不再接收非 P0/P1 新项，必要时拆分到下一 Sprint |

## 知识库承接

### Knowledge Intake Report

| ID | 优先级 | 描述 | 本 Sprint 承接方式 |
|---|---|---|---|
| A-001 | P0 | 完成 Sprint 003 `acceptance-report.md` 核心 AC 人工勾选 | 采纳：本 Sprint M5 必须对 REQ-0018 AC-001～AC-045 做 sign-off，不允许只写 Published |
| A-002 | P1 | 落地 `AdminListPage` / 列表 DOM 契约 | 部分采纳：REQ-0019 修改用户管理列表，要求不改写分页/表格 DOM；模板抽象仍保留 backlog |
| A-003 | P1 | 落地 `AdminFormPage` 单 CTA + AdminToast + DS confirm | 部分采纳：REQ-0022 作为管理端文档页不得引入保存 CTA、原生 confirm 或文档流 success/error banner |
| A-004 | P1 | Modal 宽度 CSS 层叠 gate | 部分采纳：BUG-0050 涉及用户创建弹窗错误提示，要求修复不引入 modal-card 层叠/宽度回归 |
| A-005 | P2 | Sprint scope 冻结策略 | 偏离并标注：本次按用户显式指令追加 REQ-0019、BUG-0050 与 REQ-0022；后续追加项仍需在风险表显式记录 |
| A-006 | P2 | `openspec archive` ADDED 冲突预检脚本 | 部分采纳：归档前运行 `openspec validate add-production-mysql-deployment --strict`，如需工具化另起 REQ |
| A-007 | P2 | trace.md YAML fence CI 校验 | 部分采纳：本 Sprint 人工检查 trace fence；工具化另起 REQ |
| A-008 | P2 | 导出 REQ-0017 五 Tab PNG Golden | 不适用：非本 Sprint 范围 |
| A-009 | P3 | 系统设置 P1b 登录失败锁定 | 延后：需单独需求评审 |

### 早期复盘模式承接

| 来源 | 模式 | 本 Sprint 处理 |
|---|---|---|
| sprint-002 A-005 / A-008 | 对象存储 / 大文件上传部署 checklist | 采纳：引用媒体上传最佳实践，生产 smoke 覆盖 Nginx、后端校验、MinIO、`/media/` |
| sprint-002 A-006 | 单迭代 add change ≤6，预留 fix 缓冲 | 采纳：1/6 add-*；fix buffer = 30%+ |
| sprint-002 A-007 | 父 add 优先 archive，delta 冲突预检 | 采纳：本 Sprint 仅 1 个 add-*，归档前 strict validate |

## 横切预防清单

本 Sprint 当前正式范围包含生产部署与管理端用户列表增量。生产部署包含媒体上传 smoke；REQ-0019 涉及用户管理列表行操作状态，必须引用管理端列表页一致性最佳实践。

- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`

媒体上传验收 gate：

- [ ] 经 Web 入口或等价生产反代完成图片上传，不绕过后端 API。
- [ ] 后端返回 object_key / URL，MinIO 单桶内对象存在。
- [ ] `/media/{object_key}` 可读取对象，非法 object_key 仍被拒绝。
- [ ] Nginx `client_max_body_size` 与 `MAX_IMAGE_SIZE_MB` / `MAX_VIDEO_SIZE_MB` 文档一致。
- [ ] 重启 backend/web/minio 后对象仍可访问。

管理端列表页验收 gate：

- [ ] `/admin/users` 分页 DOM 仍为左侧 `page-summary`、右侧 `page-right` 页码与每页条数。
- [ ] 受保护账号提示使用 fixed toast / title / tooltip 等不会推挤页面布局的方式。
- [ ] 普通用户冻结、解冻、删除、重置密码仍使用 DS confirm modal，不引入 `window.confirm`。
- [ ] 受保护账号仅禁用受限操作，不隐藏操作列，不硬编码 `admin`。

管理端弹窗验收 gate：

- [ ] 用户创建弹窗不新增 `modal-card` 与专属类双挂载问题。
- [ ] 错误提示展示不改变弹窗宽度、遮罩、按钮区与滚动行为。
- [ ] Vitest 覆盖创建失败错误展示，必要时 import 相关 admin CSS 栈防止层叠回归。

管理端接口文档页验收 gate：

- [ ] `/admin/api-docs` 位于 SYSTEM 分组「系统设置」下方，且仅管理员可见。
- [ ] 直链 `/admin/api-docs` 对非管理员返回 403 或等价禁止访问状态。
- [ ] 接口目录包含 `/api/v1/*`、`/health`、`/media/{object_key:path}` 与其他 FastAPI app routes。
- [ ] 生产环境展示接口文档入口，但 Swagger `Try It Out` 不可用。
- [ ] 页面展示 Orval 生成方法名；未生成项明确显示「未生成」或等价状态。
- [ ] 页面反馈使用 fixed toast / 静态状态，不使用会推挤布局的文档流提示。

## 依赖

```text
sprint-004
└─ REQ-0018-production-mysql-deployment
   └─ add-production-mysql-deployment
      ├─ database capability（新增）
      │  ├─ APP_ENV / DATABASE_URL / MySQL driver
      │  ├─ dialect-aware session
      │  ├─ schema.mysql.sql / migration entry
      │  └─ admin seed
      ├─ deployment capability（新增）
      │  ├─ docker-compose.prod.yml
      │  ├─ external MySQL runbook
      │  └─ env / README / docs sync
      ├─ object-storage capability（MODIFIED）
      │  └─ production MinIO volume + single bucket smoke
      └─ testing capability（MODIFIED）
         └─ MySQL integration path + SQLite regression
└─ REQ-0019-admin-superuser-protection
   └─ update-admin-superuser-protection（待 /req-opsx）
      ├─ user-management capability（MODIFIED）
      │  ├─ protected account fields
      │  ├─ edit/reset/status operation guard
      │  └─ disabled row actions
      ├─ auth/profile capability（MODIFIED）
      │  └─ protected account password change guard
      ├─ api-governance capability（MODIFIED）
      │  └─ error code + OpenAPI + Orval
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest regression
└─ BUG-0050-user-create-validation-message-unclear
   └─ fix-user-create-validation-message-unclear（proposed）
      ├─ user-management capability（MODIFIED）
      │  ├─ username validation error structure
      │  └─ create user modal error display
      ├─ api-governance capability（MODIFIED）
      │  └─ request validation / business validation message consistency
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest regression
└─ REQ-0022-admin-api-docs-menu
   └─ add-admin-api-docs-menu（applied，23/23 tasks complete）
      ├─ admin-shell capability（MODIFIED）
      │  ├─ SYSTEM menu item below settings
      │  └─ /admin/api-docs route guard
      ├─ api-governance capability（MODIFIED）
      │  ├─ all route inventory
      │  ├─ Swagger Try It Out environment policy
      │  └─ Orval method name mapping
      └─ testing capability（MODIFIED）
         └─ pytest + Vitest + Orval regression
```

## 发布计划

1. 完成 `/sprint-apply sprint-004` 后，先在本地 SQLite 路径跑后端回归。
2. 使用 MySQL 8 测试实例或 CI service container 跑 MySQL 集成验证。
3. 使用生产 Compose 示例做配置校验，确认不包含 mysql 服务。
4. 完成生产媒体上传与 `/media/{object_key}` 读取 smoke。
5. 对 REQ-0019 执行 `/opsx-apply update-admin-superuser-protection`，再回填验收结果。
6. 对 BUG-0050 执行 `/opsx-apply fix-user-create-validation-message-unclear`，再回填验收结果。
7. REQ-0022 已完成 `/opsx-apply add-admin-api-docs-menu`；后续归档时执行 `/opsx-archive add-admin-api-docs-menu`。
8. REQ-0019、BUG-0050 与 REQ-0022 已补跑 pytest、Vitest、Orval、OpenAPI 与接口文档校验；API governance 剩余失败为既有管理端路由缺少 decorator tags。
9. 更新 acceptance-report，核心 AC sign-off 后再 `/sprint-archive sprint-004`。

## 关联文档

| 类型 | 路径 |
|---|---|
| REQ | `issues/requirements/archive/REQ-0018-production-mysql-deployment/` |
| REQ | `issues/requirements/archive/REQ-0019-admin-superuser-protection/` |
| REQ | `issues/requirements/review/REQ-0022-admin-api-docs-menu/` |
| BUG | `issues/bugs/archive/BUG-0050-user-create-validation-message-unclear/` |
| Change | `openspec/changes/add-production-mysql-deployment/` |
| Change | `update-admin-superuser-protection`（proposed） |
| Change | `fix-user-create-validation-message-unclear`（proposed） |
| Change | `openspec/changes/add-admin-api-docs-menu/` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-003-retrospective.md` |
| 复盘 | `docs/knowledge-base/retrospectives/sprint-002-retrospective.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` |

## 变更记录

| 时间 | 说明 |
|---|---|
| 2026-06-29 10:03:38 | `/sprint-propose sprint-004` 创建四件套，纳入 REQ-0018 与 `add-production-mysql-deployment` |
| 2026-06-30 18:18:45 | `/sprint-propose REQ-0019 纳入 sprint-004` 追加 REQ-0019；OpenSpec Change 待 `/req-opsx` |
| 2026-06-30 18:26:33 | `/sprint-propose BUG-0050 纳入 sprint-004` 追加 BUG-0050；OpenSpec Change 待 `/bug-opsx` |
| 2026-06-30 18:38:37 | `/bug-opsx BUG-0050` 创建 `fix-user-create-validation-message-unclear` 并加入 sprint-004 Change 队列 |
| 2026-07-01 00:28:26 | `/sprint-propose REQ-0022 纳入 sprint-004` 追加 REQ-0022；OpenSpec Change 待 `/req-opsx REQ-0022` |
