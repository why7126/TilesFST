## Context

REQ-0084 已在 `issues/requirements/archive/REQ-0084-web-modal-disable-outside-close/` 完成需求评审并批准。现状中部分 Web 弹窗依赖点击遮罩或弹窗外区域关闭，`openspec/specs/web-client/spec.md` 也存在旧规格要求“点击遮罩关闭”的场景，例如品牌启停确认弹窗和 SKU 弹窗滚动修复中的关闭交互。该行为与 REQ-0084 的防误触目标冲突。

本 Change 是 Web 端跨页面交互策略更新，不写源码；后续实现由 `/opsx-apply update-web-modal-disable-outside-close` 执行。

原型与验收优先级：

```text
HTML > PNG > prototype context > acceptance.md > rules/ui-design.md > openspec/specs
```

本需求存在 `prototype/web/modal-disable-outside-close.html` 和 `prototype/web/context.md`，它们仅表达交互策略，不作为最终视觉尺寸、颜色或组件结构来源。若与现有 spec 中“遮罩关闭弹窗”冲突，以 REQ-0084 HTML / context 和 acceptance 为准。

## Goals / Non-Goals

**Goals:**

- Web 管理端和 Web 展示端标准 Dialog / Modal 点击遮罩或弹窗外空白区域时保持打开。
- 明确关闭入口保持可用，包括关闭图标、取消按钮、业务完成关闭，以及评审确认后的键盘关闭入口。
- 优先在统一 Dialog / Modal 封装或等价基础组件层沉淀默认策略。
- 历史自定义弹窗完成盘点，必要时逐一补齐。
- 保留弹窗宽度、滚动、上传状态机、即时回显和 Design System 语义样式横切验收。

**Non-Goals:**

- 不调整微信小程序弹窗、底部弹层或原生交互。
- 不默认修改 Popover、Dropdown、Tooltip、Select 下拉层、日期选择器等轻量浮层。
- 不引入未保存改动二次确认；如需要应另行提 REQ。
- 不重设计弹窗视觉、尺寸、遮罩颜色、按钮层级或动效。
- 不修改后端 API、数据库、OpenAPI、Orval、MinIO、Nginx 或 Docker Compose。

## Decisions

### D1. 策略选择：Design System 默认策略 + 历史弹窗补丁

选择 `tailwind-ds` / Design System 策略：优先修改共享 Dialog / Modal 或等价封装的默认 `onInteractOutside` / overlay click 行为，使新增弹窗默认继承“外部点击不关闭”。对于历史未复用共享组件的弹窗，后续 apply 阶段通过盘点清单逐个补齐。

替代方案是逐页面局部禁用外部点击关闭。该方案短期快，但容易遗漏新弹窗，也不利于后续统一治理，因此仅作为历史自定义弹窗的补充路径。

### D2. Esc 键作为明确键盘关闭入口处理

REQ-0084 capture 曾将 Esc 键列为待澄清项。评审结论要求 OpenSpec 阶段明确策略。本 Change 将 Esc 视为可保留的明确键盘关闭入口：标准弹窗 MUST 禁用鼠标外部点击关闭，但 MAY 保留 Esc 键关闭，前提是每个弹窗仍有可见关闭图标或取消按钮，且测试中单独标明 Esc 行为。

理由：Esc 是键盘用户可预期的显式退出方式，不属于鼠标误点遮罩；保留它可以兼顾可访问性与防误触目标。若某个高风险弹窗需要禁用 Esc，必须在页面级例外清单中说明。

### D3. 轻量浮层默认排除

Popover、Dropdown、Tooltip、Select 下拉层、日期选择器默认不纳入本 Change。它们通常依赖外部点击关闭完成选择控件的自然收起，强行套用 Dialog 策略会破坏基础控件体验。若后续需要治理轻量浮层，应单独提需求并制定组件级例外矩阵。

### D4. Conflict Resolution

- `prototype/web/modal-disable-outside-close.html` 展示点击遮罩 / 外部空白区域后弹窗保持打开，优先级高于旧 spec。
- `acceptance.md` AC-001 至 AC-015 是本 Change 的功能验收来源。
- 现有 `web-client` 中“点击遮罩关闭弹窗”的旧场景将改为“点击取消、关闭图标或 Esc 可关闭；点击遮罩不关闭”。
- `rules/ui-design.md` 的视觉约束继续有效，但本 Change 不改颜色、圆角、字号或布局风格。

## Risks / Trade-offs

- 历史弹窗未复用共享组件导致遗漏 → 在 tasks 中加入全量弹窗盘点清单，覆盖管理端和展示端标准 Dialog / Modal。
- 禁用遮罩关闭后出现无出口弹窗 → spec 和 tasks 强制每个可关闭弹窗必须有可见关闭入口，并测试取消 / 关闭图标。
- 旧测试仍断言遮罩关闭 → tasks 要求更新测试语义，改为外部点击保持打开。
- 上传弹窗误改上传链路 → 本 Change 明确不修改上传 API / Nginx / 存储；仅在触及上传控件时回归状态机和即时回显。
- Esc 策略与个别业务期望不同 → 以本 design 的默认保留 Esc 为准；例外必须在实现说明和测试中列出。

## Migration Plan

1. 盘点 Web 管理端和展示端标准 Dialog / Modal。
2. 优先修改共享 Dialog / Modal 封装默认策略。
3. 对自定义弹窗逐一补齐外部点击不关闭。
4. 更新或补充组件测试 / Playwright smoke。
5. 验证管理端高频弹窗、展示端预览弹窗、含上传控件弹窗。

## Open Questions

- 是否需要在后续独立 REQ 中增加“未保存改动二次确认”。
- 是否需要后续单独治理轻量浮层外部点击关闭策略。
