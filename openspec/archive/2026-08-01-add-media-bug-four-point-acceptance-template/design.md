## Context

REQ-0091 已完成 `/req-review --approve`，物理路径位于 `issues/requirements/archive/REQ-0091-media-bug-four-point-acceptance-template/`。该需求来源于 Sprint 015/016 媒体链路复盘：媒体类缺陷不能只验证对象存在或页面展示，需要同时覆盖对象 key、对象存储、受控 URL 和端侧渲染。

当前 `object-storage` capability 已定义 MinIO 单桶策略、对象 Key 前缀、媒体受控读取、真实缩略图生成和历史审计要求。本 Change 不改变运行时代码能力，而是在该 capability 下新增媒体类 BUG 四联验收契约，指导后续 BUG 修复、Sprint 验收和 Release 检查。

## Goals / Non-Goals

**Goals:**

- 建立媒体类 BUG 四联验收模板的 OpenSpec 契约。
- 明确四联维度：`key`、`object`、`URL`、`render`。
- 明确证据状态：`pass`、`fail`、`n/a`、`blocked`。
- 明确知识库横切要求：上传状态机、同会话即时回显、Docker Web `:3000` 边界文件、受控媒体 URL 一致性、小程序 evidence。
- 为后续 `/opsx-apply` 指定文档落点和验证边界。

**Non-Goals:**

- 不新增媒体上传接口、对象存储 provider、Bucket、签名 URL 策略、缩略图生成能力或视频转码能力。
- 不新增 Web 管理端、店主 Web 或微信小程序页面。
- 不直接实现自动化审计脚本；如后续需要，应在实现任务中单独说明测试和 CI 边界。
- 不替代 `/bug-capture`、`/bug-complete`、`/bug-review` 等 BUG 生命周期。

## Decisions

### D1. 修改 `object-storage` capability，而不是新增独立 capability

媒体类 BUG 四联验收直接约束对象 key、对象存储、受控媒体 URL 和端侧读取边界，现有 `object-storage` spec 已承载这些事实源。因此本 Change 使用 `MODIFIED object-storage`，新增一个验收治理 Requirement。

备选方案是新增 `media-bug-acceptance` capability。该方案会让验收模板脱离对象存储事实源，后续归档后更容易和 key/URL/MinIO 规则分叉，因此不采用。

### D2. 模板先以 Markdown 治理文档落地

REQ-0091 要求的是模板与治理闭环，而非运行时代码。`/opsx-apply` 应优先将模板沉淀到长期规则或标准文档，并在 BUG acceptance 使用方式中给出可复制结构。

候选落点：

- `rules/media.md`
- `rules/object-storage.md`
- `docs/standards/*`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- BUG `acceptance.md` 模板或相关技能说明

最终落点由 apply 阶段结合现有文档职责确认，并记录“不适用”的候选落点原因。

### D3. 不做 UI Explore

本需求 `impact.web=false`，且 REQ 目录无 `prototype/`。如未来在管理端或发布工具展示该模板，需另行通过 OpenSpec Change 或本 Change apply 阶段明确 UI 变更，并遵守 `rules/ui-design.md` semantic token、紧凑表格/检查清单和媒体上传 best practice。

## Conflict Resolution

无 prototype 冲突。优先级链路结论：

```text
HTML: N/A
PNG: N/A
context.md: N/A
acceptance.md: 使用 REQ-0091 acceptance.md 作为主要验收输入
ui-design.md: 仅作为未来 UI 展示约束
openspec/specs: 修改 object-storage capability
```

## Knowledge-base References

- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `docs/knowledge-base/retrospectives/sprint-015-retrospective.md`
- `docs/knowledge-base/retrospectives/sprint-016-retrospective.md`

后续 `/opsx-apply` 的实现记录必须说明这些引用如何转化为模板 AC，尤其是上传状态机、同会话即时回显、Docker Web `:3000` 边界文件、`object_key` 与受控媒体 URL 一致性、小程序 DevTools/真机/体验版 evidence。

## Risks / Trade-offs

- [Risk] 模板过重，导致每个媒体 BUG 验收成本过高 → Mitigation: 四联模板必须允许 `n/a` 和 `blocked`，并要求写明原因，不强制所有媒体 BUG 都跑无关端。
- [Risk] 团队只复制模板但不补证据 → Mitigation: delta spec 要求每个维度有状态、证据和失败/阻塞处理。
- [Risk] 与 REQ-0090 媒体五联模板重复 → Mitigation: 本 Change 明确聚焦 BUG 修复闭环；缩略图收益仅在原 BUG 涉及时纳入 object/URL/render 证据。
- [Risk] 小程序真机 evidence 难以及时补齐 → Mitigation: 允许标记 `blocked` 或发布前补证，但不得将缺失 evidence 写作通过。

## Migration Plan

1. 在 apply 阶段选择最终文档落点，并加入媒体类 BUG 四联验收模板。
2. 如修改 rules/docs，更新对应 `updated_at`，并保持中文优先。
3. 如更新技能或模板，运行相关静态校验或 Workflow Sync 检查。
4. 不需要数据库迁移、API 迁移、Orval 生成或 Docker Compose 启动验证，除非 apply 阶段引入自动化脚本或 UI。

## Open Questions

- 四联模板最终主落点选择 `rules/media.md`、`rules/object-storage.md`、`docs/standards` 还是 BUG acceptance 模板，需要 apply 阶段根据文档职责确认。
- 是否与 REQ-0090 的媒体五联模板合并为一个长期模板族，需要在两个 Change 的 apply 或 archive 前保持互相引用。
