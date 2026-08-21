## 上下文

REQ-0111 已纳入 `sprint-023`，目标是把 BUG-0125、BUG-0126 的小程序媒体性能验收教训沉淀为长期治理能力。现有项目已经有媒体五联、媒体 BUG 四联、小程序设备 evidence、对象存储和测试治理能力，本 Change 不需要新建业务模块，而是把“小程序媒体四联怎么落证据”补到现有规范、知识库和 helper 中。

当前痛点有三类：

- `.thumb` URL 存在不代表对象真实轻量，也不代表小程序实际命中缩略图。
- 自动化接口或静态测试不等于 DevTools / 体验版 / 真机 Network 和 render evidence。
- 历史对象审计、fallback、回填和 helper 证据容易分散在 BUG、Change、Sprint 报告中。

## 目标 / 非目标

目标：

- 提供一份小程序媒体四联最佳实践知识库文档。
- 将 key、object、URL、render 四联证据最小集接入媒体和对象存储规范。
- 明确小程序 Network evidence 对媒体资源的字段要求与 blocked / follow-up 处理。
- 提供测试 helper 和审计 helper 的实现边界与验收要求。
- 保持生产安全：审计默认 dry-run，输出脱敏摘要，apply 需要显式确认与备份。

非目标：

- 不新增媒体上传接口、上传 UI、缩略图生成流水线、视频转码、CDN 或对象存储 provider。
- 不重开 BUG-0125、BUG-0126 的修复范围。
- 不新增真机自动化平台。
- 不改变运行时 API、DB 或 Orval 契约，除非实现阶段发现必须拆分为新的 Change。

## 决策

### D1 使用现有 spec 扩展，不新增 `miniapp-media-acceptance` 能力

REQ-0111 是治理增强，已有 `media-acceptance-template`、`miniapp-device-evidence-template`、`object-storage`、`testing` 能覆盖规范边界。新增 spec 会导致模板割裂，后续使用者反而难以判断应该引用哪个能力。

### D2 四联最佳实践落入知识库，规范只保留门禁

知识库文档记录 BUG-0125、BUG-0126 案例、证据链、验收片段和执行建议；`rules/` 与 `docs/standards/` 保留 MUST/SHALL 门禁。这样既能保留可读经验，也不会把案例复盘塞进规范主文档。

### D3 测试 helper 与审计 helper 分层

测试 helper 只服务自动化断言表达，覆盖 URL、preview、poster、fallback、lazy-load 和受控媒体 URL 语义。审计 helper 服务历史对象 dry-run，输出 object、缩略图收益、fallback 风险和脱敏统计。二者都不能替代小程序 render evidence。

### D4 审计默认只读，写入能力显式受控

历史对象回填或重生成属于高风险生产维护动作。helper 默认 dry-run；如需 apply，必须要求显式参数、备份确认、幂等验证、失败重试和脱敏输出。只读审计结果只能证明风险分布，不能证明端侧体验通过。

## 实现落点

| 落点 | 说明 |
|---|---|
| `docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md` | 新增最佳实践，包含 BUG-0125/0126 案例、四联证据链、Network evidence、helper 使用边界。 |
| `docs/knowledge-base/README.md` | 增加最佳实践索引。 |
| `rules/media.md` | 补充小程序媒体四联最佳实践引用和 helper / evidence 门禁摘要。 |
| `rules/object-storage.md` | 补充历史对象审计、fallback、回填和脱敏输出门禁。 |
| `docs/standards/media-bug-four-point-acceptance-template.md` | 增加小程序媒体四联最佳实践引用和可复制字段。 |
| `docs/standards/media-five-point-acceptance-template.md` | 明确通用五联与小程序媒体四联最佳实践的关系。 |
| `docs/standards/miniapp-device-evidence-template.md` | 补充媒体资源 Network evidence 最低字段。 |
| `tests/` 或 `src/backend/tests/` helper | 新增或复用测试 helper；不新增生产 API。 |
| `scripts/` 或后端受控维护入口 | 如新增审计 helper，默认 dry-run，输出脱敏统计。 |

## 风险 / 权衡

- 风险：只写知识库，后续验收仍不引用。缓解：同步更新媒体模板和 tasks，要求后续 Change 引用。
- 风险：审计 helper 被误用于生产写入。缓解：默认 dry-run，apply 必须显式参数和备份确认。
- 风险：测试 helper 被误认为替代真机 evidence。缓解：spec 和文档明确自动化测试不得替代 DevTools / 体验版 / 真机 Network 与 render。
- 风险：实现阶段扩展到运行时 API 或 DB。缓解：本 Change 默认禁止；若必须扩展，先同步设计、OpenAPI、Orval、DB 文档和测试。

## 迁移计划

1. 新增最佳实践文档并更新知识库索引。
2. 更新媒体、对象存储、小程序 evidence 和测试相关规范。
3. 新增测试 helper 和审计 helper 的最小实现或模板化入口。
4. 补充 focused tests / validation，证明 helper 行为、安全脱敏和文档引用存在。
5. 运行 OpenSpec、语言、目录结构和相关测试校验。

## 开放问题

- 审计 helper 首轮是否只做脚本级 dry-run，还是接入后端包内 `app.modules.media.maintenance` 风格入口，由实现阶段根据现有代码结构确定。
- 小程序 Network evidence 是否需要固定 artifact 路径命名，本 Change 先要求仓库相对路径或人工摘要，后续可按发布流程再细化。
