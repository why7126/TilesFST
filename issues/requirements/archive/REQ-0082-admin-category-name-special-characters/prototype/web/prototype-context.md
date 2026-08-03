---
requirement_id: REQ-0082-admin-category-name-special-characters
title: 管理后台瓷砖类目名称允许特殊字符 - Prototype Context
status: pending_review
created_at: 2026-07-30 22:14:37
updated_at: 2026-07-30 23:52:09
---

# Prototype Context

## 目标

为后续 OpenSpec Change 和实现提供低保真 UI 语境，重点验证类目新增 / 编辑弹窗字段提示、特殊字符合法样例、列表和类目树展示兼容性。

## 页面与组件

- 管理后台类目管理页。
- 类目新增 / 编辑弹窗。
- 类目列表名称列。
- 类目树或类目选择器；类目树默认只展示一级类目，有子级类目使用 `+/-` 控件展开 / 收起，子级默认收起。

## 设计约束

- 继续复用现有管理端页面骨架和类目弹窗组件。
- 使用 Design System semantic token；实现阶段禁止新增裸 Hex。
- 弹窗字段级错误展示在类目名称输入框下方。
- 特殊字符合法示例可以作为 placeholder、帮助文案或测试样例，但不应在正式 UI 中加入过长解释。
- 类目树的展开 / 收起与类目筛选点击应分离，避免点击 `+/-` 时触发列表筛选。

## 原型文件

- `admin-category-name-special-characters.html`：低保真 HTML，用于表达字段状态和展示回归点。
- PNG：待实现阶段按实际页面导出。
