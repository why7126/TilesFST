---
note: workflow-sync — 8/8 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-011
title: Sprint 011 Acceptance Report
status: completed
created_at: 2026-07-23 09:17:23
updated_at: 2026-07-26 15:43:55
---

# Sprint 011 Acceptance Report

## 验收范围

| 类型 | ID | Change | 状态 |
|---|---|---|---|
| BUG | BUG-0081-prod-cos-video-upload-fails | fix-upload-proxy-timeout-config | applied-local |
| BUG | BUG-0082-prod-miniapp-sku-video-slow-start | fix-miniapp-sku-video-slow-start | archived |
| BUG | BUG-0083-prod-admin-brand-banner-save-500 | fix-admin-banner-create-schema-drift | production-verified |
| BUG | BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | fix-miniapp-sku-video-fullscreen-reload | archived |
| BUG | BUG-0085-admin-video-upload-stuck-at-99 | fix-admin-video-upload-stuck-at-99 | applied |
| REQ | REQ-0068-miniapp-sku-video-fullscreen-actions | add-miniapp-sku-video-fullscreen-actions | archived |
| REQ | REQ-0069-upload-observability-trace-logs | add-task-trace-audit-log-view | applied-local |
| REQ | REQ-0070-audit-log-operator-name-filter | improve-audit-log-operator-filter | applied |

## 验收清单

