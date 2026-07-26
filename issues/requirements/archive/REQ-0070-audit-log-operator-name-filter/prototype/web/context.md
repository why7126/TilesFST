---
requirement_id: REQ-0070-audit-log-operator-name-filter
title: 日志审计页面操作者名称筛选 - 原型上下文
status: pending_review
owner: product
created_at: 2026-07-25 11:57:39
updated_at: 2026-07-25 11:57:39
---

# 原型上下文

## 目标

为日志审计页面筛选区提供操作者单选可搜索下拉的交互参考。原型只表达筛选区与列表布局关系，不作为最终视觉稿。

## 页面范围

- 页面：管理端 `/admin/logs`
- 区域：日志筛选卡片中的“操作者”字段
- 控件：单选可搜索下拉
- 相关列表：日志审计表格和分页

## 关键交互

1. 管理员打开“操作者”下拉。
2. 输入用户名称或账号关键字。
3. 下拉展示候选项，主文案为用户名称，辅助文案为账号 / 角色 / 状态。
4. 选择一个用户后，控件收起并展示可读名称。
5. 日志列表使用该用户 ID 作为 `actor_user_id` 查询。
6. 点击清空或页面重置后，恢复全部操作者。

## 状态

| 状态 | UI 表现 |
|---|---|
| 默认 | placeholder 为“搜索用户名称或账号”。 |
| 展开 | 输入框聚焦，下方展示候选列表。 |
| 搜索中 | 下拉内显示“搜索中...”。 |
| 无结果 | 下拉内显示“无匹配用户”。 |
| 失败 | 下拉内显示“用户候选加载失败”，并通过固定 toast 提示。 |
| 已选择 | 输入框展示用户名称；右侧提供清空按钮或等价交互。 |

## 验收提醒

- 优先复用现有 `SearchableSelect` 或同等 Design System 组件。
- 不新增裸 Hex；颜色、边框、文字使用 semantic token。
- 下拉面板在移动端不得超出屏幕宽度。
- 分页、指标卡、toast 需满足 `admin-list-page-consistency` 横切 AC。

## 原型文件

- `prototype/web/operator-filter.html`
- PNG Golden Reference：待后续设计确认后导出，当前非阻塞。
