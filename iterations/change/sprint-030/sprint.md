---
note: workflow-sync — workflow-sync 自动同步 — 2/5 Change archived；1 applied；2 进行中；Sprint `planning`
  `planning`
title: sprint-030 规划
created_at: '2026-09-08 08:39:14'
updated_at: 2026-09-11 09:07:38
---

# sprint-030 规划

## 1. 目标

### Sprint 目标编号列表

- add-knowledge-model-lifecycle-sync
- REQ-0138-knowledge-model-lifecycle-sync
- fix-apply-continuous-execution-behavior
- BUG-0149-opsx-apply-premature-stop
- fix-miniapp-banner-image-aspect-fit
- enforce-apply-continuous-execution
- add-signed-cos-direct-media-read
- REQ-0136-signed-cos-direct-media-read
- REQ-0137-miniapp-banner-image-aspect-fit

### REQ-0137-miniapp-banner-image-aspect-fit 要点

P1，M／3人天。首页 Banner、品牌列表 Banner、品牌详情头图、商品详情顶部图片完整适配、允许留白并保持容器稳定。品牌详情在现有总高内分离图片与文字区；保持视频、非 Banner 图片、图片URL/变体来源、跳转及预览契约。需求已评审，先纳入范围，再创建 Change。

### REQ-0136-signed-cos-direct-media-read 要点

P1，XL/8人天。三端视频优先，继而图片及附件；覆盖短期授权、续签恢复、历史兼容和受控回退。批准基线沿用PRD，C-001至C-004在设计/实施/验收对应阶段关闭。与REQ-0135上传独立，与REQ-0137共用页面时保留其整图展示策略。

### fix-miniapp-banner-image-aspect-fit 要点

REQ-0137的关联Change，覆盖四类图片完整适配、品牌图文分区、静态回归与视觉证据；估算沿用REQ的3人天，不重复计量。

### BUG-0149-opsx-apply-premature-stop 要点

P1，L／5 SP／5人天。修复持续执行治理及行为验收缺口：一次apply持续推进已授权且依赖满足的开发、测试、文档和同步；集中人工问题，保留必要确认，按任务隔离阻塞，分别报告实现、自动验证、人工待验和外部阻塞，并限制无效重试。两个入口实际验证B1～B6，保留12项AC，不以关键词检查代替执行证据。已评审，修复Change为fix-apply-continuous-execution-behavior；原归档治理Change不作为本BUG交付。

### fix-apply-continuous-execution-behavior 要点

BUG-0149关联修复Change，覆盖持续执行、有限重试及两入口实际行为证据；14项实施任务。沿用BUG的5人天，不重复计量。

### REQ-0138-knowledge-model-lifecycle-sync 要点

P1，XXL／13 SP／13人天。建立元本体、产品研发本体、TilesFST M系列领域模型、格式约束、来源映射和生命周期同步；一个真实Change验证增量、本体一致性、完整Git快照、幂等及失败恢复。31条AC为验收基线，非图数据库、问答或应用生成平台。已评审，关联Change为add-knowledge-model-lifecycle-sync，已回填同一Sprint。

### add-knowledge-model-lifecycle-sync 要点

REQ-0138关联Change，4份delta spec及16项实施任务；沿用13人天，不重复计量。先本体与映射，再同步恢复、Sprint/发布集成及验证。

## 2. Scope

| 类型 | 编号 | 标题 | 状态 | 估算 | 说明 |
|---|---|---|---|---:|---|
| REQ | REQ-0137-miniapp-banner-image-aspect-fit | 小程序 Banner 图片统一完整适配展示 | in_sprint | 3 人天 | in_progress 2/12；`fix-miniapp-banner-image-aspect-fit` |
| REQ | REQ-0136-signed-cos-direct-media-read | Web 与小程序 COS 签名直读及过期恢复 | in_sprint | 8 人天 | in_progress 14/19；`add-signed-cos-direct-media-read` |
| REQ | REQ-0138-knowledge-model-lifecycle-sync | 建立 knowledge-model 基础结构与生命周期同步机制 | in_sprint | 13 人天 | apply 16/16；待 archive `add-knowledge-model-lifecycle-sync` |
| BUG | BUG-0149-opsx-apply-premature-stop | opsx-apply 持续执行缺少行为验收，提前结束无法有效检出 | done | 5 人天 | archived `fix-apply-continuous-execution-behavior`（2026-09-10 10:53:25） |
| Change | enforce-apply-continuous-execution | enforce apply continuous execution | archived | 1 人天 | archived `enforce-apply-continuous-execution`（2026-09-08 23:59:59） |

