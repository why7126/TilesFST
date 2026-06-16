---
title: 业务流程
purpose: 瓷砖类目管理列表、类目树、弹窗与删除主流程
content: 基于 requirement.md 与 prototype/web/tile-category-management-* 提炼
source: AI 根据 PRD 与原型生成，项目团队确认
update_method: PRD 或原型变更时同步更新
owner: product
status: draft
note: REQ-0005-tile-category-management
---

# 业务流程

## 1. 流程总览

```text
后台用户登录（admin / employee）
  ↓
进入 /admin/tile-categories
  ↓
浏览数据概览 + 类目树 + 列表
  ↓
可选：检索（名称/编码、状态、层级）
  ↓
可选操作：
  ├─ 点击类目树节点 → 列表过滤为节点及子级
  ├─ 新增类目 → 弹窗 → POST → Toast + 刷新树/列表/概览
  ├─ 编辑类目 → 弹窗 → PUT → Toast + 刷新
  ├─ 启用 / 停用 → POST enable/disable → Toast
  ├─ 删除（仅 SKU=0 且停用）→ 确认 → DELETE → Toast
  └─ 调整排序 → （本期占位或 reorder API）
```

## 2. 访问与权限流程

```text
用户携带 JWT 访问 /admin/tile-categories
  ↓
ProtectedRoute：已登录？
  ├─ 否 → /admin/login
  └─ 是 → 具备 category:list？
        ├─ 否 → 403 或重定向 /admin/dashboard
        └─ 是 → 渲染 TileCategoryManagementPage
```

### 2.1 角色与菜单

| 产品角色 | 后端 role（建议） | 类目管理菜单 | 说明 |
|---|---|---|---|
| 后台运营 | `employee` | OPERATIONS > 瓷砖类目 | 日常类目维护 |
| 后台管理员 | `admin` | 同上 | 全量类目操作 |
| 前台用户 | `store_owner` | 不可见 | 不允许进入管理端 |

## 3. 页面加载流程

```text
页面加载
  ↓
并行或串行请求：
  GET /api/v1/admin/tile-categories/tree
  GET /api/v1/admin/tile-categories?page=1&page_size=10&...
  ↓
响应含 summary（类目总数/启用/绑定SKU/最大层级）
  ↓
渲染 page-header + metric-grid + filter + tree + table + pager
```

## 4. 类目树联动流程

```text
默认选中「全部类目」
  ↓
列表展示全部（或分页后的根级+平铺，与 API 设计一致）
  ↓
用户点击树节点 N
  ↓
列表请求带 parent_id=N（或前端过滤子树）
  ↓
工具栏标题更新为节点名称 + 记录数
  ↓
树节点高亮 active 态
```

## 5. 搜索与重置流程

```text
用户输入关键词 / 选择状态 / 选择层级
  ↓
点击「查询」或回车
  ↓
page 重置为 1，带 query 重新请求
  ↓
点击「重置」
  ↓
清空关键词；状态=全部；层级=全部；树节点可恢复「全部类目」
  ↓
重新请求默认列表
```

## 6. 新增类目流程

```text
点击「＋ 新增类目」
  ↓
打开弹窗（560px，单列字段）
  ↓
填写：上级类目、名称*、编码*、排序*、描述、状态
  ↓
客户端校验：
  - 名称非空、1-30 字
  - 编码非空、格式建议 CAT-XXXX
  - 排序正整数
  - 上级为三级 → 拦截
  ↓
POST /api/v1/admin/tile-categories
  ↓
成功：
  ├─ Toast「类目已创建」
  ├─ 关闭弹窗
  └─ 刷新树、列表、概览
失败：CATEGORY_CODE_DUPLICATED、CATEGORY_MAX_DEPTH_EXCEEDED 等
```

## 7. 编辑类目流程

```text
列表点击「编辑」
  ↓
打开弹窗，回填字段（上级类目在编辑时是否可改由 design 定稿）
  ↓
PUT /api/v1/admin/tile-categories/{id}
  ↓
成功 → Toast「类目已更新」→ 刷新树、列表、概览
```

## 8. 启用 / 停用流程

```text
点击「停用」或「启用」
  ↓
（可选）确认
  ↓
POST .../disable 或 .../enable
  ↓
成功 → Toast → 刷新列表、树节点 SKU 数、概览
  ↓
停用后前台（未来）不展示该类目及其子级策略由产品定稿
```

## 9. 删除流程

```text
渲染操作列时计算：
  canDelete = (sku_count === 0 AND status === DISABLED)
  ↓
canDelete = false → 不展示删除（原型：启用行仅「编辑」「停用」）
  ↓
canDelete = true → 展示「删除」
  ↓
确认弹窗：标题「删除类目」
  ↓
DELETE /api/v1/admin/tile-categories/{id}
  ↓
服务端二次校验 sku_count 与 status
  ├─ 通过 → 删除 → Toast → 刷新树与列表
  └─ 拒绝 → CATEGORY_DELETE_FORBIDDEN
```

## 10. 调整排序流程（可选本期）

```text
点击「调整排序」
  ↓
方案 A（占位）：Toast「排序调整功能即将上线」
方案 B（实现）：打开排序面板或行内编辑 sort_order → POST reorder
```

## 11. 与现有能力的衔接

| 依赖 | 说明 |
|---|---|
| REQ-0004-admin-home | `AdminLayout`、Sidebar 264px、metric-card、表格与分页 |
| REQ-0005-user-management | 分页、每页显示数交互可参考 |
| REQ-0005-brand-management | 删除规则矩阵、弹窗模式可参考 |
| `tile_categories` 表 | 当前 schema 仅桩字段，需扩展 parent_id、code、level 等 |
| tiles / SKU | `sku_count` 可先子查询或占位 0 |

## 12. 异常流程

| 场景 | 期望行为 |
|---|---|
| 非授权角色访问 API | HTTP 403 |
| 类目编码重复 | HTTP 409，`CATEGORY_CODE_DUPLICATED` |
| 非法删除 | HTTP 409/422，`CATEGORY_DELETE_FORBIDDEN` |
| 超过三级层级 | HTTP 422，`CATEGORY_MAX_DEPTH_EXCEEDED` |
| 排序非正整数 | 前端拦截 + 后端校验 |
| 网络错误 | Toast，保留树选中与筛选条件 |