| AC | 验收项 | 验收标准 | 证据 |
|---|---|---|---|
| AC-001 | 外层反代上传超时 | HTTPS Nginx `/api/v1/admin/uploads/` 超时不低于 300s，推荐 600s | `docs/02-deployment.md` 已补 600s 外层 location 与 reload 步骤 |
| AC-002 | 内层 Web Nginx 上传 location | Docker Web Nginx 在 `/api/` 前配置上传专用 location | `src/web/nginx.conf.template`、`src/web/nginx.conf` 已配置并经测试断言顺序 |
| AC-003 | 环境变量化 | 上传超时和 body size 可由环境变量或等价部署参数配置 | `.env.example`、三套 Compose Web service 已配置 `UPLOAD_*` 默认值 |
| AC-004 | 上传成功 | 生产管理端上传同类视频返回 200，响应含 `object_key` 与 `/media/{object_key}` | 待生产或生产等价 smoke |
| AC-005 | COS 一致性 | COS 对象存在且 key 与响应一致 | 待生产或生产等价 smoke |
| AC-006 | SKU 保存闭环 | 上传视频可加入 SKU 表单，保存后刷新仍存在 | 待生产或生产等价 smoke |
| AC-007 | 日志回归 | 不再出现同类 60 秒 499/504 | 待生产或生产等价 smoke |
| AC-008 | 既有上传不回退 | 品牌 Logo、SKU 图片、证书上传仍可用 | `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py` 通过；仍建议上线 smoke 覆盖品牌 Logo/SKU 图片 |
| AC-009 | 视频 Range 响应 | `/media/{object_key}` 视频请求携带 `Range: bytes=0-1023` 时返回 `206 Partial Content`、`Accept-Ranges`、`Content-Range` | `uv run pytest tests/test_media_storage.py tests/test_miniapp_static.py` 41 passed，覆盖 Range、HEAD 元信息函数与 HEAD 路由响应 |
| AC-010 | 小程序视频封面兜底 | SKU 详情页视频未起播或加载中时展示 `cover_url`、商品主图或安全兜底图 | `tests/test_miniapp_static.py` 通过，断言 `poster="{{item.cover_url || product.cover_image || imageFallback}}"` |
| AC-011 | 真机首帧体验 | 生产或等价环境记录实际 SKU 视频大小、编码、时长、机型、网络和点击到首帧耗时 | 待生产或生产等价 smoke |
| AC-012 | 非视频读取回归 | 图片、PDF 或其他媒体读取不因视频 Range 支持回归 | `tests/test_media_storage.py` 通过，覆盖非 Range、非法 Range、对象不存在、非法 object_key 等路径 |
| AC-013 | MySQL schema drift | 生产 MySQL `banners` 表字段与 SQLAlchemy/Pydantic 读写契约兼容，迁移幂等可重复执行 | `tests/test_mysql_migrations.py`、`tests/test_mysql_schema_drift.py` 通过；已覆盖旧 CHECK 约束缺 `brand_logo` / `BRAND_DETAIL` / `MINIAPP_BRAND_LIST_CAROUSEL` 的重建；2026-07-23 用户确认更新后端镜像后生产保存已恢复 |
| AC-014 | 品牌 Banner 创建保存 | 管理端创建品牌类型 Banner 时 `POST /api/v1/admin/banners` 返回 200/201，响应含新 Banner ID | `src/backend/tests/test_admin_banners.py` 通过；若生产仍有 DB 写入异常，返回 `503 / 30055` 可定位错误；2026-07-23 用户确认生产创建品牌类型 Banner 已可保存 |
| AC-015 | 品牌 Banner 回填 | 保存后刷新列表与编辑详情，品牌目标字段、图片、排序、状态等信息保持一致 | `src/backend/tests/test_admin_banners.py` 覆盖新增、编辑、列表与详情回填 |
| AC-016 | 非法 payload 错误语义 | 缺少品牌目标、非法图片或字段不合法时返回 4xx 业务错误，不再返回 500 | `src/backend/tests/test_admin_banners.py` 覆盖品牌不存在、未启用、无 Logo、Logo 不匹配等场景 |
| AC-017 | 视频全屏入口 | 商品详情页视频区域提供清晰全屏播放入口，点击后进入微信 video 全屏播放态 | `src/miniapp/pages/tile-detail/index.wxml` 保留右上角图标全屏入口并隐藏内置全屏按钮；`tests/test_miniapp_static.py` 通过 |
| AC-018 | 全屏上下文保持 | 全屏播放时保持当前商品与视频上下文，不影响返回商品详情页继续浏览 | `wx.previewMedia({ sources: [当前视频], current: 0, showmenu: true })` 仅预览当前视频；真机退出回到当前详情页仍需人工确认 |
| AC-019 | 长按菜单或降级入口 | 全屏态长按优先出现 `转发给朋友`、`保存视频`、`取消` 等交互；若平台不支持自定义长按菜单，提供等价显式操作入口并记录原因 | 已改为微信原生媒体预览菜单 `showmenu: true`；平台能力边界和降级说明见归档 Change `implementation.md` |
| AC-020 | 转发给朋友 | 用户可从全屏视频交互转发当前商品或视频上下文给朋友，分享路径与 REQ-0064 小程序分享能力一致 | 视频区域不再触发商品详情页 `open-type="share"`；视频文件转发交给微信原生媒体预览菜单，真机菜单文案与行为需 follow-up |
| AC-021 | 保存视频 | 用户可触发保存视频，按微信授权/下载能力完成保存或给出明确失败反馈 | 移除自定义 `wx.downloadFile` / `wx.saveVideoToPhotosAlbum` 网络错误路径；后端 `/media/{object_key}` 已补 `HEAD` 与视频 Range 支持，保存结果仍需真机确认 |
| AC-022 | 小程序 evidence 分层 | DevTools 可验证静态结构与基础交互，真机补齐长按、保存、授权和全屏播放 evidence | 静态测试和后端媒体测试已通过；DevTools / 真机 evidence 在 `implementation.md` 中明确标记 follow_up，未写成真机通过 |
| AC-023 | 已播放视频进入全屏连续性 | SKU 详情页视频在内嵌态已可播放时，点击全屏入口后应复用当前视频上下文，不出现长时间重新加载 | 已改为 `wx.createVideoContext(...).requestFullScreen()` 复用当前 video 上下文；`uv run pytest tests/test_miniapp_static.py` 30 passed；实际 SKU 真机耗时 evidence 待补 |
| AC-024 | 全屏切换加载反馈 | 若微信原生切换全屏仍存在短暂缓冲，页面需有明确加载/恢复反馈，不让用户误判为卡死 | 已补“正在进入全屏播放 / 全屏切换中，视频正在恢复播放 / 全屏播放暂不可用”反馈；静态测试通过，真机体验待确认 |
| AC-025 | 上传阶段状态拆分 | 管理后台 SKU 视频上传在客户端传输完成后，99% 阶段必须展示服务端保存/等待确认状态，不让管理员误判为卡死 | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx` 21 passed，覆盖“正在保存视频，请稍候”且不再显示“上传中 99%” |
| AC-026 | 上传失败重试与列表稳定 | 服务端保存失败、超时或网络异常时必须给出可重试反馈，且不破坏已有视频列表和已上传成功的媒体项 | `TileSkuFormModal.test.tsx` 覆盖失败后可重新选择同一文件重试、已有视频卡片保持稳定 |
| AC-027 | 上传代理与对象存储闭环 | 生产或等价环境确认上传代理配置生效，接口 200 响应、对象 key、对象存储写入和 SKU 保存闭环一致 | `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py` 16 passed；`src/backend/tests/test_admin_tile_skus.py` 19 passed，覆盖上传返回 `/media/{object_key}` 并保存/读取 SKU 视频闭环；真实生产 Nginx/backend 日志仍需上线 sign-off |
| AC-028 | Task Trace 标识生成与关联 | 每一次可追踪业务任务生成或确认 `task_trace_id`，且 request_logs、usage_events、audit_logs 与 task spans 可通过同一 ID 串联 | `TaskTraceRepository` / `TaskTraceService` 已落地；SQLite/MySQL schema 与迁移扩展 `request_logs`、`usage_events`、`audit_logs`；`src/backend/tests/test_product_usage_logging.py` 覆盖 task_trace_id 筛选与详情串联 |
| AC-029 | 上传首批节点覆盖 | 图片、视频、文件上传记录前端选择、上传开始、请求体上传完成、后端接收、文件校验、对象存储写入、数据库记录、响应返回、前端完成或失败节点 | `src/backend/app/api/v1/uploads.py` 覆盖图片、视频、证书/文件上传；Docker Web 入口 smoke 经 `http://127.0.0.1:3000` 验证小图成功、51MB 图片按当前 50MB 上限返回 `50003`；Trace spans 含 `frontend_upload_body_done`、`storage_put_object`、`api_response`、`frontend_done` |
| AC-030 | 审计日志 Task Trace 查询与详情 | 管理端日志审计列表支持按 `task_trace_id` 查询，详情展示节点时间线、耗时、状态、错误码和关联 `request_id` | `src/web/src/pages/admin/LogAuditPage.tsx` 与 `log-audit.css` 已展示 Task Trace 列、筛选与详情时间线；`LogAuditPage.test.tsx` 覆盖筛选、复制和详情时间线；Docker smoke 通过审计日志 API 按 `task_trace_id` 回查成功 |
| AC-031 | Task Trace 安全脱敏与权限 | metadata 不保存 Authorization、Cookie、AccessKey、SecretKey、DSN、`.env`、真实客户数据、完整敏感请求体或内部绝对路径；仅系统管理员可访问 | `TaskTraceService.safe_task_metadata` 脱敏敏感 header、secret、DSN、`.env` 与内部路径；`test_admin_logs_filter_and_detail_task_trace_timeline` 覆盖 Authorization 和 `/Users/...` 不外泄；日志审计 API 沿用系统管理员权限 |
| AC-032 | API / DB / Orval / 文档同步 | 若新增或调整日志审计 API 字段与 Task Trace 数据模型，必须同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md`、错误码文档和测试 | 已运行 `scripts/generate-openapi-client.sh` 并更新 `src/web/openapi.json`、`src/web/src/shared/api/generated.ts`；已同步 `docs/03-api-index.md`、`docs/04-database-design.md`、`docs/standards/file-upload.md`；未新增错误码，沿用 `50002/50003/50005` |
| AC-033 | 操作者筛选入口 | 日志审计页面筛选区不再要求手输 User ID，提供用户名称/账号单选搜索下拉 | `src/web/src/pages/admin/LogAuditPage.tsx` 已替换为 `SearchableSelect`；筛选顺序调整为状态/结果在操作者前、`Task Trace ID` 在 `路径 / Request ID` 前；`路径 / Request ID` 与独立 `Task Trace ID` 字段去重；日志列表操作者列显示账号 `actor_username` 且单行展示；`LogAuditPage.test.tsx` 覆盖无 User ID 输入框 |
| AC-034 | 候选模糊搜索 | 下拉候选支持按用户显示名称、用户名或账号关键字模糊搜索；同名用户需展示辅助信息区分 | 复用 `GET /api/v1/admin/users` `keyword`；候选项只保留账号与用户名称两行，账号行可区分同名用户；测试覆盖 keyword 与同名用户账号区分 |
| AC-035 | 精确过滤参数 | 选择操作者后日志列表请求仍使用所选用户 `id` 作为 `actor_user_id`，不得把显示名称或账号作为日志过滤参数 | `LogAuditPage.test.tsx` 覆盖选择后请求 `actor_user_id=user_admin/user_operator` |
| AC-036 | 清空与重置 | 清空单选或点击重置后移除 `actor_user_id` 条件、回到第 1 页，并可重新加载全量操作者日志 | `LogAuditPage.test.tsx` 覆盖清空按钮与重置按钮均移除 `actor_user_id` 并回到 page 1 |
| AC-037 | 候选状态隔离 | 操作者候选加载、空态和失败提示需与日志列表加载/失败状态区分，候选失败不清空既有日志列表 | `SearchableSelect` 支持 loading/empty/error；测试覆盖无匹配、候选失败 fixed toast 且日志列表仍显示 |
| AC-038 | admin-list 横切回归 | 改造后保留分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`，并符合列表页一致性最佳实践 | `LogAuditPage.test.tsx` 覆盖 `.page-summary`、`.page-right`、`.metric-*`、fixed toast、无 `window.confirm` / `window.alert`；时间范围筛选覆盖最近5分钟至最近7天固定窗口并移除全部时间 |
| AC-039 | 移动端布局 | 移动端视口下筛选区、下拉层与日志表格不发生横向溢出或文字重叠 | `log-audit.css` 限制下拉宽度并保持移动端 1 列筛选；列表 `Task Trace` 列与 `request_id` 列统一为单行 ID + 复制按钮；表格、筛选下拉、右侧详情抽屉按层级递增，避免下拉被列表遮挡或筛选模块遮住抽屉；`AdminMobileAdaptation.test.ts` 通过 |
| AC-050 | 统一摘要与统计口径 | 页面展示请求日志、行为事件、审计操作和 Task Trace 统一摘要；摘要、分布、排行和明细入口与当前筛选条件保持同一统计口径 | 不属于 sprint-011 最终范围，已转入后续观测 dashboard 相关 Change |
| AC-051 | 慢任务/慢请求排行与下钻 | 慢任务、失败任务、最慢 span、慢请求和错误接口排行可跳转到对应 Task Trace 时间线或日志详情，并支持复制 `request_id` / `task_trace_id` | 不属于 sprint-011 最终范围，已转入后续观测 dashboard 相关 Change |
| AC-052 | 聚合查询性能与兼容 | 后端聚合查询支持 SQLite demo 与生产 MySQL，返回结构化摘要、分布、排行和跳转 ID，避免无条件全表扫描后在应用内聚合 | 不属于 sprint-011 最终范围，已转入后续观测 dashboard 相关 Change |
| AC-053 | 观测安全脱敏 | 指标聚合、日志详情和追踪结果不展示 Authorization、Cookie、Token、密码、真实密钥、数据库 DSN、`.env` 内容、真实客户数据或内部绝对路径 | 不属于 sprint-011 最终范围，已转入后续观测 dashboard 相关 Change |

