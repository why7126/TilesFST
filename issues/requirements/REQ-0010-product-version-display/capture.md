---
req_id: REQ-0010-product-version-display
status: captured
created_at: 2026-06-27 09:06:02
updated_at: 2026-06-27 09:06:02
recorded_by: product
source: 反馈
priority_hint: P2
parent_requirement:
---

# 一句话

前端展示产品版本号，版本号由人工维护与更新（非 CI/构建自动递增）。

# 原始描述

前端新增产品版本号显示，产品版本号由人工决定更新。

# 待澄清

- [ ] 展示范围：管理端、店主端，或全 Web 端统一展示？
- [ ] 展示位置：页脚、关于页、登录页、侧边栏底部等？
- [ ] 版本号格式与命名规则（如 `v1.2.0`、`2026.06`）？
- [ ] 维护方式：单一常量文件、环境变量、还是 `package.json` 人工同步？
- [ ] 是否需与后端/API 版本区分展示？
- [ ] 小程序是否纳入本期范围？

# 探索结论

（/req-explore 后人工确认写入）
