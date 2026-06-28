# fix-sidebar-menu-icons-indistinguishable — Test Plan

## 单元 / 组件（Vitest）

| 用例 | 文件 | 断言 |
|---|---|---|
| collapsed 态不同 icon | `AdminSidebar.icons.test.tsx`（或扩展 collapse test） | 至少 2 个 nav id 渲染不同 Lucide SVG / data 属性 |
| chevron 切换无回归 | `AdminSidebar.collapse.test.tsx` | `data-sidebar-state`、localStorage、aria-expanded |
| employee 隐藏 users | `AdminSidebar.user-mgmt.test.tsx` | users 不可见；其余 nav 仍渲染 |
| icon aria-hidden | 同上 | 装饰 icon `aria-hidden="true"`；button 保留 `aria-label` |

## 构建

```bash
cd src/web && pnpm test && pnpm build
```

## 手工冒烟

1. admin 登录 → `/admin/dashboard` → expanded：各菜单 icon 形状不同。
2. 收起侧栏 → collapsed：仅凭 icon 可识别并点击跳转 SKU/品牌。
3. employee 登录 → 「用户管理」不可见，其余 icon 可区分。
4. 刷新页面 → collapsed 偏好持久化；chevron 仍正常。
5. 视口 ≤1023px → 无折叠 chevron 回归。

## 不在 scope

- API / pytest 后端
- 店主端 Sidebar
- REQ-0014 profile 菜单入口（除 merge 冲突协调外）