## 测试计划

```bash
uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py
```

若实现 Nginx 模板渲染，需补充并运行模板渲染测试。

BUG-0082 实现时还需补充并运行：

```bash
uv run pytest tests/test_media_storage.py tests/test_miniapp_home.py tests/test_miniapp_static.py
```

BUG-0083 实现时还需补充并运行：

```bash
uv run pytest tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py tests/test_admin_banners.py
```

REQ-0068 已补充并运行：

```bash
uv run pytest tests/test_miniapp_static.py
```

BUG-0084 已补充并运行：

```bash
uv run pytest tests/test_miniapp_static.py
```

BUG-0085 实现时还需补充并运行：

```bash
pnpm --dir src/web test
uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py
```

REQ-0069 实现时还需补充并运行：

```bash
uv run pytest tests/test_media_storage.py src/backend/tests/test_product_usage_logging.py
pnpm --dir src/web exec vitest run src/web/src/pages/admin/LogAuditPage.test.tsx
```

REQ-0070 实现时还需补充并运行：

```bash
pnpm --dir src/web exec vitest run src/web/src/pages/admin/LogAuditPage.test.tsx
```

若 REQ-0070 新增或调整用户候选 API，需补充并运行对应后端 / OpenAPI / Orval 回归测试。

若实现新增签名下载 URL、媒体字段或 API contract，需补充并运行对应后端 / OpenAPI / Orval 回归测试。

