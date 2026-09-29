---
requirement_id: REQ-0136-signed-cos-direct-media-read
title: COS 媒体直读验收清单
acceptance_status: pending
created_at: '2026-09-07 22:58:21'
updated_at: '2026-09-09 11:25:55'
---

# 验收清单

## 1. 执行口径

所有复选框表示完整验收结论；已完成的开发验证及剩余证据以[Change验证记录](../../../../openspec/changes/add-signed-cos-direct-media-read/validation.md)为事实源。部分本地证据不勾选整条跨环境AC。approval 与验收通过不同：需求文档完整不意味着 COS、Compose 或真机已通过。第4节列出评审通过后的设计与验证约束；需求批准不代表验收通过。

- [ ] AC-001（FR-001/002）：逐项执行第2节覆盖矩阵；正常路径 Network 显示文件主体直达 COS，地址含稳定媒体关联及明确到期时间；缺失一项不把整页判定完成。
- [ ] AC-002（FR-001）：使用公开访客、合法管理者及无权限账号，覆盖可见、草稿、下架、删除、未确认媒体；篡改业务引用、媒体标识、规格、批量项或 Key 均不能越权；不可见资源不泄露存在性。
- [ ] AC-003（FR-003）：采用评审批准的 TTL、缓存和撤权策略；跨身份不复用授权，退出清理；签名前后下架、到期前后访问及禁止续签分别验证。已缓存内容不作为可撤回承诺。
- [ ] AC-004（FR-004）：对页面长停留、前后台切换、离线恢复和多图同时过期注入失败；同媒体刷新合并，重试、并发与超时符合参数表，过期备用地址不算恢复，耗尽后停止自动请求。
- [ ] AC-005（FR-005）：三端分别验证视频首播、暂停继续、快进/回拖、重播、全屏及 GET/HEAD/Range；记录实际方法与分段响应，不能仅以签名 API 200 判定通过。
- [ ] AC-006（FR-005）：播放与暂停状态分别触发过期换址，恢复同一视频位置，误差符合参数表；保持暂停意图，不绕过自动播放限制；视频总时长跨越多次 TTL 仍按预算恢复。
- [ ] AC-007（FR-006）：列表缩略图、详情展示图、原图预览及相册后续图片分别验证；缺失派生可确定性降级，规格/字节数可定位，不能静默把所有列表图降为原图。
- [ ] AC-008（FR-006/009）：PDF 等现有附件按端能力验证下载及打开；不返回伪图片派生字段；已过期、下载中断和再次打开有界恢复，失败文案可见，小程序合法域名实测。
- [ ] AC-009（FR-007）：覆盖稳定 Key、旧 /media/、历史映射、自有绝对地址、外部绝对 URL 和全候选缺失；候选仅属于同一授权媒体，缺失才继续，拒绝/故障终止；外部地址不任意抓取或重签。
- [ ] AC-010（FR-008）：按端/媒体类别启停灰度并验证新请求切换；代理同等鉴权；COS 故障、授权拒绝和不可见媒体不触发绕权回退；回退预算、计数和阈值可测试，在途链接边界明确。
- [ ] AC-011（FR-006）：管理端新建/编辑上传后，在同会话、刷新列表和重新打开编辑时验证已确认媒体回显；URL 刷新不把表单标记 dirty、不覆盖未保存业务字段、不改变现有图片裁切。
- [ ] AC-012（FR-009）：本地 MinIO/兼容存储和 COS 配置分别验证，未知模式有明确处理；Compose 从 Web 入口联调，TLS、跨域、内容类型与小程序域名分别有来源明确的证据；无公开桶或永久密钥下发。
- [ ] AC-013（FR-004/005）：模拟旧请求晚到、快速切图、取消、页面卸载、身份切换；旧响应不覆盖新资源、不继续后台循环；错误清除、键盘重试、加载固定尺寸及辅助技术状态提示通过。
- [ ] AC-014（FR-010）：三端行为 helper 到授权 API 的链路 ID 可追踪；授权有 request log，批量/外部候选解析有 Task Trace/span；直接 API 无行为上下文不伪造事件，COS 文件流只记录实际可用的端侧/存储证据。
- [ ] AC-015（FR-010）：对请求响应快照、行为事件、异常与缓存诊断注入签名 URL、凭据和内部 Key，持久化结果全部脱敏；观测写入失败不阻断媒体；继承既有保留周期并验证清理与旧数据兼容。
- [ ] AC-016（FR-002/009/010）：新增 API/错误码/头部同步 OpenAPI、Orval、文档和接口测试；DB 默认复用引用，若无 schema 变更记录 N/A 理由，若有则覆盖 SQLite/MySQL、迁移及 Pydantic；按参数表进行同条件性能和回滚验证。
- [ ] AC-017（FR-004/005/006）：原型状态逐项映射至真实页面；后续 Change 完成 UI Contract、Skeleton 首轮确认、1440px 与关键交互视觉证据及 computed style；小程序另附开发工具与真机证据，原型 Mock 不替代功能验证。

