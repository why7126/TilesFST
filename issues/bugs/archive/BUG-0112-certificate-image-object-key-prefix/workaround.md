---
bug_id: BUG-0112-certificate-image-object-key-prefix
title: 证书图片对象 key 未归入 images 前缀临时规避
workaround_status: drafted
created_at: 2026-08-04 08:20:26
updated_at: 2026-08-04 08:20:26
---

# BUG-0112 临时规避

## 当前结论

无稳定的产品侧临时规避方案。该问题属于对象 key 规范与数据治理偏差，不能通过前端展示层隐藏或手工拼接 URL 解决。

## 可采取的临时措施

- 暂停把新上传的图片类证书作为对象存储规范验收通过证据，直到修复 Change 明确图片证书前缀。
- 对新增证书图片执行人工抽查，重点检查 `brand_certificate_images.file_key` 与 `thumbnail_key` 是否位于 `images/` 前缀。
- 避免手工迁移对象 key 或直接修改数据库引用；对象迁移必须通过后续受控脚本执行 dry-run、apply 和幂等复核。
- PDF 等文档类证书继续使用 `files/` 前缀，不应为了规避本 BUG 混入 `images/`。

## 风险

人工抽查只能降低新增偏差概率，不能修复历史对象，也不能阻止脚本继续生成旧前缀。正式修复仍需要 OpenSpec Change 覆盖实现、规范、脚本和测试。
