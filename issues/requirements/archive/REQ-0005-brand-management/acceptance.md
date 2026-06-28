---
title: 需求验收标准
purpose: 瓷砖品牌管理功能、接口、数据、UI 与异常场景验收
content: 基于 requirement.md 与 prototype/web/brand-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005-brand-management
---

# 验收标准

## 1. 功能验收

### 1.1 访问与布局

- [ ] **AC-001** 已登录且具备品牌管理权限的用户可访问品牌管理页，页面标题为「瓷砖品牌」。
- [ ] **AC-002** Sidebar OPERATIONS 下「瓷砖品牌」为激活态；继承 `AdminLayout`：264px Sidebar、右侧独立滚动、内容区最大宽度 1080px。
- [ ] **AC-003** 页面头部含 eyebrow「MASTER DATA」、说明文案、主按钮「＋ 新增品牌」。
- [ ] **AC-004** 页面不出现导出按钮、批量操作入口、「品牌列表」「品牌检索」标题行。

### 1.2 数据概览

- [ ] **AC-005** 展示 4 个指标卡：品牌总数、启用品牌、停用品牌、未关联 SKU。
- [ ] **AC-006** 指标卡视觉与 admin-home / 用户管理 metric-card 一致（暗色卡片、品牌金数值）。

### 1.3 搜索与筛选

- [ ] **AC-007** 筛选区仅一行：关键词输入框、状态下拉（全部/启用/停用）、查询、重置。
- [ ] **AC-008** 关键词匹配品牌名称、品牌简称、英文名称（模糊）。
- [ ] **AC-009** 点击查询或回车触发搜索，页码重置为 1；重置清空条件并重新加载。

### 1.4 品牌列表

- [ ] **AC-010** 表格列：品牌（Logo+名称）、品牌简称、英文名称、排序、SKU 数量、状态、更新时间、操作。
- [ ] **AC-011** 无 Logo 时显示品牌首字母占位；状态展示启用/停用徽章。
- [ ] **AC-012** 操作列固定为：编辑、启用/停用、删除（无其他操作）。

### 1.5 删除规则

- [ ] **AC-013** 仅当 SKU 数量 = 0 且状态 = 停用时，删除可点击（风险色）。
- [ ] **AC-014** 其余情况删除置灰，`cursor: not-allowed`，hover 提示：`仅允许删除未关联SKU且已停用的品牌`。
- [ ] **AC-015** 可删除时点击弹出确认框，标题「删除品牌」，按钮「取消」「删除品牌」。
- [ ] **AC-016** 服务端拒绝非法删除时返回 `BRAND_DELETE_FORBIDDEN`。

### 1.6 分页

- [ ] **AC-017** 分页左侧：共 N 条、上一页、页码、下一页。
- [ ] **AC-018** 分页右侧：跳至页码输入、每页显示下拉（20 / 50 / 100）。
- [ ] **AC-019** 切换每页显示数后页码重置为 1，保留筛选条件。

### 1.7 新增 / 编辑弹窗

- [ ] **AC-020** 弹窗宽 720px，`max-height: calc(100vh - 96px)`；头部与底部固定，主体可滚动。
- [ ] **AC-021** 字段顺序：第一行品牌名称+排序；第二行简称+英文名；第三行 Logo；第四行介绍（与 Logo 同宽通栏）。
- [ ] **AC-022** 品牌名称、品牌排序必填；排序仅允许正整数（非 0、负、小数）。
- [ ] **AC-023** 品牌名称唯一；重复时文案「品牌名称已存在，请更换」；服务端 `BRAND_NAME_DUPLICATED`。
- [ ] **AC-024** 弹窗不出现：状态字段、创建默认状态提示、字段规则说明区块、国家/地区。
- [ ] **AC-025** Logo 上传支持 JPG/PNG/WebP；品牌介绍最多 500 字。
- [ ] **AC-026** 新增成功默认状态为启用（不在 UI 提示）；编辑成功 Toast 并刷新列表。

## 2. 接口验收

| 接口（建议路径） | 说明 |
|---|---|
| `GET /api/v1/admin/brands` | 分页列表 + keyword + status + summary |
| `POST /api/v1/admin/brands` | 创建，默认 ENABLED |
| `GET /api/v1/admin/brands/{id}` | 详情（编辑回填） |
| `PUT /api/v1/admin/brands/{id}` | 更新品牌 |
| `POST /api/v1/admin/brands/{id}/enable` | 启用 |
| `POST /api/v1/admin/brands/{id}/disable` | 停用 |
| `DELETE /api/v1/admin/brands/{id}` | 条件删除 |

- [ ] **AC-027** API 路径与 `rules/api.md` 一致（`/api/v1/admin/...`）。
- [ ] **AC-028** 变更后执行 OpenAPI 导出与 Orval 生成前端客户端。
- [ ] **AC-029** 权限点覆盖：brand:list/create/update/enable/disable/delete。

## 3. 数据验收

- [ ] **AC-030** 新增 `brands` 表（或等价）：name UNIQUE、sort_order、short_name、english_name、logo_object_key、description、status、sku_count（或关联统计）、created_at、updated_at。
- [ ] **AC-031** Logo 存 MinIO，经后端授权；禁止前端直连未授权存储。
- [ ] **AC-032** 删除策略在实现阶段定稿（物理删除 vs 软删除），须满足 AC-013 ~ AC-016。

## 4. 技术验收

- [ ] **AC-033** 实现策略建议 CSS Port（对齐 `add-admin-home` / 用户管理），semantic token，TSX 无裸 Hex。
- [ ] **AC-034** 复用 `AdminLayout`、`AdminSidebar`、分页组件模式与用户管理页一致。
- [ ] **AC-035** 单元/组件测试：删除按钮禁用逻辑、弹窗字段顺序、名称/排序校验。
- [ ] **AC-036** 集成测试：CRUD、enable/disable、非法删除、名称重复。

## 5. 视觉验收 Trace

原型优先级：

```text
1. prototype/web/brand-management.html
2. prototype/web/brand-management.png（待补齐 Golden Reference）
3. prototype/web/brand-management-modal.html
4. prototype/web/brand-management-modal.png（待补齐）
5. prototype/web/*-context.md
6. acceptance.md（本文件）
7. rules/ui-design.md
```

- [ ] **AC-037** 列表页与 HTML 原型并排：指标卡、筛选、表格、分页（含每页显示数）。
- [ ] **AC-038** 弹窗与 modal HTML 并排：字段网格、上传区、介绍通栏、固定头尾。
- [ ] **AC-039** `/design-system` 管理端分区可预览品牌管理相关组件（若新增）。

## 6. 不在本期

- 导出、批量操作、国家/地区、品牌合并、多语言、SEO、前台品牌预览。
