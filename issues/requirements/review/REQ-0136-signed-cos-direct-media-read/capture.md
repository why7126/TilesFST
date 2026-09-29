---
req_id: REQ-0136-signed-cos-direct-media-read
status: captured
created_at: '2026-09-07 22:38:57'
updated_at: '2026-09-07 22:38:57'
recorded_by: product
source: 用户反馈与 /explore 分析
priority_hint: P1
parent_requirement: null
related_requirements:
- REQ-0135-authorized-cos-direct-upload
product_data_collection_observability:
  applicability: applicable
  affected_layers:
  - web_admin
  - web_catalog
  - wechat_miniapp
  - backend_api
  - request_logs
  - usage_events
  - task_traces
  - task_trace_spans
  - object_storage
  reason: 读取授权与端侧续签、媒体加载回退涉及请求和行为链路；Task Trace按多阶段授权/批量解析适用性在设计时细化，普通COS读取使用端侧事件及存储访问证据。
  validation: capture阶段完成代码与现有证据范围核查；功能、性能、权限及真机验证尚未执行，按建议验收要点补证。
---

# 一句话

Web 与小程序 COS 签名直读及过期恢复。

# 原始描述

媒体上传与展示采用后端授权的COS直连，分阶段覆盖视频和图片，补齐上传确认、派生处理、签名刷新、历史回退及链路观测。

# 范围与阶段

- Web 管理端、店主展示端与小程序的现有媒体展示统一由后端返回受控 COS 读取地址，数据库继续保存稳定对象 Key；不新增公开桶权限，不让端侧拼接 bucket/endpoint。
- 优先覆盖视频播放与拖动读取，再统一图片缩略图、展示图、原图预览及现有附件读取；按页面和字段完成覆盖矩阵，具体阶段在 PRD 确认。
- 在保留业务权限边界的前提下生成短期读取授权；定义有效期、页面恢复和原图预览时的刷新、有限次数重试、失败占位及视频播放位置恢复。
- 统一处理派生图缺失、历史路径映射、旧 `/media/` 地址和外部绝对 URL；保留可回滚代理入口，防止无限回退或静默将全部流量导回服务器。
- 核对小程序域名、浏览器跨域、COS 域名预览条件及缓存寿命；签名信息不落库为长期业务引用，不进入行为日志或错误明文。
- 不包含浏览器上传实现、CDN建设、视频转码、服务器迁移；与关联直传需求通过稳定媒体标识协作，可独立交付。

# 背景与证据边界

生产服务器约 3 Mbps 出口不适合承担多人媒体转发。当前仓库已有 `OBJECT_STORAGE_DIRECT_READ_ENABLED` 与默认 300 秒签名能力，但仅部分图片字段接入；Web 与小程序的视频仍固定使用 `/media/`。已检查的端侧错误处理无自动续签，COS 直读会绕过代理的原图候选与历史 Key 回退。

代码依据：`src/backend/app/modules/media/storage.py`、`src/backend/app/services/tile_sku_admin_service.py`、`src/backend/app/services/miniapp_home_service.py`、`src/web/src/features/admin/components/FallbackListImage.tsx`、`src/miniapp/pages/tile-detail/index.ts`。现有测试 `tests/test_media_storage.py` 的直读用例为模拟存储 URL 生成验证，不代表线上 COS 或小程序真机已通过。

# 待澄清

- [ ] 确定逐页面媒体字段覆盖矩阵及读权限、有效期和缓存策略。
- [ ] 比较直接返回签名 URL 与稳定入口鉴权跳转，明确视频 Range、重播及续签行为。
- [ ] 确定历史媒体回退顺序、缺图占位、灰度开关与回滚条件。

# 建议验收要点

- Web 和小程序正常媒体请求直达 COS，验证视频首播、Range 拖动、重播、图片原图预览与附件读取，服务器不转发主要文件流量。
- 页面停留超过有效期、前后台切换、网络中断后恢复可有限续签重试；已过期备用 URL 不被当成有效恢复。
- 覆盖缺失派生图、历史对象、权限拒绝、下架对象、签名失效与代理回滚，不通过回退放宽原权限。
- 小程序合法域名和真机验证单独记录，不用静态测试代替；比较加载耗时、失败率、回退比例与服务器出口流量。
- 保留端侧媒体加载/失败/续签/回退事件，关联后端授权请求和可用 COS 侧证据；日志脱敏且采集失败不阻断展示。

# 影响与边界

本次仅 capture，不生成 PRD、不实现代码、不关联 Sprint 或 Change。P1 为优先级建议，待评审确认。后续实现预计涉及 API、Web、管理端及相关媒体端侧适配；接口变更需同步 OpenAPI/Orval 与测试，数据库结构按设计决定。部署配置、COS权限及域名变化需 Docker Compose 集成验证，线上验收另行记录。

# 规范依据

遵循 `rules/requirement-management.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、`rules/security.md`、`rules/media.md`、`rules/object-storage.md`、`rules/root-cause-evidence.md`、`rules/agent-context-budget.md`；观测事实源为 `docs/standards/product-data-collection-observability.md` 与 `docs/standards/task-trace-coverage.md`。
