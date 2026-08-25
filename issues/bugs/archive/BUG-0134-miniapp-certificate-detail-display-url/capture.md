---
bug_id: BUG-0134-miniapp-certificate-detail-display-url
status: done
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-24 17:15:12
severity_hint: high
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0112-certificate-image-object-key-prefix
lifecycle_stage: plan
captured_via: capture
classification_rationale: 证书详情页顶部展示属于既有证书展示能力；用户要求新增或返回 `display_url`，并明确“详情展示不要直接退原图”，说明当前详情展示 URL 选择不符合媒体多规格展示策略，属于已交付能力偏差，因此分类为 BUG。
---

# 现象

小程序证书详情页顶部展示缺少可直接消费的 `display_url`，详情展示在缺少合适展示图字段时可能直接回退到证书原图。

# 复现步骤

1. 打开包含图片证书的小程序证书详情页。
2. 查看证书详情接口返回字段，确认是否存在 `display_url`。
3. 检查详情页顶部展示使用的图片 URL。
4. 在 Network 面板观察顶部证书图是否请求原图资源。

# 期望 vs 实际

- 期望：证书详情接口新增或返回 `display_url`，顶部展示优先使用展示图 URL；缺展示图时也不应无条件退回原图。
- 实际：证书详情顶部展示缺少 `display_url` 消费入口，存在直接使用原图展示的风险。

# 影响范围

- 微信小程序证书详情页顶部图片展示。
- 证书详情 API 返回结构。
- 证书图片展示图、缩略图、原图的选择策略。
- 证书原图访问流量与详情页加载性能。

# 初步线索

- 需复核证书详情接口是否只暴露 `file_url` 或原始文件 URL，未返回独立展示图字段。
- 需明确图片证书与 PDF/文档证书的展示策略差异。
- 需确认 `display_url` 的来源优先级与媒体多规格生成结果一致。

# 建议验收或复现要点

- [ ] 证书详情接口返回可用于详情顶部展示的 `display_url`。
- [ ] 证书详情页顶部展示优先使用 `display_url`。
- [ ] `display_url` 缺失时不直接退回大体积原图，需采用受控展示策略或占位。
- [ ] 图片证书、PDF/文档证书均有明确展示行为。
- [ ] Network 证据显示普通详情展示不请求证书原图大文件。

# 附件

- 暂无。
