---
req_id: REQ-0062-admin-banner-placement-scope
status: done
created_at: 2026-07-20 13:23:12
updated_at: 2026-07-20 23:08:34
recorded_by: product
source: 用户反馈
priority_hint: P1
parent_requirement: REQ-0016-banner-management
captured_via: capture
classification_rationale: 用户描述的是管理后台 Banner 配置项优化，要求收敛展示端与展示位置枚举，属于对已交付 Banner 管理能力的新增/调整需求，而非明确现有行为偏差。
---

# 一句话

优化管理后台 Banner 配置范围：展示端仅保留“小程序”，展示位置提供“首页轮播”和“品牌列表页轮播”两项。

# 原始描述

管理后台优化
Banner展示端，只有一项：小程序
展示位置，有两项：首页轮播、品牌列表页轮播

# 背景与关联

- 父需求：`REQ-0016-banner-management`
- 关联需求：`REQ-0060-brand-list-page`
- 涉及端：Web 管理端、微信小程序
- 业务价值：让运营在 Banner 管理中明确配置小程序首页与品牌列表页轮播，避免展示端和展示位置选项过宽或与当前小程序展示范围不一致。
- 拆分判断：展示端选项与展示位置选项都属于 Banner 表单/筛选配置的同一管理后台优化闭环，后续可在同一 PRD 与 OpenSpec Change 中展开验收。

# 待澄清

- [ ] 是否需要迁移或兼容已有非“小程序”展示端 Banner 数据。
- [ ] 现有首页轮播枚举是否直接映射为“首页轮播”，品牌列表页轮播是否需要新增后端枚举值。
- [ ] Banner 列表筛选、表格展示、创建/编辑弹窗是否都同步限制为上述展示端和展示位置。
- [ ] 小程序首页与品牌列表页获取 Banner 数据时是否需要新增或调整公开接口查询参数。
- [ ] 是否需要保留历史位置文案或做一次性数据清理。

# 探索结论

（/req-explore 后人工确认写入）

# 分类说明（/capture）

该条目描述管理后台 Banner 展示端与展示位置的可配置范围优化，当前没有明确指出已交付功能偏离既定验收，因此判定为 REQ。
