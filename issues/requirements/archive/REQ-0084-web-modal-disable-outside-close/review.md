---
review_id: REV-REQ-0084-001
requirement_id: REQ-0084-web-modal-disable-outside-close
date: 2026-07-30
reviewed_at: 2026-07-30 23:18:07
participants:
  - product
result: approved
created_at: 2026-07-30 23:18:07
updated_at: 2026-07-30 23:18:07
---

# REQ-0084 需求评审

## 评审结论

通过。

Web 端所有标准 Dialog / Modal 禁用点击遮罩或弹窗外空白区域自动关闭的需求范围清晰，业务价值明确，能够降低管理端资料维护和展示端内容查看中的误触关闭风险。需求已明确本期包含管理端、Web 展示端标准弹窗和含上传控件弹窗，同时将小程序弹窗、轻量浮层、未保存改动二次确认、视觉重设计和业务流程重构排除在本期范围外。

验收标准可测试，已覆盖功能 AC、明确关闭入口、表单状态保留、确认弹窗、展示端预览、统一组件默认配置、历史弹窗盘点、Esc 键待确认边界、轻量浮层边界、前端测试和 Design System 约束。UI 类需求已提供 prototype 策略和静态 HTML 说明，并写入 `admin-modal`、`media-upload` 横切 AC，可进入后续 `/req-opsx`。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试。
- [x] 优先级与依赖合理。
- [x] UI 类：原型或实现策略已决。
- [x] 无与现有 REQ 重复未说明。

## 条件通过项

- [ ] 后续 `/req-opsx` 需在 design.md 中引用 `trace.md` 的 `knowledge_base_refs`。
- [ ] 后续 OpenSpec Change 需明确 Esc 键关闭策略；未确认前不得把 Esc 行为纳入已实现范围。
- [ ] 后续 OpenSpec Change 需明确轻量浮层例外边界，默认不把 Popover、Dropdown、Tooltip、Select、日期选择器纳入标准 Dialog / Modal 治理。
- [ ] 后续实现若触及上传链路，必须保留 media-upload 横切验收；若只改弹窗关闭策略，可按 AC 标注 N/A 原因。

## 下一步

```text
/req-opsx REQ-0084-web-modal-disable-outside-close
```
