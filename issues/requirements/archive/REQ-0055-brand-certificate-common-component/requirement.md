---
requirement_id: REQ-0055-brand-certificate-common-component
title: 生成品牌证书通用组件
terminal: web-admin
module: 管理后台 / 主数据 / 品牌证书 / 业务组件
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement: REQ-0038-brand-certificate-management
created_at: 2026-07-19 17:42:38
updated_at: 2026-07-19 19:54:43
---

# REQ-0055 生成品牌证书通用组件

## 1. 背景

`REQ-0038` 已交付管理后台品牌证书管理页，页面内已经包含证书缩略图、PDF 文件占位、有效期展示、有效状态 Badge、前台展示状态、文件预览和上传文件卡片等能力。随着品牌证书后续可能出现在证书列表、品牌详情快捷区、弹窗文件回显或其他后台页面中，如果继续在页面内复制展示逻辑，容易造成视觉、状态文案和异常处理不一致。

本需求将品牌证书展示与文件状态相关逻辑沉淀为管理端业务通用组件，优先服务现有 `/admin/brand-certificates` 页面，减少重复实现，并为后续店主 Web 或小程序展示能力保留清晰的上移边界。

## 2. 目标用户

| 用户 | 核心诉求 |
|---|---|
| 运营人员 | 在证书管理和品牌相关页面中获得一致的证书识别、预览和状态展示体验 |
| 管理端开发者 | 复用证书缩略图、状态 Badge、文件卡片和预览入口，避免重复拼装 UI 与判断逻辑 |
| 产品/验收人员 | 用统一组件验收证书图片、PDF、过期、隐藏、加载失败等状态，降低回归成本 |

## 3. 范围

### 3.1 包含

- 管理端品牌证书缩略图组件：图片缩略图、PDF 占位、文件占位、加载失败 fallback。
- 管理端品牌证书信息单元：证书名称、证书编号或文件名、所属品牌可选展示。
- 管理端品牌证书有效期展示：长期有效、日期区间、未设置等文案。
- 管理端品牌证书有效状态 Badge：长期有效、有效、即将到期、已过期、未设置。
- 管理端品牌证书展示状态 Badge：前台展示、前台隐藏。
- 管理端品牌证书预览入口：图片和 PDF 预览行为统一封装，预览失败提供兜底提示能力。
- 管理端品牌证书文件卡片：用于新增/编辑弹窗内展示未上传、上传中、已就绪、失败等文件状态。
- 现有品牌证书管理页对上述组件的替换应用。

### 3.2 不包含

- 不新增品牌证书管理 API、数据库字段或上传接口。
- 不新增店主 Web 品牌详情证书展示页。
- 不新增微信小程序证书展示组件。
- 不新增证书审批、OCR 识别、证书真伪校验、电子签章或批量操作。
- 不改变 `REQ-0038` 已定义的证书类型、有效状态和上传限制。
- 不将组件直接承诺为跨端共享组件；v1 先作为管理端业务组件沉淀。

## 4. 组件定位

```text
REQ-0038 品牌证书管理页（已完成）
  └─ REQ-0055 品牌证书通用组件（本需求）
      ├─ CertificateThumb
      ├─ CertificateSummary
      ├─ CertificateValidityBadge
      ├─ CertificateVisibilityBadge
      ├─ CertificatePreviewAction
      └─ CertificateFileCard
```

组件 SHOULD 优先落在管理端业务组件目录，复用现有品牌证书展示 helper。只有当店主 Web 或小程序出现真实复用诉求，并且字段、交互和视觉语义稳定后，才评估迁入跨端共享业务组件层。

## 5. 功能要求

### FR-001 证书缩略图组件

- 组件 MUST 接收证书文件 URL、文件名、MIME Type 和可选展示尺寸。
- 图片证书 MUST 展示图片缩略图，并提供空 `alt` 或由调用方传入的可访问描述。
- PDF 证书 MUST 展示统一 `PDF` 文件占位，不尝试在前端生成 PDF 首图。
- 文件 URL 为空、文件类型未知或图片加载失败时 MUST 展示统一文件占位，不显示浏览器破图。
- 缩略图尺寸 MUST 稳定，避免图片加载前后造成表格行高跳动。

### FR-002 证书信息单元

- 组件 MUST 支持展示证书名称作为主文本。
- 组件 SHOULD 支持展示证书编号；证书编号为空时展示文件名。
- 组件 MAY 支持所属品牌名称作为附加文本，但不得强耦合品牌筛选或导航行为。
- 文本超长时 MUST 使用现有管理端列表文本截断规则，不撑破表格或弹窗布局。

