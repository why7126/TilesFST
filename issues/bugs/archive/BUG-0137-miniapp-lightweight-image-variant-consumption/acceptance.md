---
bug_id: BUG-0137-miniapp-lightweight-image-variant-consumption
acceptance_status: passed
created_at: 2026-08-24 15:02:18
updated_at: 2026-08-25 14:51:36
template_ref: docs/standards/media-bug-four-point-acceptance-template.md
practice_ref: docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md
---

# Acceptance

## 回归验收清单

| AC | 验收项 | 状态 |
|---|---|---|
| AC-001 | Banner schema 暴露并消费符合规范的轻量图字段，普通展示不只依赖 `image_url` | automated_pass |
| AC-002 | 首页 Banner 和品牌列表 Banner 作为首屏大图展示位，普通展示优先使用 `display_url`，缺失或不可读时降级到 `thumbnail_url` 或安全视图占位，不请求原图 | automated_pass |
| AC-003 | 品牌列表、品牌详情和品牌卡片普通展示禁止 fallback 到 `brand_logo_url` 原图 | automated_pass |
| AC-004 | 商品详情、品牌详情、证书详情分享图字段优先级与媒体多规格消费矩阵一致；如平台要求分享高清图，必须记录为明确分享入口例外 | automated_pass |
| AC-005 | 小程序 Network evidence 覆盖 Banner、品牌 Logo、分享图普通展示，证明未冷加载原图；本次 Banner display 优先策略已补首页和品牌列表 Banner 新证据 | evidence_pass |
| AC-006 | 小程序 render evidence 覆盖有轻量图、缺轻量图、字段缺失三类状态，页面不白屏、不破图、不拉原图；本次 Banner display 优先策略已补首页和品牌列表 Banner 新证据 | evidence_pass |
| AC-007 | 品牌主页顶部品牌图位作为 Hero 大图展示位，普通展示优先消费 `brand_hero_display_url`，缺失或不可读时降级到 `brand_hero_thumbnail_url` 或安全视图占位；小 Logo/品牌卡仍保持 thumbnail 策略 | evidence_pass |

## 媒体类 BUG 四联验收

