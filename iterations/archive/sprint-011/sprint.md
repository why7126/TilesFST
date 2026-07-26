---
note: workflow-sync — workflow-sync 自动同步 — 8/8 Change archived；0 applied；Sprint `completed`
sprint_id: sprint-011
title: Sprint 011 生产阻断缺陷修复、任务链路追踪与日志审计体验增强
status: completed
lifecycle_stage: archive
created_at: 2026-07-23 09:17:23
updated_at: 2026-07-26 15:49:00
---

# Sprint 011 生产阻断缺陷修复、任务链路追踪与日志审计体验增强

## 1. 目标

- 修复生产环境管理端腾讯 COS 视频上传 99% 后返回 504 的问题。
- 修复生产环境小程序商品详情页视频播放启动慢的问题。
- 修复生产环境管理端创建品牌类型 Banner 时 `POST /api/v1/admin/banners` 返回 500 的问题。
- 建立 Docker Web Nginx 上传专用 location 与上传反代超时环境变量化配置。
- 同步外层 HTTPS Nginx 配置说明，确保 COS 对象写入成功后上传接口能稳定返回 `object_key` 与 `/media/{object_key}`。
- 补齐 `/media/{object_key}` 视频 Range/206、视频封面兜底和真机首帧验收，保留后端授权上传与受控读取策略。
- 补齐生产 MySQL `banners` 表 schema drift 迁移和 Admin Banner 保存 smoke，避免 SQLite 与 MySQL 结构差异再次导致 500。
- 增强小程序商品详情页视频全屏播放入口、全屏态长按操作菜单、转发给朋友、保存视频和平台降级验收。
- 修复小程序 SKU 详情页视频内嵌可播放但进入全屏后重新加载很久的问题，保持当前视频上下文并补充真机耗时 evidence。
- 修复管理后台 SKU 视频上传长时间停留 99% 的问题，区分客户端上传与服务端保存阶段，补充上传代理运行配置与生产 smoke 证据。
- 建立通用 Task Trace 追踪能力，将上传等长耗时任务的前端、API、对象存储、数据库和响应节点串联，并支持在管理端审计日志列表与详情中查看。
- 优化管理端日志审计页面操作者筛选，从 User ID 输入改为用户名称/账号单选搜索下拉，并保持 `actor_user_id` 精确过滤。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0068-miniapp-sku-video-fullscreen-actions | 小程序商品详情页视频全屏播放与长按操作菜单 | done | 3.0 人天 | archived `add-miniapp-sku-video-fullscreen-actions`（2026-07-23 23:36:24） |
| REQ | REQ-0069-upload-observability-trace-logs | 任务链路追踪与审计日志查看 | done | 5.0 人天 | archived `add-task-trace-audit-log-view`（2026-07-25 13:21:43） |
| REQ | REQ-0070-audit-log-operator-name-filter | 日志审计页面操作者名称筛选 | done | 1.0 人天 | archived `improve-audit-log-operator-filter`（2026-07-25 14:10:12） |
| BUG | BUG-0081-prod-cos-video-upload-fails | 生产环境腾讯 COS 视频上传 99% 后返回 504 | done | 3.0 人天 | archived `fix-upload-proxy-timeout-config`（2026-07-23 09:40:30） |
| BUG | BUG-0082-prod-miniapp-sku-video-slow-start | 生产环境小程序商品详情页视频播放启动很慢 | done | 5.0 人天 | archived `fix-miniapp-sku-video-slow-start`（2026-07-23 23:13:16） |
| BUG | BUG-0083-prod-admin-brand-banner-save-500 | 生产环境创建品牌类型 Banner 保存接口返回 500 | done | 3.0 人天 | archived `fix-admin-banner-create-schema-drift`（2026-07-23 22:59:21） |
| BUG | BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | 小程序 SKU 详情页视频内嵌可播放但进入全屏后重新加载很久 | done | 1.0 人天 | archived `fix-miniapp-sku-video-fullscreen-reload`（2026-07-24 21:14:14） |
| BUG | BUG-0085-admin-video-upload-stuck-at-99 | 管理后台视频上传长时间卡在 99% | done | 3.0 人天 | archived `fix-admin-video-upload-stuck-at-99`（2026-07-24 21:05:34） |

BUG：`BUG-0081`、`BUG-0082`、`BUG-0083`、`BUG-0084`、`BUG-0085` 已纳入正式范围，优先级高于新增体验能力；当前完成度与验收风险以 Scope 表状态、关联 Change 和 acceptance-report 为准。