REQ-0136、REQ-0137、REQ-0138及BUG-0149均已纳入正式范围；BUG-0149按P1治理修复安排，状态与验收以Scope及来源文档为准。

Change：2个REQ关联Change已在范围内，另有1个纯治理Change已归档；BUG-0149修复Change为fix-apply-continuous-execution-behavior，已通过bug-opsx回填同一Sprint。

### 包含需求

<!-- workflow-sync:scope-requirements:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| REQ-0137 | 小程序 Banner 图片统一完整适配展示 | P1 | in_sprint | in_progress 2/12；`fix-miniapp-banner-image-aspect-fit` |
| REQ-0136 | Web 与小程序 COS 签名直读及过期恢复 | P1 | in_sprint | in_progress 14/19；`add-signed-cos-direct-media-read` |
| REQ-0138 | 建立 knowledge-model 基础结构与生命周期同步机制 | P1 | in_sprint | apply 16/16；待 archive `add-knowledge-model-lifecycle-sync` |
<!-- workflow-sync:scope-requirements:end -->

### 包含 BUG

<!-- workflow-sync:scope-bugs:start -->
| 编号 | 名称 | 优先级 | 状态 | 说明 |
|---|---|---|---|---|
| BUG-0149 | opsx-apply 持续执行缺少行为验收，提前结束无法有效检出 | high | done | archived `fix-apply-continuous-execution-behavior`（2026-09-10 10:53:25） |
<!-- workflow-sync:scope-bugs:end -->

### 包含 Change

<!-- workflow-sync:scope-changes:start -->
| Change ID | 关联需求 | 状态 | Sprint 目标 |
|---|---|---|---|
| `add-signed-cos-direct-media-read` | REQ-0136-signed-cos-direct-media-read | in_progress | in_progress 14/19；`add-signed-cos-direct-media-read` |
| `enforce-apply-continuous-execution` | — | archived | archived `enforce-apply-continuous-execution`（2026-09-08 23:59:59） |
| `fix-miniapp-banner-image-aspect-fit` | REQ-0137-miniapp-banner-image-aspect-fit | in_progress | in_progress 2/12；`fix-miniapp-banner-image-aspect-fit` |
| `fix-apply-continuous-execution-behavior` | BUG-0149-opsx-apply-premature-stop | archived | archived `fix-apply-continuous-execution-behavior`（2026-09-10 10:53:25） |
| `add-knowledge-model-lifecycle-sync` | REQ-0138-knowledge-model-lifecycle-sync | applied | apply 16/16；待 archive `add-knowledge-model-lifecycle-sync` |
<!-- workflow-sync:scope-changes:end -->

## 3. 工作量与容量

| 项目 | 规划 |
|---|---|
| 容量基线 | 2开发＋1测试，30人天；沿用现有基线 |
| 已纳入估算 | 30 SP／30人天，100% |
| 剩余 fix 缓冲 | 0人天，0%，低于30%建议 |
| 未分配容量 | 0人天 |
| 主能力数量 | 现有1个add-* Change，REQ-0138预计新增1个主能力；不预填Change ID |

既有范围17人天：REQ-0137为3、REQ-0136为8、enforce-apply-continuous-execution为1、BUG-0149为5。REQ-0138新增13人天：本体与映射4、归档同步及恢复4、Sprint和发布集成2、验证文档3。总量30不超过容量30和硬上限36，容量门禁通过。

容量风险：新增需求使用原剩余13人天，原9人天修复预留及4人天未分配均被占用。没有新增缓冲可承接返修；范围或估算增加时必须重新计算容量，优先调整低优先级工作或排期，不削减验收。沿用暂定窗口及sprint-029之后承接策略，不把团队视为并行可用，不承诺固定上线日期。

## 4. 横切预防清单