## 已执行验证

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-23 09:37:50 | `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py` | 12 passed, 1 warning |
| 2026-07-23 09:37:50 | `openspec validate fix-upload-proxy-timeout-config` | passed |
| 2026-07-23 09:37:50 | `docker compose config --services` | `backend`, `web` |
| 2026-07-23 09:37:50 | `docker compose -f docker-compose.prod.yml config --services` | `minio`, `backend`, `web`, `minio-init` |
| 2026-07-23 09:37:50 | `docker compose -f docker-compose.prod.external.yml config --services` | `backend`, `web` |
| 2026-07-23 09:40:30 | `docker compose build web` | passed |
| 2026-07-23 09:40:30 | `docker run --rm --add-host backend:127.0.0.1 projecttilesfst-web nginx -t` | passed |
| 2026-07-23 12:08:13 | `uv run pytest tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py` | 5 passed |
| 2026-07-23 12:08:13 | `uv run pytest src/backend/tests/test_admin_banners.py` | 19 passed, 105 warnings |
| 2026-07-23 12:08:13 | `python scripts/check-mysql-schema-drift.py --schema-only --json` | parsed 19 expected MySQL tables |
| 2026-07-23 12:08:13 | `uv run pytest src/backend/tests/test_admin_banners.py tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py` | 25 passed, 109 warnings |
| 2026-07-23 12:08:13 | `uv run ruff check src/backend/app/core/error_codes.py src/backend/app/core/exceptions.py src/backend/app/repositories/banner_repository.py src/backend/app/services/banner_admin_service.py src/backend/tests/test_admin_banners.py tests/test_mysql_migrations.py tests/test_mysql_schema_drift.py` | passed |
| 2026-07-23 12:08:13 | `uv run pytest tests/test_mysql_migrations.py src/backend/tests/test_admin_banners.py tests/test_mysql_schema_drift.py` | 26 passed, 109 warnings |
| 2026-07-23 22:56:30 | 生产 smoke 用户确认 | 更新后端镜像并执行启动迁移后，生产创建品牌类型 Banner 保存已恢复；未记录真实 DSN、密钥或客户数据 |
| 2026-07-24 13:30:37 | `uv run pytest tests/test_miniapp_static.py` | 30 passed |
| 2026-07-24 13:30:37 | `uv run pytest tests/test_media_storage.py tests/test_miniapp_static.py` | 41 passed, 覆盖视频 Range、HEAD 元信息函数与 HEAD 路由响应、小程序静态契约 |
| 2026-07-24 16:01:52 | `/opsx-archive add-miniapp-sku-video-fullscreen-actions` | Change 已归档，REQ-0068 已迁入 `issues/requirements/archive/`，`openspec validate --specs --strict` 39 passed |
| 2026-07-24 20:51:17 | `uv run pytest tests/test_miniapp_static.py` | 30 passed，覆盖 BUG-0084 当前 video 上下文全屏主路径、等待/失败反馈和 `.ts` / `.js` 同步 |
| 2026-07-24 21:14:14 | `/opsx-archive fix-miniapp-sku-video-fullscreen-reload` | Change 已归档，BUG-0084 已迁入 `issues/bugs/archive/`，`openspec validate --specs --strict` 39 passed |
| 2026-07-24 21:03:21 | `pnpm --dir src/web exec vitest run src/features/admin/components/TileSkuFormModal.test.tsx` | 21 passed |
| 2026-07-24 21:03:21 | `uv run pytest tests/test_cloud_object_storage_deployment.py tests/test_media_storage.py` | 16 passed, 3 warnings |
| 2026-07-24 21:03:21 | `uv run pytest src/backend/tests/test_admin_brands.py src/backend/tests/test_admin_banners.py` | 43 passed, 183 warnings |
| 2026-07-24 21:03:21 | `uv run pytest tests/integration/api/test_admin_brand_certificates.py` | 5 passed, 45 warnings |
| 2026-07-24 21:03:21 | `uv run pytest src/backend/tests/test_admin_tile_skus.py` | 19 passed, 175 warnings |
| 2026-07-25 14:08:23 | `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx src/pages/admin/AdminMobileAdaptation.test.ts` | 2 files passed；18 tests passed |
| 2026-07-25 14:08:23 | `pnpm --dir src/web exec tsc --noEmit --ignoreDeprecations 6.0 --pretty false` | failed；剩余为既有项目级 tailwindcss/Node/CSS 声明、其他页面 fixture 类型等错误；本次触碰页面的 `log_type` 类型噪音已修正 |
| 2026-07-25 14:44:43 | `uv run pytest src/backend/tests/test_product_usage_logging.py src/backend/tests/test_admin_brands.py` | 35 passed, 107 warnings；覆盖 Task Trace 审计、SQLite 旧库迁移、品牌 Logo 上传成功/失败 Trace |
| 2026-07-25 14:44:43 | `pnpm --dir src/web exec vitest run src/pages/admin/LogAuditPage.test.tsx` | 1 file passed；12 tests passed |
| 2026-07-25 14:44:43 | `bash scripts/generate-openapi-client.sh` | passed；OpenAPI 与 Orval generated 已同步 |
| 2026-07-25 14:44:43 | `openspec validate add-task-trace-audit-log-view --strict` | passed |
| 2026-07-25 14:44:43 | `docker compose --profile self-hosted-storage up -d --build` | backend / web / minio / minio-init started；期间发现并修复 SQLite 旧库 task_trace 索引迁移顺序问题 |
| 2026-07-25 14:44:43 | Docker Web 入口上传 smoke via `http://127.0.0.1:3000` | 小图上传 200，媒体读取 200，审计日志按 `task_trace_id` 回查 1 条，spans 覆盖 9 个节点；51MB 图片在当前 `MAX_IMAGE_SIZE_MB=50` 下返回 `400 / 50003` |
| 2026-07-25 14:48:48 | `python scripts/validate-directory-structure.py` | passed；已清理本次 Ruff 校验生成的根目录临时缓存 `.ruff_cache` |

