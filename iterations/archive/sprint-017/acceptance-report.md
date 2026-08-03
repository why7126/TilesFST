---
note: workflow-sync — 6/6 Change 已 archive；0 applied；待人工 sign-off
sprint_id: sprint-017
title: Sprint 017 Acceptance Report
status: completed
created_at: 2026-08-01 10:35:08
updated_at: 2026-08-02 19:32:35
---

# Sprint 017 Acceptance Report

## 验收状态

当前结论：Sprint 017 正式范围内 5 个 REQ、1 个 BUG 与 6 个 OpenSpec Change 已全部归档，范围验收通过，可执行 Sprint close 与 `/sprint-archive` 收尾。

## 正式范围

| 类型 | 编号 | Change | 状态 | 验收 |
|---|---|---|---|---|
| REQ | REQ-0088-versioned-product-usage-docs | add-versioned-product-usage-docs | done，已归档（`add-versioned-product-usage-docs` archived 2026-08-02 17:58:38） | 通过 |
| REQ | REQ-0090-media-five-point-acceptance-template | add-media-five-point-acceptance-template | done，已归档（`add-media-five-point-acceptance-template` archived 2026-08-01 11:13:14） | 通过 |
| REQ | REQ-0091-media-bug-four-point-acceptance-template | add-media-bug-four-point-acceptance-template | done，已归档（`add-media-bug-four-point-acceptance-template` archived 2026-08-01 11:04:15） | 通过 |
| REQ | REQ-0089-workflow-subdocument-status-sync | improve-workflow-subdocument-status-sync | done，已归档（`improve-workflow-subdocument-status-sync` archived 2026-08-01 11:46:37） | 通过 |
| BUG | BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | fix-miniapp-brand-list-carousel-text | done，已归档（`fix-miniapp-brand-list-carousel-text` archived 2026-08-02 16:51:12） | 通过 |
| REQ | REQ-0092-brand-certificate-image-thumbnails | add-brand-certificate-image-thumbnails | done，已归档（`add-brand-certificate-image-thumbnails` archived 2026-08-02 19:21:07） | 通过 |

## 验收清单

