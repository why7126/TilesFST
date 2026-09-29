---
created_at: 2026-09-05 22:30:01
updated_at: 2026-09-07 23:16:23
---

# 公开页面分享测试计划

## 自动化

使用虚构公开对象及wx stub执行真实页面回调和onLoad/onShow，不以字符串存在作为唯一证明。运行tests/test_miniapp_static.py及新增分享专用测试。

参数：中文、空格、百分号、畸形转义、超长输入、非法ID、未知键、合法/非法枚举；keyword/spec为79/80/81字符、priceRange为39/40/41字符；编码query为2047/2048/2049字符。验证超限默认入口标题与落点一致。

状态：每页两种回调返回；完整商品条件以合法深链设定，不恢复已移除筛选UI；分页从第一页；已提交与输入草稿区分；分类分享优先；搜索恢复不写历史；find实际JS按钮可用。

事件：每次触发计一次，取消不计完成，接收事件独立，不传播发送者链路ID；payload脱敏，模拟同步throw和异步reject仍可分享与加载。

## 客户端与视觉

按2026-09-06用户指示取消iOS/Android真机矩阵。实施任务1.1冻结DevTools 2.02.2608060、基础库3.17.1（灰度）和当前工作区构建；2048应用阈值以本地边界测试证明，不推定未验证的平台能力。普通直达与朋友圈单页分别验证。截图320/375/430pt，覆盖长标题、加载、空、错、返回及重复进入。图片404、过期、HTTP成功但不可渲染需实际卡片证据。

DevTools版本、模拟机型与部分截图已取得，记录见evidence/README.md；真实客户端版本未取得，不使用模拟器version代替。无需后端迁移、Orval生成或Docker构建测试；若实际范围变化先更新设计。

## 通过与回填

以REQ acceptance及Change acceptance映射判定。记录命令、来源、执行时间和摘要；真机项按用户豁免记录waived，不计为测试通过；其他缺证据项保持未完成。终态材料不得混淆开发、体验版和线上证据。

## 本次开发执行记录

证据来源：本地Node VM，wx与公开接口响应使用测试替身；执行构建为本次工作区JS和TS源文件。该自动化批次不请求真实服务；随后DevTools连接现有线上公开API，单独按开发工具证据记录。

| 命令 | 结果 | 证明边界 |
|---|---|---|
| `node --test tests/js/miniapp-public-sharing.cjs` | 30通过 | 实际JS页面回调、解析与恢复、同步/异步埋点失败、普通无栈返回。 |
| `MINIAPP_TEST_TYPESCRIPT=1 node --test tests/js/miniapp-public-sharing.cjs` | 30通过 | 使用已安装Web TypeScript将TS转译后执行相同契约；不是完整小程序类型检查。 |
| `src/backend/.venv/bin/python -m pytest -q tests/test_miniapp_static.py tests/test_miniapp_public_sharing.py` | 39通过 | 38项既有静态回归和JS运行时入口；现有Starlette/httpx弃用警告1项。 |

已核对后端priceRange为非负有序min-max，允许单侧空值；scope为分类名称，搜索恢复同时设置filterSnapshot.category。当前路由构造使用encodeURIComponent，入口只解码一次，畸形转义不抛错。query应用阈值2047/2048/2049和关键词/规格79/80/81、价格文本39/40/41均有运行测试。发现并修复可选ID为0导致有效条件丢失的问题，新增专用回归。

Computer Use权限已恢复；DevTools Stable 2.02.2608060和基础库3.17.1（灰度）已记录，模拟器version=8.0.5、platform=devtools，不能视为真实微信版本；iOS、Android真实接收未执行。2048只是应用保护阈值，不作为平台上限声明。

## DevTools剩余验证步骤

使用本Change工作区构建与DevTools记录工具、基础库、构建标识和执行时间；无需准备实体设备。

