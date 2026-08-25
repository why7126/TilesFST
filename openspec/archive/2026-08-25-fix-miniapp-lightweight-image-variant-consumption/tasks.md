## 1. 后端响应与字段契约

- [x] 1.1 梳理小程序首页、品牌列表、品牌详情、SKU 详情、证书详情接口中 Banner、Logo、分享图字段来源。
- [x] 1.2 为首页 Banner 和品牌列表 Banner schema/API 补齐 `thumbnail_url`、`display_url` 或等价轻量字段，保留必要旧字段兼容但明确语义。
- [x] 1.3 调整 SKU 详情分享图构造，优先使用明确分享轻量字段、`display_url` 或 `thumbnail_url`，不得默认退到原图 `.jpg` 或旧 `url`。
- [x] 1.4 调整证书详情分享图构造，图片证书优先使用 `display_url`，缺失时使用 `thumbnail_url` 或安全占位；PDF/文档证书不伪造图片 display。
- [x] 1.5 若 API 响应字段、Pydantic Schema 或示例发生变化，同步 OpenAPI、Orval、`docs/03-api-index.md` 和后端测试。
- [x] 1.6 为品牌主页顶部 Hero 图位在品牌详情响应补充独立 `brand_hero_display_url` / `brand_hero_thumbnail_url` 字段，避免将小 Logo 场景扩散为 display 策略。

## 2. 小程序消费与 fallback

- [x] 2.1 首页 Banner 和品牌列表 Banner 普通展示优先消费轻量字段，缺失或加载失败时展示安全占位，不请求原图。
- [x] 2.2 品牌列表、品牌详情、商品详情品牌卡、证书详情品牌卡统一禁止普通展示 fallback 到 `brand_logo_url` 原图。
- [x] 2.3 品牌卡组件默认关闭原图 Logo fallback；如保留参数，必须只允许明确高清或兼容例外入口打开。
- [x] 2.4 SKU 详情、证书详情分享对象与页面普通展示字段解耦，分享图例外必须有代码注释或验收说明。
- [x] 2.5 缺轻量图、图片加载失败、接口缺字段三类状态均不得白屏、破图或无限重试。
- [x] 2.6 品牌主页顶部 Hero 普通展示优先消费 `brand_hero_display_url`，缺失或加载失败时降级到 `brand_hero_thumbnail_url`，再降级到安全视图占位或品牌名占位；品牌列表和品牌卡 Logo 仍保持 thumbnail 目标规格。

## 3. 测试

- [x] 3.1 补充后端测试，覆盖 Banner 多规格字段、品牌 Logo 缩略图、SKU 分享图优先级和证书分享图优先级。
- [x] 3.2 补充或更新小程序静态测试，断言普通展示不包含 `original_url || preview_url || url` 或 `brand_logo_url` 原图 fallback。
- [x] 3.3 更新旧静态断言，移除“允许品牌 Logo 原图 fallback”和“Banner 只绑定 `image_url`”的过期预期。
- [x] 3.4 运行聚焦 pytest、小程序静态测试、OpenAPI/Orval 校验和 `python scripts/validate-openspec-language.py`。
- [x] 3.5 补充品牌主页 Hero 后端响应测试和小程序静态测试，覆盖 `display -> thumbnail -> 安全占位` 顺序、列表无 Hero 字段泄漏和无 `brand_logo_url` 原图 fallback。

## 4. 小程序 evidence 与验收回填

- [x] 4.1 使用微信小程序 DevTools 禁用缓存，采集首页 Banner Network/render evidence。
- [x] 4.2 采集品牌列表 Banner、品牌列表 Logo、品牌详情 Logo 或品牌卡片 Network/render evidence。
- [x] 4.3 采集商品详情分享图 AppData/Network/render evidence，确认不再默认下发原图。
- [x] 4.4 采集证书详情分享图 AppData/Network/render evidence，确认图片证书 display 策略和 PDF/文档占位策略。
- [x] 4.5 回填 BUG-0137 `acceptance.md` 媒体四联 key、object、URL、render 和验收结果。
- [x] 4.6 补充品牌主页顶部 Hero 图位 DevTools Network/render evidence，确认首屏请求 `brand_hero_display_url` 对应 `*.display.webp`，thumbnail 仅作为兜底，小 Logo/品牌卡仍请求 `*.thumb.webp`，未见原图、preview、旧 url、语义不明 `image_url` 或不存在静态占位图。

## 5. 文档与收尾

- [x] 5.1 回填 BUG-0137 trace、Change trace 和 Sprint 验收摘要。
- [x] 5.2 运行 `openspec validate fix-miniapp-lightweight-image-variant-consumption --strict`。
- [x] 5.3 评估是否需要新增媒体消费 fallback 最佳实践；无明确新增复用价值时记录不沉淀。
- [x] 5.4 若修复发现新的历史数据缺派生图问题，按标准 capture 文案提示，不自动创建 follow-up Issue。

## 验收返修记录

- [x] 2026-08-25 08:07:55 `/opsx-modify`：首页 DevTools Network 发现 `/assets/tile-placeholder.png` 经 `__pageframe__/assets/` 307 后 500；已将小程序缺图 fallback 收敛为视图占位/空字段，移除不存在静态占位图引用，并补静态测试断言。
- [x] 2026-08-25 08:17:05 `/opsx-modify`：已补首页 DevTools Network/render 回归证据，Network 过滤 `place` 未出现 `tile-placeholder.png`，页面以视图占位正常渲染，无白屏、破图或无限重试。
- [x] 2026-08-25 08:29:38 `/opsx-modify`：根据验收策略升级，将首页 Banner 与品牌列表 Banner 从 thumbnail 目标场景调整为 display 首屏大图展示场景；实现与测试改为 `display_url` 优先、`thumbnail_url` 兜底，并同步 API 文档、README 和 delta spec。
- [x] 2026-08-25 08:40:18 `/opsx-modify`：已补首页 Banner 与品牌列表 Banner 新策略的 DevTools Network/render evidence；截图显示 `.webp` 过滤下存在 `*.display.webp` 200 请求，商品卡片和品牌 Logo 继续使用 `*.thumb.webp`，未见原图、preview、旧 url、语义不明 `image_url` 原图或不存在静态占位图。
- [x] 2026-08-25 08:53:42 `/opsx-modify`：将品牌主页顶部品牌图位从小 Logo 语义升级为独立 Hero 大图位；后端品牌详情响应新增 `brand_hero_display_url` / `brand_hero_thumbnail_url`，小程序顶部 Hero 改为 display 优先、thumbnail 兜底，小 Logo/品牌卡仍保持 thumbnail；聚焦测试、OpenAPI/Orval、OpenSpec、API 标准和 root-cause evidence 校验通过，待补品牌主页 Hero DevTools Network/render 证据。
- [x] 2026-08-25 09:03:03 `/opsx-modify`：用户补充品牌主页顶部 Hero DevTools Network/render evidence；`.webp` 过滤下可见品牌 Logo/Hero `*.display.webp` 200 请求，content-length 约 13.1 kB，同屏商品卡继续请求 `*.thumb.webp`，品牌主页 Hero 和商品列表渲染正常，未见原图、preview、旧 url、语义不明 `image_url` 原图或不存在静态占位图。
