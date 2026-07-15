---
requirement_id: REQ-0038-brand-certificate-management
status: done
created_at: 2026-07-14 22:41:33
updated_at: 2026-07-15 13:14:13
---

# 验收标准

## 功能 AC

- [ ] AC-001 左侧导航在“瓷砖规格”下方展示“品牌证书”，访问 `/admin/brand-certificates` 时独立高亮“品牌证书”。
- [ ] AC-002 品牌列表页可保留“证书”快捷入口，点击后进入 `/admin/brand-certificates?brand_id={brand_id}` 并自动应用品牌筛选。
- [ ] AC-003 页面展示证书总数、有效证书、即将到期、已过期 4 个指标，点击指标可应用对应有效状态筛选。
- [ ] AC-004 筛选区包含关键词、所属品牌、证书类型、有效状态、展示状态、重置；不存在独立“查询”按钮。
- [ ] AC-005 关键词输入 300ms 防抖生效，下拉筛选变化立即生效，任一筛选变化后页码重置为第 1 页。
- [ ] AC-006 筛选条件同步到 URL Query，刷新页面后仍能恢复当前筛选、页码和每页条数。
- [ ] AC-007 列表展示证书、所属品牌、证书类型、发证机构、有效期、有效状态、前台展示、排序、更新时间和操作。
- [ ] AC-008 图片证书显示缩略图；PDF 显示统一 PDF 文件占位；加载失败显示文件类型占位，不显示破图。
- [ ] AC-009 有效状态由服务端返回，至少覆盖长期有效、有效、即将到期、已过期、未设置有效期。
- [ ] AC-010 底部分页左侧显示 `共 x 个证书`，右侧显示上一页、页码、下一页、每页显示 20/50/100 条，不提供跳页输入框。
- [ ] AC-011 无数据时保留筛选区和新增按钮；首次空状态与筛选无结果状态文案区分。
- [ ] AC-012 新增/编辑弹窗宽度 760px，最大高度 `calc(100vh - 80px)`，头部和底部固定，主体区域可滚动。
- [ ] AC-013 新增/编辑弹窗字段包含所属品牌、证书名称、证书排序、证书类型、证书编号、发证机构、证书文件、长期有效、生效日期、到期日期、前台展示、备注。
- [ ] AC-014 所属品牌、证书名称、证书排序、证书类型、证书文件必填；非长期有效时到期日期必填。
- [ ] AC-015 同一品牌下证书名称不可重复；编辑证书切换所属品牌后按目标品牌重新校验唯一性。
- [ ] AC-016 长期有效开启后清空并禁用生效日期和到期日期；关闭后恢复日期可编辑。
- [ ] AC-017 证书文件支持 JPG、PNG、WebP、PDF，单文件最大 20MB；格式或大小不符合时展示明确错误文案。
- [ ] AC-018 编辑时未更换文件不得重复上传；更换文件后必须取得新的 `file_url` 与 `file_key` 再保存。
- [ ] AC-019 预览支持图片大图和 PDF 新窗口；预览失败时提示 `文件暂时无法预览，请稍后重试或下载查看`。
- [ ] AC-020 显示/隐藏、删除操作均需要二次确认；删除为软删除，并从店主端展示数据中移除。
- [ ] AC-021 权限点控制新增、编辑、显示、隐藏、删除入口；无权限时隐藏或只读，不允许越权提交。
- [ ] AC-022 新增、编辑、显示、隐藏、删除均写入审计记录，至少包含操作人、品牌 ID、证书 ID、操作类型、变更摘要、时间和 IP。
- [ ] AC-023 删除品牌前如存在未删除证书，必须阻止删除或要求先迁移/删除证书。

## API / 数据 AC

- [ ] AC-024 列表接口支持 `keyword`、`brand_id`、`type`、`validity_status`、`display_status`、`page`、`page_size` 查询参数。
- [ ] AC-025 `brand_certificate.brand_id` 必填，一个证书只关联一个品牌；一个品牌可关联多个证书。
- [ ] AC-026 服务端返回统一响应 envelope、标准错误码，并覆盖品牌不存在、名称重复、文件缺失、文件类型非法、文件过大、日期非法、证书不存在。
- [ ] AC-027 API 变更同步 OpenAPI、Orval、接口文档和后端集成测试。
- [ ] AC-028 DB 变更同步 SQLite/MySQL schema、数据库设计文档和迁移/初始化脚本。

## 原型 AC

- [ ] AC-029 UI 实现优先级按 acceptance.md > requirement.md > prototype-context.md > HTML > PNG > rules/ui-design.md；HTML/PNG 中早期品牌摘要栏仅作视觉参考，不作为实现门禁。
- [ ] AC-030 原型文件保留在 `prototype/web/brand-certificate-management.html`、`prototype/web/brand-certificate-management.png`、`prototype/web/prototype-context.md`，正式实现不得直接复制裸 Hex。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 1440×1024 视口下，品牌证书页分页 DOM 与用户管理基准一致：左侧 `page-summary`，右侧 `page-right` 页码和每页条数。
- [ ] AC-XCUT-002 指标卡 DOM 使用 `.metric-label`、`.metric-value`、`.metric-desc`，不得只用裸 `strong` 或 `span` 承载数值与说明。
- [ ] AC-XCUT-003 操作成功/失败反馈使用 fixed toast，不得通过文档流 notice 推挤页面、指标卡或表格布局。
- [ ] AC-XCUT-004 显示/隐藏、删除等状态或危险操作必须使用 DS confirm modal，代码中不得出现 `window.confirm`。
- [ ] AC-XCUT-005 新增/编辑证书弹窗 TSX 只能挂载业务专属 modal class，不得同时挂载通用 `modal-card` 与专属类。
- [ ] AC-XCUT-006 在 1440 视口验收新增/编辑证书弹窗 Computed width 为 760px，且未被其他 admin CSS 覆盖。
- [ ] AC-XCUT-007 矮视口下弹窗 body 可滚动，头部和底部固定，无内容被遮挡或按钮不可达。
- [ ] AC-XCUT-008 证书文件上传控件必须覆盖 `idle → uploading → done / failed` 状态机，并在控件内展示进度、成功回显和失败原因。
- [ ] AC-XCUT-009 同一会话内上传成功后，列表或弹窗刷新可即时回显证书缩略图或 PDF 文件卡片。
- [ ] AC-XCUT-010 Docker Web 入口 `http://localhost:3000` 下完成边界文件上传验收：合法小文件成功，超限文件返回业务错误而非 Nginx 413。
