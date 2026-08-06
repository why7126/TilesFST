---
requirement_id: REQ-0101-media-acceptance-three-part-template
acceptance_status: not_started
acceptance_status: pending
created_at: 2026-08-06 11:24:19
updated_at: 2026-08-06 11:26:00
owner: product
source: requirement.md
---

# 验收标准

## 功能 AC

- [ ] AC-001 模板包含“列表展示字段”“生成策略”“历史对象维护或重生成”三段，三段标题固定且不得合并为单段媒体说明。
- [ ] AC-002 模板定义启用条件：涉及媒体 URL、对象 key、缩略图、上传、对象存储、列表图片展示、历史资源维护任一项时必须启用。
- [ ] AC-003 列表展示字段段要求记录 API 字段、Orval 类型、admin web 列表字段选择、fallback 规则、空态和截图或测试证据。
- [ ] AC-004 生成策略段要求记录触发时机、尺寸体积、格式质量、命名约定、失败降级、日志或任务追踪。
- [ ] AC-005 历史对象维护或重生成段要求记录扫描范围、dry-run、apply、权限边界、幂等性、对象存储 key/prefix、成功/失败/跳过统计。
- [ ] AC-006 模板包含固定影响矩阵，至少覆盖 API、Orval、DB、对象存储、admin web 列表。
- [ ] AC-007 影响矩阵每项必须填写 `是`、`否` 或 `待确认`，并写明证据要求或不涉及原因。
- [ ] AC-008 三段证据均支持 `pass`、`fail`、`n/a`、`blocked` 状态，失败和阻塞必须记录原因与后续处理建议。
- [ ] AC-009 模板说明与 `REQ-0090` 媒体五联、`REQ-0091` 媒体类 BUG 四联的关系：三段模板负责组织证据，五联/四联负责链路维度检查。
- [ ] AC-010 模板不得记录真实客户数据、真实密钥、内部绝对路径、Authorization header、Cookie 或 `.env` 内容。
- [ ] AC-011 后续 OpenSpec design 必须明确模板最终落点，例如 `rules/media.md`、`rules/object-storage.md`、`docs/knowledge-base`、issue acceptance 模板或命令 Skill 模板。
- [ ] AC-012 若模板用于已归档 Sprint 案例说明，只能引用经验和证据来源，不得重新修改已归档 Sprint Scope。

## 影响矩阵模板 AC

| 影响项 | 是否必填 | 证据要求 |
|---|---|---|
| API | 是 | 请求入口、响应字段、错误码、兼容性；不涉及时说明“不改接口”。 |
| Orval | 是 | OpenAPI 与 generated client/type 同步结果；不涉及时说明“不改 API schema”。 |
| DB | 是 | 表、字段、迁移、Pydantic Schema 或“不改表/不改业务记录”。 |
| 对象存储 | 是 | key/prefix、object 写入或读取、URL 可访问性、权限边界。 |
| admin web 列表 | 是 | 页面入口、字段优先级、fallback、空态、截图或测试断言。 |

## 验收结果回填

```yaml
acceptance_status: not_started
accepted_at: null
accepted_by: null
source_change: null
source_sprint: null
evidence: []
failed_items: []
source_event: req.complete
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-list-page-consistency.md` — 预防 Sprint 002/003 复发类缺陷

- [ ] AC-XCUT-001 列表类媒体需求若新增或修改 admin web 列表，分页 DOM 必须与用户管理基准对齐；N/A — 本需求本身只定义模板，后续应用模板的具体 Change 需要执行。
- [ ] AC-XCUT-002 列表类媒体需求若涉及摘要指标卡，DOM 必须使用 `.metric-label` / `.metric-value` / `.metric-desc`；N/A — 本需求本身不新增指标卡。
- [ ] AC-XCUT-003 列表筛选下拉若受影响，必须复用 `AdminFilterSelect`、`SearchableSelect` 或说明等价 shared wrapper 理由；N/A — 本需求本身不改筛选控件。
- [ ] AC-XCUT-004 列表筛选下拉不得使用页面级一次性弹层样式，弹层不得被表格、滚动容器、弹窗或 sticky action column 裁切；N/A — 本需求本身不改筛选控件。
- [ ] AC-XCUT-005 列表筛选测试需覆盖 open/select/clear/reset、禁用态、已选中态、空态、加载态和 query 语义不变；N/A — 本需求本身不改筛选控件。
- [ ] AC-XCUT-006 操作成功或失败 toast 不得引起 hero、表格或列表纵向位移；N/A — 本需求本身不新增 Web 操作。
- [ ] AC-XCUT-007 状态变更类操作必须使用 DS confirm，且不得使用 `window.confirm`；N/A — 本需求本身不新增状态变更操作。

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防 Sprint 002 媒体上传与对象存储链路复发类缺陷

- [ ] AC-XCUT-008 媒体上传类 Change 必须验收上传状态机 `idle -> uploading -> done/failed`，失败信息应落在上传控件或对象附近；N/A — 本需求本身不新增上传控件，但模板必须要求后续媒体上传需求补此证据。
- [ ] AC-XCUT-009 媒体上传成功后必须验收同会话即时回显，记录缩略图、文件卡片或媒体 URL 入口；N/A — 本需求本身不新增上传控件，但模板必须保留该证据字段。
- [ ] AC-XCUT-010 含上传边界的 Change 必须经 Docker Web `http://localhost:3000` 验证边界文件，不得只调用后端 `:8000`；N/A — 本需求本身不改上传上限或 Nginx，但模板必须保留 Docker 边界证据入口。
- [ ] AC-XCUT-011 媒体对象验收必须记录 `object_key` 与 `/media/{object_key}` 代理一致性，包括脱敏 key、对象存在性、HTTP 状态、业务错误码和用户可见表现。
- [ ] AC-XCUT-012 新上传不得写入 `data/uploads/`，历史 key 兼容或迁移必须记录标准前缀、对象存在性和迁移结果；N/A — 本需求本身不新增上传，但模板必须要求后续对象存储影响项记录。
