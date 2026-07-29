---
review_id: REV-REQ-0080-001
requirement_id: REQ-0080-miniapp-certificate-detail-page
date: 2026-07-29
reviewed_at: 2026-07-29 08:15:17
participants: []
result: approved
created_at: 2026-07-29 08:15:17
updated_at: 2026-07-29 08:15:17
---

# 需求评审

## 评审结论

REQ-0080「微信小程序新增证书详情页」评审通过。

该需求边界清晰：本期聚焦小程序公开端证书详情页，补齐证书列表到单证书浏览、品牌入口与微信分享的闭环；不包含管理端证书维护、证书真伪校验、SKU 强绑定、交易动作或对象存储直连。

验收标准覆盖功能、UI、API/数据、安全、非功能与小程序自定义导航 evidence；原型策略已提供 `prototype/miniapp/` HTML 与上下文说明，可进入 `/req-opsx` 与后续 Sprint 规划。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，包含入口、媒体、公开过滤、分享、异常和埋点。
- [x] 优先级与依赖合理，父需求为 `REQ-0038-brand-certificate-management`。
- [x] UI 类需求已提供小程序原型策略。
- [x] 与现有 `REQ-0057`、`REQ-0078`、`REQ-0044` 的关系已说明，不构成重复需求。

## 条件通过项

- [ ] `/req-opsx` 设计阶段需明确证书详情接口字段、旧单文件兼容、多图字段映射和错误码。
- [ ] 纳入 Sprint 前需确认小程序证书列表页点击行为从直接预览调整为进入详情页的影响范围。
- [ ] 实现阶段需按 `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` 留存 DevTools 320/375/430 pt evidence；真机不可用时不得写作通过。

## 后续建议

1. 执行 `/req-opsx REQ-0080-miniapp-certificate-detail-page` 创建 OpenSpec Change。
2. 通过 Sprint 规划纳入正式范围后，再进入实现。
