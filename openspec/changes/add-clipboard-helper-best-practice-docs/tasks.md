## 1. 文档实现

- [ ] 1.1 新增或更新 Clipboard helper best-practice 文档，优先路径为 `docs/knowledge-base/best-practices/clipboard-fallback.md`。
- [ ] 1.2 文档 frontmatter 包含 `created_at`、`updated_at`、owner、status、update_method 等长期文档元数据。
- [ ] 1.3 文档说明适用范围：Web 管理端 Clipboard helper 调用方，不替代 `REQ-0032` 的 helper 实现要求。
- [ ] 1.4 文档覆盖 `success`、`failed`、`unavailable`、`empty` 四类结果的调用方文案原则。
- [ ] 1.5 文档覆盖 fallback 策略：手动选择文本、禁用/隐藏复制入口、失败提示、fallback 失败兜底。
- [ ] 1.6 文档覆盖敏感值边界：允许复制、谨慎复制、禁止或默认不复制。
- [ ] 1.7 文档提供调用方 checklist、推荐示例与反例，且示例使用脱敏或虚构值。

## 2. 索引与入口

- [ ] 2.1 更新 `docs/knowledge-base/README.md`，将 Clipboard helper best-practice 加入最佳实践索引。
- [ ] 2.2 更新 `src/web/README.md` Clipboard helper 小节，链接到 best-practice 文档或保留明确入口摘要。
- [ ] 2.3 确认文档未放入禁止目录，且不替代 issue / OpenSpec / Sprint 文档事实源。

## 3. 验收

- [ ] 3.1 检查文档不包含真实密钥、真实 Token、真实客户隐私数据、真实生产签名 URL 或可复用敏感凭据。
- [ ] 3.2 对照 `REQ-0036` acceptance AC-001 ~ AC-019 完成验收记录。
- [ ] 3.3 确认本 change 不修改后端 API、数据库、OpenAPI / Orval、小程序复制适配或 Docker Compose 配置。
