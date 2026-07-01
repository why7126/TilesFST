---
title: 业务流程
purpose: REQ-0022-admin-api-docs-menu 访问、接口目录、Orval 映射与 Swagger 调试流程
content: 基于 requirement.md v1、capture.md 与 req-explore 结论提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或验收策略变更时同步更新
owner: product
status: draft
created_at: 2026-07-01 00:16:00
updated_at: 2026-07-01 00:16:00
note: REQ-0022-admin-api-docs-menu
---

# 业务流程

## 1. 流程总览

```text
后台管理员登录（role=admin）
  ↓
侧栏 SYSTEM → 接口文档
  ↓
/admin/api-docs
  ↓
┌──────────────────────────────────────────────────────────────┐
│ ApiDocsPage                                                   │
│  ├─ page-hero：环境策略 + Swagger / OpenAPI 快捷入口            │
│  ├─ summary-strip：接口数、受保护接口数、Orval 映射数            │
│  ├─ filter-bar：keyword / method / tag / auth                  │
│  ├─ api-route-table：Method + Path + Tag + Auth + Orval         │
│  └─ swagger-panel/link：按环境控制 Try It Out                   │
└──────────────────────────────────────────────────────────────┘
```

## 2. 访问与权限流程

```text
用户进入 /admin/api-docs
  ↓
ProtectedRoute
  ├─ 未登录 → /admin/login
  ├─ role = admin → 允许进入 ApiDocsPage
  └─ role = employee → /admin/forbidden

AdminSidebar
  ├─ role = admin → SYSTEM 展示 用户管理 / 系统设置 / 接口文档
  └─ role = employee → 不展示 接口文档
```

如后续新增后端聚合接口：

```text
GET /api/v1/admin/api-docs
  ↓
require_system_admin
  ├─ admin → 返回接口目录补充数据
  └─ employee / 未登录 → 403 / 401
```

## 3. 接口目录构建流程

```text
ApiDocsPage mounted
  ↓
加载 OpenAPI JSON（/openapi.json 或后端聚合接口）
  ↓
读取 paths + operations
  ↓
补充非 schema 路由
  ├─ /health
  ├─ /media/{object_key:path}
  └─ 其他 FastAPI app routes
  ↓
合并认证信息、Tag、Summary、operationId
  ↓
匹配 Orval 方法名
  ↓
渲染接口目录表格
```

## 4. Orval 方法名映射流程

```text
OpenAPI operationId
  ↓
Orval 生成规则（src/web/orval.config.ts）
  ↓
src/web/src/shared/api/generated.ts
  ↓
ApiDocsPage 展示 methodName
  ├─ 有映射 → 展示方法名
  └─ 无映射 → 展示「未生成」+ 原因
```

原因示例：

- 路由 `include_in_schema=false`，未进入 OpenAPI。
- 路由是 `/health` 或 `/media/*` 等非业务客户端调用接口。
- OpenAPI 未重新导出或 Orval 未重新生成。

## 5. 筛选与检索流程

```text
用户输入 keyword 或选择筛选
  ↓
过滤字段
  ├─ Path
  ├─ Summary
  ├─ Tag / 模块
  ├─ HTTP Method
  ├─ 认证要求
  └─ Orval 方法名
  ↓
更新 route-table
  ↓
summary-strip 同步显示 filtered_count
```

## 6. Swagger 查看与调试流程

```text
用户点击 Swagger 区域 / 快捷入口
  ↓
读取当前环境
  ├─ local / development / demo
  │   └─ 展示 Swagger UI 且允许 Try It Out
  └─ production
      └─ 展示 Swagger 文档但隐藏或禁用 Try It Out
```

生产环境策略 MUST 在实现阶段选定一种或组合：

```text
前端内嵌 Swagger 配置
  OR
后端 Swagger UI 参数 / 自定义 Swagger assets
  OR
Nginx / 环境变量控制
```

无论采用哪种实现，验收必须能证明生产环境 Try It Out 不可用。

## 7. 与长期文档关系

```text
/openapi.json
  ├─ 运行时契约
  ├─ Swagger UI 数据源
  └─ Orval 生成源

docs/03-api-index.md
  ├─ 长期接口索引
  ├─ 错误码与治理入口
  └─ 人工维护说明

/admin/api-docs
  ├─ 管理端查询界面
  ├─ 聚合 OpenAPI + 非 schema 路由 + Orval 映射
  └─ 管理员可见
```

## 8. 与父需求 REQ-0017 的差异

| 对比项 | REQ-0017 系统设置 | REQ-0022 接口文档 |
|---|---|---|
| SYSTEM 分组位置 | 系统设置菜单 | 系统设置下方的接口文档菜单 |
| 页面类型 | 设置/表单/Tab | 接口目录/筛选表格/Swagger 区域 |
| 数据写入 | PATCH settings | 页面自身默认只读；Swagger 调试可能调用接口 |
| 主要风险 | 配置误改、保存/恢复默认体验 | 生产误调试、文档暴露、Orval 映射漂移 |

## 9. 后续 OpenSpec 设计关注点

- 是否新增 `/api/v1/admin/api-docs` 聚合接口，用于返回 schema 外路由与 Orval 映射。
- 生产环境隐藏 Swagger `Try It Out` 的技术实现必须在 design.md 明确。
- 非 `/api/v1` 路由如 `/media/{object_key:path}` 是否需要额外的描述 metadata。
- Orval 方法名映射是否通过 operationId 推导，还是通过生成文件静态解析。
