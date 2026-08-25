---
requirement_id: REQ-0119-admin-display-image-size-limit-setting
acceptance_status: passed
created_at: 2026-08-22 21:19:48
updated_at: 2026-08-25 14:51:36
---

# 验收清单

## 功能 AC

- [ ] AC-001 管理端 `/admin/settings/media` 展示详情展示图体积目标上限字段，单位为 KB，默认 effective 值为 `768`。
- [ ] AC-002 字段帮助文案说明该配置控制 `.display` 或详情展示图，不控制 `.thumb` 缩略图。
- [ ] AC-003 `GET /api/v1/admin/system-settings/media` 返回 display 图体积目标字段。
- [ ] AC-004 `PATCH /api/v1/admin/system-settings/media` 可以更新 display 图体积目标字段，并写入系统设置事实源。
- [ ] AC-005 `POST /api/v1/admin/system-settings/media/reset` 后 display 图体积目标恢复默认 `768`。
- [ ] AC-006 修改 display 图体积目标不改变 `media.thumbnail_max_size_kb`；修改缩略图体积目标不改变 display 图体积目标。
- [ ] AC-007 新上传图片生成 `.display` 图时读取 display 图体积目标 effective 值，而不是继续使用硬编码常量。
- [ ] AC-008 SKU pending 图片正式化时补生成 `.display` 图读取同一 effective 配置。
- [ ] AC-009 存量图片多规格维护任务重生成 `.display` 图时读取同一 effective 配置，并保留 dry-run / apply 边界。
- [ ] AC-010 保存系统设置不会自动扫描对象存储、读取历史原图或覆盖历史 `.display` 对象。
- [ ] AC-011 `.display` 图 key、URL、bucket、前缀和受控 `/media/...` 读取语义保持不变。
- [ ] AC-012 复杂 PNG、透明图或高细节图片无法达到目标体积时不阻断原图上传、业务保存或维护任务整体执行，并记录 warning 或失败原因。
- [ ] AC-013 OpenAPI、Orval、API 文档、媒体文档、对象存储文档和测试按字段新增同步更新。
- [ ] AC-014 后端测试覆盖默认值、PATCH、reset、display 生成读取配置、与缩略图配置互不影响。
- [ ] AC-015 管理端测试覆盖字段展示、编辑、保存、恢复默认、fixed toast、dirty 切换确认和上传限制 2 列网格四行顺序。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-form-page-consistency.md` — 预防 Sprint 002/003 表单页重复 CTA、原生确认和 layout shift 复发。

- [ ] AC-XCUT-001 全页仅保留一处 accessible name 为「保存设置」或等价保存按钮，位于 `settings-panel-footer` 或等价表单 footer；页头不得重复渲染保存 CTA。
- [ ] AC-XCUT-002 「恢复默认」和 dirty 态切换 Tab 必须使用 Design System modal，具备 `role="dialog"` 或等价语义；禁止使用 `window.confirm`、`window.alert`。
- [ ] AC-XCUT-003 保存成功、恢复默认成功和保存失败反馈使用 fixed toast 或等价不改变文档流的反馈区，不得在 summary 与主表单之间插入会推挤布局的条件块。
- [ ] AC-XCUT-004 1440×1024 视口下 `/admin/settings/media` 与 prototype/context 并排检查：新增字段不破坏 Settings Shell、settings-nav、summary-grid、表单网格和 footer 对齐。

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防媒体上传、对象存储、回显和 Docker Web 边界类缺陷。

- [ ] AC-XCUT-005 本需求不新增上传控件，上传状态机 `idle -> uploading -> done/failed` 为 N/A；但必须通过现有图片上传入口验证配置变更后新上传 `.display` 生成链路仍返回成功或可解释失败。
- [ ] AC-XCUT-006 配置变更后的同会话上传回显必须包含可访问的 `display_url` 或明确 fallback，失败信息不能只依赖全局 toast。
- [ ] AC-XCUT-007 若字段实现影响上传大小、Nginx 或 Docker Web 边界，必须从 `http://localhost:3000` 或等价 Web 用户入口验证边界文件；若不影响上传大小，记录 N/A 理由。
- [ ] AC-XCUT-008 验收 evidence 必须区分 key、object、URL、render：脱敏记录 `.display` key 规则、对象存在或生成失败原因、`/media/...` HTTP 状态和管理端/小程序/店主 Web 的用户可见表现。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 22:19:53
accepted_by: workflow-sync
source_change: add-admin-display-image-size-limit-setting
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

