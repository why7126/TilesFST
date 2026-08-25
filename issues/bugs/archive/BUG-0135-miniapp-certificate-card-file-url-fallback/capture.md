---
bug_id: BUG-0135-miniapp-certificate-card-file-url-fallback
status: done
created_at: 2026-08-22 20:38:13
updated_at: 2026-08-22 21:59:33
severity_hint: medium
environment: wechat-miniapp
related_requirement: REQ-0115-media-multi-variant-images
related_bug: BUG-0112-certificate-image-object-key-prefix
lifecycle_stage: plan
captured_via: capture
classification_rationale: 证书卡片列表展示属于既有证书展示能力；用户明确指出缺缩略图时应优先占位而不是拉取 `file_url` 原文件，说明当前 fallback 策略会违反缩略图优先和原文件受控加载预期，因此分类为 BUG。
---

# 现象

小程序证书卡在缺少缩略图时可能直接 fallback 到 `file_url` 原文件，导致卡片列表或摘要场景加载证书原图或原始文件。

# 复现步骤

1. 准备一条缺少证书缩略图但存在 `file_url` 的证书数据。
2. 打开展示该证书的卡片列表或详情关联卡片。
3. 检查卡片图片来源字段。
4. 在 Network 面板观察是否直接请求 `file_url` 原文件。

# 期望 vs 实际

- 期望：证书卡缺少缩略图时优先展示占位图或受控占位状态，不直接请求 `file_url` 原文件。
- 实际：证书卡 fallback 可能直接拉取 `file_url` 原文件，造成卡片展示场景加载成本过高。

# 影响范围

- 微信小程序证书卡片展示。
- 证书列表、品牌证书摘要、商品详情关联证书等卡片消费场景。
- 证书缩略图缺失时的占位和降级策略。
- 对象存储流量、移动端弱网体验和原文件访问控制边界。

# 初步线索

- 需复核证书卡组件的图片字段优先级。
- 需确认缺 `thumbnail_url` 或展示图字段时是否存在默认 `file_url` fallback。
- 需与证书详情页 `display_url` 策略区分：卡片场景更适合缩略图或占位，不应拉原文件。

# 建议验收或复现要点

- [ ] 证书卡有缩略图时使用缩略图展示。
- [ ] 证书卡缺缩略图时展示占位，不请求 `file_url` 原文件。
- [ ] 图片证书、PDF/文档证书、无预览资源证书均有明确占位状态。
- [ ] Network 证据显示卡片展示场景不会因 fallback 触发原文件下载。
- [ ] 回归证书详情顶部展示，确认详情展示策略与卡片 fallback 策略互不冲突。

# 附件

- 暂无。
