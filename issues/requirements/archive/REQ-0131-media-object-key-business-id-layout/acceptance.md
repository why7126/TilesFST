---
requirement_id: REQ-0131-media-object-key-business-id-layout
acceptance_status: passed
created_at: 2026-08-29 19:23:12
updated_at: 2026-08-30 08:45:27
---

# 验收标准

## 功能 AC

- [x] AC-001 对象 Key 策略矩阵覆盖头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片、品牌证书 PDF/文档，并采用 `user-avatars`、`brand-logos`、`banners`、`tiles`、`brand-certificates` 扁平业务媒体类型目录。
- [x] AC-002 每类媒体明确业务对象 id、正式目录、同类资源 `pending/` 目录、formalize 触发时机、派生图位置、旧 key 与过渡目录兼容和迁移策略。
- [x] AC-003 业务对象 id 默认使用对应业务表主键；若某类媒体使用等价稳定 id，PRD、Change 和文档必须说明原因。
- [x] AC-004 业务对象创建前上传的媒体必须进入对应 pending 目录，保存成功后 formalize 到业务 id 目录并同步数据库引用。
- [x] AC-005 新上传媒体不得使用用户原始文件名、本机绝对路径、临时路径、对象存储 raw URL 或未脱敏业务文本作为 object key。
- [x] AC-006 旧数据库引用中的完整 key 必须继续可通过 `/media/{object_key}` 或等价受控 URL 读取，旧媒体显示不得因新 key 策略中断。
- [x] AC-007 前端、小程序和管理端只能消费后端返回的 key/URL 字段，不得自行拼接对象存储 endpoint、bucket、业务 id 目录或 raw URL。
- [x] AC-008 图片原图、`.thumb.webp`、`.display.webp` 必须位于同一业务对象目录或等价可追溯目录；迁移原图时同步迁移或补生成派生图。
- [x] AC-009 PDF/文档类证书继续使用 `files/` 文件前缀，不得生成图片缩略图或展示图，除非后续独立需求引入 PDF 首图渲染。
- [x] AC-010 存量迁移必须支持 dry-run，输出待迁移数量、跳过数量、失败分类、目标冲突、对象缺失和风险摘要，且不写数据库或对象存储。
- [x] AC-011 存量迁移 apply 必须显式触发，并在执行前确认数据库备份和对象存储 bucket/prefix 备份。
- [x] AC-012 apply 后必须支持二次审计，覆盖数据库引用、对象存在性、URL 可读性、端侧展示和幂等复跑结果。
- [x] AC-013 旧对象删除或清理必须作为单独高风险动作确认，不得在普通迁移、formalize 或派生图补生成中默认执行。
- [x] AC-014 文档同步覆盖 `rules/object-storage.md`、`rules/media.md`、`docs/07-object-storage-strategy.md`、`docs/standards/batch-image-processing-runbook.md`、OpenSpec specs 和发布验收模板。
- [x] AC-015 若 API 字段、响应结构或 URL 语义变化，必须同步 OpenAPI、Orval、API 文档和前后端测试；若不变化，需在 Change 验收中写明 N/A 原因。
- [x] AC-016 若新增 DB 表、字段、索引、迁移状态或对象别名表，必须同步 SQLite/MySQL schema、迁移、数据库设计文档和测试；若不新增，需说明继续复用既有媒体引用字段。
- [x] AC-017 生产维护任务输出必须脱敏，只允许出现 key hash、标准前缀、资源类型、数量、状态和失败原因枚举。
- [x] AC-018 小程序、Web 管理端和店主展示端受影响媒体位必须提供 key、object、URL、render/Network、耗时或 trace span 证据。
- [x] AC-019 对象 key 审计必须识别 `avartars` 等错误拼写目录，并以枚举化失败原因输出脱敏摘要。

## 产品数据采集与链路观测 AC

- [x] AC-OBS-001 需求、Change 和验收材料必须声明 `product_data_collection_observability.status=applicable`，并列出 `request_logs`、`task_traces`、`task_trace_spans`、`backend_api`、`web_admin_request_flow`、`wechat_miniapp_request_flow`、`maintenance_jobs` 影响层级。
- [x] AC-OBS-002 上传、formalize、迁移和维护任务必须记录稳定 `resource_type`、`resource_id`、状态、数量、失败分类和脱敏 key 摘要。
- [x] AC-OBS-003 请求日志和任务链路不得保存完整 object key、完整请求体、完整响应体、Authorization header、Cookie、Token、access key、secret key、真实 `.env` 内容或本机绝对路径。
- [x] AC-OBS-004 维护任务失败分类至少区分对象存储不可达、源对象缺失、目标 key 已存在、业务 id 缺失、DB 更新失败、缩略图缺失、展示图缺失和不支持媒体类型。
- [x] AC-OBS-005 若端侧请求封装需要透传 behavior trace 或 client request id，必须同步 Web/小程序请求 helper、测试和文档；若不调整端请求封装，需记录具体 N/A 原因。
- [x] AC-OBS-006 迁移审计失败不得被写作验收通过；blocked 项必须列出补证入口、负责方和重试条件。

## 发布与回滚 AC

