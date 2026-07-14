---
req_id: REQ-0036-clipboard-helper-best-practice-docs
status: done
created_at: 2026-07-11 23:37:42
updated_at: 2026-07-12 00:32:47
recorded_by: product
source: 用户反馈
priority_hint: P2
parent_requirement: REQ-0032-clipboard-copy-helper-best-practice
---

# 一句话

为 Clipboard helper 建立 best-practice 文档，沉淀调用方文案、fallback 策略和敏感值边界。

# 原始描述

为 Clipboard helper 建立 best-practice 文档，沉淀调用方文案、fallback 和敏感值边界。

# 待澄清

- [ ] best-practice 文档应沉淀在 `docs/knowledge-base/best-practices/`、`docs/standards/`，还是设计系统/前端 README 的固定章节。
- [ ] 调用方文案是否需要覆盖成功、失败、权限受限、浏览器不支持、手动复制等全部交互状态。
- [ ] fallback 策略是否仅描述前端降级提示，还是需要定义统一的复制重试、手动选择文本、禁用复制入口等处理分支。
- [ ] 敏感值边界需要覆盖哪些类型，例如 Token、密码、AccessKey、客户隐私数据、内部 URL、对象存储签名 URL。
- [ ] 是否需要补充 lint/checklist 或示例代码，避免后续调用方复制敏感值或写出不一致提示文案。

# 探索结论

（/req-explore 后人工确认写入）
