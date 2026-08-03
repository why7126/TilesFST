---
change_id: fix-admin-certificate-list-main-image-name-only
type: fix
status: proposed
source_bug: BUG-0107-admin-certificate-list-main-image-name-only
created_at: 2026-08-03 08:33:06
updated_at: 2026-08-03 08:33:06
---

# Proposal: 修复管理后台证书列表证书字段文件名噪音

## 背景与原因

`BUG-0107-admin-certificate-list-main-image-name-only` 已评审通过。管理后台证书列表的证书字段除了证书主图和证书名称外，还额外显示图片名称、文件名称、对象 key 或原始 URL 等上传相关信息，造成列表展示噪音，并暴露不应面向业务用户的上传实现细节。

## 变更内容

- 修复 `/admin/brand-certificates` 证书列表的证书字段渲染。
- 证书字段只展示证书主图和证书名称。
- 无主图时展示稳定占位，证书名称仍清晰可读。
- 禁止在列表证书字段展示图片名称、文件名称、对象 key、原始 URL 或上传控件内部文案。
- 补充管理端品牌证书列表回归测试，覆盖 `BUG-0107` 和关联 `BUG-0089` 不回归。

## 影响范围

- 影响范围：Web 管理端品牌证书列表。
- 不影响 API 响应结构、数据库结构、权限边界、Orval 生成接口或 MinIO 对象存储策略。
- 不改变证书新增/编辑弹窗上传状态机，仅约束列表浏览场景的展示边界。

## 回滚方案

- 若修复导致证书列表主图或证书名称不可见，可回滚本 Change 的前端列表渲染改动。
- 回滚后保留既有 API、数据库和对象存储数据，无需数据迁移。
- 回滚前后均需确认新增/编辑弹窗上传和预览能力不受影响。
