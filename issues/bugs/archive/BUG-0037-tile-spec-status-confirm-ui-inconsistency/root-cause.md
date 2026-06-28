---
bug_id: BUG-0037-tile-spec-status-confirm-ui-inconsistency
status: pending_review
created_at: 2026-06-28 16:14:20
updated_at: 2026-06-28 16:14:20
root_cause_type: code/design/frontend-ui
---

# 根因分析

## 1. 分类

| 项 | 值 |
|---|---|
| 缺陷类型 | **code / design / frontend-ui**（瓷砖规格启停/删除 confirm 未对齐 DS modal） |
| 引入阶段 | `add-tile-spec-management` 初版实现；`fix-tile-spec-admin-ui` 未纳入 confirm scope |
| 责任模块 | `TileSpecManagementPage.tsx`（启停/删除 confirm 内联 JSX，约 L329–382） |
| 关联后端 | 无缺陷；enable/disable/delete API 与 Toast 反馈正常 |

## 2. 直接原因

### 2.1 规格页 confirm 使用简化内联模板

`TileSpecManagementPage.tsx` 启停/删除 confirm 未复用品牌/类目页已验收的 modal 结构：

```tsx
<section className="modal-card confirm-card" role="dialog" ...>
  <header className="modal-head">
    <h2 className="modal-title">{statusConfirmIsEnable ? '启用规格' : '停用规格'}</h2>
  </header>
  <div className="modal-body">
    <p>确认{statusConfirmIsEnable ? '启用' : '停用'}规格「{display_name}」？</p>
  </div>
  <footer className="modal-footer">
    <button className="btn primary">确认</button>
  </footer>
</section>
```

与 `TileCategoryManagementPage.tsx` 差异：无 `modal-close`、无 `aria-labelledby`、正文无 `page-desc`、主按钮泛化「确认」、停用无前台影响说明、删除使用 `btn primary danger`。

### 2.2 `confirm-card` 为无效 class

全仓库 CSS **无** `.confirm-card` 定义；该 class 不贡献样式，仅表明实现时偏离标准 modal 模板。

### 2.3 后续 fix change 未覆盖 confirm

Sprint-003 `fix-tile-spec-admin-ui`（BUG-0027/28/29）修复分页、表单弹窗、列表刷新，**scope 不含**启停/删除 confirm；修复后 confirm 仍为初版简化实现。

### 2.4 测试未覆盖 confirm 路径

`TileSpecManagementPage.test.tsx` 仅覆盖分页 DOM 与保存后刷新；**无**启停/删除 confirm 用例。`TileCategoryManagementPage.test.tsx` 已有 `opens disable confirm dialog` 测试可作门禁模板。

## 3. 根本原因

### 3.1 管理端 confirm 无共享组件与横切 CI 检查

品牌（REQ-0008）、类目（REQ-0007）、用户（BUG-0016/0017）confirm modal 均按页面/专项 change 落地，**无** `AdminConfirmDialog` 共享组件（见 `admin-list-page-consistency.md` 建议项）。新页面 `add-tile-spec-management` 实现时复制了简化 confirm 片段而非类目/品牌 Golden Reference。

### 3.2 REQ-0009 验收粒度不足于阻止简化实现

REQ-0009 AC-013 要求「启停 confirm 对齐 `BrandManagementPage`」，但初版 apply 时未以并排 diff 或 Vitest 门禁强制 modal 结构一致；`fix-tile-spec-admin-ui` tasks 亦未列出 confirm 对齐项，形成交付缺口。

### 3.3 原型未覆盖 confirm 细节

`tile-size-management.html` 为静态列表原型，启停 confirm 仅于 `tile-size-management-context.md` §8 文字引用品牌页；实现者易仅满足「有二次确认」而忽略 DOM/文案/按钮语义对齐。

## 4. 触发条件

满足以下条件即可 **100%** 稳定复现：

1. `admin` 登录 Web 管理端（local 或 Docker）；
2. 进入 `/admin/tile-specs`；
3. 对启用行点击「停用」（或对停用行点击「启用」，或对可删除行点击「删除」）；
4. 观察 confirm 弹窗与 `/admin/tile-categories` 同类弹窗差异。

**Golden Reference**：`TileCategoryManagementPage.tsx` L423–505（启停/删除 confirm）。

## 5. 非根因（排除）

| 假设 | 结论 |
|---|---|
| API 或权限错误 | 否；确认后 API 与 Toast 正常 |
| modal CSS 未加载 | 否；弹窗可显示，仅为结构/文案偏差 |
| BUG-0027/28/29 回退 | 否；分页/表单/刷新已修，confirm 从未对齐 |
| 后端缺少 confirm | 否；纯前端 UI/UE 问题 |
| Design System Token 缺失 | 否；标准 modal 类已在 `user-management.css` / `brand-management.css` 存在 |

## 6. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | code / design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否 Design System 缺陷 | 是，confirm Dialog 未横向对齐 |
| 主要修复面 | `TileSpecManagementPage` confirm JSX；Vitest；OpenSpec delta |

## 7. 修复建议（供 bug-opsx）

1. 将启停/删除两处 confirm markup 对齐 `TileCategoryManagementPage`（`display_name` 替代 `name`，「类目」→「规格」）。
2. 停用正文补「停用后前台将不再展示该规格。」；主按钮「确认启用」「确认停用」「删除规格」。
3. 移除 `confirm-card`、`danger` class；补 `modal-close`、`aria-labelledby`、`page-desc`。
4. Vitest：参照类目页 `opens disable confirm dialog before calling disableCategory`。
5. OpenSpec change：`fix-tile-spec-status-confirm-ui`；MODIFIED `tile-spec-management` 或 `web-client` confirm requirement。
