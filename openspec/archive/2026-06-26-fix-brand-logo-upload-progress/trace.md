---
title: Change Trace
purpose: fix-brand-logo-upload-progress 追溯记录
change_id: fix-brand-logo-upload-progress
bug_id: BUG-0004-brand-logo-upload-progress-missing
status: applied
created_at: 2026-06-26 09:39:00
applied_at: 2026-06-26 09:47:15
---

# Trace

## 1. 来源

| 项目 | 内容 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0004-brand-logo-upload-progress-missing` |
| Sprint | `sprint-002` |
| 严重等级 | medium |
| 评审 | `REV-BUG-0004-001`，approved |
| 父需求 | `REQ-0005-brand-management` |

## 2. Bug Analysis Report

| 维度 | 结论 |
|---|---|
| 现象 | 编辑品牌弹窗选择新 Logo 后缺少上传反馈，Logo 预览不更新 |
| 复现 | 打开品牌编辑弹窗 → 点击「更换 Logo」→ 选择图片 → 观察上传状态与预览 |
| 根因分类 | frontend-upload / preview-state / progress-feedback |
| 关联 BUG | `BUG-0003-brand-image-display-layout-shift` |
| 修复 Change | `fix-brand-logo-upload-progress` |

## 3. 验收映射

| BUG AC | OpenSpec 覆盖 |
|---|---|
| AC-001 | `web-client/spec.md` 选择 Logo 后触发上传 |
| AC-002 | `web-client/spec.md` 上传过程中展示进度反馈 |
| AC-003 | `web-client/spec.md` 上传成功后更新预览和保存对象 Key |
| AC-004 | `web-client/spec.md` 上传失败可见且可重试 |
| AC-005 | `web-client/spec.md` 同一文件可重新选择 |
| AC-006 | `web-client/spec.md` 品牌管理功能不回退 |
| AC-007 | `tasks.md` 媒体与权限安全 |
| AC-008 | `tasks.md` 测试覆盖 |
| AC-009 | `web-client/spec.md` Design System 约束 |

## 4. Checklist

- [x] 通过 OpenSpec CLI 创建 change
- [x] proposal.md 包含 Why / Impact / Rollback Plan
- [x] design.md 包含根因、修复方案、测试策略
- [x] specs 覆盖品牌 Logo 上传进度反馈
- [x] tasks.md 包含回归测试和知识库提醒
- [x] `/opsx-apply fix-brand-logo-upload-progress`
- [ ] `/opsx-archive fix-brand-logo-upload-progress`

## 5. 实现记录

| 文件 | 说明 |
|---|---|
| `src/web/src/features/admin/api/brands-api.ts` | 为品牌 Logo 上传封装增加可选 `onUploadProgress` 回调，复用既有 Orval 方法与响应结构 |
| `src/web/src/features/admin/components/BrandFormModal.tsx` | 增加 `idle/uploading/uploaded/failed` 上传状态、进度条、成功预览、失败提示、同文件重选 reset 与上传中保存保护 |
| `src/web/src/features/admin/styles/brand-management.css` | 增加品牌 Logo 上传进度与状态样式，使用既有 admin token，无裸 Hex |
| `src/web/src/features/admin/components/BrandFormModal.test.tsx` | 覆盖进度反馈、成功预览并保存最新 object_key、失败重试、同文件重选 |

## 6. 验证记录

| 命令 | 结果 |
|---|---|
| `cd src/web && ./node_modules/.bin/vitest run src/features/admin/components/BrandFormModal.test.tsx src/pages/admin/BrandManagementPage.test.tsx` | 2 files / 7 tests passed |
| `cd src/web && ./node_modules/.bin/vite build` | success；存在项目既有 lightningcss Tailwind at-rule warning |

## 7. 影响评估

| 影响面 | 结论 |
|---|---|
| API schema | 未改变；仅前端 API 封装透传 Axios 进度回调 |
| Orval | 不需要执行 |
| 数据库 | 无影响 |
| 后端 | 无变更 |
| Web 管理端 | 品牌编辑弹窗 Logo 上传体验修复 |
| 小程序 / 店主端 | 无影响 |
| Docker Compose | 本次未启动运行时；Web build 已通过 |
| 知识库 | 不属于生产事故，无需新增 `docs/knowledge-base/incidents/` |

## 8. 变更记录

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-06-26 09:39:00 | `/bug-opsx` | 创建 `fix-brand-logo-upload-progress` OpenSpec Change |
| 2026-06-26 09:47:15 | `/opsx-apply` | 完成品牌 Logo 上传状态机、进度反馈、预览更新、失败重试与回归测试 |
