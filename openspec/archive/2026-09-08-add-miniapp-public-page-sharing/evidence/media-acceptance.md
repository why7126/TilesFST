---
created_at: 2026-09-07 23:16:23
updated_at: 2026-09-07 23:16:23
---

# AC-015 图片异常开发验收

结论：开发验收通过。来源为Computer Use操作DevTools、真实原生getImageInfo/downloadFile及本机隔离HTTPS服务；服务只提供虚构素材，未变更线上对象或实际发送消息。Stable 2.02.2608060、基础库3.17.1（灰度）、430pt，当前JS SHA256为`021919e7d9ee66a19285fbd2e10234b7de4e084b8aac0f2ac5b6abd09f97fc98`。真机验证依既有用户指示豁免，不计通过。

用户于2026-09-07授权临时关闭当前项目的域名/TLS/证书校验以访问本机测试素材。操作结束已恢复校验（本地urlCheck=true）、普通编译及首页，重载清除运行时探针；临时服务已停止。恢复截图见下表。生产域名、证书策略、上传及发布配置未改动。

## HTTP与原生渲染对照

测试期间只将商品列表首项的运行时cover_image指向隔离素材，并清空当前页图片检查缓存；未setData覆盖列表视觉内容，也未写入后端。执行页面真实分享回调，等待原生图片检查结束，再分别打开朋友/朋友圈预览。每次预览后取消。

| 场景 | 实际响应与回调 | 朋友及朋友圈实际结果 |
|---|---|---|
| 图片不存在 | /missing.png返回404，检查未就绪 | 均显示产品Logo，无破图 |
| 模拟已过期素材 | /expired.png返回403及固定ExpiredTestSignature文本，检查未就绪 | 均显示产品Logo，无破图 |
| HTTP成功但不能解码 | /broken.png返回200、image/png，但正文20字节非PNG，检查未就绪 | 均显示产品Logo，无破图 |
| 成功下载后同一地址过期 | /short-lived.png先返回200有效120×120 PNG，SDK返回http://tmp/本地路径；服务端切到403，原生downloadFile确认statusCode=403 | 均显示之前解码的蓝底黄框测试图，未回用过期URL |

[HTTP响应摘要](media-http-summary.json)只含时间、虚构场景、状态、类型和字节数，不含认证或内部对象key。这里的过期由测试服务控制响应模拟，未宣称验证生产对象存储签名实现。wx.request对自签名证书的探针出现ERR_CERT_AUTHORITY_INVALID，未绕过浏览器警告；改用分享实际使用的原生下载链路确认403，截图中的该证书错误不是业务实现错误。

## 网络失败与入口边界

将运行时wx.request中公开业务GET暂时改送已停止的回环端口，原生接口真实返回ERR_CONNECTION_REFUSED；其余请求及工具文件桥接保持原样。reLaunch进入品牌详情，无前置页面栈，页面显示品牌不可查看与重新加载，分享卡片正常显示Logo。恢复wx.request后点击返回，实际到首页；最终普通编译清除全部探针。

冷启动/热启动/单页原有证据见README，网络失败新增证据见下表。需求FR-007、AC-015、AC-017分别要求这些场景，不要求关闭DevTools宿主文件桥接。此前将“全局Offline使文件桥接也断开”的工具故障列成额外阻塞，是测试方式与产品验收边界混用；现以业务请求真实失败验证网络异常，不删改原AC、不新增豁免。完全离线冷启动的工具模式仍未通过，不外推真实微信行为，也不将重定向请求测试称为整个进程完全断网冷启动。

## 证据索引

| 截图 | 保存时间（Asia/Shanghai） |
|---|---|
| [devtools-404-friend-430.png](devtools-404-friend-430.png) | 2026-09-07 23:00:35 |
| [devtools-404-timeline-430.png](devtools-404-timeline-430.png) | 2026-09-07 23:01:21 |
| [devtools-expired-friend-430.png](devtools-expired-friend-430.png) | 2026-09-07 23:02:50 |
| [devtools-expired-timeline-430.png](devtools-expired-timeline-430.png) | 2026-09-07 23:03:17 |
| [devtools-broken-friend-430.png](devtools-broken-friend-430.png) | 2026-09-07 23:04:38 |
| [devtools-broken-timeline-430.png](devtools-broken-timeline-430.png) | 2026-09-07 23:04:59 |
| [devtools-after-expiry-friend-430.png](devtools-after-expiry-friend-430.png) | 2026-09-07 23:07:28 |
| [devtools-after-expiry-timeline-430.png](devtools-after-expiry-timeline-430.png) | 2026-09-07 23:08:29 |
| [devtools-network-failure-entry-430.png](devtools-network-failure-entry-430.png) | 2026-09-07 23:08:54 |
| [devtools-network-failure-share-430.png](devtools-network-failure-share-430.png) | 2026-09-07 23:09:42 |
| [devtools-media-settings-restored-430.png](devtools-media-settings-restored-430.png) | 2026-09-07 23:14:31 |

## 自动化与影响

JS及转译TS各30项通过，pytest98项通过（4条既有弃用警告）。新增两项缓存回归修复前2失败、修复后通过。源码根因及修改记录见Change trace；本次返修无API/DB/OpenAPI/Orval、请求观测契约或WXML/WXSS变更，无需Docker构建。线上usage-events仍可能400，后端事件字典需正常发布，不以本地通过宣称线上已修复。

执行链路为原Change内返修→受控素材→真实SDK→原生预览→恢复设置→验收回填。建议媒体回归同时验证下载响应与卡片渲染，并覆盖验证后过期；未自动创建follow-up Issue/Change。
