---
change_id: fix-admin-banner-image-preview-cropped
type: fix
status: applied
created_at: 2026-07-22 09:24:00
updated_at: 2026-07-22 09:31:04
source_bug: BUG-0080-admin-banner-image-preview-cropped
related_requirement: REQ-0016-banner-management
sprint: sprint-010
---

# Trace

## 来源

| 类型 | ID | 说明 |
|---|---|---|
| BUG | BUG-0080-admin-banner-image-preview-cropped | 管理端 Banner 列表和弹窗中 Banner 图片显示不全 |
| REQ | REQ-0016-banner-management | Banner 管理能力 |

## 范围

| 项目 | 说明 |
|---|---|
| 终端 | Web 管理端 |
| 页面 | `/admin/banners` |
| 能力 | Banner 管理图片预览 |
| API | 不涉及 |
| DB | 不涉及 |
| Orval | 不涉及 |

## 状态记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-22 09:24:00 | /bug-opsx | 从 BUG-0080 创建 OpenSpec Change |
| 2026-07-22 09:27:33 | /sprint-propose | 纳入 sprint-010 正式范围 |
| 2026-07-22 09:31:04 | /opsx-apply | 调整 Banner 列表缩略图、弹窗上传预览、来源缩略图为完整图片预览，并补充前端回归测试 |

## 验证记录

| 项目 | 结果 |
|---|---|
| 代码路径 | `src/web/src/features/admin/styles/banner-management.css`、`src/web/src/features/admin/components/BannerFormModal.test.tsx` |
| 前端测试 | `pnpm --dir src/web test BannerFormModal.test.tsx BannerManagementPage.test.tsx` 通过，2 个测试文件、10 个用例通过 |
| 预览策略 | `.banner-thumb`、`.banner-upload-preview`、`.banner-source-thumb` 统一使用居中容器与 `object-fit: contain`，避免裁切图片主体 |
| 业务回归 | 聚焦测试覆盖 Banner 新建/编辑弹窗、保存流程、上线/下线、排序与跳转类型相关页面逻辑；本次未修改 API、DB、对象存储与 Orval |
| 知识沉淀 | 本缺陷为局部管理端样式回归，已由 change trace 与前端测试覆盖，不新增 `docs/knowledge-base/incidents/` 事故文档 |