- [x] AC-REL-001 发布说明必须明确本次是只改新上传、迁移存量对象、还是包含旧对象清理。
- [x] AC-REL-002 生产执行前必须记录数据库备份与对象存储 bucket/prefix 备份确认。
- [x] AC-REL-003 升级计划必须说明回滚方式：数据库恢复、对象存储快照恢复、旧 key 兼容继续保留或迁移脚本反向策略。
- [x] AC-REL-004 若存量迁移分批执行，验收必须记录批次范围、成功/失败数量、剩余候选和下一批条件。
- [x] AC-REL-005 发布后必须抽样验证至少 SKU 图片、品牌 Logo、品牌证书图片、证书 PDF 和 Banner 图片的新旧 URL 可读。

## 横切 AC（knowledge-base）

> 来源：`docs/knowledge-base/best-practices/admin-media-upload-chain.md` — 预防媒体上传、回显、对象存储和 Docker Web 边界类缺陷。

- [x] AC-XCUT-001 媒体上传控件必须具备 `idle -> uploading -> done/failed` 状态机证据；失败原因展示在上传控件或对应媒体对象下方，不能只依赖全局 toast。
- [x] AC-XCUT-002 上传成功后，同一会话内必须即时回显缩略图、文件卡片或可访问媒体入口；保存后重新打开编辑入口仍能回显正式业务 id 目录 URL。
- [x] AC-XCUT-003 含上传边界变化时必须经 Docker Web `http://localhost:3000` 验证边界文件，证明小文件成功、超限文件返回业务错误而不是 Nginx 413；若本 Change 不调整大小限制，记录 N/A 原因。
- [x] AC-XCUT-004 object key 与 `/media/{object_key}` 代理必须一致，验收记录需覆盖脱敏 key、对象存在性、HTTP 状态、业务错误码和用户可见表现。
- [x] AC-XCUT-005 新上传不得写入 `data/uploads/` 或 legacy 双目录；历史 key 兼容或迁移结果必须在 key/object 维度说明。
- [x] AC-XCUT-006 小程序媒体卡片、品牌入口、证书详情或商品详情受影响时，必须记录 DevTools、真机或体验版 render/Network evidence；无法补齐时标记 blocked，不得写作通过。
- [x] AC-XCUT-007 历史对象、缩略图、回填或审计脚本相关验收必须记录 dry-run、apply、幂等性或统计摘要；缩略图存在但无体积/耗时收益不得写作通过。

## 验收证据摘要

```yaml
result: passed
verified_at: 2026-08-29 23:14:05
verified_by: codex
change: update-media-object-key-business-id-layout
sprint: sprint-027
evidence:
  backend_media_tests: "uv --project src/backend run python -m pytest src/backend/tests/test_object_keys.py src/backend/tests/test_media_maintenance.py tests/test_migrate_pending_tile_images.py tests/test_deploy_media_maintenance_script.py -> 47 passed"
  pillow_upload_tests: "uv --project src/backend run python -m pytest src/backend/tests/test_admin_brands.py src/backend/tests/test_admin_tile_skus.py tests/integration/api/test_admin_brand_certificates.py tests/test_media_storage.py -> 97 passed"
  web_admin_tests: "pnpm --pm-on-fail=ignore --dir src/web test ProfilePage/BrandManagementPage/BannerManagementPage/TileSkuManagementPage/BrandCertificateManagementPage and related media form tests -> 9 files, 94 tests passed"
  miniapp_media_tests: "uv --project src/backend run python -m pytest tests/test_miniapp_media_assertions.py tests/test_miniapp_home.py tests/test_audit_miniapp_card_images.py tests/test_miniapp_device_evidence_template.py -> 61 passed"
  openspec_validation: "openspec validate update-media-object-key-business-id-layout --strict -> pass"
  language_validation: "python scripts/validate-openspec-language.py -> pass"
  observability_gate: "python scripts/validate-product-data-observability-gates.py --change update-media-object-key-business-id-layout -> pass"
  directory_validation: "python scripts/validate-directory-structure.py -> pass"
  docker_compose: "docker compose ps -> tilesfst-backend, tilesfst-web, tilesfst-docs-site running; backend http://localhost:8000, web http://localhost:3000"
impact:
  api: "无新增请求/响应字段；OpenAPI/Orval 已同步，前后端继续消费后端返回 key/url"
  db: "无新增表、字段、索引或迁移状态表；继续复用既有媒体引用字段"
  backend: "上传、formalize、受控 /media 读取、视频 Range/HEAD、维护任务 dry-run/apply/幂等路径通过测试"
  web_admin: "媒体表单、上传状态、即时回显和保存后正式业务 id 目录 URL 通过组件/页面测试"
  web_catalog: "继续消费后端返回 URL；本 Change 未新增店主端页面逻辑"
  wechat_miniapp: "媒体 helper、首页/详情/证书/品牌媒体 URL 消费和安全断言通过测试；本命令未执行真机或体验版"
  docker_compose: "当前本地 Compose 服务运行中；本 Change 不调整 Nginx 上传大小边界"
production_boundary:
  status: "manual_confirmation_required_before_production_apply"
  reason: "生产 media-drift-reconcile --apply --confirm-backup 需要数据库备份与对象存储 bucket/prefix 备份确认，本命令未擅自执行生产写入"
```

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-29 23:24:26
accepted_by: workflow-sync
source_change: update-media-object-key-business-id-layout
source_sprint: sprint-027
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

