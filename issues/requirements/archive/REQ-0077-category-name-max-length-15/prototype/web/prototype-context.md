---
purpose: REQ-0077 Web 管理端原型上下文
content: 类目名称 15 字符校验、弹窗和列表/树展示回归说明
source: issues/requirements/archive/REQ-0077-category-name-max-length-15/requirement.md
created_at: 2026-07-28 00:06:52
updated_at: 2026-07-28 00:13:39
status: approved
---

# Prototype Context

## 目标

本原型用于锁定类目名称上限从 10 个字符放宽到 15 个字符后的管理端验收重点：

- 新增 / 编辑类目弹窗中，15 字符名称通过，16 字符名称显示字段级错误。
- 类目列表名称列和左侧类目树能承载 15 字符样例，不发生重叠。
- 弹窗宽度、滚动和 CSS cascade 遵守 `admin-modal` best-practice。

## 视觉与组件约束

- 视觉方向沿用“工业石材 · 暗色旗舰风”。
- 实现阶段优先复用 `CategoryFormModal`、管理端列表模板、FixedAdminToast、AdminConfirmModal。
- 不新增裸 Hex；使用 semantic token 或现有 CSS 变量。
- 原型 HTML 仅用于验收语义参考，不替代最终 React / Tailwind / shadcn 实现。

## 原型文件

| 文件 | 说明 |
|---|---|
| `category-name-max-length-15.html` | 弹窗、列表和类目树的静态验收原型 |
| `prototype-context.md` | 本上下文说明 |
| `category-name-max-length-15.png` | 待导出，后续可由浏览器截图或设计工具生成 |

## 样例数据

| 场景 | 样例 | 预期 |
|---|---|---|
| 15 字符中文 | `岩板背景墙精选砖材` | 可保存 |
| 15 字符英文数字 | `ModernTile2026A` | 可保存 |
| 16 字符中文 | `岩板背景墙精选砖材加长` | 显示「类目名称最多 15 个字符」 |
| 非法字符 | `岩板-背景墙` | 沿用非法字符提示 |

## 验收重点

- 1440px 桌面视口下，弹窗 computed width 与设计批准宽度一致。
- 720px 高度以下，弹窗 body 可滚动，底部操作区不遮挡字段。
- 类目列表分页 DOM 不因本需求变更。
- 状态操作 confirm 和 fixed toast 不因本需求回归。
