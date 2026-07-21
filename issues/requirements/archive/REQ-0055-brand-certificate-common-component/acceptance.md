---
requirement_id: REQ-0055-brand-certificate-common-component
status: done
created_at: 2026-07-19 17:46:26
updated_at: 2026-07-19 19:54:43
owner: product
source: requirement.md
---

# 验收标准

## 功能 AC

- [ ] AC-001 管理端提供品牌证书缩略图组件，接收文件 URL、文件名、MIME Type 和可选尺寸。
- [ ] AC-002 图片证书展示图片缩略图，PDF 证书展示统一 `PDF` 文件占位。
- [ ] AC-003 文件 URL 为空、文件类型未知或图片加载失败时展示统一文件占位，不显示浏览器破图。
- [ ] AC-004 缩略图尺寸稳定，图片加载前后不造成表格行高明显跳动。
- [ ] AC-005 证书信息单元展示证书名称，并在证书编号为空时展示文件名。
- [ ] AC-006 证书信息单元支持可选所属品牌文本，但不得内置品牌筛选、导航或接口调用。
- [ ] AC-007 证书名称、编号、文件名等长文本使用现有管理端列表截断规则，不撑破表格或弹窗布局。
- [ ] AC-008 有效期展示覆盖长期有效、起止日期、仅到期日期和未设置。
- [ ] AC-009 有效状态 Badge 覆盖 `PERMANENT`、`VALID`、`EXPIRING_SOON`、`EXPIRED`、`UNSET`。
- [ ] AC-010 有效状态复用服务端返回字段，前端不作为唯一事实源重新计算状态。
- [ ] AC-011 未知有效状态降级展示原始状态文本，不导致页面渲染失败。
- [ ] AC-012 前台展示状态 Badge 根据 `is_visible` 展示展示中或已隐藏。
- [ ] AC-013 展示状态组件不得内置显示/隐藏接口调用。
- [ ] AC-014 统一预览入口支持由调用方渲染为按钮、链接或缩略图点击。
- [ ] AC-015 图片和 PDF v1 均可通过新窗口打开文件 URL。
- [ ] AC-016 文件 URL 缺失时阻止预览，并返回可由页面展示的失败原因。
- [ ] AC-017 预览失败提示复用 `文件暂时无法预览，请稍后重试或下载查看`。
- [ ] AC-018 文件卡片支持 `idle`、`uploading`、`done`、`failed` 四类状态。
- [ ] AC-019 `idle` 状态展示未上传提示。
- [ ] AC-020 `uploading` 状态展示文件名、进度和保存阻塞提示能力。
- [ ] AC-021 `done` 状态展示缩略图或文件类型、文件名、文件大小、重新上传和删除入口。
- [ ] AC-022 `failed` 状态展示失败原因和重新上传入口。
- [ ] AC-023 文件卡片只负责展示和触发回调，不直接调用上传 API。
- [ ] AC-024 `/admin/brand-certificates` 列表中的“证书”列使用通用证书缩略图与信息单元。
- [ ] AC-025 `/admin/brand-certificates` 列表中的“有效期”“有效状态”“前台展示”列使用通用展示方法或组件。
- [ ] AC-026 新增/编辑证书弹窗中的文件展示区使用或对齐通用文件卡片。
- [ ] AC-027 页面筛选、分页、权限判断、保存、删除、显示/隐藏确认仍保留在页面或业务容器中，不下沉到证书展示组件。
- [ ] AC-028 组件 props 面向展示模型设计，可复用 `BrandCertificateItem` 的窄类型或 `Pick<>`，不暴露页面分页、筛选和弹窗内部状态。
- [ ] AC-029 证书类型、状态 label、日期格式和 PDF 判断继续由统一 helper 提供。
- [ ] AC-030 组件导出路径清晰，后续管理端页面无需从 `BrandCertificateManagementPage.tsx` 复制内部实现。

## UI AC

- [ ] AC-UI-001 视觉延续管理端“工业石材 · 暗色旗舰风”，使用 Design System semantic token。
- [ ] AC-UI-002 新增样式不得包含裸 Hex 或硬编码 token 对应 `rgba(...)`。
- [ ] AC-UI-003 缩略图、文件卡片、Badge 和操作入口在 1440px 管理端列表视口下保持稳定尺寸。
- [ ] AC-UI-004 文件卡片在窄视口下可换行，不遮挡上传、重新上传或删除入口。
- [ ] AC-UI-005 组件内部不呈现“如何使用组件”的说明性文案，只呈现证书业务状态。
- [ ] AC-UI-006 prototype HTML 展示图片、PDF、加载失败、长期有效、即将到期、已过期、隐藏、上传中和上传失败等组件状态。
- [ ] AC-UI-007 PNG Golden Reference 可在后续设计验收时导出；v1 以 `prototype/web/brand-certificate-common-component.html` 和 `prototype/web/prototype-context.md` 为视觉与交互参考。

## API / DB AC

- [ ] AC-API-001 本需求不新增或修改品牌证书 API。
- [ ] AC-API-002 本需求不新增或修改 SQLite/MySQL 表结构、迁移或初始化数据。
- [ ] AC-API-003 本需求不修改 MinIO 单桶策略、上传前缀、文件大小限制或 MIME 白名单。
- [ ] AC-API-004 如后续实现发现组件必须新增 API 字段，必须先回到需求评审或创建独立 follow-up，不得在实现阶段静默扩大范围。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 1440×1024 视口下，品牌证书页在组件化后仍保持用户管理基准分页 DOM：左侧 `page-summary`，右侧 `page-right` 页码和每页条数。
- [ ] AC-XCUT-002 品牌证书页组件化后不得破坏指标卡 DOM，指标卡仍使用 `.metric-label`、`.metric-value`、`.metric-desc`。
- [ ] AC-XCUT-003 证书预览、上传、保存、显示/隐藏、删除等成功/失败反馈使用 fixed toast，不得通过文档流 notice 推挤页面布局。
- [ ] AC-XCUT-004 显示/隐藏、删除等状态或危险操作仍使用 DS confirm modal，代码中不得出现 `window.confirm`。
- [ ] AC-XCUT-005 新增/编辑证书弹窗 TSX 不得同时挂载通用 `modal-card` 与证书专属 modal class。
- [ ] AC-XCUT-006 1440 视口下新增/编辑证书弹窗 Computed width 与 REQ-0038 设计一致，未被其他 admin CSS 覆盖。
- [ ] AC-XCUT-007 矮视口下证书弹窗 body 可滚动，头部和底部固定，无内容被遮挡或按钮不可达。
- [ ] AC-XCUT-008 证书文件卡片必须覆盖 `idle → uploading → done / failed` 状态机，并在控件内展示进度、成功回显和失败原因。
- [ ] AC-XCUT-009 同一会话内上传成功后，列表或弹窗刷新可即时回显证书缩略图或 PDF 文件卡片。
- [ ] AC-XCUT-010 Docker Web 入口 `http://localhost:3000` 下完成证书文件边界上传验收：合法小文件成功，超限文件返回业务错误而非 Nginx 413。
