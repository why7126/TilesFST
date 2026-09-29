---
created_at: '2026-09-08 08:46:08'
updated_at: '2026-09-11 08:46:17'
---

# 签名直读与恢复设计

## 1. 边界与架构

REQ-0136全部两阶段范围属于sprint-030，沿用XL/8人天估算，不重复计算Change。现有storage.py负责签名、变体和历史Key候选；新增读取授权服务负责业务引用到对象的归属/可见性判断，端侧共享恢复控制器消费读取描述。不能直接把media_url_for_object_key作为授权服务。

不实现上传、派生处理、转码、CDN、历史迁移；数据库默认无新增表/字段，稳定媒体引用继续保留。若发现现有引用无法表达归属，在任务1.1记录具体字段与迁移必要性并修订设计，不凭Key前缀推断权限。

## 2. 技术决策

### D1 UI策略：Design System局部状态

选择DS复用：Web共享媒体状态/恢复逻辑，保留既有容器、播放器和原图预览；小程序共享恢复工具配合原生组件。CSS Port会引入演示布局，Asset方案不能表达续签状态，均不采纳。读取生命周期与视觉适配分离，REQ-0137继续控制图片适配，REQ-0135继续控制上传状态。

### D2 读取描述及API

规划新增POST /api/v1/media/read-authorizations（公开可见资源）和POST /api/v1/admin/media/read-authorizations（当前管理身份），两路共享授权服务但权限上下文不可由请求体选择。沿用统一{code,message,data}。

请求items长度1～50，每项包含resource_type、resource_id、media_id（资源无独立媒体行时由后端按受控字段定位）、variant；不接收任意URL、bucket、endpoint或自由Key。resource_type为后端白名单映射，逐类型绑定已有服务/仓储权限。公开商品下架、证书不可见、私有头像等均按业务规则拒绝，不能借资源类型切换绕权。

响应data包含server_time、items；各项包含输入关联标识、status、descriptor或安全error。descriptor包含media_ref、variant、url、expires_at、read_mode；需要HEAD的消费者可取得独立head_url，不能把GET签名当作HEAD签名。media_ref是定位标识而非授权令牌。外部URL只保留受认可的既有展示策略，read_mode=external，不伪造COS到期字段。

非法请求返回400/422；管理端未认证401；单项不可见/不存在统一安全不可用结果，不暴露归属；存储故障502，限流429。复用现有媒体/存储/权限错误常量，新增编号需在实现前核对error-codes注册避免与REQ-0135冲突。批量合法请求200返回逐项结果，单项拒绝不使其他合法项失败。授权响应Cache-Control: no-store，响应快照过滤descriptor URL及签名参数；OpenAPI/Orval/文档/接口测试同批更新。

既有业务响应保留URL语义并可附读取描述，精确字段映射在任务1.1补齐M-01至M-11；首次加载不得每个图片串行请求授权。刷新按媒体身份去重，批量合并。

### D3 权限及历史解析

读取链：业务授权 → 正规化自有引用 → 确定性候选 → 有界元信息探测 → 签发 → 端侧读取。先按requested variant查规范对象，再查同规格已知历史映射，再按thumbnail→display→original或display→original降级；original/视频/附件仅查自身及受控历史映射。最多8个去重候选，额外历史映射不动态扩展。不存在才查下一项；拒绝与存储故障终止。所有候选必须属于同一已授权业务媒体。

规范化白名单仅覆盖已配置自有域名及已知/media/路径；禁止对任意外部URL作HEAD/GET，禁止后端SSRF。对象探测可在一次请求内缓存，跨请求正缓存最多30秒、负缓存最多5秒，不缓存业务授权；替换/删除后失效。普通读取不写DB、不搬迁对象。

列表原图回退每批最多2项，其余占位并允许用户详情重试；记录规格降级，防止整页全部原图。该限制为工程保护值，实施验证后在设计记录调整依据，不能改变原图预览能力。

旧/media/兼容入口必须重新关联业务归属和权限。管理请求不能依赖img/video自动附加Bearer：先通过带身份的API取得短期、仅绑定目标媒体的代理票据；公开入口每次检查可见性。票据用途/方法/到期隔离、签名脱敏，不把业务Key当票据。无法还原合法归属则安全失败；上线前盘点遗留调用，禁止简单改为全局登录导致公开页面失效。

