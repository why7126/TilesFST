## Context

`REQ-0053-miniapp-custom-navigation-best-practice` 已评审通过并纳入 `sprint-009`。它是 `REQ-0048-miniapp-global-custom-navigation-bar` 的治理型 refinement，目标不是再交付一个导航组件，而是把已交付导航能力中的状态栏、胶囊避让、返回兜底、页面 offset 和截图验收矩阵沉淀成长期 best-practice。

当前相关事实源：

- `openspec/specs/miniapp-global-custom-navigation-bar/spec.md` 已定义自定义导航栏、返回、胶囊避让和 fixed header 内容避让能力。
- `openspec/specs/miniapp-device-evidence-template/spec.md` 已定义 DevTools、真机、自动化、N/A、blocked 与 follow_up 的 evidence 口径。
- `docs/knowledge-base/retrospectives/sprint-008-retrospective.md` 已记录固定导航遮挡风险、设备验收残留和自动化边界。
- `issues/requirements/archive/REQ-0053-miniapp-custom-navigation-best-practice/prototype/miniapp/` 是信息架构原型，不是小程序页面视觉稿。

## Goals / Non-Goals

**Goals:**

- 新增一份可复用的小程序自定义导航 best-practice 文档。
- 让 best-practice 明确页面接入 checklist、截图验收矩阵、evidence 引用和 N/A / blocked / follow_up 规则。
- 在 spec 层扩展 `miniapp-global-custom-navigation-bar` 的治理要求，确保后续导航相关 Change 引用该实践。
- 保持 REQ-0053、Sprint、OpenSpec trace 与 knowledge-base 引用一致。

**Non-Goals:**

- 不修改 `src/miniapp/components/custom-navigation/` 或任何小程序页面源码。
- 不新增小程序业务页面、后台配置能力、自动化截图工具链或真机云测能力。
- 不回填全部历史截图或设备 evidence。
- 不修改 API、数据库、Orval、Docker Compose、MinIO 或对象存储策略。

## Decisions

### D1. 文档位置选择 knowledge-base best-practices

将主交付文档放在：

```text
docs/knowledge-base/best-practices/miniapp-custom-navigation.md
```

原因：

- 本需求来自已交付能力和 Sprint 复盘行动项，性质是跨 Sprint 可复用经验。
- 它不替代正式 OpenSpec spec；OpenSpec 只规定必须存在和被引用。
- 与 `docs/knowledge-base/README.md` 中 best-practices 目录职责一致。

替代方案：

- 放在 `docs/standards/`：更适合强制流程标准，但当前内容更偏页面接入经验和验收矩阵，可在后续治理升级时迁移或双向引用。
- 放在 REQ 文档包内：会导致后续 Change 难以复用，且不符合长期知识沉淀目标。

### D2. Spec 采用 MODIFIED 而非新增 capability

本 Change 修改 `miniapp-global-custom-navigation-bar`，新增 “自定义导航 best-practice 与截图矩阵” 要求。

原因：

- best-practice 直接服务自定义导航能力，不是独立运行时能力。
- 现有 spec 已覆盖状态栏、胶囊、返回和 fixed header，本 Change 是对其治理和验收引用的补强。

### D3. 复用 REQ-0052 evidence 模板，不重复定义完整 evidence

best-practice 文档只定义导航场景下的矩阵维度和结论，不复制完整 `miniapp_device_evidence` 模板。

原因：

- 避免两个文档各自维护 `passed`、`failed`、`blocked`、`not_applicable`、`follow_up` 语义。
- Sprint 验收报告和 release note 只需要摘要，完整设备证据仍引用 REQ-0052 的模板。

### D4. 原型冲突处理

REQ-0053 的 `prototype/miniapp/prototype.html` 只是信息架构原型。

Conflict Resolution：

- HTML 原型用于确认 best-practice 文档结构、接入 checklist 和截图矩阵章节。
- 该原型不得被解释为新的小程序页面视觉稿，不要求转换为 WXML/WXSS。
- 若 acceptance 与 prototype 表达冲突，以 `acceptance.md` 的可测试 AC 和本 design 的 Non-Goals 为准。

## Risks / Trade-offs

- best-practice 过于抽象 → tasks 要求文档包含 checklist、矩阵、引用示例和 N/A / blocked / follow_up 规则。
- DevTools 结论被误认为真机通过 → 文档必须引用 `miniapp_device_evidence`，并明确 DevTools 与真机分层。
- 后续实现者顺手重构导航组件 → proposal、tasks 和 acceptance 均声明不改源码；若确需改源码，必须另行扩展 Change 范围。
- 历史截图回填扩大范围 → 文档允许引用历史案例，但本 Change 不回填全部历史 evidence。

## Migration Plan

1. 新增 best-practice 文档。
2. 更新知识库 README 索引。
3. 补充轻量校验，确认文档存在、关键章节存在且不包含本机绝对路径或敏感字段示例。
4. 更新 trace / Sprint 派生状态。
5. 后续小程序导航相关 Change 在 design/tasks/acceptance 中引用该文档。

Rollback：若 best-practice 需要撤回，移除文档与知识库索引，保留 OpenSpec Change trace 说明撤回原因；不涉及运行时代码回滚。

## Open Questions

- 后续是否将该 best-practice 升级到 `docs/standards/`，作为小程序开发强制标准？本 Change 暂不处理。
