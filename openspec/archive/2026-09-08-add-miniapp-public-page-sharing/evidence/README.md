---
created_at: 2026-09-06 12:05:34
updated_at: 2026-09-07 23:16:23
---

# 开发者工具验收证据

来源为 Computer Use 操作微信开发者工具，非真机、体验版或线上验收。Stable 2.02.2608060，基础库 3.17.1（灰度）；iPhone 5、iPhone 6/7/8、iPhone 14 Pro Max 分别模拟 320/375/430pt。模拟器 version 8.0.5 不作为真实微信版本。截图执行时间为文件保存时间（Asia/Shanghai），见下表。

构建为当前工作区小程序普通编译及热重载，2026-09-06截图批次分享工具 JS SHA256：`24cd8b9ea7e03856961d1c0edd0c5f947c9b0e60fb6f92a130f4012ebd5545bc`。旧截图与修复对照按下文区别，不视为同一构建的全部通过证据。使用既有公开 API，没有上传或实际发送消息；后端事件字典尚未部署，工具中 usage-events 400 不表示本地修复无效，也不表示线上已修复。

## 页面与三宽度覆盖

11 页各有三宽度首屏证据，375pt 品牌详情和证书详情使用错误态；正常详情见320/430pt。另有加载、空态、长标题、错误、离线和单页的代表性场景。不是11页×3宽度×全部状态×双渠道的笛卡尔积实测。11页双渠道回调与恢复由JS/TS运行测试覆盖，原生渠道通过代表性预览核对。无新WXML/WXSS，现有REQ-0133和BUG-0148视觉结果保留。

| 页面 | 320pt | 375pt | 430pt |
|---|---|---|---|
| 首页 | [截图](devtools-home-320.png) | [截图](devtools-home-375.png) | [截图](devtools-home-430.png) |
| 商品详情 | [截图](devtools-matrix-tile-detail-ready-320.png) | [截图](devtools-matrix-tile-detail-ready-375.png) | [截图](devtools-tile-detail-430.png) |
| 商品列表 | [截图](devtools-product-list-320-before.png) | [截图](devtools-matrix-product-list-ready-375.png) | [截图](devtools-matrix-product-list-ready-430.png) |
| 品牌列表 | [截图](devtools-matrix-brand-list-ready-320.png) | [截图](devtools-matrix-brand-list-ready-375.png) | [截图](devtools-brand-list-430.png) |
| 品牌详情 | [截图](devtools-matrix-brand-detail-ready-320.png) | [截图](devtools-matrix-brand-detail-ready-375.png) | [截图](devtools-brand-detail-430.png) |
| 证书列表 | [截图](devtools-matrix-certificates-ready-320.png) | [截图](devtools-error-return-certificates-375.png) | [截图](devtools-certificates-430.png) |
| 证书详情 | [截图](devtools-matrix-certificate-detail-ready-320.png) | [截图](devtools-certificate-error-computed-375.png) | [截图](devtools-certificate-detail-430.png) |
| 门店信息 | [截图](devtools-matrix-store-info-ready-320.png) | [截图](devtools-matrix-store-info-ready-375.png) | [截图](devtools-store-info-430.png) |
| 分类 | [截图](devtools-matrix-category-ready-320.png) | [截图](devtools-category-375.png) | [截图](devtools-matrix-category-ready-430.png) |
| 搜索 | [截图](devtools-search-320.png) | [截图](devtools-matrix-search-ready-375.png) | [截图](devtools-matrix-search-ready-430.png) |
| 发现 | [截图](devtools-matrix-find-ready-320.png) | [截图](devtools-matrix-find-ready-375.png) | [截图](devtools-find-430.png) |

## 根因、交互与证明边界

