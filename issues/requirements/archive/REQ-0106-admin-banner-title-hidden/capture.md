---
req_id: REQ-0106-admin-banner-title-hidden
status: archived
created_at: 2026-08-10 22:27:41
updated_at: 2026-08-11 23:17:14
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement:
---

# 一句话

Web 管理后台 Banner 标题改为非运营必填信息并直接隐藏该字段，同时移除小程序 Banner 前台标题遮罩展示。

# 原始描述

用户反馈 Web 管理后台 Banner 标题是个多余信息，没有什么用；确认希望将 Banner 标题改为非运营必填信息，同时直接隐藏该字段，并移除小程序 Banner 前台标题遮罩展示。

# 待澄清

- [ ] 隐藏标题后，后台 Banner 列表使用图片、展示位置、跳转目标、排序还是自动生成识别名作为主要识别信息。
- [ ] 后端 `title` 字段短期是否保留兼容并由前端或后端自动生成，还是进入字段语义迁移。
- [ ] 小程序首页与品牌列表页是否同时移除标题、描述和按钮遮罩，还是仅移除标题文字。

# 探索结论

（/req-explore 后人工确认写入）
