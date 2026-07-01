---
title: 用户故事
purpose: REQ-0022-admin-api-docs-menu 管理端接口文档菜单用户故事
content: 基于 requirement.md v1、capture.md 与 req-explore 结论提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或验收策略变更时同步更新
owner: product
status: draft
created_at: 2026-07-01 00:16:00
updated_at: 2026-07-01 00:16:00
note: REQ-0022-admin-api-docs-menu
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---:|---|
| US-001 | 后台管理员 | P0 | 是 |
| US-002 | 后台管理员 | P0 | 是 |
| US-003 | 后台管理员 / 前端开发协作方 | P1 | 是 |
| US-004 | 后台管理员 | P1 | 是 |
| US-005 | 后台运营 | P0 | 是（无权限边界） |
| US-006 | 运维 / 管理员 | P1 | 是 |

---

## US-001 通过管理端入口查看接口文档

**作为** 后台管理员，  
**我希望** 在管理端 SYSTEM 分组「系统设置」下方看到「接口文档」菜单，  
**以便** 不离开后台即可查询系统接口能力。

### 验收要点

- 侧栏 SYSTEM 分组顺序为：用户管理、系统设置、接口文档。
- 点击「接口文档」进入 `/admin/api-docs`。
- 当前路由下「接口文档」菜单 active 高亮，侧栏收起态仍可通过图标/aria label 识别。
- 页面继承 Admin Shell，不出现独立站点或营销式布局。

### 关联功能

- FR-001、FR-002；requirement §4、§5

---

## US-002 查看系统全部路由

**作为** 后台管理员，  
**我希望** 在接口目录中看到 `/api/v1/*`、`/health`、`/media/{object_key:path}` 等全部系统路由，  
**以便** 了解运行时实际暴露的接口边界。

### 验收要点

- 接口目录包含 OpenAPI schema 内路由与 schema 外系统路由。
- 每行展示 Method、Path、模块/Tag、Summary、认证要求、是否纳入 OpenAPI、是否有 Orval 方法名。
- 非 `/api/v1` 路由明确标注来源与用途，例如健康检查、媒体直出。
- 支持按关键字、Method、模块/Tag、认证要求筛选。

### 关联功能

- FR-002、FR-005；requirement §3.1、§5

---

## US-003 快速定位 Orval 方法名

**作为** 需要联调的后台管理员或前端开发协作方，  
**我希望** 在接口目录中直接看到 Orval 生成方法名，  
**以便** 快速定位 `src/web/src/shared/api/generated.ts` 中的调用函数。

### 验收要点

- 已纳入 OpenAPI 且被 Orval 生成的接口展示方法名。
- 未生成方法名的接口展示「未生成」及原因提示，例如 schema 外路由或未纳入 Orval。
- 支持用 Orval 方法名关键字搜索。
- 页面说明 OpenAPI JSON、Swagger UI、Orval 客户端和 `docs/03-api-index.md` 的职责边界。

### 关联功能

- FR-003、FR-006；requirement §5、§8

---

## US-004 使用 Swagger 在线调试

**作为** 后台管理员，  
**我希望** 在允许的环境中使用 Swagger 在线调试接口，  
**以便** 快速验证接口请求、响应与鉴权行为。

### 验收要点

- 本地 / 开发 / 演示环境允许 Swagger `Try It Out`。
- 生产环境展示 Swagger 文档入口，但隐藏或禁用 `Try It Out`。
- 页面明确展示当前环境的调试策略。
- 不额外持久化管理员 JWT 到新的不受控位置。

### 关联功能

- FR-004；requirement §5、§7

---

## US-005 后台运营不得查看接口文档

**作为** 后台运营人员，  
**我希望** 看不到接口文档入口，也无法通过直链访问，  
**以便** 系统接口与调试能力仅由管理员使用。

### 验收要点

- `employee` 侧栏不展示「接口文档」。
- `employee` 直链 `/admin/api-docs` 进入 403 页面或等价禁止访问状态。
- 如新增后端聚合接口，`employee` 请求返回 403。

### 关联功能

- FR-001、FR-007；requirement §2、§7

---

## US-006 识别生产环境调试风险

**作为** 运维或后台管理员，  
**我希望** 生产环境仍能查看接口文档但不能直接 Try It Out，  
**以便** 避免误操作生产数据，同时保留排查所需的接口信息。

### 验收要点

- 生产环境页面展示入口与接口目录。
- Swagger 区域或入口明确标注「生产环境仅查看」。
- `Try It Out` 隐藏或禁用，有前端/后端/配置层验证。
- 不展示真实密钥、数据库连接串、MinIO AccessKey/SecretKey、环境变量真实值。

### 关联功能

- FR-004、FR-007；requirement §7

---

## 与父需求 REQ-0017 的差异

| 维度 | REQ-0017 系统设置 | REQ-0022 接口文档 |
|---|---|---|
| 对象 | 平台配置与策略 | 接口目录、Swagger、Orval 方法映射 |
| 入口 | SYSTEM → 系统设置 | SYSTEM → 接口文档（位于系统设置下方） |
| 路由 | `/admin/settings/*` | `/admin/api-docs` |
| 主要交互 | 表单保存、恢复默认、审计 | 查询筛选、查看 Swagger、按环境控制调试 |
| 数据变更 | 会修改系统设置 | 默认只读；在线调试可能触发接口请求 |
| 权限 | 仅 admin | 仅 admin |
