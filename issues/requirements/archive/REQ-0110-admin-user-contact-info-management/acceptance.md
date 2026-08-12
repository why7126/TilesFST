---
title: 需求验收标准
purpose: 定义用户管理页维护联系邮箱和手机号码的功能、接口、数据、UI 与横切验收标准
content: 基于 requirement.md 与 knowledge-base best-practices 补齐
source: REQ-0110 requirement.md
update_method: 需求范围、原型或横切最佳实践变化时同步更新
owner: product
acceptance_status: passed
created_at: 2026-08-11 22:09:55
updated_at: 2026-08-12 00:15:15
---

# 验收标准

## 1. 功能验收

- [ ] **AC-001** 添加用户弹窗展示「联系邮箱」「手机号码」字段，字段顺序为用户名、头像、昵称、联系邮箱、手机号码、角色。
- [ ] **AC-002** 编辑用户弹窗回填当前 `email`、`phone`，并允许修改。
- [ ] **AC-003** 管理员清空联系邮箱或手机号码并保存后，再次打开编辑弹窗时对应字段为空。
- [ ] **AC-004** 邮箱和手机号允许为空，不作为必填项阻断创建或编辑。
- [ ] **AC-005** 邮箱和手机号允许与其他用户重复；系统不做唯一性冲突提示。
- [ ] **AC-006** 邮箱和手机号仅作为联系信息，不影响登录、重置密码、角色、状态或权限判断。

## 2. 校验验收

- [ ] **AC-007** 邮箱非空时执行邮箱格式校验；非法邮箱返回统一业务错误并在前端表单展示提示。
- [ ] **AC-008** 手机号非空时仅允许数字、空格、`+`、`-`；包含其他字符时返回统一业务错误并在前端表单展示提示。
- [ ] **AC-009** 邮箱、手机号保存前裁剪前后空白；空白字符串保存为空值。
- [ ] **AC-010** 手机号校验不绑定中国大陆或其他单一国家/地区格式。

## 3. 接口验收

| 接口 | 验收 |
|---|---|
| `POST /api/v1/admin/users` | 接收可选 `email`、`phone`，创建成功后返回用户对象包含保存后的值 |
| `PATCH /api/v1/admin/users/{id}` | 接收可选 `email`、`phone`，支持修改和清空 |
| `GET /api/v1/admin/users` | 列表项返回 `email`、`phone` |
| `GET /api/v1/admin/users/{id}` | 详情返回 `email`、`phone` |

- [ ] **AC-011** 上述管理端用户 API 仅 `role=admin` 可调用；非管理员仍返回 403。
- [ ] **AC-012** API 变更后同步 OpenAPI 与 Orval，前端调用类型包含 `email`、`phone`。
- [ ] **AC-013** 错误响应遵守统一响应结构，不返回 FastAPI 默认 `detail` 作为主错误体。

## 4. 列表与搜索验收

- [ ] **AC-014** 用户管理列表表头顺序为：用户、角色、状态、联系邮箱、手机号码、最后登录、创建时间、操作。
- [ ] **AC-015** 联系邮箱和手机号码作为独立列展示在「状态」列之后；不得塞入用户列第二行或操作列提示。
- [ ] **AC-016** 联系邮箱为空时显示 `-`；手机号码为空时显示 `-`。
- [ ] **AC-017** 搜索 placeholder 或帮助文案表达可搜索用户名、昵称、邮箱、手机号。
- [ ] **AC-018** 关键词搜索命中 `username`、`display_name`、`email`、`phone`。
- [ ] **AC-019** 搜索邮箱或手机号后，分页、角色筛选、状态筛选、登录情况筛选语义保持不变。
- [ ] **AC-019A** 用户管理列表「创建时间」按 `yyyy-mm-dd hh:MM` 分钟级格式展示。

## 5. UI / 视觉验收

- [ ] **AC-020** 弹窗沿用用户管理页既有窄弹窗风格，新增字段在 1440px 和移动窄屏下不溢出。
- [ ] **AC-020A** 用户新增/编辑弹窗标题区紧凑展示，标题上方不得出现过大空隙。
- [ ] **AC-020B** 用户新增/编辑弹窗整体靠近视口顶部展示，弹窗顶部与视口顶部不得出现过大空隙。
- [ ] **AC-021** 字段级错误提示显示在对应字段或字段组附近，不仅依赖全局 Toast。
- [ ] **AC-022** 列表新增两列后，用户、角色、状态、最后登录、创建时间与操作列不被遮挡；窄屏沿用既有横向滚动策略。
- [ ] **AC-023** TSX/CSS 新增样式使用 semantic token 或既有 CSS 变量，不新增裸 Hex。

## 6. 测试验收

- [ ] **AC-024** 后端测试覆盖创建用户保存邮箱和手机号。
- [ ] **AC-025** 后端测试覆盖编辑用户修改、清空邮箱和手机号。
- [ ] **AC-026** 后端测试覆盖邮箱非法、手机号非法错误。
- [ ] **AC-027** 后端测试覆盖关键词搜索命中邮箱和手机号。
- [ ] **AC-028** 前端测试覆盖添加/编辑弹窗字段展示、回填、提交 payload 和清空提交。
- [ ] **AC-029** 前端测试覆盖列表新增独立列、列顺序、空值 `-` 展示和搜索 placeholder 更新。

## 7. 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] **AC-XCUT-001** 用户管理列表分页 DOM 仍与 `/admin/users` 基准一致：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [ ] **AC-XCUT-002** 操作成功/失败反馈使用 fixed toast，不因提示信息引起 hero、筛选区或表格纵向位移。
- [ ] **AC-XCUT-003** 冻结、解冻、删除、重置密码等状态/危险操作仍使用 DS confirm modal；不得新增或回退到 `window.confirm`。
- [ ] **AC-XCUT-004** 本需求不新增筛选下拉；若实现时调整筛选控件，必须复用 `AdminFilterSelect` 或等价 shared wrapper，并覆盖 open/select/clear/reset 与 query 语义测试。
- [ ] **AC-XCUT-005** 用户弹窗 TSX 不得同时挂载通用 `modal-card` 与新的专属弹窗类；如沿用既有窄弹窗，仅保持既有单一宽度来源。
- [ ] **AC-XCUT-006** 1440px 视口验收弹窗 Computed width 与设计/既有用户弹窗一致；不得被其他管理端 CSS 层叠覆盖。
- [ ] **AC-XCUT-007** 矮视口下弹窗 body 可滚动，新增邮箱/手机号字段不得导致底部操作按钮不可达。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: update-admin-user-contact-info-management
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

