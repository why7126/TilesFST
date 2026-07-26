## ADDED Requirements

### Requirement: 管理端列表页操作反馈 Toast 布局统一

Web 客户端 MUST 在管理端以下四个列表页对「操作成功/失败且约 3.2 秒后自动消失」的全局反馈使用固定位置 toast（`.admin-toast-region` + `.admin-toast` 或等价共享组件），MUST NOT 在 `page-hero` 或主体内容上方插入文档流 `.admin-notice` 占位节点。toast 样式 MUST 来自管理端共享样式（如 `admin-home.css`），四页视觉与行为 MUST 一致。弹窗内 inline 表单错误 MAY 继续使用 inline 错误文案；`AdminLayout` 侧栏占位 notice 不在本 requirement 范围。修复 MUST NOT 回归品牌 Logo 展示、上传进度及四页 CRUD、筛选、分页、权限边界。

涵盖路由：

- `/admin/brands`（瓷砖品牌）
- `/admin/users`（用户管理）
- `/admin/tile-categories`（瓷砖类目）
- `/admin/tile-skus`（瓷砖 SKU）

#### Scenario: 用户管理列表操作反馈不推挤页面

- **WHEN** `admin` 在 `/admin/users` 执行冻结、解冻、删除、重置密码、新建/编辑用户成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 改变 page-hero、指标卡、筛选区、表格或分页的纵向位置
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 瓷砖类目列表操作反馈不推挤页面

- **WHEN** `admin` 或 `employee` 在 `/admin/tile-categories` 执行启用、停用、删除、保存类目成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 推挤 page-hero、筛选区、表格或分页
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 瓷砖 SKU 列表操作反馈不推挤页面

- **WHEN** `admin` 或 `employee` 在 `/admin/tile-skus` 执行上架、下架、删除、保存 SKU 成功或列表加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 展示 fixed toast 反馈
- **AND** 反馈出现和消失 MUST NOT 推挤 page-hero、指标卡、筛选区、表格或分页
- **AND** MUST NOT 在列表页主体顶部使用文档流 `.admin-notice` 承载该反馈

#### Scenario: 瓷砖品牌列表 toast 共享实现且不回归

- **WHEN** `admin` 或 `employee` 在 `/admin/brands` 执行启用、停用、删除、保存品牌或加载失败等会触发全局反馈的操作
- **THEN** 系统 MUST 继续使用 fixed toast，行为与 BUG-0003 / `fix-brand-image-display-layout-shift` 验收一致
- **AND** toast 样式 MUST 来自管理端共享样式，MUST NOT 仅私有于 `brand-management.css`
- **AND** 品牌 Logo 展示、上传进度、启停确认弹窗 MUST NOT 回归

#### Scenario: 四页 toast 视觉与行为一致

- **WHEN** 对比四页成功 toast（如「品牌已启用」「用户已冻结」「类目已启用」「SKU 已上架」）
- **THEN** 位置、圆角、边框、背景、字号、阴影 MUST 一致
- **AND** 自动消失时长 MUST 为 3200ms
- **AND** MUST 保留 `aria-live="polite"` 与 `role="status"` 可访问性语义

#### Scenario: Design System 约束

- **WHEN** 修复修改 Web UI 样式
- **THEN** MUST 使用既有管理端 CSS 变量与 semantic token
- **AND** MUST NOT 新增裸 Hex 或与 `rules/ui-design.md` 冲突的提示样式