- [ ] 每个产品版本支持独立 `releases/<version>/usage-docs/` 目录，目录内包含产品使用文档源文件和 `manifest.json`。
- [ ] `/release-prepare <version>` 必须先确认本次是否需要生成或更新产品使用文档；未确认时不得自动生成新版本产品文档。
- [ ] 用户确认不需要生成或更新时，不创建空的当前版本 `usage-docs/` 目录，并在 `release.json` 记录 skipped 状态、确认来源和跳过原因。
- [ ] 产品文档校验覆盖 manifest 结构、版本一致性、页面清单、实际文件一致性、Mintlify 导航、broken links 和敏感信息。
- [ ] 旧版本产品文档默认视为快照；非内容性维护和安全修复可自动化，内容性更正必须授权留痕。
- [ ] 媒体五联模板包含 key、object、URL、thumbnail benefit、miniapp render 五个维度。
- [ ] 媒体类 BUG 四联模板包含原 BUG 场景、key、object、URL、render 四个维度。
- [ ] 媒体验收模板每个维度支持 pass、fail、n/a、blocked，且 N/A/blocked 必须记录原因。
- [ ] 媒体类 BUG 四联模板失败记录可直接支撑 `/bug-capture` 或原 BUG 返修。
- [ ] 明确 `trace.md`、`requirement.md`、`bug.md`、`acceptance.md`、`review.md` 等文档的状态字段职责。
- [ ] 状态变化命令后，主文档与 `review.md` 不得保留与 `trace.md` 冲突的当前主状态。
- [ ] `acceptance.md` 或等价文档支持记录验收状态、时间、来源、证据、失败项和备注。
- [ ] Drift check 能发现 trace、registry、目录阶段、主文档状态和验收结果漂移。
- [ ] 历史 archive 漂移治理支持 dry-run，apply 只处理可安全同步项。
- [ ] `/opsx-archive` 后能检查 archived Change trace 或 fallback 证据完整性。
- [ ] `/sprint-archive` 前能扫描 Issue 包和 Sprint 四件套中的中间态文案残留。
- [ ] Workflow Sync 摘要包含子文档检查数、更新数、验收结果状态和 drift warning 数量。
- [ ] focused pytest 覆盖 release 文档治理、媒体验收模板、REQ/BUG 常规同步、验收回填、drift check、历史 dry-run/apply、archive promote 阻断和摘要输出。
- [ ] 小程序品牌列表页轮播图不显示 `BRAND GALLERY` 文案。
- [ ] 小程序品牌列表页轮播图不显示 `轮播图保持现有品牌页能力` 文案。
- [ ] 小程序品牌列表页轮播图图片展示、轮播切换、指示点和点击/跳转能力保持不变。
- [ ] 小程序品牌列表页轮播图文案删除后无空白占位、遮挡、错位、高度异常或内容重叠。
- [ ] 新上传品牌图片生成真实缩略图，缩略图像素尺寸或文件体积明显低于原图，且不是原图 bytes 复制品。
- [ ] 新上传图片类品牌证书生成真实缩略图，证书列表、卡片和默认主图优先使用缩略图。
- [ ] 品牌/证书缩略图读取失败时可安全回退原图或占位图，不显示浏览器破图。
- [ ] 管理端、小程序和店主 Web 不直连未授权对象存储，继续通过后端受控 `/media/{object_key}` 或等价链路读取媒体。
- [ ] 存量品牌图片和证书图片补齐方案支持 dry-run / apply、幂等和脱敏统计摘要。
- [ ] 媒体五联验收覆盖对象 key、对象存在、URL 可访问、真实缩略收益和端上渲染 evidence。
- [ ] 本 Sprint 治理能力不影响 Web 管理端、小程序其他页面、后端 API、数据库、Docker Compose 或对象存储运行链路。

## 验证记录

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-01 11:13:21 | `/opsx-apply add-versioned-product-usage-docs` | REQ-0088 对应 Change 已实现；`uv run pytest tests/test_release_validation.py` 21 passed；目录结构校验、v0.3.2 release prepare validator、OpenSpec strict 均通过 |
| 2026-08-02 17:58:38 | `/opsx-archive add-versioned-product-usage-docs` | REQ-0088 对应 Change 已归档；archive evidence、Workflow Sync、REQ promote、目录结构、OpenSpec specs strict 与 AI Usage hook 均通过 |
| 2026-08-01 11:13:14 | `/opsx-modify REQ-0090` | 复核 add-media-five-point-acceptance-template apply 完整性；补充模板整体结论四态说明并校准 REQ-0090 五联验收口径 |
| 2026-08-01 10:35:08 | `/sprint-propose sprint-017 REQ-0088` | Sprint 规划创建，容量门禁通过，REQ/Change 纳入正式范围 |
| 2026-08-01 10:35:31 | `/sprint-propose sprint-017 REQ-0091` | REQ-0091 与 add-media-bug-four-point-acceptance-template 纳入正式范围，容量门禁通过 |
| 2026-08-01 10:42:25 | `/sprint-propose sprint-017 REQ-0089` | REQ-0089 与 improve-workflow-subdocument-status-sync 纳入正式范围，容量门禁通过，待同步校验 |
| 2026-08-02 12:09:44 | `/sprint-propose sprint-017 BUG-0102` | BUG-0102 与 fix-miniapp-brand-list-carousel-text 纳入正式范围，容量门禁通过 |
| 2026-08-02 18:16:03 | `/sprint-propose sprint-017 REQ-0092` | REQ-0092 与 add-brand-certificate-image-thumbnails 纳入正式范围，容量门禁通过 |
| 2026-08-02 19:31:01 | `/sprint-archive sprint-017` | Sprint 017 最终验收通过；6/6 Change 已归档，Issue promote gate 与 stale scan 通过 |
