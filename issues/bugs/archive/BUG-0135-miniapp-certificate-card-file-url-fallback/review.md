---
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
review_status: approved
reviewed_at: 2026-08-22 21:15:46
reviewed_by: AI
created_at: 2026-08-22 21:15:46
updated_at: 2026-08-22 21:15:46
---

# 评审结论

确认修复，状态批准为 `approved`。

## 评审清单

- [x] 可复现或根因充分：缺陷包已记录品牌详情证书卡 `thumbnail_url || file_url` 的代码证据、后端品牌证书摘要接口返回原文件 URL 的契约风险，以及证书列表页缺缩略图时占位的对照策略；根因状态为 `probable`，并已列出接口响应、对象存储和小程序 Network 补证步骤。
- [x] 严重等级合理：问题影响微信小程序证书卡片这类可能批量渲染的展示位，缺缩略图时可能扩大原文件下载流量，并触及原文件受控访问边界，`high` 合理。
- [x] 回归验收明确：`acceptance.md` 已覆盖证书卡缩略图优先、缺缩略图占位、图片/PDF 前缀分流、历史对象审计、媒体代理一致性和小程序 DevTools/真机/体验版 evidence。
- [x] 是否需 hotfix 路径：建议优先纳入最近 Sprint；若体验版或正式版已经出现证书卡列表加载慢、原图流量异常或访问边界漂移，可按高优先级 hotfix 处理。

## 评审说明

该问题属于媒体多规格图片策略在品牌证书卡片展示链路上的契约缺口。卡片展示应消费缩略图、卡片专用展示 URL 或占位资源，不应在缺缩略图时直接退回 `file_url` 原文件；详情、预览或文件打开动作可以保留受控原文件访问。当前缺陷包已具备进入 Sprint 和 OpenSpec 修复规划的证据与验收口径。

## 后续动作

- 先执行 `/sprint-propose sprint-xxx --bug BUG-0135-miniapp-certificate-card-file-url-fallback` 纳入 Sprint 正式范围。
- 纳入 Sprint 后执行 `/bug-opsx BUG-0135-miniapp-certificate-card-file-url-fallback` 创建修复 Change。
