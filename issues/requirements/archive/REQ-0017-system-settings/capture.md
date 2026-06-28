---
req_id: REQ-0017-system-settings
status: exploring
created_at: 2026-06-28 11:06:12
updated_at: 2026-06-28 11:15:38
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0004-admin-home
---

# 一句话

实现 Web 管理后台「系统设置」页面：替换侧栏 SYSTEM 分组「系统设置」占位入口，提供可维护的全局/平台级配置能力（5 分组 Tab + 设计包已齐，交付建议分 Phase）。

# 原始描述

实现系统设置页面。

## 背景与关联

- 父需求 `REQ-0004-admin-home`：侧栏 SYSTEM 分组已预留「系统设置」导航项，当前 `admin-nav.ts` 无 `path`，点击无有效路由。
- 姊妹能力：`REQ-0005-user-management`（用户管理）、`REQ-0014-profile-page`（个人资料）、`REQ-0015-password-change`（密码修改）——个人级设置与用户级管理分离，系统设置面向平台/租户级参数。
- 视觉：继承管理端暗色旗舰风；设计包 v2 已提供 5 分组 HTML/PNG/context（见 `prototype/web/`）。

## 初步范围假设（待 `/req-explore` 确认）

- **In**：Web 管理端 `/admin/settings`（或等价路由）独立页面；侧栏「系统设置」可导航且 active 高亮。
- **Out（候选，待澄清）**：店主 Web / 小程序配置；基础设施级 `.env` 热更新；对象存储/数据库运维面板。

# 待澄清

- [x] 设置项清单：v2 设计包 5 分组（基础信息 / 安全策略 / 媒体与存储 / 通知设置 / 审计配置）——见 `requirement.md` 草稿与 `prototype/web/`
- [x] 权限：仅 `role === "admin"`（`require_system_admin`）；`employee` 隐藏菜单且路由 403，与用户管理一致
- [ ] 持久化：SQLite `system_settings` key-value vs 分组表；与 env 默认值 merge 策略
- [x] 设计包：已有 `prototype/web/system-settings-{basic,security,media,notification,audit}.{html,png}` 及 context；待 req-complete 清理重复目录 `prototype/用所选项目新建的文件夹/` 并统一 PNG 路径引用
- [ ] 与 `.env` / 运行时 `Settings` 的关系：媒体大小/JWT 超时等在线改是否必须立即生效，还是只读展示 env + 说明需重启

# 探索结论

（/req-explore 2026-06-28 11:15:38）

## 范围与定位

- **单 REQ**：保持 `REQ-0017-system-settings`，不拆 5 个 peer REQ；共用 Shell（`settings-nav` + 5 Tab）、同一路由族、预期 OpenSpec `add-system-settings`。
- **交付分 Phase**（在 PRD/acceptance 中切分，而非新建 REQ 编号）：

| Phase | 范围 | 目标 |
|-------|------|------|
| P0 | 路由 + Shell + **基础信息**（可写）+ **媒体与存储**（大小/格式可配；桶路径只读） | 侧栏占位闭环，价值可见 |
| P1 | **安全策略**（密码规则 + 会话超时；登录锁定可后置） | 与 REQ-0015 / 建用户密码校验联动 |
| P2 | **审计**（audit 表 + 设置变更日志 + 审计 Tab） | 满足「保存写审计」通用规则 |
| P3 | **通知设置** | 需先定通知通道（邮件 / 仅 UI 开关） |

## 设计包与 UI

- 信息架构：`/admin/settings/:tab`（建议子路由：basic / security / media / notification / audit）。
- 页面结构：`page-hero` + `summary-grid` + `settings-layout`（`settings-nav` | `settings-panel`）；dirty 提示；标题区 + 底部双保存入口（取消 / 恢复默认 / 保存）。
- **不宜**直接复用 `AdminEditPage`（`max-w-2xl`）；宜新建 `SystemSettingsPage` 或等价页面级布局， fidelity 对照 `prototype/web/*.html`。
- 原型优先级：HTML > PNG > context > requirement > `rules/ui-design.md`。

## 权限

- 后端：`require_system_admin`（与 `admin_users` 一致）。
- 前端：`employee` 不展示侧栏「系统设置」；直链访问返回 403 页。

## 与姊妹 REQ / 代码现状

| 关联 | 关系 |
|------|------|
| REQ-0005 用户管理 | 管「人」vs 管「平台」——不重复 |
| REQ-0014 个人资料 | 个人 vs 平台——不重复 |
| REQ-0015 改密 | 安全 Tab 密码规则须在改密/建用户处统一 enforcement |
| REQ-0012 对象存储 Key | 媒体 Tab 桶/前缀只读展示须与 0012 归档 spec 一致 |
| `config.py` Settings | 上传大小/JWT 等已在 env；无 DB 配置表、无 settings API |
| `login_logs` | 有登录记录；无失败锁定、无统一 audit 表 |
| 通知 | 项目尚无邮件/站内信基础设施——通知 Tab 风险最高 |

## 持久化策略（待 PRD 拍板）

| 类型 | 示例 | 建议 |
|------|------|------|
| 运维级 | MinIO endpoint、SECRET_KEY | 不展示或只读 |
| 策略级 | 上传大小、JWT 超时、密码长度 | SQLite + service merge env 默认值 |
| 业务级 | 平台名、公告、首页开关 | 纯 DB |

**风险**：若 upload 仍只读进程启动时的 `settings.max_*_size_mb`，UI 改 DB 不生效——须在 PRD 明确「runtime 读 DB」或「只读 + 需重启」。

## 实现难度粗估

| 分组 | 难度 | 备注 |
|------|------|------|
| 基础信息 | 中 | 可能牵动 dashboard 文案 |
| 安全策略 | 高 | auth / 锁定 / 多入口校验 |
| 媒体与存储 | 中低 | 与 env + REQ-0012 对齐 |
| 通知设置 | 很高 | 缺通知通道 |
| 审计配置 | 高 | 依赖 audit 表；与 REQ-0014 审计模型宜合并为统一 `audit_logs` |

**容量**：全量 5 Tab + audit + 部分 security 约 **10–14 人日**；通知若仅 UI 开关约 **8–10 人日**。不宜纳入 sprint-003（已含 REQ-0014/0015/0009/0012）；建议独立 Sprint 或 sprint-004。

## 资产 hygiene（generate/complete 前）

1. `requirement.md` 标题由 REQ-0011 更正为 **REQ-0017**，补规范 frontmatter。
2. context 中 `prototype/images/` 路径与 `prototype/web/*.png` 对齐。
3. 删除或合并 `prototype/用所选项目新建的文件夹/` 重复资产。

## 待产品拍板（generate 前）

1. 首期 Phase 是否接受 P0 = 基础 + 媒体，通知/审计进 P2/P3？
2. 通知 Tab：本期真实发信，还是仅配置项 + 后续 REQ？
3. 登录失败锁定是否 MVP 必须？
4. 上传限制在线改是否必须立即生效？
5. 审计模型是否与 REQ-0014 的 `profile_activity_logs` 合并为统一表？

## 下一步

1. `/req-generate REQ-0017-system-settings` — 吸收 v2 设计包，写入 Phase 切分与 env/DB 策略
2. `/req-complete` — 六件套 + 清理重复 prototype 目录