## 当前结论

BUG-0081 本地可验证项已完成。剩余 sign-off 依赖生产或生产等价环境上传同类视频，确认返回 200、COS 对象与响应 key 一致、SKU 保存闭环，以及日志不再出现同类 60 秒 499/504。

BUG-0082 本地可验证项已完成并完成 OpenSpec 归档：后端 `/media/{object_key}` 支持视频 Range/206，小程序详情页视频封面兜底已补齐，非视频读取回归已覆盖。命令行环境无法执行微信开发者工具或真机验收，实际 SKU 的机型、网络、视频大小、编码、时长和点击播放到首帧耗时仍需上线 sign-off 补证；Sprint sign-off 不得把自动化或静态测试写成真机通过。

Sprint 011 最终归档结论：8/8 Change 已归档，`python scripts/validate-sprint-archive-readiness.py --sprint sprint-011` 通过，`python scripts/promote-issues-for-archive.py --sprint sprint-011` 通过。AI usage snapshot 为 `actual`，REQ/BUG/Change 覆盖均 pass。剩余真实生产或真机证据作为发布上线 sign-off，不阻断 Sprint 归档。

BUG-0083 已完成生产验证。生产日志确认真实失败点为 MySQL 旧 CHECK 约束 `chk_banners_image_source` 不允许 `brand_logo`，已补充兼容迁移重建 Banner CHECK 约束。本次额外增加 Banner 写入前 MySQL schema 自修复检查和数据库写入异常兜底，避免继续暴露裸 500。2026-07-23 用户确认更新后端镜像并执行启动迁移后，生产创建品牌类型 Banner 保存已恢复。该问题属于生产旧表 drift 修复，本次未新增可复用事故模式文档；相关预防已沉淀到部署和数据库文档。

