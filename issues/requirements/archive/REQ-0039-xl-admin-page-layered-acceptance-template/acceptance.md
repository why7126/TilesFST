---
title: 需求验收标准
purpose: REQ-0039 XL 管理端页面分层验收模板验收标准
content: 功能 AC 与知识库横切 AC
source: requirement.md + docs/knowledge-base best-practices
owner: product
status: done
created_at: 2026-07-16 09:06:14
updated_at: 2026-07-16 09:37:04
---

# 验收标准

## 1. 模板范围与落点

- [ ] **AC-001** 模板 MUST 明确 “XL 管理端页面” 指字段多、链路长、可能跨 DB/API/上传/Web/Docker 多层的复杂管理端页面，而非某个具体页面。
- [ ] **AC-002** 模板 SHOULD 沉淀到长期治理位置，优先 `docs/standards/`；若最终选择其他位置，MUST 在 Change design 中说明原因。
- [ ] **AC-003** 模板 MUST 可被后续 REQ `acceptance.md`、OpenSpec Change `acceptance.md`、`tasks.md` 或验收报告引用。
- [ ] **AC-004** 本 REQ 不直接修改 `src/`、DB/API、上传、Orval、Docker 或具体管理端页面。

## 2. 层级矩阵与状态字段

- [ ] **AC-005** 模板 MUST 包含 DB、API、上传、Orval、Web、Docker、横切 UI 七层 gate。
- [ ] **AC-006** 每层 gate MUST 支持 `required | not_applicable | passed | failed | blocked` 等状态。
- [ ] **AC-007** 每层 gate MUST 提供 owner、evidence、N/A reason、remaining risk 等字段。
- [ ] **AC-008** N/A 不得留空；每个 N/A MUST 写明“不涉及该层”的具体原因。

## 3. DB/API/上传/Orval gate

- [ ] **AC-009** DB gate MUST 覆盖表结构、迁移、SQLite/MySQL 差异、Pydantic Schema、Repository/Service、数据库文档和测试。
- [ ] **AC-010** API gate MUST 覆盖接口路径、方法、权限、请求、响应、统一 envelope、错误码、OpenAPI、接口文档和集成测试。
- [ ] **AC-011** 上传 gate MUST 覆盖后端授权上传、MIME/大小限制、对象 key、MinIO 单桶前缀、失败态、即时回显和 Nginx/Docker 边界。
- [ ] **AC-012** Orval gate MUST 明确 API contract 变化时导出 OpenAPI 并运行 Orval；无 contract 变化时记录 Orval N/A 原因。

## 4. Web/Docker/UI gate

- [ ] **AC-013** Web gate MUST 覆盖路由、权限、列表、筛选、表格、分页、表单、弹窗、抽屉、loading/empty/error 和前端测试。
- [ ] **AC-014** Docker gate MUST 覆盖 compose、Dockerfile、Nginx、环境变量、MinIO、Web 代理和 `localhost:3000` 入口验证判定。
- [ ] **AC-015** 横切 UI gate MUST 覆盖 semantic token、DS modal、fixed toast、无裸 Hex、无布局抖动、移动/窄屏关键视口。
- [ ] **AC-016** 模板 MUST 要求复杂页面至少记录桌面视口和一个窄屏/移动视口的 UI 验收策略；具体视口可按页面风险扩展。

## 5. 验收证据与输出控制

- [ ] **AC-017** 模板 MUST 要求记录命令、测试结果、截图、接口响应或 Docker 验证的摘要证据。
- [ ] **AC-018** 模板 MUST 禁止在验收证据中复制完整 OpenAPI、Orval 生成物、大段测试日志、密钥、真实环境变量或本机绝对路径。
- [ ] **AC-019** 后续 Change 使用模板时，MUST 在 trace 或验收报告中记录 failed/blocked gate 的后续处理方式。
- [ ] **AC-020** 模板 MUST 明确若某层 gate 从 N/A 变为 required，应回到 PRD/Change 范围确认，避免实现阶段悄悄扩大范围。

## 6. 原型与可用性

- [ ] **AC-021** 本 REQ 的 prototype 可采用模板预览 HTML + context.md，用于说明层级矩阵和 gate 字段，不要求 PNG Golden Reference。
- [ ] **AC-022** 模板预览 MUST 体现管理端工作型信息密度，避免营销式 hero 或无关视觉装饰。
- [ ] **AC-023** 模板文档 MUST 保持可复制、可扫描，优先使用表格、短检查项和明确 N/A 字段。

## 7. 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-form-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003/007 复发类缺陷。

- [ ] **AC-XCUT-001** 模板的 admin-list gate MUST 要求新增列表页分页 DOM 对齐用户管理基准：左侧 `page-summary`，右侧 `page-right` 页码与每页条数。
- [ ] **AC-XCUT-002** 模板的 admin-list gate MUST 要求摘要指标卡使用 `.metric-label` / `.metric-value` / `.metric-desc` 或等价共享结构。
- [ ] **AC-XCUT-003** 模板的 admin-list gate MUST 要求操作成功/失败反馈使用 fixed toast 或等价固定反馈区域，不得造成 hero、筛选区或表格 layout shift。
- [ ] **AC-XCUT-004** 模板的 admin-list gate MUST 要求启停、冻结、上架/下架、删除、重置密码等状态/危险操作使用 DS confirm modal，且无 `window.confirm`。
- [ ] **AC-XCUT-005** 模板的 admin-form gate MUST 要求表单页全页仅保留一个主要保存 CTA，位于表单 footer 或等价固定操作区。
- [ ] **AC-XCUT-006** 模板的 admin-form gate MUST 要求页头 hero 不重复渲染保存按钮；若存在页头摘要，只承载说明或状态。
- [ ] **AC-XCUT-007** 模板的 admin-form gate MUST 要求恢复默认、dirty Tab 切换、取消修改等风险操作使用 DS modal，且无 `window.confirm` / `window.alert`。
- [ ] **AC-XCUT-008** 模板的 admin-form gate MUST 要求保存成功/失败反馈使用 fixed toast 或等价固定反馈，不得在 summary 与主表单之间插入造成 layout shift 的块级提示。
- [ ] **AC-XCUT-009** 模板的 admin-modal gate MUST 要求业务弹窗 TSX className 不得同时挂载通用 `modal-card` 与专属类。
- [ ] **AC-XCUT-010** 模板的 admin-modal gate MUST 要求宽弹窗/窄弹窗验收 computed width 或等价运行时宽度，不得只检查源 CSS。
- [ ] **AC-XCUT-011** 模板的 admin-modal gate MUST 要求矮视口下弹窗 body 可滚动，头部关闭按钮与底部主操作按钮可访问。
- [ ] **AC-XCUT-012** 模板的 media-upload gate MUST 要求上传控件覆盖 `idle -> uploading -> done / failed` 状态机。
- [ ] **AC-XCUT-013** 模板的 media-upload gate MUST 要求同会话上传成功后即时回显缩略图、文件卡片或可访问 URL，不要求刷新页面。
- [ ] **AC-XCUT-014** 模板的 media-upload gate MUST 要求上传失败信息展示在控件附近或字段组内，不得只依赖全局 toast。
- [ ] **AC-XCUT-015** 模板的 media-upload gate MUST 要求含上传能力的 Change 经 Docker Web `http://localhost:3000` 验证边界文件；若具体页面无上传，标记 `N/A — 页面不含上传控件或上传链路`。
- [ ] **AC-XCUT-016** 后续 `/req-opsx` 的 `design.md` MUST 引用 trace 中的 `knowledge_base_refs`，并说明每个横切标签如何落实或 N/A。