### D4 端侧恢复

状态：idle→loading→ready；可恢复失败→refreshing→loading；拒绝/无资源→unavailable；耗尽→failed。共享控制器按身份、媒体、规格合并请求，缓存有效期300秒，提前30秒检查；超时10秒，最多2次自动刷新、退避1/3秒、刷新并发4。用server_time和单调时间计算剩余寿命，页面重入重新校验；不后台无限轮询。

error事件缺少HTTP状态时仅做有界重新解析，不断言为签名过期。媒体或页面版本令牌防止晚到请求覆盖；退出、卸载、切换身份取消订阅并清缓存。手动重试重启有界预算，继续受后端限流。图片预览相册按使用时刷新，附件下载/打开在操作前刷新。

视频换址保存媒体身份、currentTime、暂停意图；新元信息就绪后seek并验证误差≤2秒，按平台限制等待用户手动播放。换址结果不等于恢复成功。GET/HEAD/Range与真机平台路径在任务1.2验证；不在此宣称预签名请求天然兼容全部方法。

### D5 灰度与回滚

复用DIRECT_READ开关，增设端/媒体类别白名单策略；默认关闭自动代理回退。显式灰度回退每媒体最多1次，拒绝与COS自身故障不触发。代理采用应用级并发2、超额返回429而非排队无限转发；精确多副本总限额和流量预算在任务1.1按部署拓扑确认。关闭新直读后不宣称已有签名立即失效。缓存旧内容无法远程收回。

按PRD固定样本对比：主体直读100%、正常自动回退0、出口字节降低≥90%、p95不劣于代理超过10%；5分钟≥100样本且失败率>5%触发人工回滚评估。部署逐端逐媒体放量，无公共桶策略，不自动发布。

## 3. UI Contract与冲突处理

| 项目 | 合同 |
|---|---|
| 优先级 | HTML > PNG（可选）> context > acceptance > rules/ui-design.md > archived specs；context限定原型局部适用区域 |
| 页面入口 | REQ acceptance M-01至M-11；管理端按权限，公开端按可见性；不增加演示导航 |
| 信息架构 | 保留原表格/详情/弹窗，固定媒体尺寸；局部状态、预览及原有播放操作 |
| 视觉token | 使用既有semantic bg/text/border，cn合并类；复用shared/ui/business/templates；不复制HTML的原始色值 |
| 状态 | loading、refreshing、ready、failed、unavailable、offline、degraded；hover/focus/disabled/键盘可达，aria-live及busy |
| 文案图标 | 加载/恢复/失败/重试沿用原型产品文案；状态核对侧栏和演示控件不进入产品 |
| Mock/API | HTML的800ms、固定时间、符号均是Mock，不是真实播放证据；恢复控制器接真实授权接口 |
| 权限 | denied无绕权重试；不显示无权媒体；手动重试仍重新鉴权 |
| 一致性 | 12条XCUT全部映射；列表/表单/弹窗布局不漂移，REQ-0137完整图片展示保持 |

冲突（Conflict Resolution）：HTML控制栏/侧栏是演示工具，仅状态组件适用，不用CSS Port复制全页；Mock800ms不能替代10秒超时和2次预算。原型固定播放位置不能作为真实seek依据。旧spec允许受控代理或安全占位，delta明确不自动绕权回退；保留多规格、CDN仅预留的既有场景。无REMOVED要求。

实施前先完成UI Contract字段映射和Skeleton首轮确认；1440px、低视口、关键状态与computed style记录在trace；小程序提供相应平台证据。PNG未导出非阻塞，真实页面视觉不可省略。

## 4. 观测与数据边界

```yaml
product_data_collection_observability:
  status: applicable
  affected_layers: [web_admin, web_catalog, wechat_miniapp, backend_api, request_logs, usage_events, task_traces, task_trace_spans, object_storage]
  reason: 读取授权、批量与外部候选探测、三端恢复跨越请求封装及媒体存储；普通COS传输没有后端读取日志。
  validation: 三端事件契约、授权request log/Task Trace、脱敏及采集隔离已验证；设备与性能待验，详见validation.md。
```

