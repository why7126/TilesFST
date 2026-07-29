---
req_id: REQ-0079-admin-sku-list-published-at
status: done
created_at: 2026-07-28 22:37:35
updated_at: 2026-07-29 07:54:16
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0006-tile-sku-management
---

# 一句话

管理端瓷砖 SKU 列表在“更新时间”前新增“发布时间”列，展示格式与更新时间保持一致。

# 原始描述

管理端的瓷砖SKU页列表中更新时间前新增一个发布时间，格式与更新时间保持一致

# 背景与关联

- 父需求：`REQ-0006-tile-sku-management`
- 涉及端：企业内部 Web 管理端
- 涉及页面：瓷砖 SKU 列表页
- 业务价值：帮助运营在列表中快速区分 SKU 的发布时间与后续维护更新时间，减少进入详情或编辑页确认的操作成本。
- 预期后续：需要确认列表接口是否已返回发布时间字段；若未返回，后续 OpenSpec Change 需覆盖后端响应、OpenAPI/Orval、前端列表列配置与测试。

# 待澄清

- [ ] “发布时间”字段来源是 SKU 首次发布成功时间、创建时间，还是当前已有发布状态对应的发布时间。
- [ ] 未发布或无发布时间的 SKU 应展示空值、`-`，还是隐藏该列值。
- [ ] 列表排序、筛选和导出是否需要同步支持发布时间。
- [ ] 移动端或窄屏管理端布局下该列是否参与列隐藏/横向滚动策略。

# 探索结论

（/req-explore 后人工确认写入）
