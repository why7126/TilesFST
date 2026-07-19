## Context

REQ-0039 已通过评审，目标是将 Sprint 007 复盘中的行动项 A-003 产品化：为 XL 管理端页面沉淀分层验收模板。现有项目已经有多份相关但分散的资料：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-form-page-consistency.md`
- `docs/knowledge-base/best-practices/admin-modal-width-css-cascade.md`
- `docs/knowledge-base/best-practices/admin-media-upload-chain.md`
- `openspec/specs/brand-certificate-management/spec.md` 中的品牌证书横切 UI 验收
- `issues/requirements/archive/REQ-0039-xl-admin-page-layered-acceptance-template/acceptance.md`

当前缺口不是单个页面功能，而是后续复杂管理端页面缺少统一模板来表达 DB/API/上传/Orval/Web/Docker/UI gate 的 required/N/A、证据和剩余风险。

## Goals / Non-Goals

**Goals:**

- 新增 `xl-admin-page-acceptance-template` OpenSpec 能力。
- 在长期标准文档或等价模板中沉淀可复制的 gate 矩阵。
- 明确后续复杂管理端页面如何记录 gate status、owner、evidence、N/A reason 和 remaining risk。
- 让后续 Change design 能引用 REQ trace 中的 `knowledge_base_refs` 并说明落实或 N/A。

**Non-Goals:**

- 不新增或修改具体管理端业务页面。
- 不修改 DB schema、API、上传接口、Orval 生成物、Docker Compose 或 Web 源码。
- 不在本 Change 中强制改造 `/req-complete` 等技能自动套用模板；如需自动化，只在 tasks 中作为显式实现项评估。
- 不导出 PNG Golden Reference；REQ prototype HTML 和 context 作为模板结构参考即可。

## Decisions

### D1. 新增独立 capability，而不是修改单个业务 spec

`brand-certificate-management` 已体现单页横切验收，但 REQ-0039 要沉淀跨页面模板。新增 `xl-admin-page-acceptance-template` 能避免把治理模板混入具体业务页 spec，也便于后续列表页、表单页、上传页等不同页面引用。

### D2. 模板优先沉淀到 `docs/standards/`

长期治理文档按目录规则应放入 `docs/standards/`。实现阶段 SHOULD 新增类似 `docs/standards/xl-admin-page-acceptance-template.md` 的文档，包含七层 gate 表格、N/A 判定和证据模板。若选择其他位置，必须在实现 trace 中说明理由。

### D3. Gate 状态使用统一字段而不是自由文本

每层 gate 使用 `required | not_applicable | passed | failed | blocked`。这样后续验收报告和 Sprint 复盘可以稳定读取状态，同时保留 `evidence`、`na_reason`、`remaining_risk` 做人工解释。

### D4. 横切 UI gate 引用知识库，不复制全文

模板只转化为可测试 AC，不复制 best-practices 全文。后续 Change design MUST 引用 `knowledge_base_refs`，并按 admin-list、admin-form、admin-modal、media-upload 逐项说明落实或 N/A。

## Conflict Resolution

Prototype priority:

```text
1. prototype/web/xl-admin-page-acceptance-template.html
2. prototype/web/xl-admin-page-acceptance-template-context.md
3. acceptance.md
4. requirement.md
5. rules/ui-design.md
6. openspec/specs
```

Conflict report:

| Source | Observation | Resolution |
|---|---|---|
| HTML prototype | 展示七层 gate 和运行态表格，但使用静态 HTML | 作为结构参考，不作为最终 Web 页面实现稿 |
| context.md | 明确 PNG 待导出且非阻塞 | 不将 PNG 作为本 Change 阻断项 |
| acceptance.md | 要求模板优先 `docs/standards/` | 实现阶段按此落文档，除非 design 记录替代位置 |
| ui-design.md | 管理端工作型界面要求 semantic token | 若实现模板预览页或文档 demo，必须避免裸 Hex 进入源码；当前 prototype 是 REQ 文档资产，不进入 Web 源码 |

## Risks / Trade-offs

- [Risk] 模板过重导致轻量页面也被迫执行无关 gate → Mitigation: 每层必须支持 N/A，并要求写明具体原因。
- [Risk] 后续 Change 忘记引用知识库 → Mitigation: spec 明确 design/trace 必须引用 `knowledge_base_refs`。
- [Risk] 技能自动套模板扩大本 Change 范围 → Mitigation: 本 Change 默认只做文档/规范；自动化需要在 tasks 中明确并评估。
- [Risk] 证据记录复制长日志增加上下文成本 → Mitigation: 模板要求摘要证据，禁止复制完整 OpenAPI、Orval 生成物和大段测试日志。

## Migration Plan

1. 新增长期标准文档或等价模板。
2. 在 OpenSpec spec 中新增 `xl-admin-page-acceptance-template` 能力。
3. 更新 REQ trace 与 Change trace，保留知识库引用。
4. 验证 OpenSpec CLI 校验通过。

Rollback：若模板不适合独立能力，可在归档前调整 spec capability 名称或将模板迁移到现有治理 capability；不得直接删除 REQ trace 追溯。

## Open Questions

- 后续是否要让 `/req-complete` 在命中 XL 管理端页面时自动注入该模板，需要单独在实现阶段确认。
- 模板文档最终命名是否使用 `xl-admin-page-acceptance-template.md`，实现阶段可按 docs 命名规范微调。
