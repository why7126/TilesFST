---
review_id: REV-REQ-0057-001
requirement_id: REQ-0057-certificate-list-page
date: 2026-07-19
participants: []
result: approved
created_at: 2026-07-19 23:46:28
updated_at: 2026-07-19 23:46:28
---

# REQ-0057 需求评审

## 评审结论

REQ-0057 小程序公开证书列表页评审通过。

本需求范围已明确收敛为微信小程序 TabBar「证书」页，从建设中占位升级为公开证书聚合列表。需求不重复管理端 `/admin/brand-certificates` 的创建、编辑、上传、显示/隐藏、删除与权限管理能力，而是复用 `REQ-0038-brand-certificate-management` 已建立的证书主数据和前台展示控制，面向装修客户、设计师和门店访客提供只读浏览、搜索筛选、分页加载与证书预览能力。

允许进入 `/req-opsx REQ-0057-certificate-list-page`。建议 OpenSpec change 命名为 `add-miniapp-certificate-list-page`。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖公开数据过滤、证书卡片、筛选、分页、预览、埋点、API 同步和安全边界。
- [x] 优先级与依赖合理，依赖 `REQ-0038` 品牌证书主数据、`REQ-0048` 小程序全局自定义导航和小程序公开 API。
- [x] UI 类原型或实现策略已决，后续 design 优先参考 `prototype/miniapp/certificate-list-page.html` 与 `prototype/miniapp/context.md`。
- [x] 无与现有 REQ 重复未说明；管理端证书列表已由 `REQ-0038` 覆盖，本需求定位为小程序公开列表。

## 条件通过项

- [x] 后续 `/req-opsx` 的 `design.md` MUST 引用 trace 中的 `knowledge_base_refs`，并说明小程序自定义导航、胶囊 reserve、页面 offset 和 320/375/430 pt evidence 如何落实。
- [x] 实现若新增或调整 `GET /api/v1/miniapp/certificates`，MUST 同步 OpenAPI、Orval、小程序服务层和接口测试。
- [x] 文件预览 MUST 使用后端受控 URL 或等价安全引用，不得暴露 MinIO 原始对象 Key 或未授权直连地址。
- [x] 实现阶段若扩大到证书详情页、品牌详情联动或管理端证书维护，应拆分独立 REQ 或回到需求评审。

## 后续动作

1. 执行 `/req-opsx REQ-0057-certificate-list-page` 创建 OpenSpec Change。
2. 通过 `/sprint-propose` 纳入 Sprint 后再进入实现。
3. 实现验收时按 `acceptance.md` 覆盖 API、数据过滤、小程序 UI、设备视口和文件预览。
