---
req_id: REQ-0055-brand-certificate-common-component
status: done
created_at: 2026-07-19 17:37:58
updated_at: 2026-07-19 19:54:43
recorded_by: product
source: 反馈
priority_hint: P1
parent_requirement: REQ-0038-brand-certificate-management
---

# 生成品牌证书通用组件

为品牌证书场景沉淀可复用通用组件，统一证书列表、证书图片/文件展示、状态提示、空态和预览入口等基础交互，减少管理端或展示端后续页面重复实现。

# 原始描述

生成品牌证书通用组件

# 待澄清

- [ ] 组件优先服务管理端品牌证书管理页、店主 Web 展示端、小程序展示端，还是需要跨端分别沉淀同名能力。
- [ ] 证书数据来源是否复用现有品牌证书接口与媒体字段，是否需要新增 API 字段或聚合接口。
- [ ] 证书文件类型范围是否仅图片，还是需要兼容 PDF、外链、过期证书与多文件证书组。
- [ ] 组件应包含哪些标准状态：加载、空态、上传中、审核/启停、过期提醒、预览失败、无权限等。
- [ ] 是否需要在 Design System 或业务组件目录中沉淀组件契约、示例页和视觉验收标准。

# 探索结论

（/req-explore 后人工确认写入）
