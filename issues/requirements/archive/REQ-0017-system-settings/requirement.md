---
requirement_id: REQ-0017-system-settings
title: 管理后台系统设置页面
terminal: web-admin
version: v1
status: approved
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0004-admin-home
created_at: 2026-06-28 11:17:13
updated_at: 2026-06-28 11:26:02
---

# REQ-0017 管理后台系统设置页面

## 1. 需求背景

TILESFST 管理后台在 `REQ-0004-admin-home` 的 SYSTEM 分组已预留「系统设置」导航项，当前 `admin-nav.ts` 中该项无 `path`，点击无法进入有效页面。平台级参数（站点信息、安全策略、媒体限制、通知开关、审计策略）分散在 `.env` / 代码常量中，缺少统一的管理端配置入口与变更留痕。

本需求交付 Web 管理端 **系统设置** 能力：侧栏可导航、5 分组 Tab 页面、后端持久化与（分 Phase）审计联动。视觉与交互继承管理后台暗色旗舰风， fidelity 以 v2 设计包为准。

**边界**：

- 与用户管理（`REQ-0005`）分离：用户管理管「人」，系统设置管「平台」。
- 与个人资料（`REQ-0014`）、密码修改（`REQ-0015`）分离：个人级 vs 平台级；安全 Tab 中的密码规则须在改密/建用户流程统一 enforcement。
- 与对象存储 Key 优化（`REQ-0012`）对齐：媒体 Tab 中桶/前缀/Key 规则为**只读展示**，须与已归档或进行中的存储 spec 一致。

## 2. 目标用户

| 角色 | 是否可访问 | 说明 |
|---|---:|---|
| 后台管理员（`admin`） | 是 | 唯一可访问系统设置的角色；`require_system_admin` |
| 后台运营（`employee`） | 否 | 侧栏不展示「系统设置」；直链 `/admin/settings/*` 返回 403 |
| 店主 / 前台用户 | 否 | 不得进入管理端 |

## 3. 范围

### 3.1 本期包含（REQ 总范围）

- 路由族 `/admin/settings` 及子路由（5 Tab）；侧栏「系统设置」配置 `path` 且 active 高亮。
- 页面 Shell：`page-hero` + `summary-grid` + `settings-layout`（`settings-nav` | `settings-panel`）；dirty 提示；标题区与底部「取消 / 恢复默认 / 保存设置」。
- 5 个设置分组 Tab 页面（UI + API），原型见 §10。
- SQLite 配置持久化（`system_settings` 或等价 KV/分组表）；策略类配置 **runtime 读取 DB 并与 `.env` 默认值 merge**（改上传限制/JWT 超时等须立即生效，不要求重启）。
- 统一审计表 `audit_logs`（与 `REQ-0014` 个人操作记录合并模型）；系统设置保存、恢复默认写入审计（Phase P2 起强制；P0/P1 可先写最小变更日志）。
- OpenAPI 变更 + Orval 客户端 regeneration。

### 3.2 本期不包含

- 店主 Web / 微信小程序的系统配置或展示端设置。
- MinIO endpoint、SECRET_KEY、数据库连接等**运维级** `.env` 的在线修改（不展示或只读说明）。
- 对象存储桶名、前缀路径的在线修改（媒体 Tab 只读展示）。
- 通知邮件/短信/站内信的**真实发送引擎**（通知 Tab 本期仅配置开关与阈值持久化；发送能力后续 REQ）。
- 登录失败锁定的完整风控（可选 Phase P1b，见 §11）。
- 审计日志导出文件下载、定时清理 job 的完整实现（审计 Tab 可配置保留天数；物理 purge job 可后续迭代）。
- Docker / SQLite / MinIO 运维面板。

### 3.3 交付 Phase（Sprint 切分依据）

| Phase | 交付内容 | 验收重点 |
|---|---|---|
| **P0** | 路由 + Shell + **基础信息** Tab（可写）+ **媒体与存储** Tab（大小/格式可写；桶/Key 只读） | 侧栏占位闭环；保存立即生效 |
| **P1** | **安全策略** Tab：密码最小长度、复杂度开关、密码有效期、会话超时、首次登录强制改密 | 与 REQ-0015 / 建用户校验联动 |
| **P1b**（可选） | 登录失败锁定（阈值、锁定时长） | auth 层新增失败计数 |
| **P2** | **审计配置** Tab + `audit_logs` 全量写入 + 最近变更展示 | 「保存写审计」通用规则 |
| **P3** | **通知设置** Tab（开关 + 阈值 + 模板只读/占位查看） | 无真实发信亦可验收 |

