---
created_at: '2026-09-08 08:31:48'
updated_at: 2026-09-08 17:02:59
---

# COS 授权直传设计

## 上下文与边界

来源：issues/requirements/review/REQ-0135-authorized-cos-direct-upload/ 六件套及 review.md。Readiness=Partially Ready；范围已批准，C-001～005尚未关闭。单Change按两阶段实施，不能只完成视频便归档。现有上传控制位于 src/backend/app/api/v1/uploads.py、对象存储适配与media维护模块，Web入口包括 TileSkuFormModal 及各业务上传组件。实现前按真实文件定位，不直接复刻原型JavaScript。

目标是文件主体经授权直达COS，后端负责可信状态。排除读取签名刷新、新小程序上传、转码、全量历史迁移、跨浏览器续传及收费服务开通。

## 设计决策

### D1 UI策略：Design System组件复用

采用现有React/Tailwind/shadcn组件及语义Token；不做整页CSS Port，不引入新图片资产。原型仅说明上传区域和状态，不新增产品管理页面。相比复制独立HTML，复用保留现有表单、权限和错误处理契约。

### D2 控制面和传输面分离

后端存储适配增加申请授权、对象检查、受控复制和分片终止能力；COS实现直传，MinIO/local维持既有代理模式，返回明确能力模式。客户端按后端模式执行，不能自行拼endpoint。新增申请返回会话id、任务id、模式、短期授权及传输参数，授权响应禁止缓存或记录凭证。浏览器SDK只接触本会话临时对象。限定对象STS优先，预签名为备选；C-001要求实际证明分片、最小权限和续期可行，当前不宣称验证通过。

### D3 持久会话与稳定副本

候选表 media_upload_sessions：id、owner_id、business_type/business_id、media_kind、expected_size/mime、mode、state、version、expires_at、临时及已验证对象引用、actual_size/mime、integrity摘要、multipart标识、处理状态、bound引用、task_id、时间字段。唯一约束(owner_id, client_idempotency_key)并校验重用请求指纹；索引(state, expires_at)、业务归属及任务关联。不存凭证/签名URL。分片列表由COS核对，客户端报告不能替代真实对象验证。

状态采用申请→校验→待处理/可关联→已绑定及失败/取消/过期；传输字节由客户端单独表示。确认以条件更新抢占处理租约，工作者崩溃后租约可恢复。复制使用固定源版本或条件一致性方案，将内容移至客户端无写权限的稳定对象后再验证，避免TOCTOU；若供应商方案不足以证明一致性，C-002未关闭，不进入确认实现。

新建业务先得到受控pending稳定副本，保存取得业务id后COS侧复制到唯一正式key再提交引用；现有业务也先隔离临时对象，不授予正式key写入权。外部复制不在DB事务内：持久操作记录与幂等目标key支持重试，DB用version条件更新/唯一约束确认绑定；失败副本仅经引用检查后清理。业务校验失败保留可关联对象供重试。SQLite/MySQL需同等状态竞争语义，不能用进程锁替代数据库约束。

### D4 API与错误语义

控制资源冻结为 `/api/v1/admin/uploads/sessions`：已核对 src/backend/app/api/v1/router.py 将 uploads.router 挂载在 /admin/uploads；现有 uploads.py 无 sessions 路由冲突。

| 方法 | 路径后缀 | 请求 / 响应 |
|---|---|---|
| POST | 根路径 | 媒体/业务、大小类型、幂等标识 → 会话、授权、有效期、传输参数 |
| POST | /{id}/renew | 会话身份 → 新授权或明确不可续期原因 |
| GET | /{id} | → 可信状态、可重试原因、就绪媒体字段 |
| POST | /{id}/confirm | 完成线索 → 校验中或幂等既有结果 |
| POST | /{id}/cancel | → 取消状态与清理状态 |
| POST | /{id}/retry-processing | → 受控派生重试状态 |

沿用统一code/message/data。复用登录/权限/大小类型错误，新增会话过期、对象不符、状态冲突、派生失败等语义，数值编号先查错误码目录分配。异步确认返回可轮询状态，不能把接口200当成媒体就绪。业务保存复用现有API并核验会话就绪和归属；代理模式的合法历史引用保持兼容，不能接受任意未授权新key。OpenAPI、Orval、API索引、Pydantic、契约测试一并同步。

