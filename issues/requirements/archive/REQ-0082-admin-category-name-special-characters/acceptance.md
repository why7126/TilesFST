---
requirement_id: REQ-0082-admin-category-name-special-characters
title: 管理后台瓷砖类目名称允许特殊字符 - Acceptance
status: done
created_at: 2026-07-30 22:14:37
updated_at: 2026-07-31 00:02:57
---

# Acceptance

## 功能 AC

- [ ] AC-001 管理后台新增类目弹窗中，类目名称允许输入中文、英文、数字和常见可见特殊字符，且最多 15 个用户可见字符。
- [ ] AC-002 管理后台编辑类目弹窗中，类目名称使用与新增弹窗一致的校验规则。
- [ ] AC-003 合法样例 `岩板-大规格`、`仿古砖/客厅`、`600x1200(亮面)`、`A+B#系列` 可创建和更新成功。
- [ ] AC-004 超过 15 个字符的类目名称在前端保存前被拦截，错误提示为 `类目名称最多 15 个字符` 或等价产品确认文案。
- [ ] AC-005 trim 后为空的类目名称被前端和后端拒绝，并沿用既有空名称错误提示。
- [ ] AC-006 换行、制表符、不可见控制字符被前端和后端拒绝，错误提示定位到类目名称字段。
- [ ] AC-007 创建 / 更新类目 API 服务端接受合法特殊字符名称，并继续校验鉴权、同层级唯一和统一 response envelope。
- [ ] AC-008 创建 / 更新类目 API 服务端拒绝非法名称时返回稳定业务错误；如新增错误码，错误码文档、OpenAPI 和测试同步更新。
- [ ] AC-009 API Schema、OpenAPI 字段描述、Orval 生成类型和测试夹具中不得保留“只能包含中文、英文和数字”的有效约束。
- [ ] AC-010 管理端类目列表、类目树、SKU 类目选择器和筛选控件展示特殊字符名称时不重叠、不撑破容器，搜索和选择可用。
- [ ] AC-010A 管理端类目树默认仅显示一级类目；有子级类目前置 `+/-` 控件可展开 / 收起，子级默认收起，点击 `+/-` 不触发类目筛选。
- [ ] AC-011 小程序分类页或 Web 展示端如展示类目名称，合法特殊字符名称不导致布局异常；可沿用既有截断 / tooltip 策略。
- [ ] AC-012 如果数据库字段、CHECK 约束、索引或触发器限制为旧字符集，OpenSpec Change 必须包含 SQLite / MySQL 迁移方案与回滚说明；如果无需迁移，实现说明需记录原因。
- [ ] AC-013 后端测试覆盖特殊字符名称可创建 / 可更新，以及 16 字符名称、控制字符名称被拒绝。
- [ ] AC-014 前端表单测试覆盖特殊字符名称可保存、16 字符名称显示错误、保存失败时弹窗保持打开。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md` — 预防 Sprint 002/003 复发类缺陷。

- [ ] AC-XCUT-001 类目列表如因本需求调整列表展示或回归用例，分页 DOM MUST 与用户管理基准一致：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [ ] AC-XCUT-002 类目列表操作成功 / 失败反馈 MUST 使用 fixed toast，不得使用会推挤 hero、筛选区或表格的文档流 notice。
- [ ] AC-XCUT-003 本需求若涉及启停、删除等状态变更回归，MUST 使用 Design System confirm modal；N/A 时需在实现说明中注明本需求未新增状态变更操作。
- [ ] AC-XCUT-004 管理端代码中不得新增 `window.confirm`；现有类目页相关操作如被触达修改，需确认无 `window.confirm` 回归。
- [ ] AC-XCUT-005 类目新增 / 编辑弹窗 TSX className 不得同时挂载通用 `modal-card` 与业务专属 modal 类；若未改弹窗容器，也需通过代码检查确认无双类回归。
- [ ] AC-XCUT-006 在 1440px 视口验收类目新增 / 编辑弹窗 computed width 与既有类目弹窗设计一致，不得被全局 `.modal-card` 520px 规则意外覆盖。
- [ ] AC-XCUT-007 在矮视口场景验收类目新增 / 编辑弹窗 body 可滚动，字段错误提示和底部操作按钮可访问。

## 验收证据建议

- 后端：pytest 覆盖创建 / 更新类目名称特殊字符、16 字符、控制字符。
- 前端：Vitest / Testing Library 覆盖表单校验与错误提示。
- 契约：OpenAPI diff、Orval 生成结果或说明无生成物变化。
- UI：1440x1024 与移动窄宽截图，覆盖列表、弹窗、类目树或选择器；类目树需覆盖默认折叠、`+/-` 展开 / 收起和点击分离。
