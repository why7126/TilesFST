---
title: 需求验收标准
purpose: REQ-0007 瓷砖类目管理页 UI 优化验收标准
content: 基于 requirement.md 与 prototype/web/tile-category-management-list-refine-context.md
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: approved
note: REQ-0007-tile-category-management-refine
---

# 验收标准

## 1. 启停二次确认（O-01 / FR-001）

- [ ] **AC-001** 点击「停用」时 MUST NOT 直接调用 disable API；须先展示确认弹窗。
- [ ] **AC-002** 点击「启用」时 MUST NOT 直接调用 enable API；须先展示确认弹窗。
- [ ] **AC-003** 停用确认弹窗标题为「停用类目」；正文含类目名称及停用影响说明。
- [ ] **AC-004** 启用确认弹窗标题为「启用类目」；正文含类目名称。
- [ ] **AC-005** 弹窗底部含「取消」与「确认停用」/「确认启用」；主按钮触发 API。
- [ ] **AC-006** 取消、点击遮罩或关闭按钮时弹窗关闭，类目状态不变。
- [ ] **AC-007** 确认成功后 Toast「类目已停用」/「类目已启用」，类目树与列表刷新。
- [ ] **AC-008** 启停确认弹窗视觉结构对齐现有「删除类目」确认框（modal-backdrop / modal-card）。
- [ ] **AC-009** 删除确认流程独立，不受启停确认影响。

## 2. 检索区标题（O-02 / FR-002）

- [ ] **AC-010** 页面不展示「类目检索」section 标题。
- [ ] **AC-011** 页面不展示「按名称、状态与层级筛选」副标题。
- [ ] **AC-012** 筛选区仍含：类目名称/编码、状态、层级、查询、重置；交互不变。

## 3. 列表区标题（O-03 / FR-003）

- [ ] **AC-013** 页面不展示「类目列表」section 标题。
- [ ] **AC-014** 页面不展示「删除仅支持 SKU 数量为 0 的类目」外层副标题。
- [ ] **AC-015** 表格工具栏保留：左侧树上下文标题 +「共 {total} 条记录」；右侧「调整排序」。
- [ ] **AC-016** 类目树 280px、表格列、编辑/启停/删除规则与 REQ-0005 + BUG-0001 修复后一致。

## 4. 分页区（O-04 / FR-004）

- [ ] **AC-017** 分页左侧文案为「共 {total} 个类目」，total 与当前筛选结果一致。
- [ ] **AC-018** 分页右侧含页码控件（上一页、当前页、下一页）与「每页显示」+ 条数选择。
- [ ] **AC-019** 条数选项为「10 条」「20 条」「50 条」（非「10 条/页」格式）。
- [ ] **AC-020** 分页区不展示「当前显示 x-y / N 条」「x-y / N」等旧文案。
- [ ] **AC-021** 分页 DOM 结构对齐 `UserManagementPage`（`.pagination` / `.page-summary` / `.page-right` 或等价）。
- [ ] **AC-022** 切换 10/20/50 条后 page 重置为 1，列表与 total 正确。

## 5. 回归与不回归

- [ ] **AC-023** 4 指标卡、page-hero、新增类目、CategoryFormModal 无回归。
- [ ] **AC-024** 停用 + SKU=0 行仍展示「启用」与「删除」（BUG-0001 不回归）。
- [ ] **AC-025** `admin` / `employee` 可访问；未登录跳转登录页。
- [ ] **AC-026** 无 API / OpenAPI / Orval 变更。

## 6. 自动化与构建

- [ ] **AC-027** vitest：启停点击先出确认弹窗；确认后 mock API 被调用。
- [ ] **AC-028** vitest：分页区含「共 N 个类目」；不含「当前显示」。
- [ ] **AC-029** `cd src/web && npm run build` 通过。

## 7. 视觉与流程

- [ ] **AC-030** 1280×1024 与 `tile-category-management-list-refine-context.md` 并排验收。
- [ ] **AC-031** 变更经 OpenSpec `fix-tile-category-management-refine` 进入开发并 archive。
- [ ] **AC-032** 样式使用 semantic token / CSS Port，TSX 无裸 Hex。
