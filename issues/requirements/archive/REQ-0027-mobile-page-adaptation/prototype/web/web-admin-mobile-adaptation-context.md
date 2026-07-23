---
title: Web 管理端移动端基础适配原型说明
purpose: 说明 REQ-0027 移动端验收原型的范围、优先级和后续截图要求
content: 基于 requirement.md、acceptance.md 与知识库横切 AC 生成
source: AI 根据 PRD 与知识库最佳实践生成，项目团队确认
update_method: 原型、验收视口或页面范围变更时同步更新
owner: product
status: draft
created_at: 2026-07-05 10:17:18
updated_at: 2026-07-05 10:17:18
note: REQ-0027-mobile-page-adaptation
---

# Web 管理端移动端基础适配原型说明

## 1. 原型定位

本目录原型用于 `REQ-0027` 后续 `/req-opsx` 的 design 与验收参考，不是生产代码。

本 REQ 不要求重做管理端移动端信息架构；原型只表达：

- 必测视口矩阵。
- 必测管理端页面清单。
- 每类页面的移动端基础可用检查点。
- 横切 knowledge-base AC 的验收入口。

## 2. 原型文件

| 文件 | 用途 |
|---|---|
| `web-admin-mobile-adaptation.html` | 静态验收矩阵页面，展示视口、页面、组件类型与通过标准 |
| `web-admin-mobile-adaptation-context.md` | 本说明文件 |
| PNG Golden Reference | 待导出；apply 完成前 SHOULD 用 Playwright screenshot 或等价截图补充 |

## 3. 视觉 / 验收优先级

```text
1. prototype/web/web-admin-mobile-adaptation.html
2. prototype/web/web-admin-mobile-adaptation-context.md
3. acceptance.md
4. requirement.md
5. rules/ui-design.md
6. openspec/specs/（已归档能力）
```

若 HTML 与 acceptance 冲突，以 HTML 中的“验收矩阵范围”优先，但不得扩大到店主 Web 或微信小程序。

## 4. 必测视口

| 视口 | 说明 |
|---|---|
| `375x812` | 手机小屏，优先发现弹窗、分页、筛选重叠问题 |
| `390x844` | 主流手机，验收主要管理操作可用 |
| `768x1024` | 小屏平板，验收 Sidebar / Shell 降级和表格容器滚动 |
| `1440x1024` | 桌面回归，确保移动端修复不破坏桌面布局 |

## 5. 必测页面

| 优先级 | 路由 | 验收重点 |
|---|---|---|
| P0 | `/admin/login` | 既有移动登录布局不回归 |
| P0 | `/admin/dashboard` | Shell、Sidebar、指标卡、最近更新表格 |
| P0 | `/admin/tile-skus` | 宽表格、大弹窗、媒体字段 |
| P0 | `/admin/brands` | Logo 列、品牌弹窗、启停确认 |
| P0 | `/admin/users` | 分页基准、重置密码确认、用户弹窗 |
| P1 | `/admin/logs` | 多条件筛选、日志详情抽屉 |
| P1 | `/admin/settings/basic` | 设置导航、保存、恢复默认、dirty 切换 |

## 6. 后续截图建议

apply 完成前 SHOULD 至少补充以下截图或 Playwright trace：

- `375x812`：`/admin/tile-skus` 列表 + SKU 弹窗。
- `390x844`：`/admin/brands` 列表 + 品牌弹窗。
- `768x1024`：`/admin/dashboard` + Sidebar 顶部导航。
- `375x812`：`/admin/settings/basic` 表单与确认弹窗。
- `1440x1024`：`/admin/tile-skus` 桌面回归。

## 7. Out of Scope

- 店主 Web 展示端。
- 微信小程序。
- 新增移动端专属业务流程。
- API / DB / Orval / Docker 变更。
