---
bug_id: BUG-0028-tile-spec-modal-form-layout
status: pending_review
created_at: 2026-06-28 13:21:30
updated_at: 2026-06-28 13:21:30
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 弹窗 JSX 字段顺序与 REQ-0009 / 原型不一致

`TileSpecFormModal.tsx` 当前渲染顺序：

```text
宽度* → 长度* → 厚度 → 排序* → 尺寸名称（只读，form-full）→ 备注（form-full）
```

REQ-0009 FR-006、AC-019 与 `tile-size-management-modal.html` 规范顺序：

```text
宽度* → 长度* → 尺寸名称（只读，form-full）→ 厚度 → 排序* → 备注（form-full）
```

尺寸名称块被错误地置于厚度、排序之后，导致运营在填写宽长后无法在紧邻位置看到系统生成的展示名，与原型交互路径不符。

### 1.2 `tile-spec-management.css` 未 port 表单控件宽度与 textarea 规则

弹窗网格已定义 `.form-full { grid-column: 1 / -1 }`，容器可跨列，但：

- 原型 HTML 内联 CSS 含 `.input,.textarea,.readonly { width: 100%; … }` 与 `.textarea { height: 112px; resize: none; … }`。
- `tile-spec-management.css` 仅 port 了 `.tile-spec-readonly`，**未** port `.textarea` / `.input` 在弹窗网格内的宽度与高度规则。
- 全局 `user-management.css` 的 `.admin-shell .input` 含 `width: 100%`，但 **不包含** `.textarea`。

因此备注 `textarea` 在跨列容器内仍按浏览器默认宽度渲染，视觉上未占满整行；`resize` 行为也与原型 `resize: none` 不一致。

### 1.3 弹窗 CSS Port 验收未完成（附带缺口）

`add-tile-spec-management` trace checklist 第 7–9 项（弹窗 720px 字段网格、只读 display_name 实时生成、字段集合）仍为「待人工」。AC-021 要求的宽长冲突提示（「该尺寸已存在，请勿重复创建」）与只读区 help 文案亦未在组件中实现——属同弹窗交付缺口，可与本 BUG 一并纳入 fix scope。

## 2. 根本原因

### 2.1 实现阶段以功能字段集为准，未严格对照原型 DOM 顺序完成 Port

`sprint-apply` 实现 `TileSpecFormModal` 时收集了全部必填/可选字段并放入双列 grid，但未按原型 HTML 的字段**顺序**排列 JSX 节点；尺寸名称作为只读 preview 被追加在数值字段之后，而非紧接宽/长之后。

### 2.2 CSS Port 策略不完整：只 port 页面/弹窗局部类，遗漏共享表单控件规则

`tile-spec-management.css` 从 HTML 提取了列表表、弹窗宽度、`.tile-spec-readonly` 等局部样式，但未同步 port 原型 `<style>` 中与 `.input`/`.textarea` 相关的通用表单规则；且未参照 `brand-management.css` 中已验收的 `.brand-textarea { width: 100%; … }` 模式为规格弹窗补全等价规则。

### 2.3 管理端弹窗表单仍缺少共享模板或 Port checklist 强制约束

与 BUG-0027（列表分页 invent 非标准 DOM）同类：新增管理端弹窗时手写 JSX + 局部 CSS，缺少「字段顺序 / 跨列控件宽度 MUST 对照 prototype modal HTML」的自动化或人工 gate，导致 REQ-0009 AC-019、AC-046 未在 merge 前关闭。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 admin 或 employee 登录 Web 管理端（local 或 Docker）。
2. 访问 `/admin/tile-specs`，点击「+ 新增瓷砖规格」或行内「编辑」。
3. 弹窗打开后观察字段自上而下顺序：尺寸名称位于厚度、排序下方。
4. 观察「备注」文本框横向宽度未与弹窗内容区同宽。
5. 可选：并排打开 `tile-size-management-modal.html` 对比字段顺序与备注宽度。

**非缺陷路径（无需修复）：** 宽长填写后只读 preview 显示 `600×1200mm`——与 `buildDisplayName()` 及 AC-021 一致。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（`add-tile-spec-management` 交付即存在） |
| 主要修复面 | `TileSpecFormModal.tsx` 字段重排；`tile-spec-management.css` 表单控件 port |
| 关联需求 AC | AC-019、AC-020、AC-021（冲突提示，可选同 scope）、AC-046 |
| 建议 Change | `fix-tile-spec-modal-form-layout` |

## 5. 后续修复建议

1. 调整 `TileSpecFormModal.tsx` JSX：将尺寸名称（只读）块移至宽/长之后、厚度/排序之前。
2. 在 `tile-spec-management.css` 的 `.tile-spec-form-grid` 作用域内补 port：
   - `.input`、`.textarea` → `width: 100%`
   - `.textarea` → 固定高度（对齐原型 112px 或品牌弹窗 132px，以 prototype 为准）、`resize: none`、边框/背景 semantic token
3. **不要**修改 `buildDisplayName()` 去掉 `mm` 后缀。
4. 可选：补 AC-021 宽长冲突前端提示与只读区 help 文案（参考原型 `#duplicateTip`）。
5. 建议 Change 命名：`fix-tile-spec-modal-form-layout`；可与 BUG-0027、BUG-0029 合并为 `fix-tile-spec-admin-ui`。
6. 补充 Vitest：断言弹窗 label 顺序；备注 `textarea` 在 `.form-full` 内 `width: 100%`（或 DOM 结构快照）。