## 2. 入口与字段覆盖矩阵

| 编号 | 端与入口 | 现有媒体字段/消费点 | 权限及必测动作 |
|---|---|---|---|
| M-01 | 管理 SKU 列表/编辑/预览 | main_image_url、main_image_thumbnail_url、images[].url/thumbnail_url/display_url/original_url、videos[].url | 管理权限；列表、同会话回显、视频和原图 |
| M-02 | 管理品牌列表/编辑 | logo_url、logo_thumbnail_url | 管理权限；回显、重新打开 |
| M-03 | 管理 Banner 列表/编辑 | image_url、image_thumbnail_url | 管理权限；列表和预览 |
| M-04 | 管理证书列表/编辑 | file_url、thumbnail_url | 管理权限；图片预览与PDF读取 |
| M-05 | 管理用户列表/个人资料 | avatar_url | 对应用户管理/本人权限；头像回显，其他账号隔离 |
| M-06 | 店主 Web 目录/详情及共享展示组件 | catalog-body、product-grid、product-card、detail-page 消费的实际图片/视频/品牌字段 | 公开可见性；逐渲染引用核对，精确响应绑定由实现前清单补录 |
| M-07 | 小程序首页/发现/分类/搜索/商品列表/收藏 | 商品 thumbnail_url/display_url/original_url；Banner image_url/thumbnail_url/display_url | 公开可见性；列表多图过期、滚动加载及返回恢复 |
| M-08 | 小程序品牌列表/详情 | brand_logo_url、brand_logo_thumbnail_url、brand_hero_display_url、brand_hero_thumbnail_url | 品牌可见性；列表及详情 |
| M-09 | 小程序 SKU 详情 | media[].url/preview_url/thumbnail_url/display_url/original_url/cover_url；兼容 videos[] | 商品可见性；视频、封面、相册、原图 |
| M-10 | 小程序证书列表/详情及品牌证书 | file_url、thumbnail_url、media[].url/preview_url/thumbnail_url/display_url/original_url | 证书可见性；图片/PDF，不存在字段记 N/A |
| M-11 | 小程序门店资料/个人资料 | logo_url 与实际头像绑定 | 公开门店/本人资料；按组件实际绑定回归 |

字段依据为 `src/backend/app/schemas/{tile_sku_admin,brand_admin,banner_admin,brand_certificate_admin,user_admin,miniapp_home}.py`，消费入口见对应 Web pages/shared 和 `src/miniapp/pages/`。M-06、M-11 及共享组件全部调用点仍需实现前完成字段绑定盘点；同一共享组件不能替代其他权限或响应字段的验证。不存在的视频、附件或原图入口说明 N/A，不新增入口来填表。分享卡片的延迟抓图与普通页面读取单独核对，若消费这些字段，应与 REQ-0134 分享能力兼容，不能把短期 URL 持久化为分享内容。

## 3. 证据记录与性能口径

每个 M 行记录 key hash/前缀、object 存在性/MIME/大小、URL 模式/域名/方法/状态/耗时和 render 结果。证据记录包含 evidence_source、evidence_ref、executed_at、端/页面、媒体类别、网络环境、冷/热缓存、并发、结果及证明边界。不得保存签名参数、Authorization、完整内部 Key 或真实客户媒体。

性能对照方案：使用脱敏代表视频（约20/60MB及一个超过TTL的长视频）、缩略图/展示图/原图与PDF；同客户端网络、相同缓存条件分别测代理和直读，并发1及3，每组至少20次。报告样本原值摘要、p50/p95、失败率、续签恢复率、代理回退率、媒体字节数与服务器出口字节数。批准指标见 requirement.md §8，网络不可比时不宣称性能改善。具体脱敏样本与计时口径在Change测试计划中固定，阈值按PRD执行。

