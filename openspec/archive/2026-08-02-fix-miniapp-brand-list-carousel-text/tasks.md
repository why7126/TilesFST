## 1. Miniapp Carousel Text Fix

- [x] 1.1 Locate the brand-list carousel markup, styles, and runtime entry files used by WeChat DevTools.
- [x] 1.2 Remove visible `BRAND GALLERY` text from the brand-list carousel area.
- [x] 1.3 Remove visible `轮播图保持现有品牌页能力` text from the brand-list carousel area.
- [x] 1.4 Preserve carousel data source, image rendering, autoplay/loop behavior, indicators, and click/jump handlers.
- [x] 1.5 Ensure removing text leaves no blank placeholder, overlap, layout shift, abnormal height, or blocked tap area.

## 2. Regression Tests

- [x] 2.1 Add or update miniapp static test coverage so the brand-list page no longer contains `BRAND GALLERY`.
- [x] 2.2 Add or update miniapp static test coverage so the brand-list page no longer contains `轮播图保持现有品牌页能力`.
- [x] 2.3 Add or update regression checks that the brand-list page carousel and brand list entry remain present.
- [x] 2.4 Run focused miniapp/static tests for brand-list page changes.

## 3. Scope and Documentation

- [x] 3.1 Confirm the implementation does not change backend API, database schema, Orval generated client, Web admin, or Docker Compose configuration.
- [x] 3.2 Update `BUG-0102` acceptance evidence after verification.
- [x] 3.3 Record whether this issue has reusable incident value for `docs/knowledge-base/incidents/`; no incident doc is needed because this is a low-risk miniapp UI copy cleanup with no production outage, data loss, security issue, or reusable operational incident.
- [x] 3.4 Run `openspec validate fix-miniapp-brand-list-carousel-text --strict`.

## 归档验证摘要

- 归档时间：2026-08-02 16:50:10
- 归档路径：`openspec/archive/2026-08-02-fix-miniapp-brand-list-carousel-text`
- Issue / Sprint 状态：来源 BUG `BUG-0102-miniapp-brand-list-carousel-brand-gallery-text` 已纳入 `sprint-017`，Change `fix-miniapp-brand-list-carousel-text` 已完成 apply 并进入 archive 收尾。
- 验收结论：通过自动化回归与静态检查；小程序品牌列表页不再展示 `BRAND GALLERY`、`轮播图保持现有品牌页能力`，轮播图现有图片展示、自动/循环播放、指示点与点击能力保持。
- 验证命令：`uv run pytest tests/test_miniapp_static.py -k brand_list`
- 验证结果：`1 passed, 30 deselected`
- 验证命令：`rg -n "BRAND GALLERY|轮播图保持现有品牌页能力" src/miniapp tests/test_miniapp_static.py`
- 验证结果：仅测试中的 negative assertions 保留，`src/miniapp` 无匹配。
- 验证命令：`openspec validate fix-miniapp-brand-list-carousel-text --strict`
- 验证结果：Change valid，归档前 spec delta 可合并。