REQ-0137的四个固定标签 admin-list、admin-form、admin-modal、media-upload 均不适用；主动承接 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`。

- AC-XCUT-001：key/object/URL/render各自说明证明边界，渲染以实际证据验证。
- AC-XCUT-002：正常与回退场景保留脱敏Network摘要，区分HTML、DevTools、真机和体验版。
- AC-XCUT-003：保持src回退、预览URL及懒加载，视频回归不扩展成视频改造。
- AC-PROTOTYPE-001～003：UI Contract、Skeleton首轮确认、1440px设计核对视口、小程序等价截图、关键样式与最终一致性作为实现和归档要求。

REQ-0136横切承接（12条）：

| 标签 | docs/knowledge-base/best-practices/下的文档 | AC |
|---|---|---|
| admin-list | admin-list-page-consistency.md | XCUT-001至004：分页/total、fixed toast、DS确认、列与sticky |
| admin-form | admin-form-page-consistency.md | XCUT-005至006：唯一保存、dirty与确认 |
| admin-modal | admin-modal-width-css-cascade.md | XCUT-007至008：专属类、computed width、低视口滚动 |
| media-upload（仅回显） | admin-media-upload-chain.md | XCUT-009至010：即时回显与Docker Web读取；上传状态机修改N/A，归REQ-0135 |
| 小程序媒体 | miniapp-media-four-part-acceptance-practice.md | XCUT-011至012：四联与分层Network证据 |

部分参考实践为draft，沿用已批准AC；不能替代实际渲染、权限或平台证据。

BUG-0149为治理标签，admin-list、admin-form、admin-modal、media-upload均N/A。承接来源BUG的12项行为AC与根因证明边界；三项核心场景必须真实执行，合法暂停、已有授权和范围边界作为对照，不要求用户提供历史会话。

REQ-0138：无UI横切标签，knowledge-base gate为N/A；31条AC覆盖本体语义、证据、幂等与恢复，模型中的页面和媒体类型不触发UI实现。

## 5. 知识库承接

最近复盘：`docs/knowledge-base/retrospectives/sprint-028-retrospective.md`。

| 行动项 | 本次承接 |
|---|---|
| A-028-01 / T-028-01 用量覆盖 | 运行默认会话发现及Sprint snapshot hook，实际计量与估算回退分开报告；不自动修复历史统计 |
| A-028-02 媒体证据包 | 分别承接REQ-0137的3条与REQ-0136的12条AC-XCUT，不额外创建证据包生成能力需求 |
| A-028-03 发布证据表达 | 开发证据不冒充真机或线上通过，发布时单独确认 |
| T-028-02 复盘矩阵说明 | 本次不生成复盘矩阵，不把估算回退写为实测用量 |

BUG-0149承接A-028-01/T-028-01的实际用量与估算区分、A-028-03的证据来源区分；A-028-02媒体证据包不适用。复盘open状态保持，未自动创建其建议Issue。

REQ-0138承接sprint-028的归档引用残留与治理同步矩阵经验（AC-009、AC-001），以及A-028-01/T-028-01用量归因和A-028-03证据边界；不修改历史复盘或自动创建行动项。

## 6. 依赖 ASCII 树

```text
REQ-0137-miniapp-banner-image-aspect-fit（已评审）
  -> sprint-030 正式范围
  -> /req-opsx 创建Change并回填changes[]
  -> UI Contract与Skeleton确认
  -> 四类图片实现与状态/交互回归
  -> 多宽度视觉、样式和最终一致性
  -> 验收与归档
```

REQ-0118 的图片消费矩阵和 REQ-0106 的有图Banner标题隐藏策略维持；BUG-0148的grid卡片不纳入本次实现范围。REQ-0137不新增后端或存储依赖。

REQ-0136 → req-opsx并回填changes[] → C-001字段/候选规则、C-002权限/HEAD/Range → 视频恢复 → 图片附件 → C-003视觉/设备/性能、C-004API/观测 → 全范围验收归档。

REQ-0135仅共享稳定媒体引用，不构成硬前置。REQ-0136与REQ-0137重合页面应协调：前者修改URL消费/恢复，后者保持图片尺寸/裁切；共享源码编辑按Change串行协调并做组合回归。

```text
BUG-0149-opsx-apply-premature-stop（已评审，P1）
  -> sprint-030正式范围
  -> /bug-opsx创建修复Change并回填changes[]
  -> 执行/收尾规则与有限重试设计
  -> 两入口行为验证B1～B6、12项AC证据
  -> 验收后独立归档
```

BUG-0149不以REQ-0136/0137业务实现为前置；治理文件修改与其他任务读取需协调，以固定规则版本记录行为验证结果，禁止改写原归档治理Change。

```text
REQ-0138（已评审）
  → req-opsx并回填changes[]
  → 元本体/领域模型/Schema及映射
  → Change增量与原子提交/恢复
  → Sprint语义门禁 → prepare完整快照 → publish确认关联
  → 31条AC及真实Change证据
