---
title: 需求验收标准
purpose: 系统设置页、5 分组 Tab、API、持久化与 UI 验收
content: 基于 requirement.md v1 与 prototype/web/system-settings-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
created_at: 2026-06-28 11:18:24
updated_at: 2026-06-28 11:18:24
note: REQ-0017-system-settings
---

# 验收标准

> **Phase 标记**：`[P0]`/`[P1]`/`[P2]`/`[P3]` 表示最低交付 Phase；全量验收需 P0–P3 均完成。

## 1. 功能验收 — 访问与导航

- [ ] **AC-001** `[P0]` 已登录 `admin` 可访问 `/admin/settings` 并重定向至 `/admin/settings/basic`。
- [ ] **AC-002** `[P0]` `employee` 侧栏不展示「系统设置」；直链 `/admin/settings/basic` 跳转 forbidden/403。
- [ ] **AC-003** `[P0]` `store_owner` 不得访问 system-settings 路由与 API。
- [ ] **AC-004** `[P0]` `admin-nav.ts` 为「系统设置」配置 `path: '/admin/settings'`；当前路由下侧栏项 active。
- [ ] **AC-005** `[P0]` 注册 5 个子路由；`settings-nav` 当前 Tab 品牌金 active，与 URL 同步。
- [ ] **AC-006** `[P0]` 页头眉标含 `SYSTEM / SETTINGS`；分组标题与 prototype 对应当前 Tab 一致。

## 2. 功能验收 — 页面 Shell 与交互

- [ ] **AC-007** `[P0]` 布局含 `page-hero`、`summary-grid`、`settings-layout`（`settings-nav` | `settings-panel`）；内容 max-width 1080px。
- [ ] **AC-008** `[P0]` 表单 dirty 时展示「有未保存修改」轻量提示。
- [ ] **AC-009** `[P0]` 页头与底部均提供「保存设置」；行为一致。
- [ ] **AC-010** `[P0]` 「取消」恢复最近 GET 快照；清除 dirty。
- [ ] **AC-011** `[P0]` 「恢复默认」二次确认后调用 reset API；表单刷新为默认值。
- [ ] **AC-012** `[P0]` 保存成功 inline 提示（save-tip 风格，非 toast）。
- [ ] **AC-013** `[P0]` semantic token；禁止新增裸 Hex；主 CTA 品牌金；输入高度 40px；圆角 2px/3px 对齐 prototype。

## 3. 功能验收 — 基础信息 Tab（P0）

- [ ] **AC-014** `[P0]` 字段含：平台名称*、默认语言*、默认时区*、数据刷新周期、客服邮箱、维护窗口、系统公告、首页指标卡开关、维护公告开关。
- [ ] **AC-015** `[P0]` 平台名称 2–64 字必填；邮箱格式校验；公告 ≤500 字。
- [ ] **AC-016** `[P0]` PATCH `basic` 分组持久化；GET 返回 effective 值。
- [ ] **AC-017** `[P0]` 与 `prototype/web/system-settings-basic.html` 字段顺序与分组结构一致。

## 4. 功能验收 — 媒体与存储 Tab（P0）

- [ ] **AC-018** `[P0]` 可写：图片/视频最大 MB、允许 MIME 列表（逗号分隔）。
- [ ] **AC-019** `[P0]` 只读：默认存储桶、Key 生成规则（文案对齐 REQ-0012）。
- [ ] **AC-020** `[P0]` PATCH 后下一次 `POST /uploads` 按新限制校验（无需重启容器）。
- [ ] **AC-021** `[P0]` 不可 PATCH 桶名、endpoint、prefix。
- [ ] **AC-022** `[P0]` 与 `prototype/web/system-settings-media.html` 一致。

## 5. 功能验收 — 安全策略 Tab（P1）

- [ ] **AC-023** `[P1]` 可配置：密码最小长度 8–32、四项复杂度开关、密码有效期、会话超时、首次登录强制改密。
- [ ] **AC-024** `[P1]` admin 重置用户密码、REQ-0015 改密、随机密码生成均 enforcement 当前策略。
- [ ] **AC-025** `[P1]` 会话超时变更仅影响新签发 JWT。
- [ ] **AC-026** `[P1b]`（可选）登录失败锁定：阈值、锁定时长；失败计数与锁定逻辑。
- [ ] **AC-027** `[P1]` 与 `prototype/web/system-settings-security.html` 一致。

