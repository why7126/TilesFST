---
req_id: REQ-0135-authorized-cos-direct-upload
status: captured
created_at: '2026-09-07 22:38:57'
updated_at: '2026-09-07 22:38:57'
recorded_by: product
source: 用户反馈与 /explore 分析
priority_hint: P1
parent_requirement: null
related_requirements:
- REQ-0136-signed-cos-direct-media-read
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
  reason: 上传授权、确认和派生处理涉及多阶段外部依赖；小程序无新增上传入口，本条小程序及店主端仅为关联媒体展示兼容回归。
  validation: capture阶段完成代码与现有证据范围核查；功能、性能、权限及真机验证尚未执行，按建议验收要点补证。
---

# 一句话

后端授权的 COS 媒体直传与上传确认。

# 原始描述

媒体上传与展示采用后端授权的COS直连，分阶段覆盖视频和图片，补齐上传确认、派生处理、签名刷新、历史回退及链路观测。

# 范围与阶段

- 管理端通过后端鉴权申请本次上传授权，再将文件直接传至 COS；后端控制对象 Key、允许的大小/类型/前缀、有效期与操作权限，端侧不持有永久密钥。
- 第一阶段优先视频直传，支持进度、失败重试、取消及大文件分片策略；第二阶段覆盖图片上传与派生处理。阶段切分建议在 PRD 中确认。
- 后端完成确认需校验对象存在、大小、真实内容类型和归属，区分上传完成、处理完成、业务保存完成；未经确认对象不得作为有效业务媒体发布。确认与重试需幂等，防止重复关联或确认后被旧授权覆盖。
- 保留原图和现有缩略图、展示图规格；图片上传后处理、降级与重试需有可查询状态。后端异步处理或数据万象方案留待设计比较，不预先承诺引入收费服务。
- 兼容 pending 到正式业务目录的归属规则，避免通过后端下载并重传大文件完成迁移；明确 COS 侧复制、业务保存失败、孤儿对象和未完成分片清理策略。
- 删除、替换、业务关联与权限判断继续由后端控制；不扩展小程序上传入口，不包含视频转码/CDN建设/服务器迁移。

# 背景与证据边界

用户确认生产使用北京轻量服务器与广州 COS，公网带宽约 3 Mbps。2026-09-05 线上三条视频请求的请求体约 18.7、59.1、63.2 MB，存储完成阶段累计耗时约 52、166、177 秒；约 2.9 Mbps 的表现支持跨地域出口瓶颈判断（probable），不能将累计阶段当成独立 COS 写入耗时。证据来源为管理端日志详情和用户提供的宿主机 DNS 结果，不包含后端容器网络复测。

代码依据：`src/backend/app/api/v1/uploads.py`、`src/backend/app/modules/media/storage.py`、`src/backend/app/services/tile_sku_admin_service.py`。现有上传由后端转发，图片派生在上传链路完成。

# 待澄清

- [ ] 确定各媒体大小、并发、超时、重试和分片阈值，以及性能验收基线。
- [ ] 比较图片后处理部署位置、执行方式、规格一致性及成本。
- [ ] 确定上传会话持久化、状态查询、授权失效与对象不可变策略。

# 建议验收要点

- 浏览器 Network 证明大文件请求直达 COS，后端只处理授权、确认与业务请求；对比相同文件的耗时、成功率和服务器出口流量。
- 覆盖越权、超限、类型伪装、错误对象 Key、重复确认、确认后覆盖、断网重试、取消和残留清理。
- 原图保留，派生图符合规格；处理失败可识别并重试，不把传输完成显示为业务保存完成。
- 新建与编辑 SKU、品牌、Banner、头像和证书等现有上传入口按实际支持类型列出回归矩阵。
- 日志关联申请、传输、确认、处理、保存阶段，标注证据来源；客户端不采集永久密钥、签名 URL 参数或原始文件内容。

# 影响与边界

本次仅 capture，不生成 PRD、不实现代码、不关联 Sprint 或 Change。P1 为优先级建议，待评审确认。后续实现预计涉及 API、Web、管理端及相关媒体端侧适配；接口变更需同步 OpenAPI/Orval 与测试，数据库结构按设计决定。部署配置、COS权限及域名变化需 Docker Compose 集成验证，线上验收另行记录。

# 规范依据

遵循 `rules/requirement-management.md`、`rules/issues-lifecycle.md`、`rules/document-governance.md`、`rules/security.md`、`rules/media.md`、`rules/object-storage.md`、`rules/root-cause-evidence.md`、`rules/agent-context-budget.md`；观测事实源为 `docs/standards/product-data-collection-observability.md` 与 `docs/standards/task-trace-coverage.md`。
