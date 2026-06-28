---
title: Sprint 001 发布说明
purpose: 记录 Sprint 001 交付能力与发布注意事项
content: 基于 REQ-0001/0002/0003 及全部登录相关 OpenSpec Change
source: AI根据迭代范围生成，项目团队确认
update_method: Sprint 完成或范围变更时更新
owner: 项目负责人
status: published
note: Sprint 001 已于 2026-06-14 验收通过
---

# Sprint 001 发布说明

## 版本信息

| 字段 | 内容 |
|---|---|
| Sprint | sprint-001 |
| 关联需求 | REQ-0001、REQ-0002、REQ-0003 |
| 验收日期 | 2026-06-14 |
| 发布状态 | **已验收通过** |

## 新增能力

### Web 管理端登录

- 登录页 `/admin/login`，CSS Port 左右分屏布局
- 账号 + 密码登录，表单校验、loading、「记住我」
- 品牌：**TilesFST** Logo；左栏主标题「瓷砖信息管理后台」（REQ-0003）
- 视口无页面级纵向滚动（REQ-0002）
- **无**企业微信入口、**无**忘记密码入口（REQ-0002/0003）

### 认证与鉴权

- `POST /api/v1/auth/login`、`GET /api/v1/auth/me`、`POST /api/v1/auth/logout`
- JWT Bearer Token；bcrypt 密码哈希
- 路由守卫与角色分流（admin/employee vs store_owner）
- 管理端退出登录

### Web Design System

- Token、`/design-system` 预览、shadcn/ui 工业风 override
- 登录页 port CSS（`login-page.css`）

### 数据与部署

- `users` 表、`login_logs` 预留
- Docker Compose + `ADMIN_INITIAL_PASSWORD` 种子 admin

## 不包含（后续 Sprint）

- 瓷砖目录/管理业务功能
- 忘记密码完整流程、企微 OAuth、小程序登录
- 登录限流、RBAC 配置页

## 升级说明

1. `./scripts/docker-up.sh`
2. 配置 `ADMIN_INITIAL_PASSWORD`
3. 访问 `http://localhost:3000/admin/login`
4. 可选：`./scripts/generate-openapi-client.sh`

## 已知限制

- 登录标识本期仅 `username`
- Token 存 localStorage/sessionStorage
- 瓷砖/上传 API 为桩实现，未统一 `{ code, message, data }` envelope

## 关联验收

- `iterations/archive/sprint-001/acceptance-report.md`（**通过**）
- `openspec/specs/web-client/spec.md`、`openspec/specs/auth/spec.md`
