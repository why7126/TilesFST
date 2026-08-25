---
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
acceptance_status: passed
created_at: 2026-08-22 21:11:44
updated_at: 2026-08-25 14:51:36
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
practice_ref: docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | 品牌详情证书卡有 `thumbnail_url` 时只使用缩略图展示，不请求 `file_url` 原文件 | pass |
| AC-002 | 品牌详情证书卡缺少 `thumbnail_url`、缩略图对象不可读或图片加载失败时展示占位或受控失败态，不直接 fallback 到 `file_url` | pass |
| AC-003 | 证书列表、品牌证书摘要、商品详情关联证书等卡片入口的展示策略一致：卡片展示不拉原文件 | pass |
| AC-004 | 图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/` | warn |
| AC-005 | 如涉及历史对象、缩略图补齐或审计脚本，记录 dry-run、apply、幂等摘要；若不涉及，明确标记 n/a | n/a |
| AC-006 | 微信小程序 DevTools、真机或体验版 Network 证据覆盖 URL、Size、Time、缓存状态和页面 render 结果 | pass |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`  
小程序实践引用：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0135-miniapp-certificate-card-file-url-fallback |
| 标题 | 小程序证书卡缺缩略图时不应 fallback 到 file_url 原文件 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储 / 媒体 URL |
| 复现入口 | 微信小程序品牌详情页证书 Tab、证书列表或其他证书卡片摘要入口 |
| 受影响端 | miniapp / backend / storage |
| 环境 | miniapp-devtools / miniapp-device / miniapp-trial / local |
| 媒体类型 | certificate / image / thumbnail |
| 业务资源 | 脱敏图片类品牌证书资源，另取 PDF/文档证书作占位回归 |
| 修复前实际结果 | 证书卡缺少缩略图时可能通过 `thumbnail_url || file_url` 请求证书原文件 |
| 修复后期望结果 | 证书卡缺缩略图时展示占位或受控失败态；原文件仅在详情、预览或打开动作中访问 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | warn | 用户提供 DevTools Network 截图显示卡片请求脱敏 URL `GET http://127.0.0.1:8000/media/files/default/brand-certificates/<uuid>.thumb.jpg`，属于受控 `/media` 缩略图 URL，不是 `file_url` 原文件；该样本仍位于 `files/default/brand-certificates/`，疑似历史对象或上传前缀治理遗留 | 不阻塞 BUG-0135 的“卡片不拉原文件”修复；建议后续独立 capture 历史图片证书前缀治理或通过既有媒体维护 dry-run 评估 |
| object | n/a | 本 Change 未生成、迁移或写入对象；缩略图对象缺失时端侧改为占位，不再拉原文件 | 若缩略图 object 缺失或无收益，需补充生成、回填或占位策略；对象存储不可达时记录 blocked |
| URL | pass | `tests/test_miniapp_static.py::test_miniapp_home_detail_search_smoke_contracts` 断言品牌详情证书卡 `src` 仅使用 `item.thumbnail_url`；用户 DevTools 截图确认实际卡片请求 `.thumb.jpg` 缩略图，HTTP `200 OK (from disk cache)`，Remote Address `127.0.0.1:8000`，`content-length=24427`，`content-type=image/jpeg`，未见原文件 URL 请求 | 若卡片仍请求 `file_url`、返回 403/404 或直连未授权对象存储，修复 URL 字段和媒体代理映射 |
| render | pass | 用户 DevTools 截图右侧品牌详情证书 Tab 正常渲染多张证书卡片；Network Waterfall 可见缩略图请求完成，缓存状态为 disk cache，页面未白屏、未破图 | 若后续体验版/生产域名出现 403/404、签名过期或缩略图缺失，回到后端媒体代理、对象 key 映射或缩略图维护任务排查 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦小程序证书卡消费策略，不直接修改上传入口 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及 Nginx、Docker Web 上传大小或边界文件 |
| 媒体代理一致性 | pass | 后端测试确认品牌证书摘要返回受控 `/media/...thumb.webp` 缩略图 URL；小程序卡片只消费 `thumbnail_url` 或占位 |
| 历史对象与审计 | n/a | 本 Change 只调整端侧卡片消费和文档语义，未执行历史对象、缩略图补齐或对象漂移写入维护任务 |
| 小程序 evidence | pass | 用户提供 DevTools Network + 页面截图：URL 类型为受控 `/media` 缩略图，HTTP `200 OK`，资源大小 `24427` bytes，`content-type=image/jpeg`，缓存状态 `from disk cache`，Waterfall 可见请求完成，右侧证书卡片正常渲染 |

## 验收记录

| 时间 | 类型 | 结论 |
|---|---|---|
| 2026-08-22 21:39:55 | 后端回归 | `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py -q` 通过 79 项；品牌证书摘要保留原文件 URL 兼容字段并返回 `.thumb` 缩略图 URL，证书聚合列表不下发卡片原文件 URL。 |
| 2026-08-22 21:39:55 | 小程序静态回归 | 品牌详情证书卡图片 `src` 只绑定 `item.thumbnail_url`；缺缩略图或 `image_failed` 时走占位；加载失败埋点 `brand_certificate_image_failed` 已登记后端事件字典。 |
| 2026-08-22 21:39:55 | 历史对象审计 | 本次未发现必须写入历史对象或迁移对象 key 的实现需求，未执行 dry-run/apply；生产或测试环境如需补齐缩略图，沿用既有媒体维护命令单独验收。 |
| 2026-08-22 21:50:25 | 小程序 Network evidence | 用户提供 DevTools 截图，证书卡请求脱敏 URL `/media/files/default/brand-certificates/<uuid>.thumb.jpg`，HTTP `200 OK (from disk cache)`，`content-length=24427`，`content-type=image/jpeg`，Remote Address `127.0.0.1:8000`，页面右侧证书 Tab 正常渲染证书缩略图卡片；未观察到卡片请求 `file_url` 原文件。 |
| 2026-08-22 21:50:25 | 前缀观察 | 证据样本仍位于 `files/default/brand-certificates/` 下的 `.thumb.jpg`，说明本地/历史数据可能仍有图片证书前缀治理遗留；该问题不影响 BUG-0135 的 file_url fallback 修复，建议后续独立 capture 或媒体维护 dry-run 评估。 |

## 验收数据建议

- 至少选择 1 个图片类品牌证书，存在 `file_url` 且能控制 `thumbnail_url` 缺失或不可用。
- 至少选择 1 个图片类品牌证书，缩略图正常存在，确认卡片只请求缩略图。
- 至少选择 1 个 PDF/文档类品牌证书，确认卡片展示文件类型占位，不发起图片请求。
- 记录卡片入口请求 URL、Size、Time、Waterfall、缓存状态和 render 结果。
- 记录相关 object 的 MIME、大小、扩展名、标准前缀和权限结论。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-22 21:59:26
accepted_by: workflow-sync
source_change: fix-miniapp-certificate-card-file-url-fallback
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