Change：已回填 8 个范围项关联 Change；8 archived，0 applied，0 in_progress，0 proposed。所有已纳入范围项均已关联 Change；执行开发与归档时以 Scope 表逐项状态为准。

## 3. 工作量与容量

| 指标 | 值 |
|---|---:|
| 开发 | 2 |
| 测试 | 1 |
| 容量 | 30 人天 |
| 估算 | 24.0 人天 |
| 容量占用 | 80.0% |
| fix 缓冲 | 6.0 人天 / 20.0% |

容量门禁：通过。当前 Sprint 以 `sprint.yaml` 机器范围估算 24.0 人天，占用 80.0%，低于 30 人天容量；fix 缓冲为 6.0 人天 / 20.0%。REQ-0073 已改纳入 sprint-012，本 Sprint 保留已归档生产阻断修复、REQ-0068、REQ-0069 与 REQ-0070 范围。

## 4. 里程碑

| 阶段 | 目标日期 | 交付物 |
|---|---|---|
| 方案落地 | 2026-07-23 18:00:00 | Nginx 上传 location、环境变量设计、外层配置说明、MySQL banners drift 修复方案 |
| 实现与测试 | 2026-07-24 18:00:00 | Web Nginx/Compose/env/docs/tests 更新、MySQL 兼容迁移与 schema drift 测试，OpenSpec tasks 基本完成 |
| 生产 smoke | 2026-07-25 12:00:00 | 同类视频上传 200、COS 对象一致、SKU 表单保存闭环、品牌类型 Banner 新增/刷新仍存在 |
| 小程序视频验收 | 2026-07-25 16:00:00 | 实际 SKU 视频 Range 响应、封面兜底、真机首帧耗时证据 |
| 验收收尾 | 2026-07-25 18:00:00 | acceptance-report、BUG/Change trace、必要知识库沉淀 |
| 视频全屏体验增强与修复 | 2026-07-25 18:00:00 | 视频全屏入口、长按菜单或降级入口、转发/保存/取消、全屏切换不长时间重新加载、DevTools 与真机 evidence |
| Task Trace MVP | 2026-07-25 18:00:00 | `task_trace_id` 模型、上传首批 span、日志审计筛选与详情时间线、OpenAPI/Orval/DB/docs/tests 同步计划 |

## 5. 风险

| 风险 | 影响 | 应对 |
|---|---|---|
| 外层 HTTPS Nginx 未同步 | 容器内修复后生产仍可能 504 | 在部署文档与验收中要求外层配置证据 |
| Nginx 模板渲染失败 | Web 容器启动失败 | 增加模板渲染测试或配置校验，启动时 fail fast |
| `proxy_request_buffering off` 环境差异 | 某些代理链路行为变化 | 可先回滚该项，保留长超时 |
| COS 孤儿对象已存在 | 存储成本与数据清理压力 | 记录清理策略与引用检查，避免重复上传扩大范围 |
| 视频 Range 实现影响非视频媒体 | 图片/PDF 读取可能回归 | 增加完整响应、Range 响应、非法 Range 和非视频读取测试 |
| 真机首帧证据不足 | 无法确认生产体验改善 | 在 apply 中段落盘 SKU、机型、网络、视频大小和首帧耗时 |
| MySQL `banners` 表存在 schema drift | 生产保存仍可能 500 或迁移失败 | 增加 MySQL drift 检查、兼容迁移、幂等验证和备份/回滚说明 |
| Admin Banner 表单回归不足 | 品牌类型保存成功但列表/编辑回填异常 | 覆盖新增、编辑、列表、详情/回填和非法 payload 的非 500 错误响应 |
| 微信 video 全屏态不支持自定义长按菜单 | REQ-0068 可能无法完全复刻图片全屏长按菜单 | apply 前确认平台能力；不可行时采用等价入口并在验收记录 N/A / 降级说明 |
| 保存远程视频受权限、域名或格式限制 | 保存视频可能失败或需要额外签名下载 URL | 默认使用安全媒体 URL；失败给出明确提示；若新增 API/字段则同步 OpenAPI / Orval / docs / tests |
| 已播放视频进入全屏重新加载很久 | 用户误以为全屏不可用，REQ-0068 全屏体验增强出现回归 | 复用当前视频上下文，记录全屏切换加载状态和耗时，真机 evidence 不得只用静态测试替代 |
| 管理端视频上传 99% 阶段表达不足 | 管理员误判上传卡死并重复提交，可能产生孤儿对象 | 区分客户端上传与服务端保存状态；上传 smoke 同时记录 Network、对象 key、Nginx/backend 日志 |
| REQ-0069 涉及 API、DB、管理端 UI 与上传链路 | 范围过大可能挤占 BUG-0085 生产 sign-off 缓冲 | 以 MVP 为边界：先落 `task_trace_id`、span、上传首批场景、日志审计查询/详情；完整 APM、外部日志系统、完整请求/响应体保存和视频转码增强不纳入 |
| Task Trace 写入失败影响主业务 | 可观测性增强反而放大上传失败面 | 实现降级策略；任务追踪失败不得覆盖主业务错误，必须记录可定位摘要和统一错误码 |
| 日志 metadata 脱敏不足 | 审计日志可能暴露密钥、Cookie、真实客户数据或内部路径 | metadata 统一脱敏、截断和安全 JSON 序列化，测试覆盖 Authorization、Cookie、AccessKey、SecretKey、DSN、`.env` 与内部绝对路径 |
| 日志审计操作者候选复用不足 | 现有用户列表 API 若字段过多、不支持名称/账号搜索或不含历史用户，筛选体验可能不足 | apply 阶段先确认现有 API；若新增轻量候选接口，必须同步 OpenAPI/Orval/docs/tests |

