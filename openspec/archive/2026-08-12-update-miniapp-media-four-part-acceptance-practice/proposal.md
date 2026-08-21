## 背景

BUG-0125 与 BUG-0126 证明，小程序媒体性能验收不能只确认 `object_key`、对象存在或 `.thumb` URL 存在。团队需要把 key、object、URL、render 四联证据、小程序 Network evidence、历史对象审计和测试 helper 形成可复用治理能力，避免后续媒体需求与缺陷重复遗漏真实端侧加载和渲染证据。

## 变更内容

- 沉淀小程序媒体四联验收最佳实践到 `docs/knowledge-base`，以 BUG-0125、BUG-0126 为案例说明“对象存在不等于性能验收通过”。
- 扩展媒体四联 / 五联验收口径，要求小程序媒体场景记录 key、object、URL、render 四联最小证据集。
- 扩展小程序 Network evidence 规则，明确 DevTools Network、体验版 Network、真机 evidence 与自动化测试的边界。
- 扩展对象存储审计口径，定义历史媒体对象 dry-run 审计、脱敏统计、fallback 风险和 apply 回填门禁。
- 增加测试 helper 治理要求，用于复用缩略图 URL、preview URL、视频 poster、fallback、lazy-load 和受控 `/media` URL 断言。
- 不新增上传、缩略图生成、视频转码、CDN、缓存、对象存储 provider 或自动真机云测能力。

## 能力范围

### 新增能力

无。

### 修改能力

- `media-acceptance-template`：补充小程序媒体四联最佳实践和验收记录要求。
- `miniapp-device-evidence-template`：补充小程序媒体 Network evidence 最低字段和状态边界。
- `object-storage`：补充历史媒体对象四联审计 helper、脱敏输出与回填策略门禁。
- `testing`：补充小程序媒体测试 helper 与回归断言要求。

## 影响

- 文档：新增 `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`，按需更新 `docs/knowledge-base/README.md`。
- 规范：按需更新 `rules/media.md`、`rules/object-storage.md`、`docs/standards/media-bug-four-point-acceptance-template.md`、`docs/standards/media-five-point-acceptance-template.md`、`docs/standards/miniapp-device-evidence-template.md`。
- 测试：新增或复用测试 helper，覆盖小程序媒体 URL、缩略图、预览、视频 poster、fallback、lazy-load 与受控 URL 语义。
- 后端 / 存储：可新增只读审计 helper；默认 dry-run，不默认写 DB 或对象存储。
- API / DB / Orval：默认不变；若实现阶段发现需要新增运行时 API 或 DB 字段，必须拆出或扩展设计并同步 OpenAPI / Orval / 数据库文档。