## 4. 信息架构

```text
admin-shell
├── sidebar（264px sticky）
│   └── SYSTEM
│       ├── 用户管理 → /admin/users
│       └── 系统设置 → /admin/settings/basic（默认重定向）
└── main-content（max-width 1080px）
    ├── page-hero（眉标 SYSTEM / SETTINGS、分组标题、保存 CTA、dirty 提示）
    ├── summary-grid（当前分组摘要指标，对齐 prototype）
    └── settings-layout
        ├── settings-nav（5 Tab，品牌金 active）
        │   ├── 基础信息      /admin/settings/basic
        │   ├── 安全策略      /admin/settings/security
        │   ├── 媒体与存储    /admin/settings/media
        │   ├── 通知设置      /admin/settings/notification
        │   └── 审计配置      /admin/settings/audit
        └── settings-panel（表单 + 底部固定操作条）
```

- API 建议前缀：`/api/v1/admin/system-settings`（分组 GET/PATCH）或 `/api/v1/admin/settings/{group}`。
- 默认进入 `/admin/settings` MUST 重定向至 `/admin/settings/basic`。

## 5. 数据模型

### 5.1 `system_settings`（新建，建议 KV）

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| key | TEXT PK | 点分命名，如 `basic.platform_name`、`media.max_image_size_mb` |
| value | TEXT NOT NULL | JSON 或标量字符串 |
| updated_at | TEXT NOT NULL | ISO 时间 |
| updated_by | TEXT NULL FK → users.id | 最后修改人 |

**读取策略**：Service 层 `get_effective_setting(key)` = DB 值 ?? `Settings` env 默认值。

**恢复默认**：删除对应 key 或写回 seed 默认值；须写审计。

### 5.2 `audit_logs`（新建，与 REQ-0014 统一）

| 字段 | 类型/约束 | 说明 |
|---|---|---|
| id | TEXT PK | UUID |
| actor_user_id | TEXT NULL FK | 操作人；系统 job 可为 NULL |
| domain | TEXT NOT NULL | `system_settings` \| `profile` \| `user_admin` \| `media` 等 |
| action_type | TEXT NOT NULL | 如 `settings_update`、`settings_reset`、`profile_update` |
| summary | TEXT NOT NULL | 人类可读摘要 |
| metadata | TEXT NULL | JSON（变更 diff、分组 key 列表） |
| created_at | TEXT NOT NULL | ISO 时间 |

`REQ-0014` 的 `profile_activity_logs` 若已落地，实现时 **MUST** 迁移或双写至本表，避免两套审计模型并存。

### 5.3 配置项与 env 映射（策略级）