- Logo 问题根因状态 **confirmed（限当前DevTools原生预览）**：同一包内64×64 PNG能解码，但包路径预览破图；复制到USER_DATA_PATH后，虚拟好友预览显示正常。证据链为 category-share-preview-375 → logo-path-probe-375 → share-tempfile-probe-430 → share-logo-fixed-430。不能据此推定真实微信的内部原因。共享工具在页面进入时准备一次固定公开Logo，分享同步复用本地路径，文件API受限时回退包路径。
- 冷启动/热启动与单页：普通编译和reLaunch分享直达不依赖前置栈；搜索快照页及朋友圈“查看小程序分享页”能保留空结果上下文，点击原生“前往小程序”恢复普通模式。见 snapshot-search-430、snapshot-enter-miniapp-430、timeline-receive-empty-320。
- 对象与返回：不存在商品、品牌、证书的公开GET返回404；详情显示对应不可查看提示，不冒充已下架/隐藏/删除的服务端状态。非法分类回默认浏览；离线品牌显示错误，证书错误页恢复Online后可进入证书列表。普通无栈返回和快速双击返回可到首页；强制switchTab失败后的reLaunch由VM覆盖，不称为平台失败注入实测。
- 原生卡片：empty-share-320、timeline-preview-320、share-logo-fixed-430、offline-warm-logo-375、download-domain-fallback-430均显示Logo。预览后取消，未点击发送；渠道触发不等于送达成功。
- 实际样式：320pt选择器取得导航320×82px、fixed、overflow:hidden；标题147×16.25px、ellipsis/nowrap/hidden。375pt错误页导航375×82px，标题185×20px及相同省略策略。430pt Wxml Computed盒模型导航高116px、上内边距54px、左右16px，与模拟刘海安全区对应。三宽度首屏未见标题遮挡胶囊；长标题/空态见long-title-empty-320。样式证据分别为navigation-computed-320、certificate-error-computed-375、navigation-computed-430。
- 结束恢复430pt、Online、普通编译及首页；重新编译清除运行时图片/回调探针，未修改下载域名策略。见restored-normal-430。

## 图片异常补证结论

2026-09-07已完成受控404、模拟过期403、200损坏图片及下载后过期的原生双渠道卡片验证；业务请求连接失败时的错误态、Logo及返回也已验证。完整方法、截图、HTTP摘要、授权设置恢复和工具限制见[AC-015验收](media-acceptance.md)。该结论不代表体验版、生产签名或真机通过。

真机矩阵、真实微信版本和真机截图依用户指示waived，未执行，不计为通过。全局Offline阻断工具文件桥接的历史证据保留，其证明边界见上述验收记录，不把工具内部故障等同于产品业务网络失败。

## 截图索引

以下为原始DevTools截图；matrix-brand-list-375和matrix-tile-detail-375是加载骨架，文件名含ready的截图为等待页面响应后保存。其余文件的场景与结果按上文解释。

