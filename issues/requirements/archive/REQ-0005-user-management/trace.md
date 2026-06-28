---
created_at: 2026-06-27 08:42:28
title: 需求追踪
purpose: 记录 REQ-0005 管理后台用户管理的来源、关联文档与实现追踪
content: 基于 requirement.md 与项目目录结构维护
source: AI 根据 PRD 生成，项目团队确认
update_method: 状态、迭代或 OpenSpec 变更时同步更新
owner: product
status: done
lifecycle_stage: archive
note: add-user-management 已 archive（2026-06-20）；列表 v2 见 fix-user-management-list-refine
updated_at: 2026-06-27 22:33:15
---

# 需求追踪

## 1. 基本信息

```yaml
requirement_id: REQ-0005-user-management
requirement_name: user-management
requirement_type: 管理端 / 用户与权限
priority: P0
status: done
source: 基于 admin-home 与管理端用户体系扩展
target_users:
  - 系统管理员（后台管理员）
target_clients:
  web_admin: 本期实现
  web_catalog: 不涉及
  wechat_miniapp: 不涉及
iteration: sprint-002
change_id: add-user-management
related_requirements:
  - REQ-0001-user-login
  - REQ-0004-admin-home
related_changes:
  - add-admin-home
openspec_changes:
  - change_id: add-user-management
    type: add
    status: archived
    iteration: sprint-002
    requirement_id: REQ-0005-user-management
    strategy: css-port```

## 2. 关联文档

| 文档 | 路径 | 状态 |
|---|---|---|
| 需求 PRD | `requirement.md` | 已有 |
| 用户故事 | `user-stories.md` | 已补齐 |
| 业务流程 | `business-flow.md` | 已补齐 |
| 验收标准 | `acceptance.md` | 已补齐 |
| 列表原型 PNG | `prototype/web/user-management-list.png` | 已有 |
| 列表原型 HTML | `prototype/web/user-management-list.html` | 已有 |
| 列表原型说明 | `prototype/web/user-management-list-context.md` | 已有 |
| 弹窗原型 PNG | `prototype/web/user-management-modal.png` | 已有 |
| 弹窗原型 HTML | `prototype/web/user-management-modal.html` | 已有 |
| 弹窗原型说明 | `prototype/web/user-management-modal-context.md` | 已有 |

## 3. 实现追踪（当前代码基线）

| 模块 | 路径 | 现状 |
|---|---|---|
| 导航占位 | `src/web/src/features/admin/data/admin-nav.ts` | 「用户管理」无 `path` |
| 用户 ORM | `src/backend/app/models/user.py` | 无头像、无 `deleted` 状态 |
| 认证 Spec | `openspec/specs/auth/spec.md` | 无用户管理 CRUD API |
| 管理端布局 | `src/web/src/pages/admin/AdminLayout.tsx` | REQ-0004 已实现 Sidebar |
| 用户管理页 | `src/web/src/pages/admin/UserManagementPage.tsx` | **已实现** |
| 用户管理 API | `src/backend/app/api/v1/admin_users.py` | **已实现** |

## 4. 与现有数据模型差异（实现前须定稿）

| 维度 | PRD（REQ-0005） | 当前后端 |
|---|---|---|
| 角色文案 | 前台用户 / 后台运营 / 后台管理员 | `store_owner` / `employee` / `admin` |
| 状态 | 正常 / 已冻结 / 已删除 | `active` / `disabled` |
| 昵称 | 可为空，最多 32 字符 | `display_name` NOT NULL |
| 用户名 | 4–32 位 + 格式规则 | 无专门校验（仅 UNIQUE） |
| 头像 | 支持上传 | 无字段 |

## 5. 视觉验收 Trace Checklist

- [ ] Sidebar 激活「用户管理」
- [ ] 筛选区 6 列网格（桌面）
- [ ] 4 指标卡与首页 metric-card 一致
- [ ] 表格与首页最近更新表格风格一致
- [ ] 弹窗单列、字段顺序固定
- [ ] list.png / modal.png 并排验收

## 6. 变更记录

| 日期 | 动作 | 说明 |
|---|---|---|
| 2026-06-15 | 需求入库 | requirement + prototype |
| 2026-06-15 | `/requirement-to-change` | 补齐 user-stories / business-flow / acceptance / trace（不含 OpenSpec） |
| 2026-06-15 | 文档一致性修订 | REQ-0005 标题、用户名 4–32 位、prototype context 引用对齐 |
| 2026-06-15 | 纳入 sprint-002 | 更新 `iterations/archive/sprint-002/` 四件套与本 trace |
| 2026-06-15 | `/requirement-to-opsx` | 创建 `add-user-management` OpenSpec（CSS Port） |
| 2026-06-15 | 子需求入库 | `REQ-0005-user-management-list-refine` 列表页六项 UI 优化 |
| 2026-06-20 | opsx-archive | `add-user-management` 归档；spec 写入 `openspec/specs/user-management/` |

## 7. 后续动作

1. **`/opsx-apply add-user-management`** 实现代码与测试。
2. PNG 并排验收，更新 `trace.md` checklist。
3. Sprint 002 结束前 **`/opsx-archive add-user-management`**。

## 关联缺陷

| BUG | 严重等级 | 状态 | 关联 Change | 说明 |
|---|---|---|---|---|
| BUG-0017-user-reset-password-confirm-ui-inconsistency | medium | done | fix-user-reset-password-confirm-ui | 用户重置密码二次确认弹窗与类目启用停用确认弹窗 UI 不一致 |
| BUG-0019-user-modal-avatar-upload-display | high | done | fix-user-modal-avatar-upload-display | 用户弹窗与列表头像上传后未回显且更换功能未生效 |
