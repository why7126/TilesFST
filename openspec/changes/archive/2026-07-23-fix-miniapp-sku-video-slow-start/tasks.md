## 1. 后端媒体读取

- [x] 1.1 设计 `/media/{object_key}` 的视频 Range 请求解析与响应策略，保留 object_key 校验和 legacy key 兼容。
- [x] 1.2 实现视频对象 `Range: bytes=start-end` 读取，返回 `206 Partial Content`、`Accept-Ranges: bytes`、`Content-Range`、正确 `Content-Length` 和视频 `Content-Type`。
- [x] 1.3 保持非 Range 媒体读取、图片读取、对象不存在、非法 object_key 和对象存储不可用错误不回归。

## 2. 小程序 SKU 详情视频体验

- [x] 2.1 确认 `GET /api/v1/miniapp/skus/{sku_id}` 视频媒体项的 `url` 仍为后端安全可播放 URL。
- [x] 2.2 为视频 `poster` 增加 `cover_url`、商品主图或安全兜底图策略，避免加载中长期空白。
- [x] 2.3 保持视频用户主动播放、播放期间轮播暂停、页面隐藏/跳转暂停等既有交互不回归。

## 3. API / 文档 / 契约

- [x] 3.1 若 SKU 详情响应新增或调整视频封面/播放字段，更新 OpenAPI、Orval、`docs/03-api-index.md` 相关说明和契约测试。
- [x] 3.2 若实现涉及 Nginx `/media/` Range 透传、缓存或超时配置，更新 `docs/02-deployment.md` 与部署 smoke 清单。
- [x] 3.3 若实现新增视频封面持久化字段，更新 SQLite/MySQL schema、`docs/04-database-design.md` 和迁移/测试。

## 4. 测试与验收

- [x] 4.1 补充后端媒体 Range/206 测试，覆盖合法 Range、非法 Range、完整响应和错误路径。
- [x] 4.2 补充小程序静态测试，覆盖视频封面兜底和现有播放控制不回归。
- [x] 4.3 运行相关后端 pytest 与小程序静态测试。
- [x] 4.4 生产或生产等价验收记录至少一个 SKU 的视频文件大小、格式、编码、时长、机型、网络类型、点击到首帧耗时和 `/media/{object_key}` Range 响应头。

## 5. 追溯与知识沉淀

- [x] 5.1 更新 BUG-0082 trace 与关联需求缺陷索引，保持 Change 状态可追溯。
- [x] 5.2 修复完成后评估是否需要沉淀 `docs/knowledge-base/incidents/`，记录生产小程序视频慢启动排查方法。

## 归档验证摘要

- 验证命令与结果：`uv run pytest tests/test_media_storage.py tests/test_miniapp_static.py` 于 `2026-07-24 13:30:37` 通过，结果 `41 passed`，覆盖视频 Range、HEAD 元信息函数与 HEAD 路由响应、小程序静态契约；`openspec validate --specs --strict` 已在同批 Sprint 归档校验中通过。
- 验收结论：BUG-0082 的核心本地验收通过，已补齐 `/media/{object_key}` 视频 Range/206 分段读取、小程序视频 `poster` 封面兜底和非视频读取回归测试。命令行环境不能执行微信开发者工具或真机验收，实际 SKU 的机型、网络、视频大小、编码、时长和点击到首帧耗时仍需上线 sign-off 补证，不得写成真机已通过。
- Issue / Sprint 状态：`issues/bugs/archive/BUG-0082-prod-miniapp-sku-video-slow-start/trace.md` 显示 BUG 状态为 `done`、`lifecycle_stage: archive`，关联 Change `fix-miniapp-sku-video-slow-start` 状态为 `archived`，已纳入 `sprint-011`。
- 归档路径与时间证据：Change 已归档至 `openspec/changes/archive/2026-07-23-fix-miniapp-sku-video-slow-start/`；BUG trace 记录 `/opsx-archive fix-miniapp-sku-video-slow-start` 于 `2026-07-23 23:12:44` 完成状态同步，并于 `2026-07-23 23:13:16` 执行 `review -> archive` lifecycle-stage-migrate。