```

REQ-0138与媒体需求无业务硬依赖；生命周期技能和Workflow Sync改动与既有治理文件编辑串行协调。设计确定试点与来源Commit、并发锁、回执位置和快照体积阈值；无需新增人员或改写已归档治理Change。

## 7. 里程碑、风险与发布计划

暂定规划窗口为 2026-09-08 08:39:14 至 2026-09-22 08:39:14，默认两周。该窗口用于规划，实际开工按sprint-029后续排期更新，不作为人员并行投入或固定上线日期承诺。

| 里程碑 | 完成条件 |
|---|---|
| 规划 | 需求in_sprint，四件套与范围一致 |
| 设计 | Change已回填；局部尺寸、UI Contract和Skeleton已确认 |
| 实现 | 图片适配及17项AC对应实现/测试完成 |
| 验收 | 320/375/430pt等价宽度、长文案及回退证据齐；视觉与样式一致 |
| 发布准备 | 验收归档后再进入产品版本发布计划 |

风险：PNG与浏览器视觉证据仍缺，不能将原型源码检查替代渲染；品牌220rpx/160rpx分区需验证真实padding和文案；视频共用样式需防止误改。fix缓冲为0，新增范围重算容量。任何补证缺口在对应实现门禁处理，不提前标已通过。

BUG-0149里程碑：修复Change就绪→治理实现→两入口真实行为验收→独立归档。主要风险是实际Agent运行环境与规则版本变化，缺证据的具体场景保持待验；静态探针通过不代表行为达标。

REQ-0138里程碑：Change就绪→本体和映射验收→同步与恢复→Sprint门禁与快照流程验证。真实发布确认与模拟证据分开；工具自举须明确输入固定和归档顺序，缺失发布证据不伪报完成。

本次不部署、不确定发布版本。发布候选说明见release-note.md，验收结论见acceptance-report.md。

## 8. 产品数据采集与链路观测

product_data_collection_observability: applicable。REQ-0136 affected_layers=[web_admin, web_catalog, wechat_miniapp, backend_api, request_logs, usage_events, task_traces, task_trace_spans, object_storage]。读取授权、续签及历史候选适用，直接COS文件流无后端读取日志；DB默认不预设结构变更，发生结构变化才同步SQLite/MySQL及迁移。AC-014至016承接脱敏、保留周期、旧数据、API/Orval与测试；隔离Compose开发验证已有证据，平台验收仍待执行，详见对应Change validation.md。事实源为docs/standards/product-data-collection-observability.md。

REQ-0137仍not_applicable：仅小程序图片渲染，无API/DB/日志/请求封装/保留周期改变，以AC-OBS-001/002核对；其独立Orval/Compose为N/A，不抵消REQ-0136的适用要求。

BUG-0149：not_applicable，affected_layers=[]；仅治理执行与验收，不触及产品数据流。validation：BUG根因门禁与范围核对通过，12项自动行为AC已通过，人工验收pending；Orval、Compose不适用，不改变其他REQ的观测要求。

REQ-0138：not_applicable，affected_layers=[]；本地治理工具只读消费资料，无业务API、DB、端请求或观测链路改变，AC-OBS-001/002覆盖脱敏和保留边界，尚未实施；无Orval或Compose要求。Sprint整体applicable仍由REQ-0136决定。

## 9. 关联文档

- `issues/requirements/review/REQ-0138-knowledge-model-lifecycle-sync/requirement.md`
- `issues/requirements/review/REQ-0138-knowledge-model-lifecycle-sync/acceptance.md`
- `issues/requirements/review/REQ-0138-knowledge-model-lifecycle-sync/review.md`

- issues/bugs/archive/BUG-0149-opsx-apply-premature-stop/trace.md
- issues/bugs/archive/BUG-0149-opsx-apply-premature-stop/acceptance.md

- `issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/requirement.md`
- `issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/review.md`
- `issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/acceptance.md`
- `issues/requirements/review/REQ-0137-miniapp-banner-image-aspect-fit/prototype/web/context.md`
- `sprint.yaml`、`release-note.md`、`acceptance-report.md`

- `issues/requirements/review/REQ-0136-signed-cos-direct-media-read/requirement.md`、`review.md`、`acceptance.md`、`trace.md`

## 10. 延后项

当前无未评审候选项。已评审REQ尚无Change，下一步由req-opsx创建并回填同一Sprint；不将其视为范围外延后项。



## REQ-0137 部分实施记录

本轮完成首页、品牌列表与商品详情五处图片mode调整，以及4项聚焦静态测试；保留REQ-0136授权图片组件及媒体契约。品牌详情分区待Skeleton确认。局部开发工具观察不能替代完整视觉、Network与样式矩阵；端口基线失败及行为运行器资源阻塞见对应Change implementation-evidence.md。维持in_progress和archive_ready=false，仅刷新部分事实，无apply完成事件。
