---
title: Change Trace
purpose: fix-brand-image-display-layout-shift 追溯记录
change_id: fix-brand-image-display-layout-shift
bug_id: BUG-0003-brand-image-display-layout-shift
status: archived
created_at: 2026-06-25 22:28:15
applied_at: 2026-06-25 22:41:42
archived_at: 2026-06-26 08:43:24
---

# Trace

## 1. 来源

| 项目 | 内容 |
|---|---|
| BUG | `issues/bugs/BUG-0003-brand-image-display-layout-shift` |
| Sprint | `sprint-002` |
| 严重等级 | high |
| 评审 | `REV-BUG-0003-001`，approved |

## 2. Bug Analysis Report

| 维度 | 结论 |
|---|---|
| 现象 | 品牌 Logo 上传后列表/编辑弹窗不显示；状态 Tips 出现/消失导致页面上下波动 |
| 复现 | 上传 Logo 保存后查看列表与编辑弹窗；执行启用/停用后观察 Tips |
| 根因分类 | code / frontend-ui / media-routing |
| 关联需求 | `REQ-0005-brand-management` |
| 关联 Change | `add-brand-management`、`fix-brand-ui-consistency` |
| 修复 Change | `fix-brand-image-display-layout-shift` |

## 3. 验收映射

| BUG AC | OpenSpec 覆盖 |
|---|---|
| AC-001 | `brand-management/spec.md` 品牌 Logo 可访问媒体 URL |
| AC-002 | `web-client/spec.md` 品牌列表 Logo 展示 |
| AC-003 | `web-client/spec.md` 品牌编辑弹窗 Logo 回显 |
| AC-004/AC-005 | `web-client/spec.md` 品牌页状态提示不推挤主体 |
| AC-006 | `brand-management/spec.md` 媒体安全与对象存储 |
| AC-007 | `web-client/spec.md` 品牌既有功能不回退 |
| AC-008 | `tasks.md` 与 `test-plan.md` |
| AC-009 | `web-client/spec.md` Design System 约束 |

## 4. Checklist

- [x] 通过 OpenSpec CLI 创建 change
- [x] proposal.md 包含 Why / Impact / Rollback Plan
- [x] design.md 包含根因、修复方案、测试策略
- [x] specs 覆盖品牌媒体访问与 Web 提示布局
- [x] tasks.md 包含回归测试和知识库提醒
- [x] `/opsx-apply fix-brand-image-display-layout-shift`
- [x] `/opsx-archive fix-brand-image-display-layout-shift`

## 5. 实施记录

| 范围 | 结论 |
|---|---|
| 后端媒体访问 | 新增受控 `/media/{object_key}` 读取入口，上传文件写入 `UPLOAD_DIR`，object_key 使用 UUID 与业务前缀生成 |
| 品牌 Logo URL | `UploadResult.url` 与 `BrandAdminItem.logo_url` 仍为 `/media/{object_key}`，schema 未变化 |
| 安全校验 | 拒绝空路径、绝对路径、反斜杠、重复分隔符、`.` / `..` 路径段；保留 JPG/PNG/WebP MIME 校验和 admin/employee 鉴权 |
| Web 列表与弹窗 | 列表和编辑弹窗均渲染后端 URL；无 Logo 或图片加载失败时显示固定尺寸占位 |
| Tips 布局 | 品牌页状态提示改为固定定位 `.admin-toast-region`，不插入主体文档流 |
| API / Orval | 响应字段未变化，未执行 Orval |
| 数据库 | 未新增或修改数据库字段 |
| 长期文档 | 本 change 仅补齐当前开发存储与 `/media` 代理闭环，未形成 MinIO 生产策略变更，暂不更新长期媒体文档 |

## 6. 扩散风险

| 页面 | 发现 | 本次处理 |
|---|---|---|
| 用户管理 | 仍存在文档流 `admin-notice` | 记录风险，不扩大修复面 |
| 类目管理 | 仍存在文档流 `admin-notice` | 记录风险，不扩大修复面 |
| SKU 管理 | 仍存在文档流 `admin-notice` | 记录风险，不扩大修复面 |
| SKU 表单 | 表单内错误仍使用 inline notice | 保持可访问的表单内错误，不影响品牌列表主体 |

## 7. 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-06-25 22:40:15 | `pytest src/backend/tests/test_admin_brands.py` | 15 passed |
| 2026-06-25 22:40:15 | `./node_modules/.bin/vitest run src/pages/admin/BrandManagementPage.test.tsx src/features/admin/components/BrandFormModal.test.tsx` | 2 files / 5 tests passed |
| 2026-06-25 22:41:42 | `./node_modules/.bin/vite build` | passed；保留项目既有 lightningcss unknown at-rule warnings |
| 2026-06-25 22:41:42 | `openspec validate fix-brand-image-display-layout-shift --strict` | passed |
| 2026-06-25 22:41:42 | `python scripts/validate-directory-structure.py` | failed；根目录存在既有未登记项 `.cursor`、`.env`、`.codex`、`.agents` 等，非本次修复新增 |
| 2026-06-26 08:43:24 | `openspec archive fix-brand-image-display-layout-shift -y` | synced specs；archived to `openspec/changes/archive/2026-06-26-fix-brand-image-display-layout-shift/` |

## 8. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-25 22:28:15 | `/bug-opsx` | 创建 `fix-brand-image-display-layout-shift` OpenSpec Change |
| 2026-06-25 22:41:42 | `/opsx-apply` | 完成媒体访问、品牌 Logo 展示、品牌页 Tips 非位移修复与回归测试 |
| 2026-06-26 08:43:24 | `/opsx-archive` | 同步 `brand-management` 与 `web-client` 正式 spec，并归档 change |
