## 背景

当前对象存储已采用单 Bucket 与标准媒体前缀，`object-storage` 规格已经覆盖上传鉴权、受控读取、图片派生图和部分历史 key 修复。REQ-0131 进一步把 Key 目录从“媒体资源类型目录”统一为“业务对象 id 目录”，目标是让媒体归属、迁移、审计和排障都能通过稳定规则追溯。

本 Change 不直接实现业务代码，而是为后续 `/opsx-apply` 固化设计边界、规格 delta 和任务顺序。

## 目标与非目标

目标：

- 建立统一媒体 Key 矩阵，覆盖头像、品牌 Logo、Banner 图片、SKU 图片、SKU 视频、品牌证书图片和证书文件。
- 对业务对象创建前上传统一使用 pending 目录，保存成功后 formalize 到业务对象 id 目录。
- 保留旧 key 读取兼容，确保旧数据库引用仍可通过 `/media/{object_key}` 或等价受控 URL 读取。
- 提供受控存量迁移：dry-run、apply、audit、幂等、备份确认和回滚说明。
- 将产品数据采集与链路观测作为本 Change 的固定验收门禁。

非目标：

- 不在本 Change 中默认删除旧对象。
- 不新增媒体资产中心、迁移审计页面或独立 UI。
- 不新增视频转码、多清晰度播放或 PDF 首图渲染能力。
- 不要求客户端根据业务 id 拼接对象存储路径。

## 关键决策

### D1 统一 Key 矩阵

新媒体正式 Key 使用 `{media_prefix}/default/{business_media_type}/{business_id}/{uuid}.{ext}` 扁平形态。目标矩阵：

| 媒体类型 | 业务对象 id | 正式目录 |
|---|---|---|
| 用户头像 | `user_id` | `images/default/user-avatars/{user_id}/{uuid}.{ext}` |
| 品牌 Logo | `brand_id` | `images/default/brand-logos/{brand_id}/{uuid}.{ext}` |
| Banner 图片 | `banner_id` | `images/default/banners/{banner_id}/{uuid}.{ext}` |
| SKU 图片 | `tile_id` | `images/default/tiles/{tile_id}/{uuid}.{ext}` |
| SKU 视频 | `tile_id` | `videos/default/tiles/{tile_id}/{uuid}.{ext}` |
| 品牌证书图片 | `certificate_id` | `images/default/brand-certificates/{certificate_id}/{uuid}.{ext}` |
| 品牌证书 PDF/文档 | `certificate_id` | `files/default/brand-certificates/{certificate_id}/{uuid}.{ext}` |

选择该方案是为了让业务媒体类型和业务对象 id 成为排障第一索引，同时保持 `images/`、`videos/`、`files/` 语义前缀不变，并避免 `users/{id}/avatars`、`brands/{id}/logos`、`tiles/{id}/images` 等重复语义层。

### D2 pending 与 formalize

当业务对象 id 未产生时，上传写入同类资源下的 `pending/` 目录；业务对象保存成功后，由后端 formalize 原图、视频、文件和图片派生图，并同步数据库媒体引用。formalize 必须幂等：目标已存在且内容可确认一致时跳过，失败时不得让业务记录引用不存在对象。

### D3 旧 key 兼容优先

系统继续把数据库保存的完整 key 作为读取事实源。`/media/{object_key}` 或等价受控 URL 必须直接按保存 key 读取对象，不允许端侧或后端展示层根据新目录推导旧对象新路径。旧对象和已短暂生成的过渡目录只作为兼容来源，旧对象清理晚于迁移审计，并作为单独高风险动作确认。

### D4 迁移以审计和回滚为中心

存量迁移默认 dry-run，不写数据库和对象存储；apply 必须显式触发并要求数据库备份与对象存储 bucket/prefix 备份确认。迁移任务需要输出脱敏摘要、失败分类、目标冲突、对象缺失、幂等复跑和二次审计结果。未验证反向脚本不得被描述为默认可靠回滚，回滚以快照恢复和旧 key 兼容保留为主。

### D5 API 与 DB 变更采取最小化

