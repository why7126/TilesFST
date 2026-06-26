## Context

- **BUG**: `BUG-0002-brand-ui-inconsistency`
- **Severity**: medium
- **Root cause type**: design / frontend-ui
- **Existing related change**: `add-brand-management`（in-progress，品牌管理能力尚未归档）
- **Reference page**: `/admin/users`
- **Target page**: `/admin/brands`

## Bug Analysis Report

### 现象

品牌管理相关界面存在两处 UI 设计一致性问题：

1. 品牌列表底部分页 UI 与用户管理页分页 UI 不一致。
2. 添加品牌弹窗「品牌Logo」选择文件控件与整体管理端设计不一致。

### 复现路径

1. 以 admin 登录 Web 管理端。
2. 访问 `/admin/brands`，观察列表底部分页区域。
3. 访问 `/admin/users`，对比分页区域结构、控件尺寸、文案、边框、圆角、激活态和布局。
4. 返回 `/admin/brands`，点击「新增品牌」。
5. 对比「品牌Logo」区域与用户管理弹窗「头像」上传区域及其他表单控件。

### 影响

- 不阻断品牌管理业务功能。
- 不影响 API、数据库、权限和媒体上传安全策略。
- 影响管理端视觉一致性、Design System 执行质量和后续复用。

## Root Cause

### RC-001：品牌分页结构与用户分页结构未复用

用户管理页分页结构为：

```text
pagination
├── page-summary
└── page-right
    ├── page-buttons
    └── page-size-wrap
```

品牌管理页分页结构为：

```text
pagination
├── page-left
└── brand-pagination-right
    ├── jump-input
    └── page-size
```

品牌页虽然复用部分 `.pagination` / `.page-btn` / `.page-size` 样式，但额外局部结构导致同类页面视觉不一致。

### RC-002：Logo 上传控件使用页面专属大面积上传框

品牌 Logo 控件使用 `button.brand-upload` 大面积虚线框；用户头像上传使用 `avatar-upload` 行内结构。两者同属弹窗内图片选择文件控件，但没有统一模式。

## Design Decisions

### D1：分页优先对齐用户管理页

品牌列表分页 MUST 对齐用户管理页分页结构。默认目标结构：

```text
pagination
├── page-summary
└── page-right
    ├── page-buttons
    └── page-size-wrap
```

若保留跳页输入，MAY 在 `page-right` 内作为可选扩展，但 MUST 不破坏用户管理页分页的主视觉结构。

### D2：Logo 上传采用紧凑表单控件

品牌 Logo 选择文件控件 SHOULD 参考用户管理弹窗 `avatar-upload`：

- 左侧展示 Logo 预览或占位说明。
- 右侧使用管理端 `btn` 风格触发文件选择。
- 帮助文案使用现有 `form-help` 层级。
- 隐藏原生 file input，仅通过明确按钮/label 触发。

### D3：不扩大行为面

本 change 不修改：

- 品牌 API 请求/响应。
- 品牌 Logo 上传 API。
- 数据库结构。
- 鉴权和角色权限。
- MinIO bucket / prefix / object_key 策略。

## Test Strategy

- Vitest / Testing Library：
  - 验证品牌列表分页渲染与用户管理页一致的摘要、按钮、每页显示区域。
  - 验证品牌弹窗 Logo 上传入口为统一按钮/label 模式，隐藏 file input 可触发上传。
  - 保留品牌创建/编辑/上传 Logo 的既有行为测试。
- 人工视觉验收：
  - 并排对比 `/admin/brands` 与 `/admin/users` 分页。
  - 打开新增品牌弹窗，对比用户管理弹窗头像上传控件。
- 构建：
  - `cd src/web && npx vitest run src/pages/admin src/features/admin`
  - `cd src/web && npm run build`

## Risks

| 风险 | 缓解 |
|---|---|
| 调整分页 DOM 影响品牌分页功能 | 保留 page/pageSize 状态流与事件处理；补充测试 |
| 调整 Logo 控件影响上传 | 保持原 `handleLogoChange` 与 `uploadBrandLogo` 调用不变 |
| 跳页能力去留影响使用习惯 | 若去除需在 acceptance 中确认；若保留则纳入统一布局 |