| 文件 | 保存时间（Asia/Shanghai） |
|---|---|
| [devtools-brand-detail-430.png](devtools-brand-detail-430.png) | 2026-09-06 11:56:41 |
| [devtools-brand-list-430.png](devtools-brand-list-430.png) | 2026-09-06 11:55:53 |
| [devtools-category-375.png](devtools-category-375.png) | 2026-09-06 11:47:39 |
| [devtools-category-share-preview-375.png](devtools-category-share-preview-375.png) | 2026-09-06 11:51:02 |
| [devtools-certificate-detail-430.png](devtools-certificate-detail-430.png) | 2026-09-06 11:58:28 |
| [devtools-certificate-error-computed-375.png](devtools-certificate-error-computed-375.png) | 2026-09-06 14:54:48 |
| [devtools-certificates-430.png](devtools-certificates-430.png) | 2026-09-06 11:59:25 |
| [devtools-download-domain-fallback-430.png](devtools-download-domain-fallback-430.png) | 2026-09-06 15:17:54 |
| [devtools-empty-share-320.png](devtools-empty-share-320.png) | 2026-09-06 14:41:25 |
| [devtools-error-return-certificates-375.png](devtools-error-return-certificates-375.png) | 2026-09-06 14:58:58 |
| [devtools-find-430.png](devtools-find-430.png) | 2026-09-06 12:04:02 |
| [devtools-home-320.png](devtools-home-320.png) | 2026-09-06 11:36:03 |
| [devtools-home-375.png](devtools-home-375.png) | 2026-09-06 11:46:35 |
| [devtools-home-430.png](devtools-home-430.png) | 2026-09-06 11:32:10 |
| [devtools-logo-path-probe-375.png](devtools-logo-path-probe-375.png) | 2026-09-06 11:53:31 |
| [devtools-long-title-empty-320.png](devtools-long-title-empty-320.png) | 2026-09-06 14:39:42 |
| [devtools-matrix-brand-detail-ready-320.png](devtools-matrix-brand-detail-ready-320.png) | 2026-09-06 15:07:50 |
| [devtools-matrix-brand-detail-ready-375.png](devtools-matrix-brand-detail-ready-375.png) | 2026-09-06 15:02:56 |
| [devtools-matrix-brand-list-375.png](devtools-matrix-brand-list-375.png) | 2026-09-06 15:02:05 |
| [devtools-matrix-brand-list-ready-320.png](devtools-matrix-brand-list-ready-320.png) | 2026-09-06 15:07:04 |
| [devtools-matrix-brand-list-ready-375.png](devtools-matrix-brand-list-ready-375.png) | 2026-09-06 15:02:31 |
| [devtools-matrix-category-ready-320.png](devtools-matrix-category-ready-320.png) | 2026-09-06 15:06:25 |
| [devtools-matrix-category-ready-430.png](devtools-matrix-category-ready-430.png) | 2026-09-06 15:18:41 |
| [devtools-matrix-certificate-detail-ready-320.png](devtools-matrix-certificate-detail-ready-320.png) | 2026-09-06 15:09:02 |
| [devtools-matrix-certificates-ready-320.png](devtools-matrix-certificates-ready-320.png) | 2026-09-06 15:08:12 |
| [devtools-matrix-find-ready-320.png](devtools-matrix-find-ready-320.png) | 2026-09-06 15:10:39 |
| [devtools-matrix-find-ready-375.png](devtools-matrix-find-ready-375.png) | 2026-09-06 15:04:14 |
| [devtools-matrix-product-list-ready-375.png](devtools-matrix-product-list-ready-375.png) | 2026-09-06 15:04:55 |
| [devtools-matrix-product-list-ready-430.png](devtools-matrix-product-list-ready-430.png) | 2026-09-06 15:12:40 |
| [devtools-matrix-search-ready-375.png](devtools-matrix-search-ready-375.png) | 2026-09-06 15:04:35 |
| [devtools-matrix-search-ready-430.png](devtools-matrix-search-ready-430.png) | 2026-09-06 15:19:33 |
| [devtools-matrix-store-info-ready-320.png](devtools-matrix-store-info-ready-320.png) | 2026-09-06 15:09:57 |
| [devtools-matrix-store-info-ready-375.png](devtools-matrix-store-info-ready-375.png) | 2026-09-06 15:03:49 |
| [devtools-matrix-tile-detail-375.png](devtools-matrix-tile-detail-375.png) | 2026-09-06 15:03:00 |
| [devtools-matrix-tile-detail-ready-320.png](devtools-matrix-tile-detail-ready-320.png) | 2026-09-06 15:09:32 |
| [devtools-matrix-tile-detail-ready-375.png](devtools-matrix-tile-detail-ready-375.png) | 2026-09-06 15:03:24 |
| [devtools-native-menu-375.png](devtools-native-menu-375.png) | 2026-09-06 11:50:04 |
| [devtools-navigation-computed-320.png](devtools-navigation-computed-320.png) | 2026-09-06 14:40:44 |
| [devtools-navigation-computed-430.png](devtools-navigation-computed-430.png) | 2026-09-06 14:26:31 |
| [devtools-offline-brand-375.png](devtools-offline-brand-375.png) | 2026-09-06 14:47:45 |
| [devtools-offline-cold-file-bridge-375.png](devtools-offline-cold-file-bridge-375.png) | 2026-09-06 14:50:08 |
| [devtools-offline-warm-logo-375.png](devtools-offline-warm-logo-375.png) | 2026-09-06 14:56:45 |
| [devtools-product-list-320-before.png](devtools-product-list-320-before.png) | 2026-09-06 11:41:39 |
| [devtools-restored-normal-430.png](devtools-restored-normal-430.png) | 2026-09-06 15:20:04 |
| [devtools-search-320.png](devtools-search-320.png) | 2026-09-06 11:44:33 |
| [devtools-share-logo-fixed-430.png](devtools-share-logo-fixed-430.png) | 2026-09-06 14:32:41 |
| [devtools-share-tempfile-probe-430.png](devtools-share-tempfile-probe-430.png) | 2026-09-06 14:29:44 |
| [devtools-sku-unavailable-430.png](devtools-sku-unavailable-430.png) | 2026-09-06 14:34:09 |
| [devtools-snapshot-enter-miniapp-430.png](devtools-snapshot-enter-miniapp-430.png) | 2026-09-06 14:37:39 |
| [devtools-snapshot-search-430.png](devtools-snapshot-search-430.png) | 2026-09-06 14:36:52 |
| [devtools-store-info-430.png](devtools-store-info-430.png) | 2026-09-06 12:01:56 |
| [devtools-tile-detail-430.png](devtools-tile-detail-430.png) | 2026-09-06 12:00:36 |
| [devtools-timeline-preview-320.png](devtools-timeline-preview-320.png) | 2026-09-06 14:42:29 |
| [devtools-timeline-receive-empty-320.png](devtools-timeline-receive-empty-320.png) | 2026-09-06 14:43:13 |

## 2026-09-07 返修构建

分享缓存已改用解码后的本地文件；JS SHA256：`021919e7d9ee66a19285fbd2e10234b7de4e084b8aac0f2ac5b6abd09f97fc98`。JS/TS各30项与pytest98项通过，详见Change trace。本轮远程异常素材渲染证据已独立保存在media-acceptance.md，不由旧截图替代。
