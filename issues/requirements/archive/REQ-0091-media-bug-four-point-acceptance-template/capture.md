---
req_id: REQ-0091-media-bug-four-point-acceptance-template
status: done
created_at: 2026-08-01 09:48:06
updated_at: 2026-08-01 11:14:55
recorded_by: product
source: 用户输入
priority_hint: P1
parent_requirement:
---

# 媒体类 BUG 四联验收模板

建立媒体类 BUG 修复后的四联验收模板，用于在缺陷修复、回归与发布前统一检查媒体 key、object、URL 与端侧 render 是否闭环。

# 原始描述

媒体类 BUG 四联验收模板

# 待澄清

- [ ] 四联验收是否固定为 key、object、URL、render，还是需要按媒体类型扩展为图片、视频、证书图片、品牌 Logo 等差异化检查项？
- [ ] 该模板是否用于 BUG 修复验收报告、回归测试清单、发布前检查，还是三者组合？
- [ ] render 验收是否必须同时覆盖 Web 管理端、店主 Web 展示端和微信小程序端？
- [ ] 是否需要为每次媒体类 BUG 验收强制记录请求 ID、对象 key、访问 URL、截图或日志证据？
- [ ] 是否需要与现有媒体五联验收模板建立父子关系或复用公共检查项？

# 建议验收要点

- [ ] key：BUG 修复后业务记录中的媒体 key 稳定可追溯，符合 MinIO 单桶前缀策略，不使用用户原始文件名或本机路径。
- [ ] object：对象存储中的真实 object 存在且与业务记录一致，MIME、大小、权限和生命周期符合媒体安全规则。
- [ ] URL：接口返回、前端使用或签名生成的 URL 可访问，过期、缺失、权限不足等失败态有明确错误信息。
- [ ] render：受影响端可正确渲染媒体及失败态，微信小程序端不依赖 Web 浏览器专属能力，回归覆盖原 BUG 场景。

# 探索结论

（/req-explore 后人工确认写入）
