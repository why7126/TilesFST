---
requirement_id: REQ-0111-miniapp-media-four-part-acceptance-practice
created_at: 2026-08-12 14:29:30
updated_at: 2026-08-12 14:29:30
---

# User Stories

## US-001 产品负责人识别媒体验收是否闭环

作为产品负责人，我希望在媒体性能需求或 BUG 验收中看到 key、object、URL、render 四联证据，以便判断验收是否覆盖真实小程序用户体验，而不是只确认对象存在。

验收要点：

- 能从验收记录中看到四联维度的状态、证据和非 pass 处理。
- 能看出自动化测试、审计摘要和小程序 Network evidence 的边界。
- 能识别缺少真机或体验版证据时的 blocked / follow-up 承接方式。

## US-002 测试人员复用媒体四联断言

作为测试人员，我希望有可复用的测试 helper 检查缩略图 URL、预览 URL、视频 poster、fallback 和页面绑定，以便减少每个媒体需求重复编写断言且避免遗漏关键链路。

验收要点：

- helper 能表达图片展示 URL 优先缩略图、预览 URL 保留原图。
- helper 能表达视频 URL 不被替换、poster / cover 优先轻量图。
- helper 能表达页面模板绑定、fallback、lazy-load 和受控 `/media` URL 语义。

## US-003 后端与媒体开发审计历史对象风险

作为后端 / 媒体开发，我希望有 dry-run 审计 helper 检查历史媒体对象的 object、缩略图收益、URL fallback 和脱敏统计，以便在不默认写入生产数据的前提下识别回填或重生成风险。

验收要点：

- 审计 helper 默认 dry-run，输出脱敏统计摘要。
- 审计结果能分类为已闭环、缺缩略图、缩略图无收益、URL fallback、object 缺失、权限异常或证据不足。
- 需要 apply 时必须显式参数、备份确认、幂等验证和失败重试策略。

## US-004 小程序开发补齐真实端侧 evidence

作为小程序开发，我希望最佳实践明确 DevTools、真机、体验版 Network evidence 的最低字段，以便在媒体性能验收中证明页面实际请求和渲染符合预期。

验收要点：

- evidence 记录页面路径、场景、请求域名、HTTP 状态、业务响应、资源大小或耗时摘要。
- DevTools Network 明确不等同于体验版或真机网络验收。
- render evidence 覆盖展示、预览、播放、占位、失败态和用户可见行为。

## US-005 Sprint / 发布负责人识别发布前补证项

作为 Sprint / 发布负责人，我希望媒体四联最佳实践能进入 Sprint 验收和发布检查，以便对缺少 Network evidence、历史对象审计或回填策略的媒体改动做出发布前决策。

验收要点：

- Sprint 验收报告能引用四联结论、blocked 项和剩余风险。
- 发布检查能识别小程序体验版、真实域名、历史对象和公开媒体 URL 的补证要求。
- 不把只读审计或批处理摘要当作端侧 render 通过证据。
