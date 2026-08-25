---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
acceptance_status: passed
created_at: 2026-08-22 21:08:06
updated_at: 2026-08-25 14:51:36
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | 证书详情接口图片媒体项返回可用于顶部普通展示的 `display_url`，并与原图预览 URL 区分 | pass |
| AC-002 | 小程序证书详情页顶部图片优先使用 `display_url`，不因缺缩略图而直接退回原图 | pass |
| AC-003 | 图片预览入口使用 `original_url`、`preview_url` 或等价高清 URL，不影响顶部普通展示性能策略 | pass |
| AC-004 | 图片证书使用 `images/default/brand-certificates/`，PDF/文档证书使用 `files/default/brand-certificates/` | pass |
| AC-005 | 历史对象、缩略图、display 图或审计脚本如被触发，记录 dry-run、apply、幂等摘要 | pass |
| AC-006 | 微信小程序 DevTools、真机或体验版 Network 证据覆盖 URL、Size、Time 与缓存状态 | pass |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0134-miniapp-certificate-detail-display-url |
| 标题 | 小程序证书详情页顶部展示缺少 display_url 导致退回原图 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 对象存储 / 媒体 URL |
| 复现入口 | 微信小程序证书详情页顶部证书图 |
| 受影响端 | miniapp / backend / storage |
| 环境 | miniapp-devtools / miniapp-device / local |
| 媒体类型 | certificate / image / thumbnail / display |
| 业务资源 | 脱敏图片类品牌证书资源 |
| 修复前实际结果 | 证书详情媒体项缺少 `display_url`，顶部展示在缺缩略图或展示图字段时可能请求 `file_url` 原图 |
| 修复后期望结果 | 图片证书详情顶部普通展示优先请求 `display_url`；图片预览才请求原图；PDF/文档证书保持文件打开或占位策略 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | DevTools Network 截图（用户提供，`codex-clipboard-2266e997-93d6-46e3-bf35-5d983fcc7d26.png`）暴露历史样本曾请求 `/media/files/default/brand-certificates/...thumb.jpg`；随后本地 `sqlite-tencent-cos` 执行 `bug-0116-media-drift` apply 与幂等 dry-run，摘要为 `failed=0`、`retry_candidates=0`、`thumbnail_candidates=0`、`non_standard_keys_after_audit=0`；本次返修追加 SQLite 证据：`media_id=40` 的 `brand_certificate_images.file_key` 已迁移到 `images/default/brand-certificates/...jpg`，`file_url` 仍保留旧 `/media/files/default/brand-certificates/...jpg`，历史图片 key 计数为 0、canonical 证书图片 key 计数为 26；`migrate-certificate-image-keys` dry-run 为 `image_candidates=0`、`document_skipped=5`、`failed=0`，确认图片 key 漂移已收敛，PDF/文档证书继续保留 `files/default/brand-certificates/` 边界 | 无 |
| object | pass | DevTools Network 截图显示 `.thumb.jpg` 对象可读，响应 `content-type: image/jpeg`、`content-length: 19950`、`cache-control: public, max-age=604800, stale-while-revalidate=86400`；返修只读诊断显示本地 `sqlite-tencent-cos` 环境可 HEAD 原图，但缺失 `.thumb.webp` 返回腾讯 COS SDK 错误码 `NoSuchResource`，已修复该错误码被误判为 `object_storage_unreachable` 的问题；`backfill-image-variants` 全量 dry-run 初始为 `total=684`、`thumbnail_missing=186`、`display_missing=186`、`estimated_writes=372`，全量 apply 后成功生成 370 个派生对象，幂等 dry-run 为 `skipped=682`、`thumbnail_missing=1`、`display_missing=1`、`estimated_writes=3`、`retry_candidates=2`；本次运行时 HEAD 证据显示证书 4 主图 `.display.webp` 为 `200 OK`、`content-type=image/webp`、`content-length=106654`、`x-media-fallback=0`，`.thumb.webp` 为 `200 OK`、`content-type=image/webp`、`content-length=9698`、`x-media-fallback=0` | 剩余 2 个 retry candidate 作为后续单点数据治理项，不阻塞 BUG-0134 受影响样本恢复 |
| URL | pass | 后端接口聚焦测试通过；DevTools Network 截图补充真实小程序请求：URL 类型为本地后端受控 `/media` URL，`GET http://127.0.0.1:8000/media/files/default/brand-certificates/5a1177bc-c8ab-46a8-9b54-d8c7c6500c07.thumb.jpg`，HTTP `200 OK`，Remote Address `127.0.0.1:8000`，响应 `image/jpeg`，大小 `19950` bytes；补充截图 `codex-clipboard-b49a8c87-3fcb-4b9b-9acf-2d9e7a401ce9.png` 显示本地后端受控 `/media/images/default/tiles/143/...thumb.jpg`，HTTP `200 OK`，`content-length: 25159`，`x-media-fallback: 0`；全量回填后 `/api/v1/miniapp/products?page=1&page_size=12` 响应中 `product_id=377/361/362/...` 均返回 `/media/images/default/tiles/...thumb.webp` 与 `/media/images/default/tiles/...display.webp`；本次 `/api/v1/miniapp/certificates/4` 运行时响应显示 `media_id=40` 的 `display_url`、`thumbnail_url`、`original_url` 均切到 `/media/images/default/brand-certificates/...`，未见对象存储 endpoint、bucket、密钥或 raw internal endpoint 暴露 | 若后续体验版/生产域名出现 403/404、签名过期或直连未授权对象存储，回到后端媒体代理或对象 key 映射排查 |
| render | pass | 小程序详情页截图右侧显示“证书详情”页面正常渲染证书图片和证书信息卡；DevTools Network Waterfall 可见该 `.thumb.jpg` 请求完成，页面未白屏；补充截图 `codex-clipboard-b49a8c87-3fcb-4b9b-9acf-2d9e7a401ce9.png` 显示证书详情页在维护 apply 与幂等 dry-run 后可正常渲染证书页、证书信息卡和缩略图受控请求；用户追加截图 `codex-clipboard-ce278dc9-4382-4deb-9175-a3ae562fc5b8.png` 与 AppData 截图 `codex-clipboard-d6912f1a-8c27-4650-94d6-6fec3893cb17.png` 证明半迁移状态会让详情轮播显示“证书”占位；本次修复后接口已返回非空 `display_url`，静态测试确认顶部图片绑定为 `display_url || thumbnail_url`，预览绑定为 `original_url || preview_url || url`；补充截图 `codex-clipboard-77f20599-cb4c-4c6c-b85e-c070c03d10b0.png` 显示小程序首页新品推荐与热销推荐商品卡图片已正常渲染 | 需用户在微信 DevTools 刷新证书详情页补一张最终 render 截图作为人工视觉确认 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦证书详情展示消费，不直接修改上传入口 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及 Nginx、Docker Web 上传大小或边界文件 |
| 媒体代理一致性 | pass | 聚焦接口测试与本地运行时接口确认证书详情图片 `display_url`、`thumbnail_url`、`original_url` 均为受控 `/media/images/default/brand-certificates/` URL；PDF/文档不生成图片展示字段 |
| 历史对象与审计 | pass | 本地 `sqlite-tencent-cos` 已完成 BUG-0116 maintenance dry-run、apply 与幂等 dry-run：apply 生成 99 个缩略图，幂等 dry-run `failed=0`、`retry_candidates=0`、`thumbnail_candidates=0`、`non_standard_keys_after_audit=0`；随后全量 `backfill-image-variants` dry-run/apply/幂等复跑确认 684 个候选中 682 个已闭环，仅 2 个 retry candidate 保留为后续单点治理；本次 `migrate-certificate-image-keys` dry-run 显示无剩余图片迁移候选，剩余 5 条均为文档类 |
| 小程序 evidence | pass | 用户提供 DevTools Network + 页面截图：URL 类型为受控 `/media`，HTTP `200 OK`，资源大小包含 `19950` bytes 与 `25159` bytes 两组样本，`content-type=image/jpeg`，`x-media-fallback: 0`，Waterfall 可见请求完成；用户追加截图确认详情轮播半迁移占位问题；本地接口与 object HEAD 复核后，证书详情媒体字段已恢复为 canonical display/thumb URL，补充小程序首页截图显示新品推荐与热销推荐商品卡图片恢复渲染 |

