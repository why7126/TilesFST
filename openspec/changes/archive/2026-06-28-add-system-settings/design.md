## Context

- **现状**：`admin-nav.ts`「系统设置」无 `path`；无 system-settings API/表；upload/auth 仅读 `Settings()` 进程 env snapshot。
- **依赖**：`AdminLayout`、`admin-home.css`、用户管理页表单模式、`require_system_admin`、REQ-0015 改密、REQ-0012 object key spec。
- **原型来源**（OpenSpec / AGENTS 强制优先级）：
  1. `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-*.html`
  2. `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-*.png`（待导出）
  3. `issues/requirements/archive/REQ-0017-system-settings/prototype/web/system-settings-*-context.md`
  4. `issues/requirements/archive/REQ-0017-system-settings/acceptance.md`
  5. `rules/ui-design.md`
  6. `openspec/specs/`

## Conflict Resolution

| 检查项 | HTML | PNG | acceptance / PRD | 决议 |
|--------|------|-----|------------------|------|
| Golden PNG | 5×HTML 齐 | **待导出** | Partially Ready | 开发以 HTML 为准；apply 前导出 PNG 并排验收 |
| 上传限制来源 | 表单可编辑 MB/MIME | 同 HTML | runtime effective settings | **MODIFIED** object-storage spec；service 层 merge |
| 桶/Key 路径 | 只读展示块 | 同 HTML | 不可 PATCH | 只读字段来自 `Settings` + REQ-0012 文案 |
| 通知发信 | 模板「查看」按钮 | 同 HTML | 不发真实通知 | UI + DB 开关 only；无 SMTP |
| 审计表 | 最近变更列表 | 同 HTML | 与 REQ-0014 统一 `audit_logs` | P2 建表；profile 若已有 `profile_activity_logs` 双写/迁移 |
| Tab dirty 切换 | 未显式 modal | — | business-flow 待定 | **D5**：切换 Tab 前若 dirty → `window.confirm` 放弃未保存 |
| 保存成功 | inline save-tip | 同 HTML | 非 toast | 以 HTML 为准 |
| employee 菜单 | HTML 样例 admin | — | employee 隐藏 | 实现按 role 过滤 nav；HTML 为 admin 视角 |

## Goals / Non-Goals

**Goals:**

- P0–P3 按 acceptance Phase 标记交付；侧栏占位闭环。
- CSS Port：`system-settings.css`；5 Tab 共用 Shell；1080px max-width。
- `system_settings` + effective merge；upload 立即生效。
- PNG checklist 写入 change `trace.md`（导出后）。

**Non-Goals:**

- 通知邮件/短信/站内信发送引擎。
- `.env` 运维项、MinIO endpoint/bucket 在线修改。
- 审计导出下载、purge cron job（可配置保留天数即可）。
- 店主端 / 小程序系统配置。

## Decisions

### D1：CSS Port（与 profile/user-management 一致）

- **决策**：新增 `src/web/src/features/admin/styles/system-settings.css`，自 5 份 HTML port 共用布局（`.settings-layout`、`.settings-nav`、`.settings-panel`、`.summary-grid`、`.save-tip`）；Shell 复用 `AdminLayout` + `admin-home.css`。
- **理由**：原型含固定 1080px 双栏 settings-nav；`AdminEditPage` max-w-2xl 不适用。
- **Token**：禁止裸 Hex；主按钮品牌金；输入 40px。

### D2：路由与导航

```text
/admin/settings              → redirect /admin/settings/basic
/admin/settings/:tab         → basic | security | media | notification | audit

admin-nav.ts:
  settings: { path: '/admin/settings', adminOnly: true }  # 或 role filter

AdminSidebar:
  employee → 过滤掉 settings 项
ProtectedRoute + requireAdmin for /admin/settings/*
```

### D3：API 与数据模型

```text
GET    /api/v1/admin/system-settings/{group}
PATCH  /api/v1/admin/system-settings/{group}
POST   /api/v1/admin/system-settings/{group}/reset
GET    /api/v1/admin/system-settings/audit/recent?limit=10
```

```sql
CREATE TABLE system_settings (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  updated_by TEXT NULL REFERENCES users(id)
);

-- P2
CREATE TABLE audit_logs (
  id TEXT PRIMARY KEY,
  actor_user_id TEXT NULL REFERENCES users(id),
  domain TEXT NOT NULL,
  action_type TEXT NOT NULL,
  summary TEXT NOT NULL,
  metadata TEXT NULL,
  created_at TEXT NOT NULL
);
```

`get_effective(key)` = DB value ?? env/code default.

### D4：Effective settings 注入点

| 消费者 | keys |
|--------|------|
| `uploads` / `save_upload_file` | `media.max_*_size_mb`, `media.allowed_*_types` |
| `create_access_token` | `security.jwt_access_token_expire_minutes` |
| `validate_password` | `security.password_*`, complexity flags |
| Dashboard（可选 P0） | `basic.platform_name`, 公告开关 |

### D5：Tab dirty 与取消

- dirty → 展示「有未保存修改」。
- 切换 Tab：confirm 放弃未保存。
- 取消：恢复最近 GET 快照。
- 恢复默认：Modal 二次确认 → POST reset。

### D6：Phase 实现顺序（tasks.md 对齐）

1. **P0**：migration `system_settings`、basic+media API/UI、nav path、effective upload。
2. **P1**：security group、password policy service、JWT expire、must_change_password（可选）。
3. **P2**：`audit_logs`、audit group UI、PATCH/reset 写 audit。
4. **P3**：notification group UI（开关+阈值+模板 modal 占位）。

### D7：与 REQ-0014 审计协调

- 若 `add-admin-profile-page` 已建 `profile_activity_logs`，本 change P2 **SHOULD** 引入 `audit_logs` 并双写 profile 事件，或 migration 合并；design 取「统一 `audit_logs`」为 target state。

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 全量 10–14 人日 | tasks 分 Phase；Sprint 可只 apply P0 |
| REQ-0015 未合并 | P1 密码 enforcement 与改密 change 同 Sprint 联调 |
| REQ-0012 Key 文案漂移 | 媒体 Tab 只读块读 shared helper 或 constants |
| PNG 缺失 | HTML gate 先行；trace 记录待导出 |