模板引用：`docs/standards/media-bug-four-point-acceptance-template.md`  
小程序实践引用：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`

### 原 BUG 场景

| 字段 | 内容 |
|---|---|
| BUG | BUG-0137-miniapp-lightweight-image-variant-consumption |
| 标题 | 小程序 Banner、品牌 Logo、分享图普通展示未统一消费轻量图字段 |
| 严重等级 | high |
| 影响范围 | 小程序 / 后端接口 / 媒体 URL / 对象存储 |
| 复现入口 | 首页 Banner、品牌列表 Banner、品牌列表 Logo、品牌详情 Logo、商品详情分享、证书详情分享 |
| 受影响端 | miniapp / backend / storage |
| 环境 | local / miniapp-devtools / miniapp-device / miniapp-trial |
| 媒体类型 | image / logo / banner / share_image / thumbnail |
| 业务资源 | 脱敏 Banner、品牌 Logo、商品主图、证书图片资源 |
| 修复前实际结果 | Banner 只消费 `image_url`；品牌 Logo 可退到 `brand_logo_url`；商品详情分享图已复现为 `.jpg` 原图，且同对象存在 `.thumb.webp`；证书详情分享图当前对照样本为 `.display.webp` |
| 修复后期望结果 | 普通展示统一消费轻量图字段；缺轻量图时占位或失败态；原图仅在明确预览、下载或受控分享例外中使用 |

### 四联检查

| 维度 | 状态 | 证据 | 失败 / 阻塞处理 |
|---|---|---|---|
| key | pass | 修复前已定位脱敏媒体 URL 前缀：商品主图使用 `images/default/tiles/`，证书图片使用 `images/default/brand-certificates/`；修复后 DevTools Network 样本显示首页、品牌列表、SKU 详情和证书详情只出现脱敏媒体资源名或本地 tabbar 占位资源，未出现 raw object key、bucket 内部路径、Authorization header 或 Cookie | 无 |
| object | pass | 首轮修复后 Network 样本中首页、品牌列表、SKU 详情普通图片请求均为 `webp`，资源大小约 5.9-78.4 kB；返修反馈显示首页 fallback `/assets/tile-placeholder.png` 经 `__pageframe__/assets/` 307 后 500；返修后首页 Network 过滤 `place` 未出现 `tile-placeholder.png` 请求 | 无 |
| URL | pass | 首轮 DevTools evidence：`/home` XHR 200，约 10.3 kB / 2.18 s；返修后自动化扫描确认 `src/miniapp` 不再引用 `/assets/tile-placeholder.png`，聚焦测试通过；首页回归截图未见 `tile-placeholder.png` 307/500；本次返修将 Banner 普通展示 URL 顺序收紧为 `display_url -> thumbnail_url -> 安全视图占位` | 若后续新增历史素材缺派生图，仍需按媒体维护流程补派生图，不允许恢复普通展示原图 fallback |
| render | pass | 返修后首页 Banner 以视图占位正常渲染，商品卡片正常展示；品牌列表 Banner 缺图同样采用视图占位，商品卡片/收藏/列表缺图由现有空态渲染 | 无 |

### 媒体上传横切检查

| Gate | 状态 | 说明 |
|---|---|---|
| 上传状态机 | n/a | 本 BUG 聚焦小程序消费侧字段和 fallback，不直接修改上传入口 |
| 同会话即时回显 | n/a | 本 BUG 不涉及 Web 管理端上传或编辑即时回显 |
| Docker Web 边界 | n/a | 本 BUG 不涉及 Nginx、Docker Web 上传大小或边界文件 |
| 媒体代理一致性 | pass | 修复后 DevTools Network 样本显示小程序通过本地后端聚合接口和受控媒体资源加载，未见未授权对象存储直连、bucket 内部路径或敏感头 |
| 历史对象与审计 | n/a | 本 BUG 只收紧消费字段与 fallback，不新增历史对象维护任务；若后续发现缺派生图，按媒体维护流程另行处理 |
| 小程序 evidence | pass | 首轮修复前后 DevTools Network/render evidence 已补齐；返修反馈新增首页 `tile-placeholder.png` 307/500；返修后首页 Network/render 证据确认不再出现该本地占位图请求，页面正常渲染 | 无 |

## 修复前 Network / Render Evidence

| 场景 | source | page_path | media_kind | media_url_type | request_domain | http_status | business_status | resource_bytes | duration_ms | render_result | blocker_or_follow_up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 首页 Banner | network_devtools | `/pages/index/index`，调用 `/home` | banner | controlled_media_url / schema_single_image_url | `127.0.0.1:8000` | 200 | `code=0` | XHR 约 10.1 kB；可见 `.webp` 图片请求约 9.5 kB | XHR 约 3030；图片约 543 | 首页 Banner 渲染可见；当前样本图片为 `.webp` | 修复后需验证字段不再只依赖 `image_url`，并覆盖缺轻量图状态 |
| 品牌 Logo / 品牌 Banner | network_devtools | `/pages/brand-list/index`，调用 `/brands?page=1&pageSize=20` | logo / banner | controlled_media_url / thumbnail_or_original_fallback | `127.0.0.1:8000` | 200 | N/A | XHR 约 8.1 kB；图片约 5.9-10.4 kB | XHR 约 1220；图片约 143-340 | 品牌列表 Banner、品牌矩阵和 Logo 渲染可见 | 当前样本未复现原图请求；修复后需验证缺 thumbnail 时不回退 `brand_logo_url` |
| 品牌详情商品入口 | network_devtools | `/pages/brand-detail/index?brandId=6`，调用 `products?brandId=6&page=1...` | product_thumbnail / logo | controlled_media_url | `127.0.0.1:8000` | 200 | N/A | XHR 约 8.5 kB | XHR 约 1210 | 品牌详情 Banner 与商品网格渲染可见 | 截图未完整展示图片 URL 列，修复后需补图片 URL 级 Network evidence |
| 商品详情分享图 | appdata_devtools + render | `/pages/tile-detail/index?skuId=94` | share_image | original_fallback | `127.0.0.1:8000` | N/A | N/A | N/A | N/A | 商品详情与分享按钮可见；AppData `share.image_url` 为脱敏 `.jpg` 原图，同对象存在 `.thumb.webp` | 已复现分享图原图 fallback；修复后需验证分享图优先级与例外策略 |
| 证书详情分享图 | appdata_devtools + render | `/pages/certificate-detail/index?certificateId=4` | share_image / certificate_image | display_url | `127.0.0.1:8000` | N/A | N/A | N/A | N/A | 证书详情报告图可见；AppData `share.image_url` 为 `images/default/brand-certificates/...display.webp`，同对象存在 `.thumb.webp` | 作为对照样本；修复后需确认证书分享策略仍符合矩阵 |

## 修复后自动化 Evidence

| 类型 | 命令 / 文件 | 结论 |
|---|---|---|
| 后端与静态测试 | `uv run pytest tests/test_miniapp_home.py tests/test_miniapp_static.py` | 80 passed；覆盖 Banner `thumbnail_url` / `display_url`、品牌详情不下发原图 Logo、SKU 分享图使用 `.display.webp`、缺轻量图时 `share.image_url=null`、小程序普通展示不含原图 fallback；返修后同步断言 `src/miniapp` 不再引用 `/assets/tile-placeholder.png` |
| API 同步 | `bash scripts/generate-openapi-client.sh` | 已重新生成 `src/web/openapi.json` 与 `src/web/src/shared/api/generated.ts` |
| API 标准 | `python scripts/validate-api-standard.py` | 通过 |
| OpenSpec | `openspec validate fix-miniapp-lightweight-image-variant-consumption --strict` | 通过 |
| 文档语言 | `python scripts/validate-openspec-language.py` | 通过 |

## 修复后 Network / Render Evidence

| 场景 | source | page_path | media_kind | media_url_type | request_domain | http_status | business_status | resource_bytes | duration_ms | render_result | blocker_or_follow_up |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 首页 Banner | network_devtools + render | `/pages/index/index`，调用 `/home` 与 `/products?page=1&page_size=12` | banner / product_thumbnail | lightweight_webp / controlled_media_url | `127.0.0.1:8000` | 200 | `code=0` | `/home` XHR 约 10.3 kB；产品 XHR 约 11.2 kB；可见图片请求约 7.9-10.4 kB | `/home` 约 2180；产品约 1730；图片约 253-329 | 首页 Banner、新品推荐和商品卡片渲染可见 | 截图中 `Disable cache` 未呈现为勾选状态；但 Network 有实际图片请求且未见 `.jpg` 原图 |
| 品牌 Banner / Logo | network_devtools + render | `/pages/brand-list/index`，调用 `/brands?page=1&pageSize=20` | banner / logo | lightweight_webp / thumbnail_or_placeholder | `127.0.0.1:8000` | 200 | N/A | XHR 约 8.5 kB；图片约 5.9-10.4 kB；本地 tabbar PNG 90-478 B | XHR 约 850；图片约 95-198 | 品牌列表 Banner、品牌矩阵、Logo 和缺类目占位渲染可见 | 未见 `brand_logo_url` 原图请求；缺轻量图时按占位或首字母策略处理 |
| 商品详情分享图 / 普通展示 | network_devtools + render | `/pages/tile-detail/index?skuId=94`，调用 `/skus/94?client_id=...` | product_display / share_image / logo_thumbnail | display_webp / thumbnail_webp | `127.0.0.1:8000` | 200 | N/A | XHR 约 11.5 kB；图片约 9.4 kB、9.5 kB、10.1 kB、78.4 kB、46.4 kB | XHR 约 2070；图片约 104-135 | 商品详情主图、商品信息、品牌卡与分享按钮可见 | Network 未见 `.jpg` 原图冷加载行；分享图字段优先级由自动化测试断言为 `.display.webp` |
| 证书详情分享图 / 普通展示 | network_devtools + render | `/pages/certificate-detail/index?certificateId=4`，调用 `/certificates/4` | certificate_display / share_image / brand_logo_thumbnail | display_or_cached_lightweight / placeholder_png | `127.0.0.1:8000` | 200 | N/A | XHR 约 4.8 kB；本地 tabbar / 默认图 PNG 约 90 B | XHR 约 563；本地图约 3-4 | 证书报告图、证书信息和品牌入口渲染可见 | Network 未见 `.jpg` 原图冷加载行；证书分享图策略由自动化测试和修复前后对照确认为 display 优先 |

## 验收返修 Evidence

| 时间 | 反馈 / 验证 | 结论 |
|---|---|---|
| 2026-08-25 08:07:55 | 用户补充首页 Network 截图：`tile-placeholder.png` 先 307 Redirect，随后 500 `text/plain` | 首轮 accepted 撤回为补充复核；确认小程序包内缺少 `/assets/tile-placeholder.png` 且 fallback 会产生无效本地静态资源请求 |
| 2026-08-25 08:07:55 | 代码返修：移除首页、品牌列表、商品列表、搜索、收藏、商品卡片的 `/assets/tile-placeholder.png` fallback；Banner 缺图改为视图占位，列表缺图改为空字段触发现有空态 | 自动化返修完成，并由后续首页 DevTools Network/render 回归截图确认 |
| 2026-08-25 08:07:55 | `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py` | 80 passed；静态断言确认普通展示不再引用 `tile-placeholder.png` |
| 2026-08-25 08:17:05 | 用户补充首页返修后 Network/render 截图：Network 过滤 `place` 后列表无 `tile-placeholder.png` 请求；右侧首页 Banner 视图占位、新品推荐商品卡片和底部导航渲染可见 | 返修验收通过；未见 `tile-placeholder.png` 307/500，无白屏、破图或无限重试 |
| 2026-08-25 08:29:38 | 验收策略升级：小程序 Banner 轮播图归类为首屏大图展示位，目标规格从 thumbnail 调整为 display；自动化返修改为 `display_url` 优先、`thumbnail_url` 兜底 | 待用户补充或确认新的首页/品牌列表 DevTools Network/render 回归证据；自动化测试负责先证明字段顺序与不回退原图 |
| 2026-08-25 08:40:18 | 用户补充首页 Banner 新策略 Network/render 截图：DevTools 过滤 `.webp`，可见 `*.display.webp` 请求 200，content-type `image/webp`，content-length 约 7.6 kB；同屏商品卡片继续请求 `*.thumb.webp`；右侧首页 Banner、快捷入口和商品卡片渲染正常 | 首页 Banner display 优先策略通过；未见 `.jpg` 原图、preview、旧 url、语义不明 `image_url` 原图或 `tile-placeholder.png` 请求 |
| 2026-08-25 08:40:18 | 用户补充品牌列表 Banner 新策略 Network/render 截图：DevTools 过滤 `.webp`，可见品牌列表页 `*.display.webp` 请求及品牌 Logo `*.thumb.webp` 请求均 200，content-type `image/webp`，选中缩略图 content-length 约 7.1 kB；右侧品牌轮播、品牌矩阵和 Logo 渲染正常 | 品牌列表 Banner display 优先策略通过；Logo/卡片仍走 thumb 分工，未见原图或不存在静态占位图请求 |
| 2026-08-25 08:53:42 | 品牌主页顶部品牌图位升级为 Hero 大图位；后端品牌详情响应新增 `brand_hero_display_url` / `brand_hero_thumbnail_url`，小程序顶部 Hero 改为 display 优先、thumbnail 兜底；聚焦测试、OpenAPI/Orval、OpenSpec、API 标准和 root-cause evidence 校验通过 | 自动化返修通过；仍需用户补充品牌主页 DevTools Network/render 截图，确认 `.webp` 过滤下顶部 Hero 请求 `*.display.webp` 200，小 Logo/品牌卡仍为 `*.thumb.webp`，未见原图或不存在静态占位图 |
| 2026-08-25 09:03:03 | 用户补充品牌主页顶部 Hero Network/render 截图：DevTools 过滤 `.webp`，选中品牌 Logo/Hero `*.display.webp` 请求，Status Code 200 OK，content-length 约 13.1 kB；同屏商品卡请求多条 `*.thumb.webp`；右侧品牌主页顶部 Hero、品牌名称浮层、商品 Tab 和商品卡片渲染正常 | 品牌主页顶部 Hero display 优先策略通过；小 Logo/商品卡继续保持 thumb 分工，未见 `.jpg` 原图、preview、旧 url、语义不明 `image_url` 原图或不存在静态占位图请求 |

## 验收数据建议

- 至少 1 条首页 Banner，存在轻量图和原图。
- 至少 1 条品牌列表 Banner，存在轻量图和原图。
- 至少 1 个品牌 Logo，存在 `brand_logo_thumbnail_url` 和 `brand_logo_url`。
- 至少 1 个缺少轻量 Logo 的品牌，验证展示占位或失败态。
- 至少 1 个商品详情分享入口和 1 个证书详情分享入口，记录分享图来源字段。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-25 09:43:38
accepted_by: workflow-sync
source_change: fix-miniapp-lightweight-image-variant-consumption
source_sprint: sprint-025
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

