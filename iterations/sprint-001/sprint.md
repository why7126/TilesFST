---
title: Sprint 001 迭代说明
purpose: 记录 Sprint 001 目标、范围、Change、工作量与风险
content: 基于 REQ-0001 及全部登录相关 OpenSpec Change 规划
source: AI根据 issues/openspec 目录生成，项目团队确认
update_method: 迭代范围或状态变化时更新
owner: 项目负责人
status: completed
note: Sprint 001 已于 2026-06-14 验收通过
---

# Sprint 001

## Sprint 目标

本迭代交付 REQ-0001 **用户登录**完整能力（功能 + 视觉），并纳入 REQ-0002 **产品品牌与登录页简化**、REQ-0003 **登录页左栏文案与布局微调**（追溯补登），含：

- Web 管理端账号密码登录（`/admin/login`）
- 产品名 **TilesFST**、登录页无企微、无页面级纵向滚动（REQ-0002）
- 左栏主标题「瓷砖信息管理后台」、隐藏忘记密码入口、左栏间距与统计卡布局（REQ-0003）
- 后端认证 API、用户模型、路由守卫、角色分流
- Web Design System（Token + shadcn/ui）
- 登录页 UI 组件化与 PNG/CSS Port 视觉对齐

本迭代为 `add-tile-catalog`、`add-tile-admin` 提供安全与视觉基础。

**验收结论：** ✓ 通过（2026-06-14）

## Scope

### 包含需求

| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0001 | 用户登录 | P0 | resolved | 认证 + 登录页视觉；全部 login change 已归档 |
| REQ-0002 | 产品品牌与登录页简化 | P0 | resolved | TilesFST 品牌、移除企微、视口无滚动 |
| REQ-0003 | 登录页左栏文案与布局微调 | P1 | resolved | 主标题、隐藏忘记密码、左栏布局 |

### 包含技术改造

| 名称 | Change | 状态 |
|---|---|---|
| Web Design System | `add-design-system` | ✓ 已归档 |
| 登录页 DS 组件化 | `refactor-login-ui` | ✓ 已归档 |
| 登录页 checklist 对齐 | `align-login-prototype` | ✓ 已归档 |
| 登录页 PNG 像素级 | `fix-login-pixel-fidelity` | ✓ 已归档 |
| TilesFST 品牌与登录简化 | `update-tilesfst-login-simplify` | ✓ 已归档 |
| 登录页左栏微调 | `fix-login-left-panel-refine` | ✓ 已归档 |

### 不包含（延后至后续 Sprint）

| 项目 | 延后原因 |
|---|---|
| 瓷砖目录/管理 | 计划 Sprint 002+ |
| 企微 OAuth / 忘记密码完整流程 / 小程序登录 | P2+ |

## Change 列表

| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-user-login` | REQ-0001 | 已归档 | 认证 API、路由守卫 |
| `add-design-system` | REQ-0001 | 已归档 | Design Token、shadcn |
| `refactor-login-ui` | REQ-0001 | 已归档 | DS 组件化 |
| `align-login-prototype` | REQ-0001 | 已归档 | checklist 对齐 |
| `fix-login-pixel-fidelity` | REQ-0001 | 已归档 | PNG golden reference |
| `update-tilesfst-login-simplify` | REQ-0002 | 已归档 | TilesFST / 无企微 / 无整页滚动 |
| `fix-login-left-panel-refine` | REQ-0003 | 已归档 | 左栏文案 / 隐藏忘记密码 / 布局 |

**活跃 Change 路径：** 无

## 工作量预估

| 工作包 | Change | 人天 | 状态 |
|---|---|---|---|
| 认证 + DS + UI 组件化 | 前三个 Change | 22.5 | ✓ |
| 原型 checklist | align-login-prototype | 2.5 | ✓ |
| PNG 像素级 | fix-login-pixel-fidelity | 2 | ✓ |
| 左栏微调 | fix-login-left-panel-refine | 1.5 | ✓ |
| Sprint 验收 | 全部 | 1 | ✓ |
| **合计** | | **29.5** | |

## 里程碑

| 阶段 | 交付 | 状态 |
|---|---|---|
| M1–M3 认证 + DS + 组件化 | 前三个 Change | ✓ |
| M4 checklist 对齐 | align-login-prototype | ✓ |
| M5 PNG 像素级 | fix-login-pixel-fidelity | ✓ |
| M5b 左栏微调 | fix-login-left-panel-refine | ✓ |
| **M6 Sprint 验收** | acceptance-report 全项 | **✓ 通过** |

## 依赖关系

```text
REQ-0001
  ├── add-user-login ✓
  ├── add-design-system ✓
  ├── refactor-login-ui ✓
  └── align-login-prototype ✓
        └── fix-login-pixel-fidelity ✓
              └── REQ-0002 update-tilesfst-login-simplify ✓
                    └── REQ-0003 fix-login-left-panel-refine ✓
                          └── [后续] add-tile-catalog / add-tile-admin
```

## 关联文档

| 文档 | 路径 |
|---|---|
| Sprint 索引 | `iterations/sprint-001/sprint.yaml` |
| Sprint 验收 | `iterations/sprint-001/acceptance-report.md` |
| 发布说明 | `iterations/sprint-001/release-note.md` |
| 正式 Spec | `openspec/specs/web-client/spec.md`、`openspec/specs/auth/spec.md` |