沿用标准helper、事件字典、request_id和behavior_trace_id；直接API无行为上下文不伪造事件。批量/外部探测有Task Trace，纯本地单项签名无外部步骤时可仅request log并声明理由。记录media hash、规格、模式、耗时、预算、失败枚举；URL参数、代理票据和签名不落快照/日志。观测失败不阻断加载。保留周期不变；DB结构N/A因为复用引用与既有日志表，若新增字段必须同步SQLite/MySQL文档和测试。

事实源：docs/standards/product-data-collection-observability.md、task-trace-coverage.md；knowledge_base_refs见REQ trace，design承接admin-list/form/modal/media-upload与小程序四联实践。

## 5. 实施与待验证事项

C-001：精确字段/权限映射、多副本代理总限额在任务1.1完成；C-002：HEAD/Range及平台代理路径可行性在1.2完成；C-003/C-004在视觉/性能/观测验收任务关闭。禁止在无证据时勾选。

上线顺序：后端向后兼容描述与授权→三端消费→受控旧入口→灰度视频→图片附件。回滚使用兼容授权版本和端侧策略，不重新开放任意Key。无DB迁移默认，不做数据搬迁。共享storage.py与REQ-0135串行协调；小程序页面与REQ-0137组合回归。

## 6. 实施字段映射与依赖

| 矩阵 | 授权资源与数据来源 | 已核对权限 / 边界 |
|---|---|---|
| M-01 | sku_image / sku_video；TileSkuRepository.list_images/list_videos，resource_id 为 SKU，media_id 为对应行 ID；图片无媒体 ID 时取主图 | 管理角色；不接受其他 SKU 的媒体 ID |
| M-02 | brand_logo；BrandRepository.logo_object_key | 管理角色；单字段不接受 media_id |
| M-03 | banner_image；BannerRepository.image_object_key | 管理角色；公开解析复用 list_public_banners 的在线、时间窗口及关联业务规则 |
| M-04 | certificate；BrandCertificateRepository.file_key/file_url；多图使用现有 brand_certificate_images.id | 管理角色；软删除拒绝；图片ID属于指定证书；缺媒体ID的thumbnail/display选当前主图，original选主附件；非image MIME只允许original |
| M-05 | avatar；UserRepository.avatar_object_key | 员工仅本人；admin 可读用户管理头像；公开接口一律拒绝 |
| M-06 | CatalogBody 传 ProductGrid，再传 ProductCard.imageUrl；DetailPage.imageUrl | 已定位调用只属于共享模板/Design System 展示，没有实际目录/详情业务 API 绑定；不存在可接入的店主 Web 目录/详情业务页面，当前字段消费 N/A；共享模板不替代真实页面验收 |
| M-07 | sku_image 与 banner_image | SKU 复用 MiniappHomeRepository.get_product，检查 PUBLISHED、品牌/类目/规格启用；Banner 复用公开列表 |
| M-08 | brand_logo；hero 与 logo 使用同一品牌对象不同规格 | get_public_brand 检查品牌启用 |
| M-09 | sku_image / sku_video；稳定业务 ID 与独立媒体行 ID | 与 M-07 同等商品可见性；原生视频已接入位置/意图恢复；相册先准备临时文件，隐藏或切换取消旧任务 |
| M-10 | certificate；get_public_certificate_detail 与 list_public_certificate_images | 证书未删除、可见且品牌启用；子图 ID 必须属于证书 |
| M-11 | 首页 custom-navigation 消费 home.store.logo_url，对应 store_logo/store 与固定配置 miniapp.logo_url；store-info 本身无图片 | 自定义门店Logo按公开配置授权，默认产品Logo仍是静态资产；不允许选择其他设置。小程序无头像业务消费，N/A；Web私有头像仍按身份授权 |

缓存仅在一次授权请求内保存探测结果，跨请求不缓存，替换/删除后下一请求重新校验。候选最多8个，只尝试同一原图规格、确定性迁移映射、旧 `.thumb` 与 `thumbnails/` 路径；不猜测其他扩展名原图。原图降级每批最多2项。失败、拒绝不进入更多候选；外部 URL 不抓取。任务2.2测试通过。

