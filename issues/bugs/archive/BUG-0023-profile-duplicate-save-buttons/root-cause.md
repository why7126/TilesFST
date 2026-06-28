---
bug_id: BUG-0023-profile-duplicate-save-buttons
status: pending_review
created_at: 2026-06-28 12:53:12
updated_at: 2026-06-28 12:53:12
root_cause_type: design
---

# 根因分析

## 1. 直接原因

### 1.1 页头与表单底部各渲染一个「保存修改」按钮

`ProfilePage.tsx` 在 `profile-page-head` 与 `profile-form-actions` 两处分别渲染文案、样式、行为相同的 `<button className="btn primary">保存修改</button>`，均绑定 `handleSave()`：

```tsx
// 页头 L194–201
<button type="button" className="btn primary" onClick={() => void handleSave()}>保存修改</button>

// 表单底部 L329–336（与「重置」并列）
<button type="button" className="btn primary" onClick={() => void handleSave()}>保存修改</button>
```

### 1.2 测试用例假设双按钮存在

`ProfilePage.test.tsx` 使用 `getAllByRole('button', { name: '保存修改' })` 点击 `[0]`，与当前双按钮实现一致，未断言单入口 UX。

### 1.3 inline save-tip 位于表单底部

保存成功提示 `.save-tip` 渲染在 `profile-form-actions` 左侧，与表单底部按钮同区；页头按钮与成功反馈视觉分离，进一步放大「双 CTA」冗余感。

## 2. 根本原因

### 2.1 REQ-0014 原型 HTML 含双按钮，验收未禁止

`profile-page.html` 原型在 page-head 与 form-actions 各有一个「保存修改」。REQ-0014 **FR-003** 规定页头 **MAY** 提供保存按钮；**AC-017** 仅要求「页头与卡片内行为一致」，未要求单入口。`add-admin-profile-page` 按原型与 AC 交付时保留了双按钮。

### 2.2 上下文文档与原型存在轻微分歧

`profile-page-context.md` §5 按钮列表仅含表单区「重置 + 保存修改」，未强调页头 CTA；实现优先对齐 HTML 原型而非 context 单区描述，导致交付后用户反馈与 spec 需 reconcile。

### 2.3 管理端 Page Head 模式未统一约束单 CTA

其他管理端列表/编辑页多采用表单内或弹窗内单一提交入口；个人资料页同时采用「页头全局 CTA + 表单底 actions」双轨，属该页 CSS Port 策略下的 UX 过度对齐，非功能必需。

## 3. 触发条件

满足以下条件时可 **100% 稳定复现**：

1. 以 `admin` 或 `employee` 登录 Web 管理端（local `5173` 或 Docker `3000`）。
2. 访问 `/admin/profile`。
3. 页面加载完成即见页头与表单底部各一个「保存修改」按钮。
4. 无需修改表单字段；可选点击任一按钮验证行为相同。

## 4. 分类结论

| 维度 | 结论 |
|---|---|
| 缺陷分类 | design / frontend-ui |
| 是否接口缺陷 | 否 |
| 是否数据库缺陷 | 否 |
| 是否权限缺陷 | 否 |
| 是否回归 | 否（自 `add-admin-profile-page` 归档起即存在） |
| 主要修复面 | `ProfilePage.tsx`、`ProfilePage.test.tsx`、REQ-0014 AC-017 delta |
| 关联需求 | REQ-0014 AC-015、AC-016、AC-017 |
| 关联 BUG | BUG-0022（同页 UX；建议同 change） |
| 建议 Change | `fix-profile-page-ux-refine` |

## 5. 后续修复建议

1. **移除页头**「保存修改」按钮（推荐：与「重置」、inline save-tip 同区保留表单底按钮）。
2. 更新 `ProfilePage.test.tsx`：`getAllByRole` → `getByRole('button', { name: '保存修改' })`。
3. 在 fix change delta spec 中 **MODIFIED AC-017**：页面仅保留一处「保存修改」主 CTA。
4. 1440×1024 并排验收：确认 page-head 无重复按钮、表单 actions 与 save-tip 布局无回归。
5. 可选与 BUG-0022（移除表单内角色/状态字段）合并为同一 `fix-profile-page-ux-refine` change。
