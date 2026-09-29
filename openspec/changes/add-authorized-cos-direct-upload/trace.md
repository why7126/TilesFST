---
change_id: add-authorized-cos-direct-upload
requirement_id: REQ-0135-authorized-cos-direct-upload
iteration: sprint-029
status: in_progress
created_at: '2026-09-08 08:33:01'
updated_at: '2026-09-11 09:17:10'
impact:
  backend: true
  web: true
  miniapp: false
  admin: true
  database: true
  storage: true
  api: true
product_data_collection_observability:
  status: applicable
  affected_layers:
  - web_admin
  - backend_api
  - request_logs
  - usage_events
  - task_traces
  - task_trace_spans
  - object_storage
  reason: 授权确认复制派生绑定为跨系统任务；小程序和店主端仅展示回归，上传封装N/A。
  validation: 本地行为契约、控制/绑定/派生/清理阶段关联、失败降级和90/180天定向保留测试通过；Compose、生产和真机边界分别由5.3～5.5验收。
prototype_refs:
- issues/requirements/review/REQ-0135-authorized-cos-direct-upload/prototype/web/index.html
- issues/requirements/review/REQ-0135-authorized-cos-direct-upload/prototype/web/context.md
---

# Change跟踪

## 变更记录
| 时间 | 动作 | 结果 |
|---|---|---|
| 2026-09-08 08:33:01 | /req-opsx | CLI创建及生成工件；未实现，C-001～005未关闭。 |

## 原型与证据清单

- [ ] PNG导出及1440px Skeleton首轮确认
- [ ] 1440px关键状态及矮视口截图
- [ ] computed style、CSS栈回归与实际媒体预览
- [ ] Mock/API边界和最终一致性复核
- [ ] C-001～005及24条验收证据

小程序impact为展示兼容回归，不新增上传代码。规格校验不能替代生产、Compose、真机证据。Sprint完整范围13人天，阶段一不单独关闭REQ。


## 本轮实施前置检查

Sprint inclusion通过，REQ为in_sprint且Change在sprint-029正式范围。admin-modal/media-upload两标签、AC-XCUT、知识库引用及读库均pass；admin-filter-dropdown为N/A（未变更筛选控件），横切结论WARN-PROCEED（引用draft且视觉证据未完成）。观测门禁脚本通过，UI Contract已存在。

仅完成任务1.1的路由/权限/响应/幂等契约冻结（1/22）；SDK只读检查支持后续验证准备，任务1.2/1.3不标完成。C-003参数待输入，C-001/C-002验证门禁尚未关闭，未进入2～3组业务实现，未编辑src。不存在功能通过、生产通过或可归档结论。Workflow opsx.apply事件仅表示本轮执行记录，不替代任务完成度。


## 直接验证结果回填

已执行实际COS签名、分片、复制实验及SQLite/MySQL候选CAS实验，数据和证明边界见 [validation.md](validation.md)。初始配置采用8MiB/并发2，其他工程默认可配置；参数不再等待用户逐项输入，正式p95目标待基准测量。C-001～003尚未全部关闭，当前应用任务仍1/22，不宣称业务实现已通过。COS已启用版本控制，清理实现必须携带会话对应版本ID，保护稳定副本及业务引用；不能仅创建删除标记。

测试清理终验：本轮5个随机前缀的37个对象历史版本及35个删除标记，共72项已按确切Key/VersionId删除，重新列举确认不存在；隔离MySQL容器及卷已移除。


## 浏览器与持久会话实现验证

完成阶段一设计门禁1.2～1.4及持久会话2.1，本轮新增4项完成，累计5/22。2.2/2.3的底层COS适配已部分实现，但控制API、实际媒体内容校验、业务绑定、清理任务及Web接入未完成，不能将整个任务勾选。没有部署业务代码或启用新上传入口。

- 浏览器：隔离Chromium（localhost:3000来源）真实CORS PUT，正确长度200、超长403、过期403、新有效签名200；分片上传ETag可读，服务端合并总大小1048580字节正确；测试对象3个版本已清理。
- COS配置：原桶无CORS（NoSuchCORSConfiguration），现增加仅管理端HTTPS域名与localhost:3000的GET/HEAD/PUT，content-type/content-md5和ETag/Content-Length/x-cos-version-id暴露，MaxAge600；已回读确认，不改变桶读写权限。若需回滚仅删除ID为req0135-authorized-web-upload的本轮规则并保留其他规则。
- 会话实现：新增media_upload_sessions、幂等迁移和Pydantic入参/状态模型；CAS、租约心跳与恢复、幂等请求摘要、过期及取消/绑定/清理约束。不同用户无法读取，绑定归属字段支持字符串用户ID；MySQL幂等键使用二进制排序规则保持大小写语义与SQLite一致。
- 本地回归：tests/test_media_upload_sessions.py 10项 + tests/test_cos_upload_gateway.py 12项 + tests/test_media_storage.py 32项，共54项通过。存在项目已有弃用警告，无测试失败。
- 真实MySQL：一次性MySQL8.2容器执行最新DDL连续两次及相同10项仓储测试，全部通过；测试容器与卷已移除。这不是生产数据库迁移证据。
- 新COS适配器：真实请求测试逐片预签名、ListParts精确大小校验、固定版本完成确认、受限读取、固定版本复制通过；测试对象各轮均按版本清理。未执行生产业务绑定。

发现并修复的两项实现问题：SQLite最外层SAVEPOINT可能先于调用方rollback提交（test_create_rollback_leaves_no_session反例失败后改为原生冲突INSERT并通过）；COS复制返回目标VersionId位于解析体，不能只读取x-cos-version-id响应头（真实SDK字段名取证后修复，单元及真实COS复测通过）。证据仅限本实现和测试场景。

观测门禁、OpenSpec严格校验、中文语言、目录及上下文预算校验通过；当前仅增加基础模块，尚无新业务HTTP路由，Orval需在2.2接口接入时同步。完整Web :3000业务联调、性能门槛、图片阶段、视觉证据和全量验收仍未完成，不可归档。


## 当前交付状态

累计21/22任务完成，状态in_progress，不可归档。SKU视频和图片、品牌Logo、Banner、头像、证书图片/PDF已接入，客户端行为、后端绑定与清理观测已补齐。多入口真实Compose/COS集成、Web四联与视觉矩阵、冻结性能和回滚通过；4.4的小程序/店主端新媒体展示及真机证明尚未完成。24条AC与证明边界已汇总至acceptance-matrix.md。功能默认关闭，未部署生产。详细证据以validation.md为准。


## 图片处理选型

用户因新增费用约束选择后端异步处理，选型已同步requirement.md第8节与design.md D5。不继续数据万象授权或云端处理实验；浏览器授权直传COS保持不变。工作者资源、超时和重试实施上限见D5，资源验证及后端异步实现证据见validation.md，4.1/4.2已关闭，其他图片入口和完整验收保持未完成。


本轮新增4.3、5.1～5.5完成项，累计21/22；最新回归与真实COS性能、回滚、清理证据见validation.md与acceptance-matrix.md。4.4仍待验收环境中的小程序/店主端展示验证，不部署生产、不申请归档。


## 小程序补验进度

9月11日新增5类真实COS直传绑定的小程序DevTools展示四联证据，视频首播至43秒；47项后端聚焦验证通过，小程序静态37通过/1项既有环境端口差异。21/22保持in_progress；店主Web无媒体入口的适用性与真机证据边界待用户处理。具体证据、失败恢复与清理以validation.md最新章节为准。