| 设置 key（示例） | env 默认来源 | 在线可写 |
|---|---|---|
| `media.max_image_size_mb` | `MAX_IMAGE_SIZE_MB` | 是（P0） |
| `media.max_video_size_mb` | `MAX_VIDEO_SIZE_MB` | 是（P0） |
| `media.allowed_image_types` | `ALLOWED_IMAGE_TYPES` | 是（P0） |
| `media.allowed_video_types` | `ALLOWED_VIDEO_TYPES` | 是（P0） |
| `security.jwt_access_token_expire_minutes` | `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 是（P1） |
| `security.password_min_length` | 代码默认 12 | 是（P1） |
| `basic.platform_name` | 无（纯 DB） | 是（P0） |

MinIO bucket、prefix、endpoint：**只读展示**，来自 runtime `Settings`，不可 PATCH。

## 6. API 要求（实现时对齐 `rules/api.md`）

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| GET | `/api/v1/admin/system-settings/{group}` | `require_system_admin` | `group` ∈ `basic` \| `security` \| `media` \| `notification` \| `audit`；返回该分组 effective 配置 + 只读字段 |
| PATCH | `/api/v1/admin/system-settings/{group}` | `require_system_admin` | 部分更新；校验后写 DB；P2 起写 `audit_logs` |
| POST | `/api/v1/admin/system-settings/{group}/reset` | `require_system_admin` | 恢复该分组默认；写审计 |
| GET | `/api/v1/admin/system-settings/audit/recent` | `require_system_admin` | 审计 Tab：最近 N 条系统设置变更（默认 10） |

响应 MUST 使用统一 `ApiResponse` 包装。

## 7. 功能要求

### FR-001 导航与路由

- MUST 为侧栏「系统设置」配置 `path: '/admin/settings'`（或等价）。
- MUST 注册 5 个子路由；`/admin/settings` 重定向至 `basic`。
- MUST 在对应路由下高亮侧栏「系统设置」与 `settings-nav` 当前 Tab。
- `employee` 角色 MUST NOT 在侧栏看到「系统设置」；直链 MUST 403。

### FR-002 页面 Shell 与交互

- MUST 实现 prototype 定义的 `page-hero`、`summary-grid`、`settings-layout` 结构。
- 表单 dirty 时 MUST 展示「有未保存修改」提示。
- MUST 提供标题区与底部两处「保存设置」入口；「取消」放弃未保存修改；「恢复默认」二次确认后调用 reset API。
- 保存成功 MUST inline 提示（非 toast 亦可，与 profile 页 `save-tip` 风格一致）。

### FR-003 权限

- 所有 system-settings API MUST 使用 `require_system_admin`（与 `admin_users` 一致）。

### FR-004 配置生效

- 上传校验（`uploads`、SKU/品牌/头像等）MUST 通过 effective settings 读取 `max_*_size_mb` 与 allowed types，不得仅读进程启动 snapshot。
- JWT 会话超时修改（P1）MUST 作用于**新签发的 token**；已有 token 按原 exp 失效。

### FR-005 安全策略联动（P1）

- 密码最小长度、复杂度要求（大写/小写/数字/特殊字符）MUST 在以下路径 enforcement：
  - 管理员重置用户密码（`admin_users`）
  - 用户自助改密（`REQ-0015`）
  - 随机密码生成（`generate_random_password`）
- 「首次登录强制改密」：用户表增加 `must_change_password` 或等价 flag；登录响应携带标志，前端引导改密 modal。

### FR-006 审计（P2）

- 每次 PATCH / reset system-settings MUST 写入 `audit_logs`（domain=`system_settings`）。
- 审计 Tab MUST 展示可配置的审计范围说明、保留天数、导出权限开关、敏感字段脱敏策略、最近变更列表（修改人/时间/摘要）。

### FR-007 通知（P3）

- MUST 持久化开关：账号冻结通知、SKU 待处理提醒、存储容量预警及容量阈值。
- 通知模板 MUST 只读展示 + 「查看」入口（可为 modal 占位文案）；**不要求**本期触发真实通知。

## 8. 分组功能详述

### 8.1 基础信息（P0）

| 字段 | 必填 | 规则 |
|---|---|---|
| 平台名称 | 是 | 2–64 字；影响 dashboard 等展示文案 |
| 默认语言 | 是 | 枚举：`zh-CN`（首期可仅支持中文） |
| 默认时区 | 是 | IANA，默认 `Asia/Shanghai` |
| 数据刷新周期 | 否 | 分钟，正整数；dashboard 指标刷新 hint |
| 客服邮箱 | 否 | 邮箱格式 |
| 系统维护窗口 | 否 | 文本说明 |
| 系统公告 | 否 | 0–500 字 |
| 首页展示核心指标卡 | 否 | boolean |
| 首页展示维护公告 | 否 | boolean |

原型：`prototype/web/system-settings-basic.html`、`system-settings-basic.png`、`system-settings-basic-context.md`。

### 8.2 安全策略（P1）

| 字段 | 必填 | 规则 |
|---|---|---|
| 密码最小长度 | 是 | 8–32，默认 12 |
| 密码有效期（天） | 否 | 0 表示不过期 |
| 复杂度：大写/小写/数字/特殊字符 | 否 | 各 boolean，默认全开 |
| 首次登录强制改密 | 否 | boolean |
| 登录失败锁定 | 否 | boolean（P1b） |
| 失败次数阈值 | 条件 | 锁定开启时必填 |
| 锁定时长（分钟） | 条件 | 锁定开启时必填 |
| 会话超时时长（分钟） | 是 | 映射 JWT access expire |

原型：`prototype/web/system-settings-security.html` 等。

### 8.3 媒体与存储（P0）

| 字段 | 可写 | 规则 |
|---|---|---|
| 图片最大尺寸（MB） | 是 | 1–100，默认来自 env |
| 视频最大尺寸（MB） | 是 | 1–2000，默认来自 env |
| 允许的图片 MIME 列表 | 是 | 逗号分隔，subset 校验 |
| 允许的视频 MIME 列表 | 是 | 逗号分隔 |
| 默认存储桶 | 只读 | 来自 `MINIO_BUCKET` |
| 目录/Key 生成规则 | 只读 | 对齐 REQ-0012 spec 文案 |

原型：`prototype/web/system-settings-media.html` 等。

### 8.4 通知设置（P3）

| 字段 | 可写 | 说明 |
|---|---|---|
| 账号冻结通知 | 是 | boolean |
| SKU 待处理提醒 | 是 | boolean |
| 存储容量预警 | 是 | boolean |
| 容量预警阈值（%） | 条件 | 预警开启时 50–95 |
| 通知模板 | 只读 | 列表 + 查看入口 |

原型：`prototype/web/system-settings-notification.html` 等。

### 8.5 审计配置（P2）

| 字段 | 可写 | 说明 |
|---|---|---|
| 审计范围说明 | 只读 | 系统设置变更、账号敏感操作、媒体删除等 |
| 操作日志保留天数 | 是 | 30–3650 |
| 允许导出审计日志 | 是 | boolean（导出实现可后续） |
| 敏感操作强制记录 | 是 | boolean |
| 敏感字段脱敏展示 | 是 | boolean |
| 最近变更记录 | 只读 | 来自 `audit_logs` |

原型：`prototype/web/system-settings-audit.html` 等。

## 9. UI 约束

- MUST 遵守 `rules/ui-design.md`：semantic token，禁止裸 Hex；工业暗色风；主 CTA 品牌金；输入高度 40px；圆角 `rounded-industrial` / `rounded-card`。
- 页面画布：Sidebar 264px；内容 max-width **1080px**（非 `AdminEditPage` 的 max-w-2xl）。
- 组件：优先组合 `AdminShell` + 新建 `SystemSettingsPage`；表单使用 shadcn Input/Label/Checkbox。
- **原型优先级**（有 prototype 时强制）：
  1. `prototype/web/system-settings-*.html`
  2. `prototype/web/system-settings-*.png`
  3. `prototype/web/system-settings-*-context.md`
  4. 本 `requirement.md`
  5. `rules/ui-design.md`

## 10. 原型资产

| 分组 | HTML | Golden PNG | Context |
|---|---|---|---|
| 基础信息 | `prototype/web/system-settings-basic.html` | `prototype/web/system-settings-basic.png` | `prototype/web/system-settings-basic-context.md` |
| 安全策略 | `prototype/web/system-settings-security.html` | `prototype/web/system-settings-security.png` | `prototype/web/system-settings-security-context.md` |
| 媒体与存储 | `prototype/web/system-settings-media.html` | `prototype/web/system-settings-media.png` | `prototype/web/system-settings-media-context.md` |
| 通知设置 | `prototype/web/system-settings-notification.html` | `prototype/web/system-settings-notification.png` | `prototype/web/system-settings-notification-context.md` |
| 审计配置 | `prototype/web/system-settings-audit.html` | `prototype/web/system-settings-audit.png` | `prototype/web/system-settings-audit-context.md` |

`/req-complete` 时 MUST 清理重复目录 `prototype/用所选项目新建的文件夹/`。

## 11. 关联需求

| REQ | 关系 |
|---|---|
| REQ-0004-admin-home | 父需求；侧栏占位入口 |
| REQ-0005-user-management | 姊妹 SYSTEM 页；权限模型参考 |
| REQ-0012-object-storage-key-layout | 媒体 Tab 只读 Key 规则对齐 |
| REQ-0014-profile-page | 审计表统一；个人操作写入同一 `audit_logs` |
| REQ-0015-password-change | 安全 Tab 密码规则 enforcement |

## 12. 非功能要求

- 单分组 PATCH 响应 P95 < 500ms（本地 Docker）。
- 配置变更 MUST NOT 要求重启 backend 容器（策略级）。
- 敏感配置（密码规则、锁定阈值）变更 MUST 写审计（P2 起）。

## 13. 状态

| 项 | 值 |
|---|---|
| requirement_id | REQ-0017-system-settings |
| status | approved |
| expected_openspec_change | `add-system-settings` |
| readiness | 评审通过；PNG Golden 待导出（opsx-apply 前） |
