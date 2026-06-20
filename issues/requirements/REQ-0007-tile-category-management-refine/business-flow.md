---
title: 业务流程
purpose: 描述类目管理页 UI 优化后的启停、列表与分页交互流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
note: REQ-0007-tile-category-management-refine
---

# 业务流程

## 1. 与 REQ-0005 的差异

本需求 **仅修改** 下列流程节点；新增/编辑/删除/树联动/筛选 API 不变（见 `REQ-0005-tile-category-management/business-flow.md`）。

```text
变更前                              变更后
──────────────────────────────────────────────────────────────────
点击「启用/停用」→ 直接 API      →    弹出确认框 → 确认后 API
检索区 section-head「类目检索」   →    删除；filter-card 直接展示
列表区 section-head「类目列表」   →    删除；cat-work-grid 直接展示
分页「当前显示 x-y / N 条」       →    左「共 x 个类目」+ 右页码与每页条数
分页 select「10 条/页」           →    「10 条」（对齐用户管理 v2）
```

## 2. 启用 / 停用流程（优化后）

```text
用户点击行内「启用」或「停用」
  ↓
打开确认弹窗（标题：启用类目 / 停用类目）
  ├─ 取消 / 遮罩 / ×  → 关闭弹窗，状态不变
  └─ 确认启用 / 确认停用
        ↓
     POST .../enable 或 POST .../disable
        ↓
     Toast「类目已启用」/「类目已停用」
        ↓
     refreshAll()（树 + 列表 + summary）
```

### 2.1 与删除流程的关系

```text
删除：独立「删除类目」确认弹窗（不变）
启停：独立「启用/停用类目」确认弹窗（新增）
MUST NOT 合并为同一弹窗
```

## 3. 页面布局流程（优化后）

```text
page-hero（不变）
  ↓
4 指标卡（不变）
  ↓
filter-card（无 section-head）
  ↓
cat-work-grid
  ├─ CategoryTree 280px（不变）
  └─ table-card
       ├─ cat-table-toolbar（保留：树上下文 + 共 N 条记录 + 调整排序）
       ├─ 表格 + 行操作（编辑 / 启停 / 删除规则不变）
       └─ pagination v2（对齐 UserManagementPage）
```

## 4. 分页交互

```text
左侧展示 API total → 「共 {total} 个类目」
  ↓
右侧：‹ 页码 › + 「每页显示 [10|20|50] 条」
  ↓
切换每页条数 → page=1，保留 keyword/status/level/parent_id
切换页码 → 带当前筛选条件请求
```

## 5. 依赖

| 依赖 | 说明 |
|---|---|
| REQ-0005-tile-category-management | 类目 API、页面基线、删除规则 |
| REQ-0005-user-management-list-refine | 分页 DOM / 文案参考 |
| add-tile-category-management | 已 archive 基线代码 |
| BUG-0001-tile-category-enable-missing | 启停按钮可见性已修复，本需求不回归 |