### D5 图片处理与清理

图片处理选型按用户费用约束确定为后端异步，复用现有Pillow算法；不调用数据万象、不申请其服务角色或启用云端处理。浏览器仍经后端授权直传COS，后台工作者按固定版本下载原图，生成派生图后上传COS；后端继续承担该阶段的网络、CPU与内存消耗，不宣称存储或流量零费用。

异步处理采用数据库持久任务与幂等结果，不采用响应结束后无持久性的后台任务作为唯一保障，也不为本需求新增Redis等队列基础设施。规格复用generate_image_thumbnail：缩略图480×480、默认质量82；展示图1600×1600、默认质量86及768KiB目标；均为WebP、等比缩小、不放大小图，执行EXIF方向修正并保持透明度，生效配置优先。保留原图及既有特殊格式拒绝/跳过策略。

面向2核2GB宿主机，实施参数冻结为：专用工作者同时处理1张图片，派生图顺序生成；工作者容器CPU上限1核、内存上限512MiB，不与API进程共用图片解码内存；单次任务总超时120秒，缩略图生成子进程单独限时18秒以满足20秒长尾约束，租约120秒、每30秒续租。暂时性网络/存储故障最多自动重试3次，退避5/15/45秒；格式错误、解码失败及内存上限触发不自动重复消耗资源，记录可定位失败后由受控人工重试。超时须终止处理子进程，重启后由租约恢复持久任务，取消后的晚到结果不得绑定。这些是实施上限，尚非2GB生产资源验收结论；内存、超时、故障恢复及规格矩阵仍需验证后关闭任务4.1。

必要派生失败禁止新媒体绑定；仅未达目标体积但有效派生已存在时维持warning，不误判为缺失派生。C-004的处理位置与费用选择已确定，不再等待云端授权；完整资源与兼容性证据由4组任务承接。

清理只处理本Change创建的过期会话临时对象、未绑定副本和分片，不触及历史批量删除。数据库状态CAS取得清理租约，绑定与清理互斥，逐对象重查引用后删除；失败保留重试记录。已绑定对象不随会话过期清理。TTL、分片、并发、退避、保留期及性能样本/阈值均由C-003冻结，禁止通过临时常量跳过决策。

## 原型冲突处理（Conflict Resolution）

| 冲突 | 处理 |
|---|---|
| 原型100%与传统上传成功语义 | 保留校验/处理/可保存分层；object-storage delta修改成功条件 |
| 原型按钮可直接模拟任意状态、切换文件 | 仅Mock工具，不进入产品；真实API状态和权限门禁始终生效 |
| 原型只展示一个SKU文件，需求覆盖多入口 | 以HTML为局部卡片视觉源；跨入口采用相同状态组件，各业务保持原宽度/字段 |
| HTML取消态没有重新选择按钮，context提到该入口 | 本原型无该按钮；实现由现有上传选择器提供重新选择，Skeleton中留证，不宣称原型已覆盖 |
| 正式spec倾向直接写业务目录，直传要求隔离 | object-storage完整MODIFIED块明确临时授权与正式归属分离 |
| 旧规格后端派生及目标体积warning与新就绪门禁 | delta允许受控异步处理器，区分有效派生超体积warning与必要派生缺失 |

## UI Contract

事实源优先级：HTML > PNG（未导出）> context.md > acceptance.md > rules/ui-design.md > 正式spec。Mock交互不是生产授权依据。

| 维度 | 契约 |
|---|---|
| 页面入口 | 现有管理端SKU、品牌、Banner、头像、证书上传入口，不新增导航；各入口角色与业务归属沿用现有授权 |
| 信息架构 | 保留页面壳/表单；文件卡含预览、文件名大小、状态、进度、就近错误、重试/取消；底部保留业务保存 |
| 视觉 | 语义bg-page/bg-surface/text-primary/text-secondary/text-brand-gold/border-border-default/error；默认system字体15px/1.6、标题22px，卡片间距16/20px、圆角12px，SKU弹窗880px、窄屏留16px边距；其他入口用原专属尺寸 |
| 交互 | focus可见、键盘可达、hover/disabled使用现有DS；100%后显示校验，派生失败重试不重传；保存失败保留预览；关闭/Escape/点击遮罩遵循现有弹窗，未完成任务需离开提示和安全取消，不静默丢失 |
| 图标文案 | 使用项目统一图标，上传/校验/处理中/可保存分明；取消传输与移除未绑定文件有区别，移除不等于删除已发布媒体 |
| Mock/API | 原型静态纹理、模拟进度、场景选择器全部为Mock；产品接入真实会话和COS进度，视频可播放性单独验收 |
| 权限 | 按角色显示操作且后端重新鉴权；店主端/小程序不增加上传菜单；签名和SDK错误不进入用户文案 |
| 最终参照 | SKU及各入口即时预览、保存再进入、历史媒体、小程序展示；1440px/矮视口、computed width与全局CSS冲突测试对应6条AC-XCUT |