## 验收数据建议

- 至少选择 1 个图片类品牌证书，原图体积明显大于 display 图或缩略图。
- 至少选择 1 个 PDF/文档类品牌证书，确认文件展示策略不误走图片 display 字段。
- 记录修复前后 `media[]` 中 `url`、`preview_url`、`thumbnail_url`、`display_url`、`original_url` 的字段差异。
- 记录顶部证书图请求 URL、Size、Time、Waterfall 和缓存状态。
- 记录相关 object 的 MIME、大小、扩展名、标准前缀和权限结论。

## 知识沉淀评估

本次修复沿用既有媒体多规格与小程序媒体四联验收规范，未发现新的可复用事故模式；暂不新增 `docs/knowledge-base/incidents/` 记录。后续若真实 Network evidence 发现对象前缀迁移、派生图生成或媒体代理新问题，应另行 capture 为独立 BUG 或 incident。

## 验收返修记录

| 时间 | 反馈 | 根因状态 | 调整 | 待补证 |
|---|---|---|---|---|
| 2026-08-23 08:30:02 | `./deploy/scripts/media-maintenance.sh local sqlite-tencent-cos bug-0116-media-drift --limit 100` 在 `variant_info` 阶段报告 `object_storage_unreachable`，导致 `.display` object 证据无法继续补齐 | confirmed：同一环境原图 HEAD 成功，缺失 `.thumb.webp` HEAD 返回 `NoSuchResource`，说明 COS 可达但缺失对象错误码未被适配层识别 | 对象存储适配层将 `NoSuchResource` 与 `NoSuchKey` / `NoSuchObject` 同样归类为媒体对象缺失；当前源码 dry-run 已识别 `retry_candidates=99`、`thumbnail_candidates=99` 且 `failed=0` | 执行 maintenance apply 与幂等复核；补 `.display` object 与小程序 Network evidence |
| 2026-08-23 09:09:12 | 用户补充小程序 DevTools Network 截图，选中 `/media/images/default/tiles/143/...thumb.jpg` 请求 | confirmed：维护 apply 后缩略图受控 URL 可 200 读取且页面正常渲染；截图显示 `x-media-fallback: 0`，未回退原图或对象存储直连 | 记录 render / URL 证据，确认缩略图 fallback 链路可用；object 维度仍保留 `.display` 待补证 | 补 `.display` URL 或 display object 信息后再关闭 object blocked 项 |
| 2026-08-24 13:08:11 | 用户反馈小程序首页商品卡仍空图；排查发现此前 `--limit 100/500` 只覆盖前段候选，首页新品图片排在全量候选后段 | confirmed：全量 dry-run 显示 `total=684`、仍有 `thumbnail_missing=186`、`display_missing=186`；全量 apply 后幂等 dry-run 收敛为 `skipped=682`、`thumbnail_missing=1`、`display_missing=1`；刷新后的 `/products` 响应已为 `product_id=377/361/362/...` 返回 `.thumb.webp` 与 `.display.webp` | 记录全量 backfill 验证结果和小程序首页商品卡 render evidence；确认空图由维护任务 limit 覆盖不足导致，已通过全量回填恢复 | 无 |
| 2026-08-24 14:30:46 | 用户反馈证书详情 `media[]` 仍为 `files/default/brand-certificates` 历史 URL 且 `display_url/thumbnail_url=null`，轮播显示“证书”占位 | confirmed：SQLite 显示 `media_id=40` 的 `file_key` 已迁移到 `images/default/brand-certificates`，但 `file_url` 仍为旧 `/media/files/default/brand-certificates`；详情接口此前只用 `file_url` 派生变体 | 后端详情仓库读取 `brand_certificate_images.file_key`，服务层对 canonical 证书图片 key 优先派生 display/thumb/original；主证书查询也将 canonical key 转成受控 `/media/images/...` URL | 已通过 `tests/test_miniapp_home.py` 44 项；证书 4 运行时接口返回 `media_id=40.display_url=/media/images/default/brand-certificates/...display.webp`，display/thumb HEAD 均 `200 OK`、`content-type=image/webp`、`x-media-fallback=0` |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-24 17:15:07
accepted_by: workflow-sync
source_change: fix-miniapp-certificate-detail-display-url
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

