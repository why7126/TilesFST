---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
review_status: approved
reviewed_at: 2026-08-22 21:13:19
reviewed_by: AI
created_at: 2026-08-22 21:13:19
updated_at: 2026-08-22 21:13:19
---

# 评审结论

确认修复，状态批准为 `approved`。

## 评审清单

- [x] 可复现或根因充分：缺陷包已记录证书详情接口媒体项缺少 `display_url`、后端图片媒体 `url`/`preview_url` 指向 `file_url`、小程序顶部展示 `thumbnail_url || url` 的证据链；根因状态为 `probable`，并已列出接口响应与小程序 Network 补证步骤。
- [x] 严重等级合理：问题影响微信小程序证书详情页核心展示链路，可能导致普通详情浏览请求证书原图，带来加载性能退化和原图访问流量增加，`high` 合理。
- [x] 回归验收明确：`acceptance.md` 已覆盖证书详情 `display_url`、顶部展示优先级、图片预览原图策略、图片/PDF 前缀分流、历史对象与小程序 Network evidence。
- [x] 是否需 hotfix 路径：建议优先纳入最近 Sprint；若体验版或正式版已经暴露证书详情加载慢或原图流量异常，可按高优先级 hotfix 处理。

## 评审说明

该问题属于媒体多规格图片策略在品牌证书详情链路上的契约缺口。证书详情普通展示应使用 `display_url`，图片预览才使用原图或高清 URL；当前缺陷包已具备进入修复规划的证据与验收口径，但实现和验收阶段仍需补齐真实接口响应、小程序 DevTools Network 和页面渲染证据。

## 后续动作

- 先执行 `/sprint-propose sprint-xxx --bug BUG-0134-miniapp-certificate-detail-display-url` 纳入 Sprint 正式范围。
- 纳入 Sprint 后执行 `/bug-opsx BUG-0134-miniapp-certificate-detail-display-url` 创建修复 Change。
