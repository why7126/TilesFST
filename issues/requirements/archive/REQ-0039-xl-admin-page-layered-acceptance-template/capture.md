---
req_id: REQ-0039-xl-admin-page-layered-acceptance-template
status: done
created_at: 2026-07-16 08:58:07
updated_at: 2026-07-16 09:37:04
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement:
---

# XL 管理端页面分层验收模板

沉淀一套面向 XL 管理端页面的分层验收模板，用于后续管理端页面需求或变更在开发前后统一检查 DB、API、上传、Orval、Web、Docker 与横切 UI gate。

# 原始描述

沉淀 XL 管理端页面分层验收模板，覆盖 DB/API/上传/Orval/Web/Docker/横切 UI gate。

# 待澄清

- [ ] “XL 管理端页面”是否指特定大型管理页类型，还是所有复杂管理端页面的验收模板。
- [ ] 模板最终沉淀位置：`docs/standards/`、`rules/`，还是作为 OpenSpec/REQ/验收报告模板的一部分。
- [ ] 各层 gate 是否需要绑定固定命令，例如 OpenAPI/Orval 生成、pytest、Vitest、Docker Compose 验证与 UI semantic token 检查。
- [ ] 上传 gate 是否仅覆盖图片/证书等通用媒体上传，还是也要预留视频/文件增强能力。

# 探索结论

（/req-explore 后人工确认写入）