## 观测与数据契约

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers: [web_admin, backend_api, request_logs, usage_events, task_traces, task_trace_spans, object_storage]
  reason: 上传控制、传输、确认、复制、派生和绑定跨系统；店主Web与小程序仅展示兼容，新上传封装N/A。
  validation: AC-016至018待实现；验证客户端与服务端来源、并行耗时口径、脱敏、保留周期、OpenAPI/Orval及SQLite/MySQL契约。
```

事实源：docs/standards/product-data-collection-observability.md 与 task-trace-coverage.md。控制请求全量请求日志；端侧开始/重试/取消/失败/保存行为按事件规范去重；同一任务关联传输和服务端阶段，采集失败不阻断业务。令牌、完整签名URL、内部Key不记日志；只保留指纹/类型/大小/状态，保留期沿用规范。新表、索引、迁移同步docs/04-database-design.md、schema与MySQL升级/回滚验证；API文档与错误码同步，不在本Change生成阶段修改业务文件。

## 迁移、验证与风险

先部署兼容的会话schema和控制API，再按媒体启用客户端，视频验证后启用图片。回滚新会话至代理模式，旧直传会话仍可确认/清理，已绑定媒体仍可读；不破坏性删除新表或对象。需更新.env.example、部署文档/CORS与最小权限说明并通过Compose，生产配置另行验证。

同文件同网络对比代理与直传，记录服务器出口、传输/确认/处理/保存分段及成功率；19/59/63MB与生效边界样本，阈值先冻结。CPU/内存有限、图片处理选型不明与跨域可能阻塞第二阶段；保留关闭开关，不静默回退。Sprint35/30人天，无修复缓冲，估算增加超过1人天即需重新规划。

## 知识库与待关闭条件

引用 docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md、admin-media-upload-chain.md 及 retrospectives/sprint-028-retrospective.md；沿用四联证据与环境来源边界，不以静态Mock替代生产/真机。

C-001授权可行性、C-002复制与事务证据、C-003参数/阈值需在阶段一实现前关闭；图片专属参数与C-004在阶段二前关闭；C-005按Skeleton/视觉交付门禁关闭。当前仅完成方案文档，以上均未验证。后续opsx-apply可以先执行设计验证任务，未关门禁不得推进对应业务实现。


## 阶段一契约冻结与验证记录

任务1.1已完成代码级核对。当前统一响应为ApiResponse(code=0,message=success,data)，入参错误沿用422/40001；任务型确认返回HTTP 200和可信处理中状态，不使用HTTP成功冒充就绪。

| 权限/契约 | 冻结结果 |
|---|---|
| 头像 | require_admin_access（admin/employee），限定当前用户，不接受客户端任意user_id |
| SKU图片/视频、Logo、Banner | require_admin_access，存在业务ID时查存在性及该业务保存权限；新建时验证对应创建权限，保存再次核验 |
| 证书图片/文件 | require_system_admin，仅admin，不能因通用会话接口放宽到employee |
| 会话隔离 | 所有操作owner_id与当前用户一致，未知或他人会话统一404/30080，避免枚举；已绑定取消409 |
| 幂等 | 申请使用client_idempotency_key和owner唯一约束；media_kind、business引用、expected_size/mime规范化摘要必须匹配；同key异payload返回409/30082 |
| 查询/确认 | 返回session_id、state、retryable、error_code、task_trace_id、expires_at；仅ready/bound可返回可信media引用及既有UploadResult展示语义；不回显临时凭证 |
| 申请/续期 | 返回会话与传输授权，Cache-Control:no-store；敏感授权禁止日志/Trace收集；mode明确区分cos_direct与proxy |
| 超限和类型 | 复用FILE_SIZE_EXCEEDED=50003、FILE_TYPE_NOT_ALLOWED=50002；证书复用50004/50005；保持有效配置读取 |
| 新错误码预留 | 30080会话不可访问(404)、30081会话过期(409)、30082状态或幂等冲突(409)、30083对象校验不符(400)、30084必要派生失败(409)；已扫描当前core/API与错误码文档无占用，实现时登记并再次查冲突 |

申请字段冻结为media_kind（枚举）、business_id（可空）、expected_size（正整数）、mime_type（白名单）、client_idempotency_key（限定长度和字符集）；不得接受客户端Key或bucket。路由详表见D4。权限、跨业务/跨用户、同幂等键异请求、过期和参数非法均为接口契约测试反例。此处冻结文档不代表API已存在，尚不生成Orval产物。

### C-001与C-002当前证据边界

本地安装的COS SDK具备get_presigned_url/get_auth、create_multipart_upload、upload_part、complete_multipart_upload、abort_multipart_upload、copy_object、head_object方法，已经通过inspect.signature只读确认；项目适配层仅暴露put/get/info/range/direct-read，MediaObjectInfo未保留版本/ETag，尚无授权及分片适配。

腾讯云官方[复制对象接口](https://intl.cloud.tencent.com/ind/document/api/436/10881)说明复制可指定源版本及源ETag条件，且HTTP200可能包含复制错误；因此实现必须解析SDK结果并核对稳定副本，不得仅凭状态码绑定。该文档证明接口支持范围，不证明当前桶权限、版本配置或竞态实验已通过。

C-001仍缺最小权限真实反例及聚合大小实验；C-002仍缺源复制竞态、数据库租约/清理并发实验。不得将SDK存在性检查勾选为这两项完成。

### C-003候选参数（未冻结）

已提交参数选择：并发2、分片8MiB、授权15分钟、最多重试3次、未绑定对象保留24小时；同网络各视频样本20次，直传传输阶段p95相比代理降低至少50%。这组最初候选已由后续直接验证结论修正，以文末及validation.md为准；对确认/派生耗时不据此作承诺。任务1.4保持未完成。


## 直接验证结果回填

已执行实际COS签名、分片、复制实验及SQLite/MySQL候选CAS实验，数据和证明边界见 [validation.md](validation.md)。初始配置采用8MiB/并发2，其他工程默认可配置；参数不再等待用户逐项输入，正式p95目标待基准测量。C-001～003尚未全部关闭，当前应用任务仍1/22，不宣称业务实现已通过。COS已启用版本控制，清理实现必须携带会话对应版本ID，保护稳定副本及业务引用；不能仅创建删除标记。


## 阶段一实现基线冻结

C-001：采用逐请求预签名备选，后端初始化/查询/合并/终止分片，仅签PUT到确定Key+uploadId+partNumber+Content-Length；浏览器不获合并、初始化或正式对象写权限。分片号和长度由expected_size与part_size推导，后端合并前ListParts校验编号集合/逐片大小/总大小，完成后HEAD再检查，不信任客户端ETag清单。需要后端新增签发分片URL能力 `POST /{id}/parts/{part_number}/authorize`；renew只刷新合法会话授权，不延长取消/绝对过期会话。简单PUT同样绑定精确长度。缓存签名和发放数量受会话约束，签名泄露仍可能重复写入临时对象，业务不得引用临时源。

浏览器证据：隔离Chromium localhost:3000来源，正确4字节PUT=200，5字节=403，过期=403，有效新签名=200；两个分片ETag均可读，后端合并后大小1048580字节正确。测试对象3个版本已清理。当前桶原无CORS，已增限定生产管理端域名与localhost:3000的GET/HEAD/PUT、content-type/content-md5及ETag/Content-Length/x-cos-version-id暴露，600秒预检缓存；未改对象权限。部署时按实际Web origin配置，不能复制通配域。

C-002：生产桶版本控制已启用，确认持久化源version_id，针对固定版本读取校验并复制；禁止在缺失版本保护时仅把ETag当密码学身份。稳定副本Key在会话创建时唯一分配并持久化，重试仍指向该稳定Key及固定源版本；工作者CAS version与lease_token更新状态，租约到期旧工作者不得提交DB状态。清理前原子抢占cleaning，ready→binding与ready→cleaning互斥；bound不可清理。版本清单持久化，重复外部复制产生的版本须逐版本识别清理，不能只创建删除标记。SQLite/MySQL各100次CAS单赢家证明数据库机制可用；具体实现的租约过期、补偿及并发反例仍作为2组必测项，设计门禁不代表实现测试完成。

C-003：固定工程初值为文件并发1、分片并发2、8MiB阈值及分片、签名900秒、会话绝对有效期24小时、失败额外重试3次（1/2/4秒加随机抖动）、租约120秒并心跳续租、每小时清理过期且无引用对象，活跃租约不清理。大小白名单沿用effective配置。参数均可配置，续期不得延长绝对会话有效期。

性能验收口径在实现前固定：同一客户端网络、相同文件，对照已验证的最小浏览器直传探针；集成上传传输阶段p95不超过对照p95的1.25倍，授权/查询控制接口p95目标1秒，视频校验和服务端复制阶段p95目标5秒（均为单文件活动上传，无图片派生）。19/59/63MiB各组20次、配对交替采样，报告失败率、p50/p95和范围；小样本分位波动大时扩至50次，不以删掉失败样本达标。旧代理同网络比较作为改善幅度事实报告，不预先承诺降低50%。超时、安全或有效上限失败单列阻断，不以平均性能掩盖。以上是后续验收目标，当前未通过；图片处理性能在第二阶段另定。

阶段一1.2/1.3/1.4设计验证完成，可以进入2组；C-004/C-005及完整功能验收继续保留。授权后的当前任务不再等待用户逐项选参。

## 视频控制与绑定实施细化

实际鉴权沿用 `AuthUnauthorizedError=40102`、`AuthForbiddenError=40302`；此前阶段一冻结表提及的 20001/20004 是常量表编号，未用于现有依赖抛错。本次契约按运行时修正，不改全站鉴权行为。

新建 SKU 的现有保存流程本已先创建草稿再写媒体。直传接入将“草稿插入 + ready→binding + 预留业务 ID”放在同一短事务，随后在事务外复制 COS 对象，再将正式引用与 bound 状态原子提交。失败保留预留草稿，重试原会话复用该 SKU，避免重复创建；这不是上传完成即发布。现有 SKU 更新的字段、媒体引用与绑定状态同事务提交。其他入口仍返回明确代理能力，图片阶段接入后补齐覆盖。

控制操作的请求日志沿用现有中间件；独立事务记录同一会话的 Task Trace 控制阶段，日志失败不回滚会话或业务。API 全量签名响应禁止缓存且不写响应正文日志。客户端行为、传输阶段和绑定/派生细分观测仍由 5.1 补齐。

当前视频内容验证采用固定版本的有限前缀容器签名检查，复制校验使用固定版本、大小与可用 CRC64；不宣称完整解码或恶意内容扫描。真实播放与冻结性能样本仍待 Web/Compose 验收。

## 品牌Logo绑定实现补充

品牌Logo复用SKU图片持久处理和固定版本派生，媒体类别为brand_logo，目录为images/default/brand-logos/{id|pending}/direct-upload。现有admin/employee角色可申请，各会话按owner隔离；保留已绑定品牌Logo允许现有品牌管理者编辑其他字段。新建失败预留停用品牌且无Logo引用，重试复用ID；复制完成后同事务提交引用、bound和启用状态。复制不持有数据库写事务，复制或引用写入失败释放会话供重试。品牌状态原有契约保持，其他入口由后续任务分别接入。


## 多入口绑定与观测实现

Banner预留无媒体DRAFT，头像预留UUID但不提前创建账号，证书预留隐藏记录；业务引用和会话bound均在相应仓储短事务中提交。COS固定版本复制在写事务外进行，失败释放会话供重试。证书business_id是品牌上下文，不能用作正式证书目录ID。PDF不派生；图片沿用持久Pillow队列。接口字段、权限与错误的事实源为API索引第12节。

客户端每次阶段变化记录media_upload事件，不按进度回调采集；业务成功提交后每任务只记录一次save。所有会话共用同一控制/传输任务，客户端阶段耗时和后端含子步骤的总耗时分开标注。绑定及清理以独立观测事务写入，失败不回滚业务。日志保留仅对media_direct_upload应用90/180天策略，默认dry-run；不扩展其他业务日志清理范围。
