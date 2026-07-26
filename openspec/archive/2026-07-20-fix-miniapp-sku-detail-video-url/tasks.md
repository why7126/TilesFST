## 1. OpenSpec 与追溯

- [x] 1.1 确认 `BUG-0069`、`REQ-0044` 与本 Change 双向追溯完整。
- [x] 1.2 复核本 Change 不新增视频转码、封面生成、管理端上传流程或数据库结构。
- [x] 1.3 运行 OpenSpec 校验并修复规格格式问题。（2026-07-20 22:46:35 已重跑：`openspec status --change "fix-miniapp-sku-detail-video-url" --json` 返回 `isComplete: true`；`openspec validate fix-miniapp-sku-detail-video-url --strict` 通过）

## 2. 后端 SKU 详情视频 URL 修复

- [x] 2.1 调整小程序 SKU 详情媒体查询，视频媒体使用 `tile_videos.object_key` 作为 URL 生成来源。
- [x] 2.2 保持视频 URL 经后端媒体访问层归一化为 `/media/{object_key}` 或完整公开安全 URL。
- [x] 2.3 保持图片媒体读取、主图排序、图片数、视频数、分享图和推荐数据不退化。
- [x] 2.4 确认不向小程序返回未授权对象存储地址、内部路径或原始上传文件名作为播放 URL。
- [x] 2.5 调整小程序 SKU 详情图片、主图和分享图读取，使用 `tile_images.object_key` 生成安全媒体 URL，不再向小程序返回历史 `tile_images.url`。
- [x] 2.6 为 `/media/{object_key}` 增加历史图片 key 兼容映射，避免旧 `original/default/...` 图片路径残留导致 404。

## 3. 小程序详情页回归

- [x] 3.1 回归 `pages/tile-detail/index.wxml` 的 `<video src="{{item.url}}">` 能消费接口返回的视频 URL。
- [x] 3.2 回归 `onVideoPlay`、`pauseVideo`、`onMediaChange` 和 `onMediaError` 行为。
- [x] 3.3 确认视频播放期间轮播不自动切换，页面隐藏、返回或跳转时暂停视频。
- [x] 3.4 确认单个视频失败不阻断图片媒体和 SKU 文本信息浏览。
- [x] 3.5 移除视频未播放态对商品主图或图片兜底图的 poster 回落，只保留视频自身 `cover_url`。
- [x] 3.6 调整详情页内容顺序为“商品信息 >> 品牌信息 >> 商品参数”，且商品信息仅显示商品名称和商品价格。
- [x] 3.7 调整商品参数顺序为“SKU 编码 >> 类目 >> 规格 >> 主色系 >> 表面工艺”。

## 4. 测试与文档

- [x] 4.1 补充后端测试：`object_key` 与 `file_name` 语义不同时，SKU 详情视频 URL 使用 `object_key` 生成。
- [x] 4.2 补充或更新小程序静态测试，覆盖视频节点、`src="{{item.url}}"`、播放事件、错误提示和暂停逻辑。
- [x] 4.3 若 API 响应结构不变，记录“不需要 Orval”；若 API 契约变化，则同步 OpenAPI、Orval、`docs/03-api-index.md` 和相关测试。
- [x] 4.4 评估是否需要写入 `docs/knowledge-base/incidents/`，沉淀“测试种子误用显示名掩盖媒体 URL 缺陷”的经验。（本次为窄修复，暂不新增 incident 文档；经验已沉淀在 BUG root-cause、acceptance 与回归测试）
- [x] 4.5 补充媒体访问测试，覆盖历史图片 key 到当前对象 key 的兼容映射。
- [x] 4.6 补充 SKU 详情与小程序静态测试，覆盖图片 URL 不返回旧路径、视频 poster 无主图覆盖、内容顺序和参数顺序。

## 5. 验收收尾

- [x] 5.1 运行后端目标测试与小程序静态测试。
- [x] 5.2 汇总接口响应、测试命令、影响范围和剩余人工真机验收项。
- [x] 5.3 更新 BUG、REQ-0044、Sprint 和本 Change 的追溯状态。（归档阶段已执行 Workflow Sync 与 Issue Promote；Change 状态为 `archived`，BUG-0069 已迁入 `issues/bugs/archive/`）