### FR-003 有效期与有效状态

- 组件 MUST 复用服务端返回的有效状态，不在前端作为唯一事实源重新计算。
- 有效期展示 MUST 覆盖长期有效、起止日期、仅到期日期、未设置等状态。
- 有效状态 Badge MUST 覆盖 `PERMANENT`、`VALID`、`EXPIRING_SOON`、`EXPIRED`、`UNSET`。
- 已过期、即将到期、未设置等状态 MUST 使用管理端既有 Badge 语义，不新增裸 Hex 颜色。
- 未知状态 MUST 降级展示原始状态文本，不导致页面渲染失败。

### FR-004 前台展示状态

- 组件 MUST 支持根据 `is_visible` 展示前台展示或前台隐藏。
- 展示状态 Badge MUST 与管理端现有启用/禁用视觉语义一致。
- 组件不得内置显示/隐藏接口调用；状态切换动作仍由页面或业务容器负责。

### FR-005 预览入口

- 组件 MUST 提供统一预览触发能力，由调用方决定渲染为按钮、链接或缩略图点击。
- 图片和 PDF v1 均可通过新窗口打开文件 URL。
- 文件 URL 缺失时 MUST 阻止预览，并返回可由页面展示的失败原因。
- 预览失败文案 SHOULD 复用 `文件暂时无法预览，请稍后重试或下载查看`。
- 组件不得绕过后端鉴权或生成未授权对象存储直连地址。

### FR-006 文件卡片状态

- 文件卡片 MUST 支持 `idle`、`uploading`、`done`、`failed` 四类状态。
- `idle` 状态展示未上传提示。
- `uploading` 状态展示文件名、进度和禁用保存提示能力。
- `done` 状态展示缩略图或文件类型、文件名、文件大小、重新上传和删除入口。
- `failed` 状态展示失败原因和重新上传入口。
- 文件卡片只负责展示和触发回调，不直接调用上传 API。

### FR-007 现有页面应用

- `/admin/brand-certificates` 列表中的“证书”列 MUST 使用通用证书缩略图与信息单元。
- 列表中的“有效期”“有效状态”“前台展示”列 MUST 使用通用展示方法或组件。
- 新增/编辑证书弹窗中的文件展示区 SHOULD 使用通用文件卡片。
- 页面筛选、分页、权限判断、保存、删除、显示/隐藏确认仍保留在页面或现有容器中，不下沉到证书展示组件。

### FR-008 组件契约与导出

- 组件 props MUST 面向展示模型设计，避免直接暴露页面筛选、分页或弹窗内部状态。
- 组件 SHOULD 复用 `BrandCertificateItem` 或更窄的 `Pick<>` 类型，减少与完整 API 模型的耦合。
- 证书类型、状态 label、日期格式和 PDF 判断 SHOULD 继续由现有 helper 统一提供。
- 管理端业务组件导出路径 SHOULD 清晰，便于后续页面复用。

## 6. UI 约束

- 视觉 MUST 延续管理端“工业石材 · 暗色旗舰风”和现有 Design System semantic token。
- 组件不得新增裸 Hex 颜色；新增样式必须使用已有 semantic token 或现有管理端 Badge / 文本 / 边框语义。
- 缩略图、文件卡片、Badge 和操作入口 MUST 在 1440px 管理端列表视口下保持稳定尺寸。
- 组件不得使用 `window.confirm`；涉及确认的行为仍交由页面现有 DS confirm modal 处理。
- 文件卡片在窄视口下 MUST 可换行，不遮挡上传、重新上传或删除入口。
- 组件内部文本不得出现用于解释组件如何使用的说明性文案，只呈现业务状态。

## 7. 关联需求

- `REQ-0038-brand-certificate-management`：父需求，已交付品牌证书管理页，本需求从中沉淀通用组件。
- `REQ-0005-brand-management`：品牌主数据能力，品牌证书通过品牌关系服务品牌可信资料维护。

## 8. 状态块

```yaml
requirement_id: REQ-0055-brand-certificate-common-component
status: done
terminal: web-admin
version: v1
source: capture.md
priority: P1
parent_requirement: REQ-0038-brand-certificate-management
scope_summary: 管理端品牌证书缩略图、状态 Badge、有效期展示、预览入口、文件卡片和现有品牌证书管理页组件化应用
excluded_scope:
  - 新增或修改品牌证书 API
  - 新增或修改数据库结构
  - 店主 Web 品牌详情证书展示
  - 微信小程序证书展示组件
  - 证书审批、OCR、真伪校验、电子签章
next: /req-opsx REQ-0055-brand-certificate-common-component
```