REQ-0068 已完成 OpenSpec 归档。实现采用微信原生 `wx.previewMedia({ showmenu: true })` 预览当前视频文件，替代页面自定义操作浮层；视频文件转发与保存交给微信原生媒体预览菜单处理，并补齐 `/media/{object_key}` 的 `HEAD` 元信息响应以支持原生预览探测。当前静态测试、媒体 Range/HEAD 测试与 OpenSpec 归档校验已通过；DevTools 和真机 evidence 仍为 follow-up，Sprint sign-off 不得把静态测试写成真机通过。

BUG-0084 本地实现已完成：视频全屏入口从独立 `wx.previewMedia` 预览链路改为当前 `VideoContext.requestFullScreen()` 主路径，避免已播放视频进入全屏时重新打开独立媒体预览层；全屏切换等待和失败反馈已补充，`tests/test_miniapp_static.py` 通过。当前命令行环境无法执行微信开发者工具或真机验收，实际 SKU 的内嵌首帧耗时、全屏切换首帧/恢复播放耗时、机型、微信版本、网络类型、视频大小、格式、编码和时长仍为 follow-up；Sprint sign-off 不得把静态测试写成真机通过。

BUG-0085 本地与生产等价自动化验证已完成：管理端 SKU 视频上传前端状态拆分为客户端传输和服务端保存阶段，99% 后显示“正在保存视频，请稍候”；失败后可重新选择同一文件重试，已有视频列表保持稳定。后端上传测试确认 SKU 视频上传返回 `object_key` 与 `/media/{object_key}`，对象写入后可保存到 SKU 并读取回填。部署测试确认 Web Nginx 上传专用 location、600 秒级超时和 `proxy_request_buffering` 配置已覆盖。真实生产环境仍需上线 sign-off 时补充浏览器 Network、外层/容器内 Nginx 与 backend 日志，确认无同类 60 秒 499/504；本次不新增 incidents 文档，因为 `docs/standards/file-upload.md` 已有“99% / 504 诊断”章节，且 best-practice `admin-media-upload-chain.md` 已覆盖同类预防清单。

REQ-0069 本地实现与 Docker Web 入口 smoke 已完成。Task Trace 数据模型、上传首批节点、审计日志查询/详情、脱敏与 OpenAPI/Orval/文档同步均已落地；Docker smoke 覆盖 `localhost:3000` 小图成功、审计日志回查和超限图片统一错误码。PNG Golden Reference 未导出，原因是 Sprint 已有 HTML prototype 与自动化/接口 evidence，本次实现重点为链路可观测性和审计查询，不新增静态 PNG 作为验收阻塞；不新增 incidents/best-practices 文档，原因是 `docs/standards/file-upload.md` 与 `docs/knowledge-base/best-practices/admin-media-upload-chain.md` 已覆盖 99% / 504 诊断与上传链路预防。REQ-0070 本地实现已完成：日志审计页操作者筛选已从 User ID 输入框改为用户名称/账号单选搜索下拉，复用现有系统管理员用户列表 API，选择后仍传 `actor_user_id` 精确过滤；清空、重置、候选空态/失败、同名用户辅助文案和 admin-list 横切回归均已由聚焦前端测试覆盖。真实浏览器移动端截图和生产数据候选表现仍建议在 archive 前补充人工 sign-off。
