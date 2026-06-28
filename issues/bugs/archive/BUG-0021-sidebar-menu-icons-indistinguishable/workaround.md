---
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
status: pending_review
created_at: 2026-06-27 21:40:26
updated_at: 2026-06-27 21:40:26
---

# 临时规避方案

## 1. 可用性规避

该缺陷不阻断路由与业务功能，当前可继续使用：

1. **保持侧栏展开**：点击 chevron 展开侧栏（`data-sidebar-state="expanded"`），通过 `.nav-label` 文字标签识别菜单。
2. **依赖 active 态**：当前路由对应项仍有 `.nav-item.active` 金色高亮与左侧 2px accent bar，可确认「当前页」但无法快速定位其他菜单。
3. **读屏用户**：各 nav 按钮已有 `aria-label={label}`，辅助技术可正确朗读菜单名称。

## 2. 操作规避

习惯使用 collapsed 侧栏的用户：

1. 切换菜单前可先展开侧栏确认目标，再收起（增加一步操作）。
2. 或记住菜单在列表中的**垂直顺序**（首页 → SKU → 品牌 → 类目 → Banner → 用户 → 设置），通过位置而非图标识别。

## 3. 持久化偏好规避

若 localStorage 已保存 `admin-sidebar-collapsed=true`：

1. 开发者工具 → Application → Local Storage → 删除 `admin-sidebar-collapsed`，或设为 `false`。
2. 刷新后默认 expanded，直至用户再次手动收起。

## 4. 风险说明

上述规避只能保证功能可用，不能消除：

- collapsed 态下误点错误菜单、增加导航时间。
- 新用户或偶发使用者无法凭图标建立心智模型。
- REQ-0011「icon-only 窄栏」的设计意图（参照 SoulKing）未完整达成。

仍建议进入 `/bug-review BUG-0021 --approve`，通过 `fix-sidebar-menu-icons-indistinguishable` OpenSpec Change 修复。
