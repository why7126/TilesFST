---
change_id: add-miniapp-public-page-sharing
requirement_id: REQ-0134-miniapp-public-page-sharing
requirement_ids:
  - REQ-0134-miniapp-public-page-sharing
iteration: sprint-029
status: archived
type: add
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-028-retrospective.md
product_data_collection_observability:
  status: applicable
  affected_layers: [miniapp, backend, usage_events]
  reason: 分享触发与接收事件复用现有请求链路，API和DB无契约变化；Task Trace因无新增后端复杂任务为N/A。
  validation: Node VM实际JS及转译TS各30项通过，覆盖事件计数、脱敏、同步与异步失败隔离；本地API及落库摘要验证通过，真实双渠道接收已豁免，线上采集留待发布验证。
created_at: 2026-09-05 22:30:01
updated_at: 2026-09-08 08:29:23
---

# 变更追踪

来源需求已通过评审并纳入sprint-029。Change由OpenSpec CLI创建，已实现11页双渠道分享和白名单恢复；自动化通过，DevTools三宽度、样式与关键交互已补证，AC-015原生补证完成，真机验收已豁免，开发任务已完成，已于2026-09-08归档。

## 证据与视觉检查

- [x] 小程序页面基线与关键交互截图，320/375/430pt。
- iOS/Android朋友与朋友圈接收矩阵：用户豁免，未执行。
- [x] 导航/图片疑点的实际样式或等价工具证据。
- [x] TS/JS、参数恢复、脱敏事件测试与29条验收回填。

无prototype PNG待导出；原型策略为原生菜单与现有布局。上述实施截图不可由源码检查替代，桌面1440px为N/A。

## 变更记录

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-09-05 22:30:01 | req.opsx | 从已评审需求创建公开页面分享Change，准备回填Sprint。 |

## 开发证据

证据来源为本地源代码和Node VM，执行时间见updated_at；构建为当前工作区开发源码，未上传体验版；DevTools 2.02.2608060、基础库3.17.1灰度已读取，真实客户端版本未取得。JS及转译TS分别运行30项实际回调测试通过，含采集接口回归的pytest共98项通过。可复现命令、覆盖与缺口见test-plan.md。

Cross-cutting Gate：标签为miniapp导航及媒体回归；AC-XCUT为warn，knowledge_base_refs为pass，best-practices read为pass；admin-filter-dropdown及其子项为N/A。结论WARN-PROCEED，已有5条横切AC和UI Contract，允许完成逻辑与自动化；DevTools视觉及本地Logo卡片已闭环，AC-015受控异常已补证，双端真机接收已豁免。

Computer Use权限于2026-09-06恢复，现可操作并截图。页面基线与原生菜单证据见evidence/README.md；已补三宽度计算样式及对象/单页/离线异常，iOS/Android真机矩阵已豁免。

REQ-0133价格及BUG-0148-miniapp-product-list-card-image-fit 图片相关工作区内容保留。本Change修改小程序逻辑、后端事件字典、测试和交付文档，不改WXML/WXSS、数据库、Web或管理端。usage-events路径及相关OpenAPI Schema与现有导出一致，无Orval输出或迁移变更；后端尚未部署，Docker镜像及线上验证留待正常发布。

执行链路：REQ评审→sprint-029→CLI Change→apply开发检查；发现前后端事件契约覆盖遗漏，已补真实JS载荷到FastAPI及落库测试；已补平台单页替代入口证据。规范优化建议：跨端事件变更增加真实载荷契约测试，未自动创建follow-up Issue或Change。

## DevTools采集契约修正

2026-09-06权限恢复后，模拟器分享直达正常加载，usage-events出现HTTP 400。本地真实JS载荷→FastAPI集成测试复现29项失败，错误40001分别为未知事件和缺少必填属性。根因状态confirmed（本地契约）：共享工具遗漏旧事件兼容字段，后端字典未注册7个新增事件。修复范围增加后端事件注册；保留旧事件必填约束，小程序补充无query的share_path、接收端本地requestId、sourcePage及camelCase公开ID兼容字段。新事件拒绝原文关键词/完整URL属性。请求响应Pydantic/OpenAPI结构、数据库表、错误码与请求封装保持不变；后端修复须随正常发布交付，不能以本地通过表示线上已修复。

图片异常根因状态confirmed（限当前DevTools）：包内PNG可解码但包路径在原生分享预览破图，同一PNG复制USER_DATA_PATH后渲染正常。共享工具改为进入页面时预备固定公开Logo，分享同步复用；文件API受限保留包路径回退。修复后的朋友、朋友圈及预缓存后离线卡片均显示正常，新增3项JS/TS缓存/失败回退测试。对照与剩余AC-015限制见evidence/README.md；不能外推真机内部行为。

## 真机验证豁免

2026-09-06用户明确要求“不需要做真机验证”。本次验收豁免iOS/Android实体设备双渠道接收矩阵、真实微信版本采集及真机截图；AC-023状态为waived（未执行），不计为测试通过，也不再作为完成或归档门槛。其他AC中涉及真机操作的部分同样豁免，保留本地自动化与DevTools可执行验证。开发工具分享图片异常、计算样式及异常场景仍须如实处理，不能据此认定已通过；体验版和线上成功不在已有证据证明范围内。

## 2026-09-07 图片缓存验收返修

根因状态confirmed（源码与运行测试）：getImageInfo验证成功后仍返回原远程URL，已下载的本地文件未被采用；URL在验证后过期时仍会进入后续分享配置。新增两项回归，修复前28通过/2失败，修复后JS与转译TS各30通过。现在只采用微信返回的已解码本地path，缺少有效本地路径时保留Logo；分享回调不等待下载，不再把已验证远程URL作为图片缓存结果。

本地pytest98通过，4条既有框架弃用警告。接口、数据库、OpenAPI/Orval、事件字段、WXML/WXSS及页面布局均未变化，无需Docker构建；观测适用层级沿用miniapp/backend/usage_events，Task Trace仍为N/A。

隔离回环HTTPS测试服务已返回404（不存在）、403（模拟过期拒绝）、200但PNG内容损坏及正常PNG；服务使用虚构素材，不接触线上对象。DevTools对localhost下载仍在合法域名校验阶段拒绝，尚未调整安全校验开关；这些HTTP结果来自本机Python客户端，不是DevTools下载或原生卡片渲染通过。原生截图仍待补证，AC-015与任务4.4保持未完成。

## 2026-09-07 原生补证完成

本轮在用户授权下临时调整DevTools本地下载校验，完成404、模拟过期403、200损坏PNG、先下载后过期的朋友及朋友圈实际渲染。业务GET重定向到关闭的回环端口产生真实连接失败，错误页面、分享Logo及无栈返回正常。截图、服务端响应摘要与工具限制见evidence/media-acceptance.md。临时校验已恢复，服务已停止，普通编译清除探针，生产配置未变更。

4.4完成，28条开发AC通过，AC-023保持用户豁免；正式验收/归档状态由对应Workflow维护。此前全局Offline断开工具文件桥接被过度列为额外阻塞，现按FR-007与AC-015/017区分业务失败测试和工具内部故障；没有把完全断网冷启动模式写为通过，也未扩大用户豁免。无新增功能、数据库/API或对象存储边界。