1. 在开发者工具320/375/430pt截取11页首屏及加载/空/错/长标题状态，记录导航胶囊间距与图片实际样式；在DevTools核对原生菜单和虚拟卡片。
2. 在DevTools以分享路径和可用入口检查页面、渠道参数、冷/热/单页入口与最终公开对象；工具不支持的原生能力如实记录未验证，不要求实体设备补证。搜索预置不同历史，确认恢复不改历史；商品列表从第二页发送完整条件，确认接收第一页。
3. 使用受控测试数据覆盖下架、删除、无权限、失效分类、离线、图片404/过期/不可渲染，观察兜底和返回/重试。朋友圈限制操作需记录实际替代入口，不能以wx stub通过判定平台能力。
4. 采集脱敏事件请求和服务端摘要，检查触发/接收分离、无原始关键词或完整URL、接收独立链路；将结果逐项回填REQ acceptance。缺证据项继续保持未勾选。

## 2026-09-06补充验证

`src/backend/.venv/bin/python -m pytest -q tests/test_miniapp_static.py tests/test_miniapp_public_sharing.py src/backend/tests/test_miniapp_public_share_events.py src/backend/tests/test_product_usage_logging.py`：98通过，4条既有框架弃用警告。转译TS运行时28项通过。新增34项接口测试使用实际JS分享工具生成载荷，33项覆盖11页两次触发和接收，1项拒绝关键词原文；修复前29失败/5通过，修复后34通过，并验证数据库metadata不含原始关键词和分享query。

以本地app.openapi()与src/web/openapi.json对比usage-events路径及UsageEvent相关Schema，完全一致，因此不重写Orval生成物。Docker/线上后端未部署；DevTools仍可能对新事件返回400，该状态不能标为线上已修复。

页面截图、普通无栈返回和原生菜单记录见evidence/README.md。三宽度首屏、实际计算样式、原生Logo修复、对象错误和单页入口已补证；远程图片404/过期/不可渲染及完全离线冷启动卡片仍未闭环；双端真机接收已豁免。此前样式探针因selectComponent返回null而失败，截图中的该TypeError来自探针，不作为业务页面故障证据。

## 真机验证豁免

2026-09-06用户明确要求“不需要做真机验证”。本次验收豁免iOS/Android实体设备双渠道接收矩阵、真实微信版本采集及真机截图；AC-023状态为waived（未执行），不计为测试通过，也不再作为完成或归档门槛。其他AC中涉及真机操作的部分同样豁免，保留本地自动化与DevTools可执行验证。开发工具分享图片异常、计算样式及异常场景仍须如实处理，不能据此认定已通过；体验版和线上成功不在已有证据证明范围内。

## DevTools本轮执行结果

逐页三宽度矩阵、代表性异常、原生双渠道预览、computed style、冷/热与单页入口见evidence/README.md。新增3项本地Logo缓存、受限回退、预准备后离线复用测试，JS/TS各28通过，聚焦pytest98通过。AC-015剩余补证需合法下载测试素材或明确调整范围；保持下载安全校验，未将白名单拒绝记作404。

## 2026-09-07 图片缓存验收返修

根因状态confirmed（源码与运行测试）：getImageInfo验证成功后仍返回原远程URL，已下载的本地文件未被采用；URL在验证后过期时仍会进入后续分享配置。新增两项回归，修复前28通过/2失败，修复后JS与转译TS各30通过。现在只采用微信返回的已解码本地path，缺少有效本地路径时保留Logo；分享回调不等待下载，不再把已验证远程URL作为图片缓存结果。

本地pytest98通过，4条既有框架弃用警告。接口、数据库、OpenAPI/Orval、事件字段、WXML/WXSS及页面布局均未变化，无需Docker构建；观测适用层级沿用miniapp/backend/usage_events，Task Trace仍为N/A。

隔离回环HTTPS测试服务已返回404（不存在）、403（模拟过期拒绝）、200但PNG内容损坏及正常PNG；服务使用虚构素材，不接触线上对象。DevTools对localhost下载仍在合法域名校验阶段拒绝，尚未调整安全校验开关；这些HTTP结果来自本机Python客户端，不是DevTools下载或原生卡片渲染通过。原生截图仍待补证，AC-015与任务4.4保持未完成。

## 最终补证结果

2026-09-07受控HTTP素材与原生SDK/双渠道渲染全部完成，见evidence/media-acceptance.md。前述“待补证”描述为此前执行批次状态，已由本节和REQ逐项结果更新。网络异常改为业务请求真实连接失败，保持工具桥接可用；全局Offline的工具内部限制保留说明，不作为原AC外额外组合门槛。JS/TS各30项、pytest98项通过，临时安全校验已恢复。4.4已完成，未执行归档。