## 6. 知识库承接

- 承接 `docs/knowledge-base/best-practices/admin-media-upload-chain.md`：媒体上传必须同时验收前端、后端 API、媒体读取、Nginx、环境与文档五层。
- 承接 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：日志审计列表新增 `task_trace_id` 筛选后，分页 DOM、指标摘要、fixed toast 和无 `window.confirm` 约束必须保持一致。
- 承接 `docs/knowledge-base/best-practices/admin-list-page-consistency.md`：日志审计操作者筛选改造后，分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm` 和移动端筛选区不溢出约束必须保持一致。
- 承接 `docs/knowledge-base/best-practices/admin-form-page-consistency.md`：管理端表单必须覆盖新增、编辑、刷新回填、错误 toast 与服务端错误非 500 语义。
- 承接 sprint-010 复盘行动：生产 smoke 应在 apply 中段落盘，不等 archive 才补证据。
- 承接 sprint-010 复盘行动 T-004：生产 smoke 与真机 evidence 在 apply 中段生成 evidence stub，archive 阶段只校验状态。
- 承接 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md`：小程序详情页和分享直达场景必须记录 DevTools / 真机 evidence，不能把静态测试写成真机通过。
- 承接 sprint-010 复盘：小程序分享必须同时考虑路径参数保留、运行入口同步和埋点失败不阻断。
- 本 Sprint 修复完成后评估是否新增 `docs/knowledge-base/incidents/` 事故沉淀；若不新增，在验收输出中说明理由。
- 复盘已沉淀：`docs/knowledge-base/retrospectives/sprint-011-retrospective.md`。

## 7. 横切预防清单

| 检查项 | 要求 |
|---|---|
| media-upload | 上传成功必须返回 `object_key` 与 `/media/{object_key}`，并可保存到 SKU 表单 |
| deployment | 外层 HTTPS Nginx 与容器内 Web Nginx 上传超时必须同时覆盖 |
| object-storage | COS 已写入但前端失败时必须能诊断并控制孤儿对象 |
| API/Orval | 上传 API Schema 不变则无需 Orval；若变更必须同步 OpenAPI/Orval/docs/tests |
| Docker | 修改 Web Nginx 后必须重建并重启 Web 镜像 |
| miniapp-video | SKU 详情视频必须验证 `poster` 兜底、用户主动播放、页面隐藏暂停和真机首帧耗时 |
| media-read | `/media/{object_key}` 视频 Range/206 必须覆盖合法 Range、非法 Range、完整响应和非视频回归 |
| admin-form | Banner 新增/编辑保存必须覆盖成功 toast、列表刷新、详情回填和服务端错误提示 |
| database/deployment | MySQL 生产表结构兼容迁移必须有 drift 证据、幂等执行结果、备份与回滚边界 |
| miniapp-fullscreen-video | 视频全屏入口、长按菜单或降级入口、转发、保存、取消必须区分静态测试、DevTools 和真机 evidence |
| miniapp-fullscreen-continuity | 已内嵌播放的视频进入全屏后不得长时间重新加载；需记录 inline 可播放、进入全屏、首帧/恢复播放耗时 |
| miniapp-runtime | `tile-detail/index.ts` 与运行时 `index.js` 必须同步，避免微信开发者工具加载入口漂移 |
| admin-video-upload-status | 99% 后必须展示服务端保存/等待确认状态，并保持失败重试与已有视频列表稳定 |
| task-trace | 每一次可追踪任务必须生成或确认 `task_trace_id`，并关联 request_logs、usage_events、audit_logs 与 task spans |
| audit-log-task-view | 管理端日志审计列表支持 `task_trace_id` 查询，详情展示时间线、慢节点、错误码和关联 `request_id` |
| observability-security | 任务追踪 metadata 必须脱敏，禁止保存 Authorization、Cookie、AccessKey、SecretKey、DSN、`.env`、真实客户数据、完整敏感请求体或内部绝对路径 |
| admin-list-operator-filter | 日志审计操作者筛选改造后必须保持分页 DOM、指标卡 DOM、fixed toast、无 `window.confirm`、移动端筛选区不溢出 |

