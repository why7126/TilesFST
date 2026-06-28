---
bug_id: BUG-0015-admin-list-status-tips-layout-shift
status: pending_review
created_at: 2026-06-27 12:40:41
updated_at: 2026-06-27 12:40:41
root_cause_type: code/design/frontend-ui
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code / design / frontend-ui**（管理端操作反馈组件模式不一致） |
| 引入阶段 | 各管理列表页初版 apply（`add-brand-management`、`add-user-management`、`add-tile-category-management`、`add-tile-sku-management`） |
| 责任模块 | 四页 `*ManagementPage.tsx` + `admin-home.css` / `brand-management.css` |
| 关联后端 | 无缺陷；API 调用与 `setNotice()` 触发逻辑正常 |

## 2. 直接原因

### 2.1 自动消失 Tips 使用文档流 `.admin-notice`

用户管理、瓷砖类目、瓷砖 SKU 三页在 `page-hero` 前条件渲染：

```tsx
{notice ? (
  <p className="admin-notice" role="status" aria-live="polite">
    {notice}
  </p>
) : null}
```

涉及文件：

- `src/web/src/pages/admin/UserManagementPage.tsx`
- `src/web/src/pages/admin/TileCategoryManagementPage.tsx`
- `src/web/src/pages/admin/TileSkuManagementPage.tsx`

`.admin-notice`（`admin-home.css`）仅定义 `margin-bottom: 16px`、`padding`、`border`、`background` 等，**无** `position: fixed`、overlay 容器或预留高度。

每页均有相同模式：

```tsx
useEffect(() => {
  if (!notice) return;
  const timer = window.setTimeout(() => setNotice(null), 3200);
  return () => window.clearTimeout(timer);
}, [notice]);
```

因此操作成功/失败后：

1. `setNotice(...)` 在主体内容上方插入一行 block 节点；
2. 3.2s 后定时器清空 notice，节点从 DOM 移除；
3. hero、指标卡、筛选区、表格随文档流高度变化产生纵向位移。

### 2.2 品牌页局部修复未推广至其他列表页

`BUG-0003` / `fix-brand-image-display-layout-shift` 已将品牌页改为：

```tsx
<div className="admin-toast-region" aria-live="polite" aria-atomic="true">
  <p className="admin-toast" role="status">{notice}</p>
</div>
```

样式定义在 `brand-management.css`：

```css
.admin-shell .admin-toast-region {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 60;
  pointer-events: none;
}
```

品牌页行为正确，但：

- toast 样式**未**提升至管理端共享样式；
- 用户/类目/SKU 页**未**同步改造；
- `BUG-0003` root-cause §5 已建议「回归检查用户管理、类目管理、SKU 管理等页面」，该建议未在后续 change 中闭环。

## 3. 根本原因

### 3.1 管理端缺少统一的操作反馈组件契约

各列表页独立复制 `notice` state + 条件渲染，无共享 `AdminToast` 或 design 规范约束「自动消失反馈 MUST 使用 fixed toast」。`.admin-notice` 被混用于：

- 适合场景：表单 inline 错误、静态说明（如弹窗内 `form-error`）；
- 不适合场景：操作成功后 3.2s 自动消失的全局反馈（会改变布局高度）。

### 3.2 修复范围在 BUG-0003 中仅覆盖品牌页

`fix-brand-image-display-layout-shift` 以品牌图片 + 品牌 Tips 为 scope，归档时未将 toast 模式提取为跨页能力。后续新增/迭代列表页（用户 v2、类目 refine、SKU）继续沿用初版 `.admin-notice` 模板。

### 3.3 缺少跨页布局稳定性自动化

除 `BrandManagementPage.test.tsx` 对启用操作断言 `.admin-toast-region` 外，用户/类目/SKU 页无「Tips 不得使用文档流 `.admin-notice`」测试，缺陷在联调/产品验收阶段才暴露。

## 4. 触发条件

满足以下条件即可稳定复现（用户/类目/SKU 页）：

1. 管理员或员工登录 Web 管理端；
2. 进入对应列表页；
3. 执行会调用 `setNotice()` 的操作（状态变更、CRUD 成功、API 错误等）；
4. 观察 Tips 出现与 3.2s 后消失时主体内容纵向位移。

品牌页当前源码使用 fixed toast，**不应**复现文档流推挤；纳入本 BUG 是为统一实现与防回归。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| API 响应慢导致布局重排 | 否；位移与 notice 节点插入/移除同步，与数据刷新无必然关系 |
| Sidebar 折叠/展开 | 否；与 notice 生命周期无关 |
| `AdminLayout` 占位 notice | 否；侧栏「功能建设中」提示，非四列表页 scope |
| Design System Token 缺失 | 否；样式变量可用，问题在于组件模式选型 |

## 6. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否 Design System 缺陷 | 是，自动消失 Tips 误用占位文档流 |
| 主要修复面 | 四页统一 fixed toast；共享样式/可选 `AdminToast` 组件；Vitest 布局稳定性 |

## 7. 修复建议（供 bug-opsx）

1. 将 `.admin-toast-region` / `.admin-toast` 从 `brand-management.css` 迁移至 `admin-home.css`（或 `src/web/src/shared/ui/AdminToast.tsx` + 对应样式）。
2. 用户、类目、SKU 三页 notice JSX 对齐品牌页结构；品牌页改引用共享实现。
3. 保留 3200ms 自动消失与 `aria-live="polite"`；成功/错误反馈均走 toast（列表页顶部文档流路径）。
4. 四页各补至少一条 Vitest：操作成功后 MUST 有 `.admin-toast-region`，MUST NOT 在 `page-hero` 前渲染文档流 `.admin-notice`（成功反馈路径）。
5. OpenSpec：`fix-admin-list-status-toast-layout`；delta 可参考 `fix-brand-image-display-layout-shift` AC-004/AC-005 写法并扩展至四页。