当前Compose为单宿主机，所有后端共享data/tmp。代理通过该本地卷中的两枚flock槽与持久字节账本实现工作进程/同宿主机副本合计并发2、固定60秒窗口128MiB；单响应64MiB、Range分块4MiB。启动重建实例不重置流量，槽由内核在退出后释放；账本损坏/不可写时拒绝代理。窗口边界两侧可能出现256MiB突发。配置MEDIA_READ_PROXY_BUDGET_DIR必须指向同一卷，禁止在线删除或替换锁文件；跨宿主机/NFS未支持，不应以该实现宣称跨机集群限额。C-001采用当前单宿主机部署边界，扩容到跨宿主机需另行共享协调器。

REQ-0135已提供持久上传会话。新增 upload_session 引用仅接受当前上传者、ready且未过期会话；非原图必须出现在variants_json输出中。bound后必须走当前业务引用，避免旧会话绕过业务下线/对象替换。无需新增数据库表或迁移。此前临时媒体归属阻塞已解除。

共享文件顺序：storage.py新增独立HEAD签名；读取端消费REQ-0135会话，不改上传生命周期。小程序只改请求封装并新增恢复控制器，REQ-0137/REQ-0134页面改动保持；页面接入与组合回归等待Skeleton确认。

Skeleton入口为Web开发服务的 `/req0136-preview.html`，仅合成状态、不调用业务API；列表64×64、预览保持比例、局部覆盖层不改变布局。首轮人工确认待回复。浏览器工具访问localhost与127.0.0.1均返回net::ERR_BLOCKED_BY_CLIENT，未取得1440px/样式截图；不能将构建成功视为视觉通过。

预览恢复更新：本地服务重启，入口避开/media代理前缀，补齐Tailwind Vite编译插件及共享配置解析。浏览器已显示真实Skeleton，1280×720视口computed style验证5个缩略图均64×64、5个预览均600×337.5；人工首轮确认仍待回复，小程序及1440px完整验收未完成。此前浏览器不可访问记录为历史证据，当前Web通道已恢复。

## 7. 页面接入与验证边界

用户已确认Skeleton方向。管理端SKU、品牌、Banner、证书、用户与个人资料使用授权图片/视频组件，表单只保存稳定业务值；选择文件使用可释放的本地blob，读取刷新不写表单字段。编辑窗关闭恢复触发按钮焦点。

小程序共享卡片、搜索品牌/证书、收藏、详情推荐及首页自定义Logo均按业务引用读取；图片src变化也重新解析，旧响应不覆盖替换后对象。原生相册与附件下载使用统一页面任务，最多4并发、10秒超时、2次有界恢复，页面隐藏或再次预览取消旧下载；原生界面消费临时文件，不将签名URL持久化。REQ-0134分享仍沿用本地解码图片/产品Logo兜底，组合回归不改归档事实。

注册的外部HTTPS图片不抓取、不重签。请求派生规格时可作为原图降级，计入每批最多2项限制；非图片附件不伪造派生规格。旧/media仅接受当前公开业务归属，包括固定门店Logo配置；隐藏、删除、私有或未知对象拒绝。

观测result只使用既有数据库允许的success/failed，started/unavailable由outcome表达；异常堆栈也脱敏。小程序媒体读取的RUM维度为固定/media-read，避免接口名称被误认为Authorization凭据。C-001和C-004已落实；C-002有COS方法签名与本地播放器/代理可行性证据，COS真实播放器和微信域名仍待平台验收。C-003固定样本性能对照仍未完成。

### PDF预览验收更新

主动文件预览按当前身份独立管理控制器，避免新窗口隐藏来源页时取消授权；PDF下载为临时blob预览，兼容COS attachment响应头，并保留超时、身份/资源变化取消及释放约束。本地Web已获授权并完成更新；PDF正文已由用户人工确认正常显示；工具自身仍受blob URL安全策略限制。当前验证边界以[验证记录](validation.md#本地web更新及pdf人工确认边界)为准；微信真机按用户决定跳过，当前14/19，archive_ready=false。

### 小程序视频缺省封面

原生video的poster仅使用授权网络封面；不存在时传空值，由播放器显示视频首帧，不把包内Logo路径传入poster。该平台约束及修复前后证据见[验证记录](validation.md#2026-09-11-补验与无封面视频修复)。图片组件的静态兜底保持既有行为。
