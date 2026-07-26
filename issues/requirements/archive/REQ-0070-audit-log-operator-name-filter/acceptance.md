---
requirement_id: REQ-0070-audit-log-operator-name-filter
title: 日志审计页面操作者名称筛选 - 验收标准
status: done
owner: product
created_at: 2026-07-25 11:57:39
updated_at: 2026-07-26 11:42:52
knowledge_base_refs:
  - docs/knowledge-base/best-practices/admin-list-page-consistency.md
  - docs/knowledge-base/retrospectives/sprint-010-retrospective.md
cross_cutting_tags:
  - admin-list
---

# 验收标准

## 功能 AC

- [ ] AC-001 日志审计页面操作者筛选 MUST 从普通 User ID 输入框改为单选可搜索下拉。
- [ ] AC-002 下拉控件 MUST 支持按用户名称模糊搜索操作者候选。
- [ ] AC-003 下拉控件 SHOULD 同时支持按账号搜索操作者候选，便于名称为空或只知道账号时定位用户。
- [ ] AC-004 候选项 MUST 只展示两行：第一行账号 `username`，第二行用户名称 `display_name || username`。
- [ ] AC-005 同名用户 MUST 能通过账号行区分；候选项不展示角色或状态。
- [ ] AC-006 选择候选用户后，日志列表接口请求 MUST 使用候选用户 `id` 作为 `actor_user_id`。
- [ ] AC-007 前端 MUST NOT 将用户名称或账号字符串作为 `actor_user_id` 传给日志列表接口。
- [ ] AC-008 切换操作者筛选后，日志列表 MUST 回到第一页并重新查询。
- [ ] AC-009 操作者筛选必须能与日志类型、时间范围、状态、Task Trace ID、路径 / Request ID 等条件组合生效。
- [ ] AC-010 清空操作者筛选后，日志列表 MUST 按全部操作者重新查询。
- [ ] AC-011 页面“重置”按钮 MUST 清空操作者筛选，并恢复全部默认筛选条件。
- [ ] AC-012 控件收起且已选择用户时，MUST 显示用户名称或名称 + 账号，不展示裸 User ID。
- [ ] AC-013 候选搜索加载中 MUST 有可感知状态或禁用重复选择反馈。
- [ ] AC-014 搜索无匹配结果时，控件 MUST 显示无结果提示。
- [ ] AC-015 候选接口失败时，页面 MUST 显示候选加载失败反馈，且不影响其他日志筛选条件使用。
- [ ] AC-016 日志列表查询失败与用户候选查询失败 MUST 有可区分反馈。
- [ ] AC-017 操作者候选数据 MUST 复用系统管理员鉴权，不得暴露超出当前管理员可见范围的用户信息。
- [ ] AC-018 候选项不得展示密码、Token、内部绝对路径、敏感备注或其他非必要信息。
- [ ] AC-019 若复用 `GET /api/v1/admin/users`，实现 MUST 确认其支持 `keyword`、`page_size` 和系统管理员鉴权。
- [ ] AC-020 若新增或修改 API 字段，MUST 同步 OpenAPI、Orval、API 文档、错误码文档和后端/前端测试。
- [ ] AC-021 日志列表 API 现有 `actor_user_id` 查询参数 SHOULD 保持兼容，不破坏既有调用方和测试。
- [ ] AC-022 前端测试 MUST 覆盖下拉渲染、关键字搜索、选择用户、清空筛选、重置筛选和日志查询参数为 `actor_user_id`。
- [ ] AC-023 前端测试 SHOULD 覆盖无匹配结果、候选加载失败和同名用户辅助展示。
- [ ] AC-024 1440x1024 与移动端视口下，操作者下拉、筛选区和日志表格 MUST 不溢出、不遮挡、不引起布局跳动。
- [ ] AC-025 原型策略 MUST 至少提供日志审计筛选区 HTML/context；PNG Golden Reference 可在后续设计确认后导出。
- [ ] AC-026 时间范围筛选 MUST 只提供最近5分钟、最近10分钟、最近30分钟、最近1小时、最近3小时、最近6小时、最近12小时、最近1天、最近2天、最近3天、最近7天，并移除全部时间。
- [ ] AC-027 日志列表操作者列 MUST 显示账号 `actor_username`，不显示用户名称，并保持单行展示。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 管理端列表页一致性复发类缺陷。

- [ ] AC-XCUT-001 操作者筛选改造后，日志审计列表分页 DOM MUST 对齐用户管理基准：左侧 `.page-summary`，右侧 `.page-right` 页码 + 每页条数。
- [ ] AC-XCUT-002 日志审计摘要指标卡 DOM MUST 使用 `.metric-label` / `.metric-value` / `.metric-desc`，不得只复用外层 `metric-card` 后用裸 `strong` / `span` 承载数值与说明。
- [ ] AC-XCUT-003 候选加载失败、日志查询失败、复制 request_id 或其他操作反馈 MUST 使用 fixed toast 或等价固定层，不得造成 hero、筛选区或表格纵向位移。
- [ ] AC-XCUT-004 N/A — 本需求只优化筛选查询，不包含启停、冻结、上架/下架、删除、重置密码等危险状态变更；若后续新增危险操作，MUST 使用 DS confirm modal。
- [ ] AC-XCUT-005 日志审计页面实现 MUST 不调用 `window.confirm`；本期无确认操作时以静态检查或代码 review 说明 N/A。
