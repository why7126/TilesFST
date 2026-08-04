## 设计目标

本变更将 REQ-0095 的管理端列表字段展示检查表沉淀到 `design-system` 能力，目标是为后续管理端列表页新增、重构或回归验收提供统一口径，而不是在本阶段直接重写所有列表页面。

## 需求来源

- REQ：`issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/`
- PRD：`issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/requirement.md`
- 验收：`issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/acceptance.md`
- 原型策略：`issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/prototype/web/context.md`
- HTML 参考：`issues/requirements/archive/REQ-0095-admin-list-field-display-adapter-checklist/prototype/web/admin-list-field-adapter-checklist.html`

## 知识库引用

后续 `/opsx-apply` 与验收必须引用以下知识库条目：

- `docs/knowledge-base/best-practices/admin-list-page-consistency.md`
- `docs/knowledge-base/retrospectives/sprint-018-retrospective.md`

横切标签：

```yaml
cross_cutting_tags:
  - admin-list
```

## 冲突处理

优先级按 `HTML > PNG > context.md > acceptance.md > rules/ui-design.md > openspec/specs` 执行。

| 来源 | 结论 |
|---|---|
| HTML prototype | 作为检查表工作台形态参考，表达信息结构和高密度管理端风格；不要求直接作为生产页面。 |
| PNG | 当前无 PNG Golden Reference；不阻塞本 Change。 |
| context.md | 明确 prototype 是策略参考，不是最终产品页面承诺。 |
| acceptance.md | 作为验收事实源，必须覆盖功能 AC 与 `admin-list` 横切 AC。 |
| rules/ui-design.md | 管理端列表必须遵守暗色旗舰风、semantic token、列表效率优先。 |
| openspec/specs/design-system/spec.md | 作为本次 delta spec 的修改目标。 |

## Adapter 检查表结构

检查表应按以下结构组织：

| 字段 | 说明 |
|---|---|
| 列表 | 品牌、证书、SKU、Banner 等管理端列表。 |
| Adapter | `image`、`name`、`fallback`。 |
| 检查项 | 可测试的单项规则，例如缩略图优先、长名称截断、未知枚举兜底。 |
| 期望表现 | 用户可观察的结果，例如行高稳定、文案明确、不泄露敏感信息。 |
| 验证方式 | 自动测试、人工样例、源码检查或 N/A 理由。 |
| 状态 | 必选、推荐、N/A、待治理。 |

## 首批列表口径

| 列表 | image adapter | name adapter | fallback adapter |
|---|---|---|---|
| 品牌列表 | Logo、缩略图、首字母兜底 | 品牌名称 | 无 Logo、名称异常、未知状态 |
| 证书列表 | 证书图片、缩略图、PDF 或文件类型标识 | 证书名、编号、发证机构 | 未设置有效期、无证书图片、文件缺失 |
| SKU 列表 | 主图、图片集合第一张、缺主图 | SKU 名称、品牌、分类 | 素材缺失、未知状态、时间为空 |
| Banner 列表 | Banner 图、SKU 主图、品牌 Logo、自定义上传图 | Banner 标题、展示位置、跳转目标 | 未设置时间、无跳转、关联对象缺失 |

## UI Explore Gate 决策

本需求影响管理端 Web 且存在 prototype。策略选择：`tailwind-ds` / Design System 治理优先。

原因：

- 本 Change 的核心是检查表与设计系统规范，不是从 HTML 原型直接 CSS Port 一个业务页面。
- 原型表达工作台结构，后续如果产品决定做可视化检查页，应复用管理端列表模板与 semantic token。
- 若只落文档/检查表，则不需要新增运行时页面或截图。

## 实现边界

- 不写业务源码作为本命令的一部分。
- `/opsx-apply` 阶段可选择补充长期文档、Design System 文档、测试模板或代表性验收说明。
- 若后续实现触及具体列表页面，应优先复用现有管理端列表模板、shared UI 和 display helper。
- 若后续抽公共 adapter 函数或组件，应单独说明 API 形态、输入输出、迁移范围和测试策略。

## 验证策略

- OpenSpec delta spec 通过 `openspec validate`。
- 文档语言通过 `python scripts/validate-openspec-language.py`。
- 若 `/opsx-apply` 仅更新文档和规范，测试可使用文档/校验脚本作为证据。
- 若 `/opsx-apply` 改动 Web 代码，必须补充 Vitest/Testing Library 或代表页面 DOM smoke，覆盖 `acceptance.md` 的功能 AC 与 AC-XCUT。
