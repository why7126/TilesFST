---
sprint_id: sprint-017
title: Sprint 017 Release Note
status: published
created_at: 2026-08-01 10:35:08
updated_at: 2026-08-02 19:31:01
---

# Sprint 017 Release Note

## 计划交付

- 建立版本化产品使用文档目录与 manifest 规范，默认放在 `releases/<version>/usage-docs/`。
- 在 `/release-prepare <version>` 中加入“是否需要生成或更新产品使用文档”的确认点。
- 用户确认需要时，生成并校验当前版本 usage docs；用户确认不需要时，在 `release.json` 记录 skipped rationale，且不创建空文档目录。
- 扩展 `release.json` 的 `usage_docs` 元数据和 `usage_docs_preview` gate。
- 增加产品文档生成与校验能力，覆盖 manifest、Mintlify 导航、broken links、敏感信息、覆盖度和旧版本误改策略。
- 明确旧版本产品文档的快照语义：内容默认冻结，非内容性维护和安全修复可自动化，内容性更正需授权留痕。
- 明确 `域名/docs` 浏览的项目边界，包括 Mintlify base path、rewrite、反向代理或托管平台配置说明。
- 建立媒体五联验收模板，覆盖上传、API/对象、URL、前端/小程序渲染和性能/降级。
- 建立媒体类 BUG 四联验收模板，覆盖原 BUG 场景、key、object、URL、render、状态、证据和失败/阻塞处理。
- 建立 REQ/BUG 子文档状态同步规则，减少 `requirement.md`、`bug.md`、`acceptance.md` 等文档停留在旧状态的问题。
- 为 `acceptance.md` 或等价文档补齐验收结果回填结构，记录状态、证据、失败项、来源 Change 和来源 Sprint。
- 增加 drift check，覆盖 trace、registry、目录阶段、子文档状态和验收结果。
- 为历史 archive 漂移提供受控 dry-run / apply 治理路径，并在 Sprint close 前扫描中间态残留。
- 修复小程序品牌列表页轮播图多余说明文案，移除 `BRAND GALLERY` 与 `轮播图保持现有品牌页能力` 的用户可见展示，同时保持轮播图现有能力。
- 将真实缩略图生成与优先读取能力扩展到品牌图片和图片类品牌证书，覆盖管理端、小程序、店主 Web、对象存储和存量补齐治理。

发布状态：已发布。Sprint 017 纳入的 5 个 REQ、1 个 BUG 与 6 个 OpenSpec Change 已全部归档，Sprint close 前验收通过。

## 影响范围

- 影响：发布规则、目录结构规则、文档治理规则、`releases/` 文档、release metadata、Mintlify 导航、发布校验脚本、release skills、对象存储与媒体验收治理文档、Workflow Sync、REQ/BUG/OPSX/Sprint 命令 Skill、Issue 生命周期规则、品牌/证书缩略图生成与读取、管理端上传/回显、小程序与店主端小图展示、focused workflow 和媒体测试。
- 可能影响：发布准备与发布确认流程、文档站部署说明、Sprint close 与 workflow sync 门禁。
- 条件影响：后端 API、数据库表结构、Orval、Docker Compose 和镜像依赖仅在 REQ-0092 实现新增字段、持久化缩略图字段或图片处理依赖时同步。
- 小程序影响：品牌列表页轮播图展示层，需验证两段多余说明文案不可见且轮播图图片、切换、指示点和点击/跳转不回归。

## 发布风险

中等风险。主要风险不在运行时链路，而在发布治理、媒体验收和 workflow 治理口径：未确认时误生成 usage docs、skipped 流程记录不足、旧版本内容被自动化改写、媒体验收模板边界混淆、子文档状态同步误改历史事实、验收结果回填遗漏，或 Sprint close 中间态残留扫描误报。需通过 release validation、usage docs validation、Workflow Sync、OpenSpec strict 与聚焦测试闭环。

## 关联范围

| 类型 | 编号 | Change | 状态 |
|---|---|---|---|
| REQ | REQ-0088-versioned-product-usage-docs | add-versioned-product-usage-docs | archived |
| REQ | REQ-0090-media-five-point-acceptance-template | add-media-five-point-acceptance-template | archived |
| REQ | REQ-0091-media-bug-four-point-acceptance-template | add-media-bug-four-point-acceptance-template | archived |
| REQ | REQ-0089-workflow-subdocument-status-sync | improve-workflow-subdocument-status-sync | archived |
| BUG | BUG-0102-miniapp-brand-list-carousel-brand-gallery-text | fix-miniapp-brand-list-carousel-text | archived |
| REQ | REQ-0092-brand-certificate-image-thumbnails | add-brand-certificate-image-thumbnails | archived |
