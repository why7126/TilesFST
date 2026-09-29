---
change_id: add-signed-cos-direct-media-read
requirement_id: REQ-0136-signed-cos-direct-media-read
iteration: sprint-030
status: proposed
created_at: '2026-09-08 08:47:12'
updated_at: '2026-09-11 08:45:38'
impact:
  backend: true
  web: true
  miniapp: true
  admin: true
  database: false
  storage: true
  api: true
capabilities:
  new:
  - signed-media-read
  modified:
  - media-multi-variant-images
product_data_collection_observability:
  status: applicable
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
  reason: 三端读取与授权、恢复、外部候选解析适用；直接COS传输不伪造后端读取日志，DB不预设结构变更。
  validation: 三端事件契约、API/日志/Trace脱敏及本地UI采集通过；详细证据见validation.md；生产设备与性能待验。
prototype_refs:
- issues/requirements/review/REQ-0136-signed-cos-direct-media-read/prototype/web/media-states.html
- issues/requirements/review/REQ-0136-signed-cos-direct-media-read/prototype/web/context.md
knowledge_base_refs:
- docs/knowledge-base/best-practices/admin-list-page-consistency.md
- docs/knowledge-base/best-practices/admin-form-page-consistency.md
- docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md
- docs/knowledge-base/best-practices/admin-media-upload-chain.md
- docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
- docs/knowledge-base/retrospectives/sprint-028-retrospective.md
---

# Change跟踪

## 变更记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-09-08 08:47:12 | /req-opsx | CLI创建proposal/design/specs/tasks；DS局部策略，未实现，C-001至C-004未验收关闭。 |

## 原型与证据清单

- [ ] 可选PNG导出；缺少PNG不代替真实页面视觉门禁。
- [x] Skeleton首轮确认与1440px/小程序等价证据。
- [x] Skeleton关键状态、实际低视口与computed style；完整产品验收另见validation.md。
- [ ] 视频真实恢复、COS/Compose/设备证据与四联矩阵。
- [ ] 17功能AC、12横切AC和性能对照。

## 就绪与冲突结论

Partially Ready：已评审并在sprint-030，五件套与HTML齐全；PNG可选，参考实践部分draft。DS局部状态策略已定。Conflict Resolution与UI Contract见design.md；没有产品范围决策阻塞，技术验证按tasks依赖关闭。已有基础实现，当前证据与阻塞见下节；无自动follow-up。

## 实施进展与验收边界

用户已确认Skeleton及本地Web PDF正文。实现、自动验证、人工待验及外部阻塞统一见[剩余验收](remaining-acceptance.md)；测试、根因和17+12项AC证据见[validation.md](validation.md)。

剩余2.5、3.2、5.1至5.3依赖完整端侧及可比性能证据；4.4已完成适用验证。微信真机按用户决定跳过，不计通过；archive_ready: false。未发送opsx.apply完成事件，不自动发布或归档。

执行链路复盘：Sprint门禁通过；授权、三端消费、旧媒体权限及观测已实现，联调发现的混合证书/事件字典/性能维度问题已有修复和回归。部分完成只运行无事件Workflow Sync及AI Usage记录。规范优化建议：无明显优化点。未自动创建follow-up Issue/Change。

### PDF预览验收更新

主动文件预览按当前身份独立管理控制器，避免新窗口隐藏来源页时取消授权；PDF下载为临时blob预览，兼容COS attachment响应头，并保留超时、身份/资源变化取消及释放约束。本地Web已获授权并完成更新；PDF正文已由用户人工确认正常显示；工具自身仍受blob URL安全策略限制。当前验证边界以[验证记录](validation.md#本地web更新及pdf人工确认边界)为准；微信真机按用户决定跳过，当前14/19，archive_ready=false。

当前未完成任务的依赖、补验结果及恢复条件统一见[剩余验收](remaining-acceptance.md)，进度14/19，未发送完成事件。