实现优先复用既有媒体引用字段，例如 `avatar_object_key`、`logo_object_key`、`image_object_key`、`object_key`、`file_key`。如不调整响应字段，仅改变后端生成的 key 和 URL 指向，则 OpenAPI/Orval 可记录 N/A；如新增字段、错误码或响应结构，必须同步 OpenAPI、Orval、API 文档和端侧测试。

若引入媒体别名表、迁移状态表或索引，必须同步 SQLite/MySQL schema、迁移、数据库设计文档和测试；否则需要在验收中说明继续复用既有业务表媒体字段。

## 原型与验收冲突处理

`prototype/web/context.md` 明确本需求默认不新增用户可见页面，不生成独立 HTML 或 PNG 原型。事实源优先级为：

```text
prototype/web/context.md > acceptance.md > rules/ui-design.md > openspec/specs
```

冲突处理：

- 若实现只调整上传 Key、formalize、迁移和文档，复用既有管理端上传入口做验收，不新增 UI Contract。
- 若后续新增迁移任务页面、审计报告页或媒体资产管理页，必须另行补充 UI Contract、Design System 复用、权限和脱敏展示规则。
- 既有上传控件必须继续覆盖 `idle -> uploading -> done/failed`、同会话即时回显、保存后重新打开回显和字段级错误展示。
- UI 不得展示 object key、内部路径、对象存储 endpoint、bucket、raw URL 或维护脚本输出。

## 产品数据采集与链路观测

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers:
    - request_logs
    - task_traces
    - task_trace_spans
    - backend_api
    - web_admin_request_flow
    - wechat_miniapp_request_flow
    - maintenance_jobs
  reason: 本变更涉及媒体上传、业务对象保存后 formalize、存量对象迁移、维护任务审计、受控媒体 URL 和数据库媒体引用一致性，需要记录请求日志、任务链路、流程节点和脱敏维护摘要。
  validation: 实现阶段必须补齐上传/formalize/迁移任务的脱敏字段、失败分类、trace 或维护摘要测试，并在验收中记录 key/object/URL/render/Network 证据。
```

日志、Trace 和维护输出不得保存完整 object key、完整请求体、完整响应体、Authorization header、Cookie、Token、access key、secret key、真实 `.env` 内容或本机绝对路径。允许输出标准前缀、资源类型、业务对象 id、数量、状态、失败原因枚举和不可逆 key hash。

## 迁移计划

1. 实现并验证新上传 Key 生成和 pending/formalize，不改变旧 key 读取。
2. 补齐图片派生图在正式业务对象目录中的生成、迁移或补生成策略。
3. 实现存量迁移 dry-run，确认候选数量、失败分类、目标冲突和对象缺失。
4. 在测试环境执行 apply 和二次审计，验证数据库引用、对象存在性、URL 可读、端侧 render/Network 和幂等复跑。
5. 更新 rules、长期文档、Runbook、发布验收模板和 OpenSpec 规格。
6. 生产执行前确认 DB 备份和对象存储 bucket/prefix 备份；生产 apply 后保留审计摘要。

## 风险与缓解

- 旧媒体不可见 → 保留旧 key 直接读取兼容，禁止端侧推导路径，迁移前后抽样验证旧 URL。
- 迁移误写数据库引用 → 默认 dry-run，apply 前备份，分批执行，失败时保留源对象和可重试上下文。
- 派生图与原图目录不一致 → formalize 和迁移同时处理 `.thumb.webp`、`.display.webp`，缺失时进入维护候选。
- 日志泄露对象路径或凭据 → 输出脱敏 key hash、标准前缀和失败枚举，增加敏感字段测试。
- API/DB 影响被漏判 → tasks 中要求明确 OpenAPI/Orval 和 SQLite/MySQL N/A 或同步证据。

## 开放问题

- 存量迁移是否在首个发布版本执行，还是先只改变新上传并保留旧 key 兼容。
- 是否需要引入媒体别名表或迁移状态表，还是继续仅更新既有业务字段。
- 旧对象保留周期、清理窗口和生产回滚责任需在发布计划中确认。
