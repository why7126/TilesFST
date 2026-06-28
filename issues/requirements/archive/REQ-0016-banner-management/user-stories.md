---
title: 用户故事
purpose: REQ-0016-banner-management Banner 管理各角色用户故事
content: 基于 requirement.md v1 与 prototype/web/banner-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 11:07:50
updated_at: 2026-06-28 11:07:50
note: REQ-0016-banner-management
---

# 用户故事

## 故事索引

| 编号 | 角色 | 优先级 | 本期范围 |
|---|---|---|---|
| US-001 | 后台运营 | P0 | 是 |
| US-002 | 后台管理员 | P0 | 是 |
| US-003 | 后台运营（Dashboard 快捷入口） | P1 | 是 |
| US-004 | 店主 | P2 | 否（不得访问管理端） |

---

## US-001 后台运营维护 Banner

**作为** 后台运营人员，  
**我希望** 在管理后台维护各展示端 Banner 的素材、排序、跳转与有效期，并在列表控制上线/下线，  
**以便** 前台首页与专题运营位内容可配置且状态可控。

### 验收要点

- 可访问 `/admin/banners`，Sidebar「Banner 管理」高亮。
- 列表支持关键词、展示端、状态、时间状态筛选；四指标卡；分页 10/20/50。
- 表格含 Banner 缩略图、展示端、跳转类型、状态、有效期、排序、更新时间、操作（编辑、上线/下线、删除）。
- 「＋ 新增 Banner」打开弹窗；按跳转类型展示条件字段；弹窗 **不含** 状态编辑与状态策略说明块。
- 新建保存为草稿；上线/下线在列表二次确认；已上线须先下线再删除。
- 跳转类型支持：SKU 详情、外部链接、专题页、无跳转（不含类目页创建）。

### 关联功能

- FR-001 ~ FR-013、FR-008

---

## US-002 后台管理员监管 Banner 配置

**作为** 后台管理员，  
**我希望** 与运营人员一样访问 Banner API 并受统一 RBAC 约束，  
**以便** 运营配置可追溯、误删与非法上线可防范。

### 验收要点

- `admin`、`employee` 可列表/新增/编辑/上线/下线/删除（满足删除条件）；`store_owner` 返回 403。
- 标题唯一性、跳转目标完整性、HTTPS 外链校验前后端双重校验。
- Banner 自定义图片走 MinIO 授权上传；SKU 图库引用不重复存文件。

### 关联功能

- FR-006、FR-007、FR-014、FR-015

---

## US-003 从 Dashboard 快捷新增 Banner

**作为** 后台运营人员，  
**我希望** 从管理首页快捷操作「新增 Banner」直接进入 Banner 管理并发起新建，  
**以便** 减少从占位入口到真实功能的操作断点。

### 验收要点

- Dashboard「新增 Banner」导航至 `/admin/banners` 并自动打开新增弹窗（或等效：导航后一键可达新增）。
- 父需求 `REQ-0004-admin-home` 快捷宫格不再为 toast 占位。

### 关联功能

- FR-001

---

## US-004 店主不得访问 Banner 管理（边界）

**作为** 店主，  
**我希望** 无法进入 Banner 管理页面与 API，  
**以便** 权限边界清晰。

### 验收要点

- `store_owner` 无法访问 `/admin/banners` 与 `/api/v1/admin/banners*`、`/api/v1/admin/topics`。

### 关联功能

- FR-014

---

## 与父需求差异

| 对比项 | REQ-0004-admin-home | REQ-0016 |
|---|---|---|
| Banner 导航 | 占位，无 path | `/admin/banners` 真实页面 |
| Dashboard 快捷「新增 Banner」 | 占位 | 导航至 Banner 管理 |
| Banner 数据 | mock 指标数字 | 真实 CRUD + 状态机 |
| 消费端展示 | 未实现 | 本期仍不包含店主端/小程序展示 |
