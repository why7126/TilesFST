---
bug_id: BUG-0079-admin-dashboard-overview-mock-data
title: 管理端首页数据概览仍使用 Mock 数据
status: done
created_at: 2026-07-22 08:21:05
updated_at: 2026-07-22 09:27:20
severity_hint: medium
environment: admin
source: 用户反馈
source_command: /capture
captured_via: capture
classification_rationale: 管理端首页数据概览属于已有展示能力，当前仍使用 Mock 数据而非真实业务数据，属于已交付能力与实际数据源接入预期不一致的缺陷。
related_requirement:
related_bug:
---

# 现象

admin 管理端首页的数据概览仍展示 Mock 数据，未接入真实业务数据。

# 复现步骤

1. 登录 admin 管理端。
2. 进入首页 / 数据概览区域。
3. 对比页面展示的概览指标与后端真实业务数据、数据库记录或管理端其他列表统计。
4. 观察首页数据概览是否仍为固定 Mock 值或与真实数据不一致。

# 期望 vs 实际

期望：首页数据概览展示来自后端接口或真实业务数据聚合的指标，并能随数据变化更新。

实际：首页数据概览仍使用 Mock 数据，无法反映当前系统真实业务状态。

# 附件

- 用户原始反馈：`admin管理端 首页的数据概览用的还是Mock数据，需要调整为真实数据`
- 暂无截图、具体指标清单、接口路径与当前 Mock 数据位置；后续 `/bug-explore` 阶段需补充。
