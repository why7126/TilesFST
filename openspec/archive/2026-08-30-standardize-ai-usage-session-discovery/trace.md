---
title: AI Usage session 默认发现治理 trace
created_at: 2026-08-30 08:50:35
updated_at: 2026-08-30 08:55:17
status: applied
sprint: sprint-028
---

# Trace

```yaml
change_id: standardize-ai-usage-session-discovery
status: applied
sprint: sprint-028
source: /spec-opt
product_data_collection_observability:
  status: n/a
  affected_layers: []
  reason: 本 Change 仅调整 AI Usage 治理规范、命令技能和脚本提示文案，不新增或修改业务 API、DB、请求日志、行为事件、Task Trace、Web/小程序/App 请求封装。
  validation: N/A；无产品数据采集链路变更。
```

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-30 08:55:17 | /spec-opt | 已同步治理 Skill、规则、AI Usage 脚本文案、测试、治理日志和 OpenSpec delta。 |
| 2026-08-30 08:50:35 | /spec-opt | 创建治理 Change，准备同步 AI Usage 默认 session 发现规范。 |