## 8. 依赖

```text
BUG-0081-prod-cos-video-upload-fails
└── fix-upload-proxy-timeout-config
    ├── deployment spec delta
    ├── object-storage spec delta
    ├── Web Nginx upload location
    ├── env/Compose/docs/tests
    └── production smoke evidence

BUG-0082-prod-miniapp-sku-video-slow-start
└── fix-miniapp-sku-video-slow-start
    ├── miniapp-sku-detail-page spec delta
    ├── object-storage spec delta
    ├── /media Range/206 response
    ├── miniapp video poster fallback
    ├── backend + miniapp tests
    └── production real-device first-frame evidence

BUG-0083-prod-admin-brand-banner-save-500
└── fix-admin-banner-create-schema-drift
    ├── banner-management spec delta
    ├── database spec delta
    ├── deployment spec delta
    ├── MySQL banners compatible migration
    ├── Admin Banner create/edit regression
    └── production brand Banner smoke evidence

REQ-0068-miniapp-sku-video-fullscreen-actions
└── add-miniapp-sku-video-fullscreen-actions
    ├── miniapp-sku-detail-page spec delta
    ├── 微信 video 全屏/长按/保存能力确认
    ├── tile-detail 视频全屏入口与上下文保持
    ├── 转发给朋友、保存视频、取消交互或降级入口
    ├── .ts/.js 运行入口同步
    └── static / DevTools / real-device evidence

BUG-0084-miniapp-sku-video-fullscreen-reloads-slow
└── fix-miniapp-sku-video-fullscreen-reload
    ├── miniapp-sku-detail-page spec delta
    ├── inline 播放态进入全屏的当前视频上下文保持
    ├── 全屏切换加载反馈与耗时记录
    ├── tile-detail .ts/.js 运行入口同步
    └── static / DevTools / real-device evidence

BUG-0085-admin-video-upload-stuck-at-99
└── fix-admin-video-upload-stuck-at-99
    ├── tile-sku-management / object-storage / deployment spec delta
    ├── SKU 视频上传客户端进度与服务端保存状态拆分
    ├── 上传代理运行配置与外层 HTTPS Nginx 生效确认
    ├── 对象存储写入成功后的响应闭环与孤儿对象风险诊断
    └── frontend vitest / deployment pytest / production-equivalent smoke

REQ-0069-upload-observability-trace-logs
└── add-task-trace-audit-log-view
    ├── product-usage-logging / object-storage spec delta
    ├── task trace / task span 数据模型与索引
    ├── 日志审计列表 task_trace_id 查询与详情时间线
    ├── 图片、视频、文件上传首批 span 覆盖
    ├── OpenAPI / Orval / DB docs / error codes 同步
    └── backend pytest / frontend Vitest / Docker :3000 上传边界 evidence

REQ-0070-audit-log-operator-name-filter
└── improve-audit-log-operator-filter
    ├── product-usage-logging / web-client spec delta
    ├── 管理端日志审计操作者名称/账号单选搜索下拉
    ├── 仍以 `actor_user_id` 作为日志过滤参数
    └── admin-list 横切回归与候选 API 契约确认

```

## 9. 发布计划

