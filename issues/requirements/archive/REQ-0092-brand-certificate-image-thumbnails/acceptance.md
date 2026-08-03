---
requirement_id: REQ-0092-brand-certificate-image-thumbnails
title: 品牌图片与证书图片真实缩略图生成与使用 - 验收标准
acceptance_status: passed
owner: product
source: requirement.md
created_at: 2026-08-02 17:55:40
updated_at: 2026-08-02 19:32:35
---

# REQ-0092 验收标准

## 功能 AC

- [ ] AC-001 新上传品牌图片后生成真实缩略图，缩略图像素尺寸或文件体积明显低于原图，且不是原图 bytes 复制品。
- [ ] AC-002 新上传证书图片后生成真实缩略图，证书列表、证书卡片和默认证书主图可优先使用缩略图。
- [ ] AC-003 PDF 或非图片证书不被错误进入图片缩略图生成流程，继续使用文件类型占位或既有 PDF 占位策略。
- [ ] AC-004 品牌列表 Logo、品牌编辑小预览、证书列表封面、证书卡片、小程序品牌/证书展示、店主 Web 品牌/证书展示均明确小图优先缩略图。
- [ ] AC-005 点击大图预览、证书预览或原文件查看时使用原图或原文件，不因缩略图替代而降低预览质量。
- [ ] AC-006 缩略图不存在、生成失败、读取失败或对象损坏时，可安全回退原图或占位图，并记录可定位的失败信息。
- [ ] AC-007 管理端、小程序和店主 Web 不直连未授权对象存储，继续通过后端受控 `/media/{object_key}` 或等价链路读取媒体。
- [ ] AC-008 小图、横图、竖图、PNG 透明图、WebP、损坏图片、超大图片和非允许 MIME 均有明确处理策略和回归样例。
- [ ] AC-009 横图和竖图缩略图保持比例，不出现拉伸变形。
- [ ] AC-010 PNG 透明图缩略图不产生明显黑底或白底误差；若后续采用转码策略，必须在设计中说明。
- [ ] AC-011 存量品牌图片和证书图片补齐方案支持 dry-run，输出待处理数量、预计生成数量、跳过原因和风险提示。
- [ ] AC-012 存量补齐 apply 可审计、可重入，输出成功、失败、跳过和重试统计。
- [ ] AC-013 存量补齐和审计输出不得泄露真实密钥、本机绝对路径、真实客户数据、Cookie、Authorization header 或 `.env` 内容。
- [ ] AC-014 若实现新增或显式化 thumbnail URL / object_key 字段，必须同步 OpenAPI、Orval、API 文档和相关测试；若复用现有媒体字段，也必须在 Change 设计中说明不需要 Orval 的原因。
- [ ] AC-015 若实现新增图片处理依赖或 Docker 镜像层变更，必须同步部署/镜像文档，并保留容器内依赖导入或缩略图生成验证摘要。
- [ ] AC-016 小程序侧至少完成静态或 DevTools evidence；真机/体验版 evidence 如无法在本 Change 阶段补齐，必须进入 release-prepare 检查清单，不得写作已真机通过。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷。

- [ ] AC-XCUT-001 管理端品牌列表与证书列表如调整列表 DOM，分页必须对齐用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [ ] AC-XCUT-002 管理端列表中缩略图加载成功、失败或回退提示不得造成 hero、筛选区、表格或卡片纵向位移；成功/失败反馈使用 fixed toast 或控件内错误。
- [ ] AC-XCUT-003 管理端列表若涉及启停、删除、重生成、批量补齐等危险或状态变更操作，必须使用 Design System confirm modal，禁止 `window.confirm`。
- [ ] AC-XCUT-004 管理端筛选区如新增或调整图片状态、缩略图状态等筛选控件，必须复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper，并覆盖 open/select/clear/reset、禁用态、空态、加载态和 query 语义。
- [ ] AC-XCUT-005 品牌或证书上传弹窗 TSX 禁止同时挂载通用 `modal-card` 与业务专属 modal 类；若修改弹窗宽度，必须验证 computed width 与设计一致。
- [ ] AC-XCUT-006 品牌或证书上传弹窗在矮视口下 body scroll 不回归，上传成功态、失败态、文件卡片和预览区域不遮挡底部操作按钮。
- [ ] AC-XCUT-007 品牌图片和证书图片上传控件必须覆盖 `idle -> uploading -> done/failed` 状态机，失败原因展示在上传控件或字段组内，不只依赖全局 toast。
- [ ] AC-XCUT-008 上传成功后，同一会话内品牌 Logo、证书图片缩略图或文件卡片必须即时回显；刷新列表或重新打开弹窗后仍可展示。
- [ ] AC-XCUT-009 含上传边界的实现必须经 Docker Web `http://localhost:3000` 用户入口验证边界文件；小文件成功返回 object_key，超限文件返回业务错误而不是 Nginx 413。
- [ ] AC-XCUT-010 媒体链路验收必须覆盖对象 key、对象存在性、后端 `/media/` URL 可访问、缩略图真实尺寸/体积收益和小程序或店主端渲染 evidence。
- [ ] AC-XCUT-011 存量脚本或审计命令必须具备 dry-run、apply、幂等性和统计摘要，且不把 `data/uploads/` 作为新上传通过证据。
- [ ] AC-XCUT-012 小程序媒体展示 evidence 可作为发布前补证项，但缺证时必须标记为待补证或 blocked，不得用 Web 静态测试替代真机通过结论。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-02 19:32:35
accepted_by: workflow-sync
source_change: add-brand-certificate-image-thumbnails
source_sprint: sprint-017
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

