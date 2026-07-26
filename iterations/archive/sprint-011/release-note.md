---
sprint_id: sprint-011
title: Sprint 011 Release Note
status: published
created_at: 2026-07-23 09:17:23
updated_at: 2026-07-26 15:43:55
---

# Sprint 011 Release Note

## 已发布内容

| 类型 | ID | Change | 用户价值 |
|---|---|---|---|
| BUG | BUG-0081-prod-cos-video-upload-fails | fix-upload-proxy-timeout-config | 修复生产管理端视频上传 99% 后返回 504 的问题，降低 COS 孤儿对象风险 |
| BUG | BUG-0082-prod-miniapp-sku-video-slow-start | fix-miniapp-sku-video-slow-start | 修复生产小程序商品详情页视频启动慢的问题，提升客户查看商品视频素材体验 |
| BUG | BUG-0083-prod-admin-brand-banner-save-500 | fix-admin-banner-create-schema-drift | 修复生产管理端创建品牌类型 Banner 返回 500 的问题，恢复品牌 Banner 配置发布能力 |
| BUG | BUG-0084-miniapp-sku-video-fullscreen-reloads-slow | fix-miniapp-sku-video-fullscreen-reload | 修复小程序 SKU 详情页视频内嵌可播放但进入全屏后重新加载很久的问题，保持视频全屏播放连续性 |
| BUG | BUG-0085-admin-video-upload-stuck-at-99 | fix-admin-video-upload-stuck-at-99 | 修复管理后台 SKU 视频上传长时间停留 99% 的问题，让客户端上传和服务端保存状态可感知 |
| REQ | REQ-0068-miniapp-sku-video-fullscreen-actions | add-miniapp-sku-video-fullscreen-actions | 增强小程序商品详情页视频全屏播放入口和全屏态转发、保存、取消交互 |
| REQ | REQ-0069-upload-observability-trace-logs | add-task-trace-audit-log-view | 建立任务链路追踪与审计日志查看能力，用 `task_trace_id` 串联上传等长耗时任务的各节点日志 |
| REQ | REQ-0070-audit-log-operator-name-filter | improve-audit-log-operator-filter | 将日志审计操作者筛选从 User ID 输入优化为用户名称/账号搜索下拉，降低管理端查询门槛 |

## 影响范围

- 管理端：SKU 视频上传体验恢复。
- 管理端：SKU 视频上传 99% 后展示服务端保存/等待确认状态，降低重复提交和孤儿对象风险。
- 管理端：品牌类型 Banner 新增/编辑保存恢复，列表和详情回填保持一致。
- 小程序：SKU 详情页视频播放首帧体验与封面兜底增强。
- 小程序：SKU 详情页视频全屏入口、长按菜单或降级入口、转发给朋友、保存视频和取消交互增强。
- 小程序：SKU 详情页已内嵌播放的视频进入全屏后保持当前视频上下文，避免长时间重新加载。
- 部署：Web Nginx 上传专用 location、上传超时环境变量、外层 HTTPS Nginx 配置说明。
- 数据库：生产 MySQL `banners` 表按兼容迁移补齐与 SQLAlchemy 模型/Pydantic Schema 对齐的字段。
- 对象存储：保持腾讯 COS/S3 兼容对象存储单桶策略与 `/media/{object_key}` 受控读取，并补齐视频 Range/206 验收。
- 日志审计：新增或扩展 Task Trace 查询与详情时间线，支持按 `task_trace_id` 追踪图片、视频、文件上传链路。
- 日志审计：操作者筛选改为用户名称/账号单选搜索下拉，候选项仅展示账号和用户名称两行，仍按 `actor_user_id` 精确过滤。
- 日志审计：时间范围筛选固定为最近5分钟至最近7天的常用窗口，移除全部时间；列表操作者列显示账号并单行展示。

## 不包含

- 不新增上传 API。
- 不新增管理端上传 API 字段或数据库字段。
- 不新增 Banner API 字段或 Banner 类型。
- 不引入视频转码、多清晰度或小程序直连对象存储。
- 不允许前端直连未授权 COS 写入。
- 不新增视频海报、管理端配置或默认 API/DB/Orval 变更；若实现保存视频需要签名下载 URL，需另行同步契约。
- 不建设完整 APM 平台、外部日志系统、跨服务拓扑大屏、完整请求/响应体保存或历史任务回填。
- 不在 REQ-0069 中新增视频转码、压缩、多清晰度或封面生成增强能力。
- 不按用户名称直接过滤日志，不改写审计日志事实源。
- 默认不新增用户管理能力、数据库字段或对象存储策略；若用户候选搜索需要新增 API，需随实现同步契约。
- 不接入外部 APM、跨服务拓扑大屏、全量历史回填或小程序观测入口。

## 发布前检查

- Web 镜像已重建并重启。
- 外层 HTTPS Nginx 已 reload。
- 同类视频上传返回 200。
- COS 对象 key 与接口响应一致。
- SKU 表单保存后刷新仍有关联视频。
- 管理端 SKU 视频上传 99% 后有明确服务端保存/等待确认状态，失败可重试且不破坏已有视频列表。
- 小程序实际 SKU 视频点击播放有封面/兜底等待态，并记录首帧耗时。
- `/media/{object_key}` 视频 Range 请求返回 `206 Partial Content`。
- 生产 MySQL `banners` schema drift 检查通过，迁移执行前已记录备份/回滚边界。
- 管理端创建品牌类型 Banner 返回 200，刷新列表和编辑回填仍可见。
- Banner 非法 payload 返回 4xx 业务错误，不再出现 500。
- 小程序商品详情页视频全屏入口可感知，退出全屏后回到当前 SKU 和当前媒体上下文。
- 小程序商品详情页视频内嵌播放后进入全屏，不出现长时间重新加载；需记录点击全屏到首帧或恢复播放耗时。
- 视频全屏态长按菜单或降级入口覆盖“转发给朋友”“保存视频”“取消”。
- DevTools 与至少一台真机 evidence 区分记录；真机不可用时标记 `real_device_follow_up` 或 `blocked`。
- 每次可追踪业务任务生成或确认 `task_trace_id`，并关联请求日志、行为事件、审计操作和任务节点。
- 图片、视频、文件上传记录前端选择、上传开始、请求体上传完成、后端接收、文件校验、对象存储写入、数据库记录、响应返回、前端完成或失败节点。
- 日志审计列表可按 `task_trace_id` 查询，详情可查看节点时间线、耗时、状态、错误码和关联 `request_id`。
- Task Trace metadata 已脱敏，不保存 Authorization、Cookie、AccessKey、SecretKey、DSN、`.env`、真实客户数据、完整敏感请求体或内部绝对路径。
- 日志审计操作者下拉支持按用户名称/账号模糊搜索、单选、清空和重置。
- 操作者下拉选择后日志查询请求使用用户 `id` 作为 `actor_user_id`，不得把显示名称作为过滤参数。
- 同名用户通过账号行区分，候选加载、空态和失败状态不影响日志列表错误状态。
- 时间范围筛选默认最近1天，且仅提供最近5分钟、10分钟、30分钟、1小时、3小时、6小时、12小时、1天、2天、3天、7天。
- 日志审计页面保留分页 DOM、指标卡 DOM、fixed toast、无原生确认框，移动端筛选区不溢出。
- 聚合查询在 SQLite demo 与生产 MySQL 下均可用，避免无条件全表扫描后在应用内聚合。
- 若新增或调整观测 API，已同步 OpenAPI、Orval、`docs/03-api-index.md`、错误码文档和后端/前端测试。