本 Sprint 适合作为生产 hotfix + 小程序体验增强 + 管理端治理体验增强发布。媒体链路修复若仅涉及 Nginx、Docker、环境变量和文档，不改变 API/DB/前端业务逻辑，可按配置/镜像热修策略发布；仍需记录 Web 镜像重建、外层 Nginx reload 与上传 smoke 证据。BUG-0085 若仅修改管理端上传状态文案和测试，不新增 API/DB/Orval，可随 Web 管理端修复发布；若发现生产部署未应用 BUG-0081 上传反代修复，必须同步部署步骤和 smoke 证据后再 sign-off。Banner 修复涉及生产 MySQL schema drift 时，发布前必须记录备份、幂等迁移结果、drift 复查和品牌类型 Banner 保存 smoke 证据。REQ-0068 与 BUG-0084 若仅修改小程序端，不新增 API/DB/Orval，可作为小程序版本体验增强与修复发布；若保存视频需要签名下载 URL 或媒体字段，必须同步 API/Orval/docs/tests 后再发布。REQ-0069 预计会新增或调整日志审计 API 字段、Task Trace 数据模型和管理端日志审计 UI，必须同步 OpenAPI、Orval、`docs/03-api-index.md`、`docs/04-database-design.md`、错误码文档与后端/前端测试；若 apply 阶段发现只能先做后端记录或只做上传首批场景，需在 Change trace 中记录降级范围。REQ-0070 默认仅改 Web 管理端筛选交互，日志查询仍传 `actor_user_id`；若新增用户候选 API，必须同步 OpenAPI/Orval/docs/tests 后再发布。REQ-0073 已改纳入 sprint-012。

## 10. 关联文档

| 类型 | 路径 |
|---|---|
| BUG | `issues/bugs/archive/BUG-0081-prod-cos-video-upload-fails/` |
| BUG | `issues/bugs/archive/BUG-0082-prod-miniapp-sku-video-slow-start/` |
| BUG | `issues/bugs/archive/BUG-0083-prod-admin-brand-banner-save-500/` |
| BUG | `issues/bugs/archive/BUG-0084-miniapp-sku-video-fullscreen-reloads-slow/` |
| BUG | `issues/bugs/archive/BUG-0085-admin-video-upload-stuck-at-99/` |
| REQ | `issues/requirements/archive/REQ-0069-upload-observability-trace-logs/` |
| REQ | `issues/requirements/archive/REQ-0070-audit-log-operator-name-filter/` |
| Change | `openspec/changes/archive/2026-07-23-fix-upload-proxy-timeout-config/` |
| Change | `openspec/changes/archive/2026-07-23-fix-miniapp-sku-video-slow-start/` |
| Change | `openspec/changes/archive/2026-07-23-fix-admin-banner-create-schema-drift/` |
| REQ | `issues/requirements/archive/REQ-0068-miniapp-sku-video-fullscreen-actions/` |
| Change | `openspec/changes/archive/2026-07-24-add-miniapp-sku-video-fullscreen-actions/` |
| Change | `openspec/changes/archive/2026-07-24-fix-miniapp-sku-video-fullscreen-reload/` |
| Change | `openspec/changes/archive/2026-07-26-fix-admin-video-upload-stuck-at-99/` |
| Change | `openspec/changes/archive/2026-07-26-add-task-trace-audit-log-view/` |
| Change | `openspec/changes/archive/2026-07-26-improve-audit-log-operator-filter/` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-media-upload-chain.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-list-page-consistency.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/admin-form-page-consistency.md` |
| 最佳实践 | `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-26 15:45:00 | /sprint-propose | REQ-0073 改纳入 sprint-012，sprint-011 移出 `fix-task-trace-parent-request-model` |
| 2026-07-26 15:43:55 | /sprint-archive | 8/8 Change 已归档，readiness 与 issue promote gate 通过，Sprint 关闭并迁移至 `iterations/archive/sprint-011/` |
| 2026-07-25 13:27:23 | /sprint-propose | 纳入 REQ-0070 与 improve-audit-log-operator-filter |
| 2026-07-25 13:21:43 | /sprint-propose | 纳入 REQ-0069 与 add-task-trace-audit-log-view |
| 2026-07-24 20:50:00 | /sprint-propose | 纳入 BUG-0085 与 fix-admin-video-upload-stuck-at-99 |
| 2026-07-24 20:42:34 | /sprint-propose | 纳入 BUG-0084 与 fix-miniapp-sku-video-fullscreen-reload |
| 2026-07-23 23:36:24 | /sprint-propose | 纳入 REQ-0068 与 add-miniapp-sku-video-fullscreen-actions |
| 2026-07-23 12:08:13 | /sprint-propose | 纳入 BUG-0083 与 fix-admin-banner-create-schema-drift |
| 2026-07-23 12:06:22 | /sprint-propose | 纳入 BUG-0082 与 fix-miniapp-sku-video-slow-start |
| 2026-07-23 09:17:23 | /sprint-propose | 创建 sprint-011，纳入 BUG-0081 与 fix-upload-proxy-timeout-config |
