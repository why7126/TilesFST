---
title: 业务流程
purpose: 描述品牌管理页启停二次确认交互流程
content: 基于 requirement.md 提炼
source: AI 根据 PRD 生成，项目团队确认
update_method: PRD 变更时同步更新
owner: product
status: draft
note: REQ-0008-brand-status-confirm
---

# 业务流程

## 1. 与 REQ-0005 的差异

本需求 **仅修改** 启停流程节点；新增/编辑/删除/筛选/分页 API 与业务规则不变（见 `REQ-0005-brand-management` 及既有 business-flow）。

```text
变更前                              变更后
──────────────────────────────────────────────────────────────────
点击「启用/停用」→ 直接 API      →    弹出确认框 → 确认后 API
删除：独立确认弹窗（不变）        →    不变
```

## 2. 启用 / 停用流程（优化后）

```text
用户点击行内「启用」或「停用」
  ↓
打开确认弹窗（标题：启用品牌 / 停用品牌）
  ├─ 取消 / 遮罩 / × / ESC  → 关闭弹窗，状态不变
  └─ 确认启用 / 确认停用
        ↓
     POST /admin/brands/{id}/enable 或 POST .../disable
        ↓
     Toast「品牌已启用」/「品牌已停用」
        ↓
     loadBrands()（列表 + summary 指标卡）
```

### 2.1 弹窗文案

| 动作 | 标题 | 正文 |
|------|------|------|
| 停用 | 停用品牌 | 确认停用品牌「{name}」？停用后前台将不再展示该品牌。 |
| 启用 | 启用品牌 | 确认启用品牌「{name}」？ |

### 2.2 与删除流程的关系

```text
删除：独立「删除品牌」确认弹窗（不变）
启停：独立「启用/停用品牌」确认弹窗（新增）
MUST NOT 合并为同一弹窗
```

## 3. 页面其他区域（不变）

```text
page-header（不变）
  ↓
4 指标卡（不变）
  ↓
filter-card（不变）
  ↓
brand-table-card + 行操作（编辑 / 启停 / 删除规则不变）
  ↓
pagination（不变）
```

## 4. 依赖

| 依赖 | 说明 |
|---|---|
| REQ-0005-brand-management | 品牌 API、页面基线、删除规则 |
| REQ-0007-tile-category-management-refine | 启停确认交互与文案模式参考 |
| add-brand-management | 已 archive 基线代码 |
