---
req_id: REQ-0090-media-five-point-acceptance-template
status: done
created_at: 2026-08-01 09:46:23
updated_at: 2026-08-01 11:38:21
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement:
---

# 媒体五联验收模板

建立媒体链路五联验收模板，用于在媒体相关能力交付、回归或发布前统一检查 key、object、URL、thumbnail benefit 与 miniapp render。

# 原始描述

媒体五联验收模板，覆盖 key、object、URL、thumbnail benefit、miniapp render

# 待澄清

- [ ] 该模板适用于所有媒体类型，还是优先覆盖图片、视频、证书图片、品牌 Logo 等已有媒体能力？
- [ ] 五联验收的输出形式是 Markdown 模板、自动化测试清单、发布检查项，还是三者组合？
- [ ] `thumbnail benefit` 的验收表达是否需要量化，例如列表首屏加载、带宽节省、弱网体验或后台预览效率？
- [ ] `miniapp render` 是否要求覆盖真机预览、开发者工具和生产域名资源加载三种场景？
- [ ] 是否需要将该模板接入 release / sprint acceptance report 的固定检查项？

# 建议验收要点

- [ ] key：媒体对象 key 命名稳定、不可使用用户原始文件名、符合 MinIO 单桶前缀策略，并能从业务记录追溯到对象存储位置。
- [ ] object：对象存储中真实 object 存在，MIME、大小、权限和生命周期符合媒体安全规则。
- [ ] URL：前后端返回或渲染的 URL 可访问，签名/公开策略符合安全边界，错误时返回可诊断信息。
- [ ] thumbnail benefit：缩略图在列表、卡片或预览场景中带来明确体验收益，并与原图/视频封面关系可追溯。
- [ ] miniapp render：微信小程序端可正确渲染媒体、缩略图和失败态，不依赖 Web 浏览器专属能力。

# 探索结论

（/req-explore 后人工确认写入）
