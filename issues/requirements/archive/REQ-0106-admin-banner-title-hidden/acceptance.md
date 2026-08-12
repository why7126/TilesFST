---
requirement_id: REQ-0106-admin-banner-title-hidden
acceptance_status: passed
created_at: 2026-08-10 22:40:54
updated_at: 2026-08-12 00:15:15
---

# Acceptance Criteria

## 功能 AC

- [ ] AC-001 新增 Banner 弹窗不展示“Banner 标题”字段。
- [ ] AC-002 编辑 Banner 弹窗不展示“Banner 标题”字段。
- [ ] AC-003 管理端保存 Banner 时，运营未填写标题也不会出现“Banner 标题不能为空”错误。
- [ ] AC-004 系统能为仍需 `title` 的保存链路自动生成或保留内部标题，且同展示端 + 展示位置下不发生唯一性冲突。
- [ ] AC-005 Banner 列表第一列不再只依赖人工标题，能通过缩略图、展示位置、跳转类型、跳转目标、排序或更新时间识别记录。
- [ ] AC-006 Banner 列表搜索占位文案不再把“标题”作为主要搜索对象；如保留标题搜索，仅作为内部兼容能力。
- [ ] AC-007 小程序首页有在线有效 Banner 时，不渲染 Banner `title` 文本作为前台主标题。
- [ ] AC-008 小程序品牌列表页有在线有效 Banner 时，不渲染 Banner `title` 文本作为前台主标题。
- [ ] AC-009 小程序首页和品牌列表页无 Banner 时，原有兜底 Hero 文案继续可用，不白屏。
- [ ] AC-010 Banner 点击跳转能力不因标题隐藏回归，SKU、品牌、搜索、门店和无跳转行为按既有规则执行。
- [ ] AC-011 若实现修改 API 请求或响应结构，OpenAPI、Orval、接口文档和前后端测试均同步更新；若 API 不变，需在实现说明中明确“不需要 Orval”的依据。
- [ ] AC-012 自动生成的内部标题不得暴露到小程序 Banner 主视觉，不得包含真实客户数据、密钥、访问令牌或用户隐私信息。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md`、`docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`、`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002/003/020 复发类缺陷

- [ ] AC-XCUT-001 Banner 列表保持用户管理基准分页 DOM：左侧 `page-summary`，右侧 `page-right` 页码与每页条数；不得新增页面私有分页结构。
- [ ] AC-XCUT-002 Banner 列表操作成功/失败反馈使用 fixed toast，不得使用会推挤 page hero 或表格的文档流 notice。
- [ ] AC-XCUT-003 Banner 上线、下线、删除等状态/危险操作继续使用 DS confirm modal；不得使用 `window.confirm`。
- [ ] AC-XCUT-004 如调整 Banner 列表筛选下拉或关键词筛选，必须复用 `AdminFilterSelect`、`SearchableSelect` 或等价 shared wrapper，并覆盖 open/select/clear/reset 与 query 语义不变。
- [ ] AC-XCUT-005 Banner 弹窗 TSX 不得同时挂载通用 `modal-card` 与 `banner-modal-card` 等专属类；Computed width 需与既有 Banner/SKU 弹窗基准一致。
- [ ] AC-XCUT-006 Banner 弹窗在矮视口下 body scroll 不回归，隐藏标题字段后不出现空白行、遮挡或底部按钮不可见。
- [ ] AC-XCUT-007 Banner 图片上传状态机保持 `idle -> uploading -> done/failed`，标题隐藏不得破坏上传进度、失败提示和成功即时回显。
- [ ] AC-XCUT-008 Banner 图片同会话上传后，新增/编辑弹窗与列表刷新仍可通过 `/media/{object_key}` 回显缩略图或原图 fallback。
- [ ] AC-XCUT-009 如本需求触碰上传边界、Nginx 或 Docker Web 配置，必须经 `http://localhost:3000` 验证边界文件上传；若未触碰，标记 `N/A — 本需求未修改上传大小、Nginx 或 Docker Web 配置`。
- [ ] AC-XCUT-010 小程序 UI 验收需记录 DevTools、体验版或真机来源；不能把未执行的端上验证写作自动通过。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-12 00:15:15
accepted_by: workflow-sync
source_change: update-banner-title-hidden-display
source_sprint: sprint-022
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