## 6. 功能验收 — 审计配置 Tab（P2）

- [ ] **AC-028** `[P2]` 可写：日志保留天数 30–3650、导出权限、敏感操作强制记录、脱敏展示开关。
- [ ] **AC-029** `[P2]` 只读：审计范围说明、最近变更列表（修改人/时间/摘要）。
- [ ] **AC-030** `[P2]` 每次 settings PATCH/reset 写入 `audit_logs`（domain=`system_settings`）。
- [ ] **AC-031** `[P2]` 与 `prototype/web/system-settings-audit.html` 一致。

## 7. 功能验收 — 通知设置 Tab（P3）

- [ ] **AC-032** `[P3]` 可写：账号冻结通知、SKU 待处理、存储容量预警开关；阈值 50–95%。
- [ ] **AC-033** `[P3]` 通知模板只读列表 + 「查看」入口（modal 占位可接受）。
- [ ] **AC-034** `[P3]` **不验收**真实邮件/短信/站内信发送。
- [ ] **AC-035** `[P3]` 与 `prototype/web/system-settings-notification.html` 一致。

## 8. 接口验收

| 接口 | Phase | 说明 |
|---|---|---|
| `GET /api/v1/admin/system-settings/{group}` | P0+ | group ∈ basic/security/media/notification/audit |
| `PATCH /api/v1/admin/system-settings/{group}` | P0+ | 按 Tab 分阶段开放 group |
| `POST /api/v1/admin/system-settings/{group}/reset` | P0+ | 分组恢复默认 |
| `GET /api/v1/admin/system-settings/audit/recent` | P2 | 最近变更 |

- [ ] **AC-036** `[P0]` 全部接口 `require_system_admin`；`employee` → 403。
- [ ] **AC-037** `[P0]` 统一 `ApiResponse`；错误码符合 `rules/api.md`。
- [ ] **AC-038** `[P0]` OpenAPI 更新 + Orval 重新生成前端客户端。

## 9. 数据验收

- [ ] **AC-039** `[P0]` Migration 新建 `system_settings`（key、value、updated_at、updated_by）。
- [ ] **AC-040** `[P2]` Migration 新建 `audit_logs`（与 REQ-0014 统一模型）；若已有 `profile_activity_logs` 则迁移或双写策略 documented。
- [ ] **AC-041** `[P1]`（若启用）用户表 `must_change_password` 或等价字段；登录响应携带 flag。

## 10. 技术验收

- [ ] **AC-042** `[P0]` 后端 pytest：GET/PATCH/reset、RBAC、effective settings merge、upload 限制联动。
- [ ] **AC-043** `[P1]` pytest：密码策略 enforcement（admin reset + change password）。
- [ ] **AC-044** `[P2]` pytest：audit_logs 写入与 recent 查询。
- [ ] **AC-045** `[P0]` 前端 vitest：Tab 路由、dirty、保存/取消/reset mock、employee 菜单隐藏。

## 11. 原型 trace checklist（/opsx-apply 阶段填写「实现」列）

| 检查项 | HTML | PNG | 实现 |
|---|---|---|---|
| Shell + settings-nav 5 Tab | ✓ | 待导出 | |
| 基础信息 Tab | ✓ | 待导出 | |
| 安全策略 Tab | ✓ | 待导出 | |
| 媒体与存储 Tab | ✓ | 待导出 | |
| 通知设置 Tab | ✓ | 待导出 | |
| 审计配置 Tab | ✓ | 待导出 | |
| dirty 提示 + 双保存 + 底部操作条 | ✓ | 待导出 | |
| summary-grid 摘要卡 | ✓ | 待导出 | |

> PNG Golden 文件待从 HTML 导出至 `prototype/web/system-settings-*.png`；当前以 HTML 为开发优先参考。

## 12. 范围外（不验收）

- 通知真实发送引擎、邮件 SMTP 配置。
- MinIO/SQLite/Docker 运维面板；`.env` 运维项在线修改。
- 审计日志导出文件下载、定时 purge job（可配置保留天数即可）。
- 店主 Web / 小程序系统配置。
- 登录失败锁定（未纳入 P1 且未声明 P1b 时）。
