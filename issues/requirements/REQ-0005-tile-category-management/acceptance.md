---
title: 需求验收标准
purpose: 瓷砖类目管理功能、接口、数据、UI 与异常场景验收
content: 基于 requirement.md 与 prototype/web/tile-category-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005-tile-category-management
---

# 验收标准

## 1. 功能验收

### 1.1 访问与布局

- [ ] **AC-001** 已登录且具备类目管理权限的用户可访问类目管理页，页面标题为「瓷砖类目管理」。
- [ ] **AC-002** Sidebar OPERATIONS 下「瓷砖类目」为激活态；继承 `AdminLayout`：264px Sidebar、右侧独立滚动、内容区最大宽度 1080px。
- [ ] **AC-003** 页面头部含眉标 `CATEGORY MANAGEMENT`、说明文案、主按钮「＋ 新增类目」。
- [ ] **AC-004** 页面不出现导出按钮、批量操作入口或任何导出入口。

### 1.2 数据概览

- [ ] **AC-005** 展示 4 个指标卡：类目总数、启用类目、绑定 SKU、最大层级（值为 3）。
- [ ] **AC-006** 指标卡视觉与 admin-home / 用户管理 metric-card 一致（暗色卡片、品牌金数值）。

### 1.3 类目检索

- [ ] **AC-007** 筛选区含：类目名称/编码输入、状态下拉（全部/启用/停用）、层级下拉（全部/一/二/三级）、查询、重置。
- [ ] **AC-008** 关键词模糊匹配类目名称、英文名或编码。
- [ ] **AC-009** 点击查询或回车触发搜索，页码重置为 1；重置恢复全部状态与全部层级并清空关键词。

### 1.4 类目树

- [ ] **AC-010** 左侧类目树宽 280px，展示「全部类目」根节点与各层级缩进节点。
- [ ] **AC-011** 树节点右侧展示 SKU 数量；选中节点高亮（品牌金背景）。
- [ ] **AC-012** 点击树节点后，右侧列表展示该节点及其子级类目；工具栏标题与记录数同步更新。

### 1.5 类目列表

- [ ] **AC-013** 表格列：类目名称（含路径副行）、层级、排序、SKU 数量、状态、更新时间、操作。
- [ ] **AC-014** 列表工具栏仅有「调整排序」；不得出现「导出」。
- [ ] **AC-015** 操作列：编辑、启用/停用；删除按 §1.6 规则展示。

### 1.6 删除规则

- [ ] **AC-016** 仅当 SKU 数量 = 0 且状态 = 停用时，展示可点击删除（风险色）。
- [ ] **AC-017** 有 SKU 绑定或启用状态的类目行不展示删除入口（与 HTML 原型一致）。
- [ ] **AC-018** 可删除时点击弹出确认框，标题「删除类目」，按钮「取消」「删除类目」。
- [ ] **AC-019** 服务端拒绝非法删除时返回 `CATEGORY_DELETE_FORBIDDEN`。

### 1.7 分页

- [ ] **AC-020** 分页左侧展示「当前显示 x-y / N 条」。
- [ ] **AC-021** 分页右侧含页码与每页显示下拉（10 / 20 / 50）。
- [ ] **AC-022** 切换每页显示数后页码重置为 1，保留筛选与树选中条件（若适用）。

### 1.8 新增 / 编辑弹窗

- [ ] **AC-023** 弹窗宽 560px，居中；遮罩暗色半透明 + blur。
- [ ] **AC-024** 字段顺序（一行一个）：上级类目、类目名称、类目编码、排序权重、类目描述、状态。
- [ ] **AC-025** 类目名称、类目编码、排序权重必填；名称 1–30 字；描述最多 200 字。
- [ ] **AC-026** 排序权重仅允许正整数；类目编码唯一，重复文案「类目编码已存在，请更换」；服务端 `CATEGORY_CODE_DUPLICATED`。
- [ ] **AC-027** 上级类目为空时创建一级类目；选择三级类目作为上级时禁止新增子级。
- [ ] **AC-028** 状态默认启用；保存成功后关闭弹窗并刷新类目树、列表与数据概览。

### 1.9 层级约束

- [ ] **AC-029** 系统最多支持三级类目；树与列表层级徽章正确展示一级/二级/三级。
- [ ] **AC-030** 违反最大层级时服务端返回 `CATEGORY_MAX_DEPTH_EXCEEDED`（或等价错误码）。

## 2. 接口验收

| 接口（建议路径） | 说明 |
|---|---|
| `GET /api/v1/admin/tile-categories` | 分页列表 + keyword + status + level + parent_id + summary |
| `GET /api/v1/admin/tile-categories/tree` | 类目树 + sku_count |
| `POST /api/v1/admin/tile-categories` | 创建类目 |
| `PUT /api/v1/admin/tile-categories/{id}` | 更新类目 |
| `POST /api/v1/admin/tile-categories/{id}/enable` | 启用 |
| `POST /api/v1/admin/tile-categories/{id}/disable` | 停用 |
| `DELETE /api/v1/admin/tile-categories/{id}` | 条件删除 |

- [ ] **AC-031** API 路径与 `rules/api.md` 一致（`/api/v1/admin/...`）。
- [ ] **AC-032** 变更后执行 OpenAPI 导出与 Orval 生成前端客户端。
- [ ] **AC-033** 权限点覆盖：category:list/create/update/enable/disable/delete。

## 3. 数据验收

- [ ] **AC-034** 扩展 `tile_categories` 表：parent_id、code UNIQUE、sort_order、level、description、status、sku_count（或关联统计）、path、created_at、updated_at。
- [ ] **AC-035** 删除策略在实现阶段定稿（物理删除 vs 软删除），须满足 AC-016 ~ AC-019。
- [ ] **AC-036** 类目树 parent_id 自引用完整，无环；迁移脚本可回滚或幂等。

## 4. 技术验收

- [ ] **AC-037** 实现策略建议 CSS Port（对齐 admin-home / 用户管理 / 品牌管理），semantic token，TSX 无裸 Hex。
- [ ] **AC-038** 复用 `AdminLayout`、`AdminSidebar`、分页组件模式。
- [ ] **AC-039** 单元/组件测试：删除展示逻辑、弹窗字段顺序、编码/排序校验、三级深度拦截。
- [ ] **AC-040** 集成测试：CRUD、tree、enable/disable、非法删除、编码重复、超深度创建。

## 5. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/tile-category-management.html
2. prototype/web/tile-category-management.png（待补齐 Golden Reference）
3. prototype/web/tile-category-management-add.html
4. prototype/web/tile-category-management-add.png（待补齐）
5. prototype/web/prototype-context-list.md
6. prototype/web/prototype-context-add.md
7. acceptance.md（本文件）
8. rules/ui-design.md
```

- [ ] **AC-041** 列表页与 HTML 原型并排：指标卡、检索、类目树+列表、工具栏仅「调整排序」、分页。
- [ ] **AC-042** 弹窗与 add HTML 并排：560px、单列字段、Switch 状态、固定头尾。
- [ ] **AC-043** `/design-system` 管理端分区可预览类目管理相关组件（若新增）。

## 6. 不在本期

- 导出、批量操作、四级类目、类目合并、多语言、前台目录预览。
- 「调整排序」若未实现交互，须占位且不阻塞其余 AC。
