# fix-brand-ui-consistency — Trace

## 变更摘要

- **BUG**: `BUG-0002-brand-ui-inconsistency`
- **Type**: fix
- **Status**: archived
- **Severity**: medium
- **Hotfix**: no
- **Target**: Web 管理端 `/admin/brands`
- **Related Change**: `add-brand-management`
- **Iteration**: `sprint-002`

## Bug Readiness

| 文档 | 状态 |
|---|---|
| `bug.md` | done |
| `root-cause.md` | done |
| `workaround.md` | done |
| `acceptance.md` | done |
| `review.md` | approved |

**Readiness:** Ready

## Bug Analysis

| 项 | 结论 |
|---|---|
| 现象 | 品牌页分页与用户管理页不一致；品牌 Logo 选择文件控件与管理端整体设计不一致 |
| 根因 | 管理端分页和图片上传控件未形成统一复用结构，品牌页叠加局部样式导致偏差 |
| 影响 | Web 管理端视觉一致性与 Design System 执行质量 |
| API / DB | 不影响 |

## Change Artifacts

| 文档 | 状态 |
|---|---|
| proposal.md | done |
| design.md | done |
| tasks.md | done |
| acceptance.md | done |
| test-plan.md | done |
| specs/web-client/spec.md | done |

## 视觉验收 Checklist

| # | 检查项 | 结果 | 说明 |
|---|---|---|---|
| 1 | 品牌页分页布局对齐用户管理页 | pass | `/admin/brands` 使用 `page-summary` + `page-right` + `page-buttons` + `page-size-wrap` |
| 2 | 品牌页分页按钮尺寸/圆角/激活态一致 | pass | 复用 `user-management.css` 中 `.pagination` / `.page-btn` / `.page-size` 样式 |
| 3 | 每页显示控件一致 | pass | `select.page-size` 增加 `aria-label="每页显示条数"`，选项文案对齐 `20/50/100 条` |
| 4 | 跳页能力不破坏统一布局 | pass | 移除品牌页独立跳页输入，避免 `page-left` / `brand-pagination-right` 分叉结构 |
| 5 | Logo 上传空态与用户头像上传风格一致 | pass | 使用 `avatar-upload brand-logo-upload` 紧凑表单控件 |
| 6 | Logo 上传预览态不挤压弹窗 | pass | 预览固定 34px，弹窗头尾结构不变 |
| 7 | 原生 file input 不展示默认皮相 | pass | file input 使用 `hidden` 并由 label 按钮触发 |
| 8 | 品牌创建/编辑/Logo 上传功能不回退 | pass | 保持 `uploadBrandLogo` 与 `logo_object_key` 写入；新增组件测试覆盖保存 |

## 验证记录

| 类型 | 命令 / 方式 | 结果 |
|---|---|---|
| 单元/组件测试 | `cd src/web && npx vitest run src/pages/admin src/features/admin` | pass：12 files / 26 tests |
| 生产构建 | `cd src/web && npm run build` | pass；仅保留既有 Tailwind at-rule minify warning |
| 分页对照 | 代码 DOM + Testing Library 断言 | pass：品牌页与用户页分页结构同构 |
| 弹窗对照 | 代码 DOM + Testing Library 断言 | pass：品牌 Logo 上传与用户头像上传同为紧凑行内控件 |

## 归档记录

| 项 | 结果 |
|---|---|
| 归档日期 | 2026-06-25 |
| Spec 同步 | 已同步至 `openspec/specs/web-client/spec.md` |
| 归档目标 | `openspec/changes/archive/2026-06-25-fix-brand-ui-consistency/` |