## 4. 评审结论与验收状态

D-001至D-006按requirement.md §8获批为需求基线；review.md的C-001至C-004约束后续设计、实施与验收。需求状态为approved，验收保持not_started，不自动发布。

acceptance_status: pending。授权核心与 Web 控制器已有本地自动化测试，证据及证明边界见 Change trace；三端业务接入、真实 COS、性能、Compose 与小程序真机尚未验收。

## 横切 AC（knowledge-base）

来源与适用范围由 trace.md knowledge_base_refs 维护。以下均为已有容器内媒体替换的回归约束，不扩展 CRUD 功能。

- [ ] AC-XCUT-001（admin-list）：列表分页保留 page-summary/page-right 及后端真实 total；媒体恢复不重置筛选、页码或改为前端伪分页。
- [ ] AC-XCUT-002（admin-list）：成功/失败反馈使用 fixed toast，媒体状态切换不推动表格；截图比较前后边界。
- [ ] AC-XCUT-003（admin-list）：原有上下架/删除继续 DS confirm，无 window.confirm；媒体重试不触发业务状态变更。
- [ ] AC-XCUT-004（admin-list）：现有列单行/截断、sticky操作与横向滚动保持，缩略图失败不撑宽整表；筛选下拉实现 N/A — 本需求不新增或改写筛选控件。
- [ ] AC-XCUT-005（admin-form）：个人资料保留表单底部唯一保存CTA，无页头重复按钮；续签不新增保存入口或造成dirty。
- [ ] AC-XCUT-006（admin-form）：存在的放弃dirty/恢复默认流程继续DS modal、无原生confirm；不存在恢复默认的页面标N/A；反馈fixed toast不产生布局位移。
- [ ] AC-XCUT-007（admin-modal）：受影响编辑弹窗无 modal-card 与专属类双挂载；1440视口 computed width 与对应既有容器一致，不因媒体状态变化收窄。
- [ ] AC-XCUT-008（admin-modal）：矮视口可滚动，预览/重试及底部保存可达，关闭后恢复焦点。
- [ ] AC-XCUT-009（media-upload）：上传状态机实现 N/A — REQ-0135负责；本需求验证既有上传完成后同会话、列表刷新、重新打开编辑的即时媒体回显。
- [ ] AC-XCUT-010（media-upload）：经Docker Web入口验证现有允许边界媒体的读取、Range和回退；上传超限/Nginx请求体修改 N/A — 无上传契约变更，不以仅后端端口测试代替端侧读取。
- [ ] AC-XCUT-011（miniapp-media）：每类受影响媒体保留key/object/URL/render四联，HTTP200或对象存在不能替代真实渲染；失败/阻塞明确记录来源和补证步骤。
- [ ] AC-XCUT-012（miniapp-media）：DevTools、真机/体验版Network分别记录域名、状态、字节数、耗时和render；历史审计仅只读，本需求不执行迁移apply；媒体helper应允许受控签名URL，不把所有非/media/地址误判非法。

## 验收结果回填

```yaml
acceptance_status: pending
accepted_at: null
accepted_by: null
source_change: add-signed-cos-direct-media-read
source_sprint: sprint-030
evidence: []
failed_items: []
source_event: opsx.apply
notes: 待验收；由 opsx.apply 标记，后续 archive 时回填结论。
```


## 验收范围调整：微信真机

用户明确要求跳过微信真机验收。微信真实设备、体验版及相应手机网络/合法域名证明记为skipped_by_user，不计为通过，不再作为本轮继续执行的阻塞；已有开发者工具证据仍仅证明开发环境行为。Web、PDF、性能对照及非真机自动化验证继续执行，其他尚未验证项不随此决定自动豁免。

## 本地Web PDF人工验收

用户明确确认“PDF正文正常显示”。本地Web重建后的证书PDF内容显示验收通过，证据来源为用户人工观察；自动工具已确认预览生成blob标签页，但受浏览器URL策略限制未读取正文。证据见[PDF预览验收](../../../../openspec/changes/add-signed-cos-direct-media-read/evidence/pdf-preview-fix.json)。此项确认不代表整个需求通过，整体acceptance_status保持pending，其他端侧覆盖、附件到期与性能验证仍按Change任务跟踪。
