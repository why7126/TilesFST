---
requirement_id: REQ-0096-miniapp-network-panel-release-checklist
created_at: 2026-08-04 08:42:00
updated_at: 2026-08-04 08:42:00
---

# User Stories

## US-001 发布负责人执行小程序发布准备

作为发布负责人，我希望 `/miniapp-prepare` 输出除自动门禁外的 DevTools Network 与体验版 Network checklist，以便发布前知道哪些真实小程序网络链路仍需人工确认。

验收要点：

- [ ] checklist 明确区分自动完成项与人工待执行项。
- [ ] DevTools Network 与体验版 Network 不得被自动标记为已通过。
- [ ] checklist 能指向后续 `/miniapp-confirm` 记录结论。

## US-002 测试人员验证 DevTools 网络面板

作为测试人员，我希望在微信开发者工具中按页面和资源类型检查 Network evidence，以便确认开发者工具运行态没有错误环境、错误域名或资源加载失败。

验收要点：

- [ ] 记录 DevTools 版本、基础库版本、页面路径和运行策略。
- [ ] 记录关键 API 的 HTTP 状态与业务响应状态。
- [ ] 记录图片、视频、证书或静态资源加载结论。
- [ ] 结论说明 DevTools Network 不等同于体验版或真机网络验收。

## US-003 测试人员验证体验版网络链路

作为测试人员，我希望在体验版入口中验证生产域名、关键页面和媒体资源加载，以便确认用户将访问到正确的生产链路。

验收要点：

- [ ] 确认已上传最新开发版本并设为体验版。
- [ ] 手机删除旧体验版入口后重新扫码体验版二维码。
- [ ] 体验版首页、列表页和详情页请求生产 API 域名。
- [ ] 缺少体验版 Network evidence 时只能记录 blocked 或 follow_up，不得写作 passed。

## US-004 小程序开发定位发布前网络问题

作为小程序开发，我希望 Network checklist 能记录失败项、页面路径、请求域名和资源类型，以便快速定位环境策略、合法域名、接口状态或受控媒体 URL 问题。

验收要点：

- [ ] failed 状态包含失败表现、影响页面、影响范围和后续处理建议。
- [ ] blocked 状态包含账号、设备、域名、服务或网络阻塞原因。
- [ ] 记录不得包含 token、Cookie、Authorization header、`.env` 或真实隐私数据。

## US-005 产品负责人判断发布风险

作为产品负责人，我希望发布记录能区分 passed、failed、blocked、follow_up 和 not_applicable，以便判断是否允许发布、暂缓发布或带风险发布。

验收要点：

- [ ] 生产 API smoke 失败、错误环境请求和核心页面资源不可用应进入阻断说明。
- [ ] 非核心页面未覆盖可记录为 follow_up，但必须写明剩余风险和责任人。
- [ ] 与小程序设备 evidence 的边界清晰，避免把静态测试通过写成真实网络链路通过。
