---
review_id: REV-REQ-0077-001
date: 2026-07-28
participants:
  - product
result: approved
created_at: 2026-07-28 00:13:39
updated_at: 2026-07-28 00:13:39
---

# REQ-0077 需求评审

## 评审结论

评审通过。REQ-0077 将类目名称输入长度上限从 10 个字符放宽到 15 个字符，范围边界清晰，明确只覆盖长度规则，不改变字符集、同层级唯一、编码自动生成、层级和排序权重等既有规则。

该需求具备进入 `/req-opsx` 和 Sprint 规划的条件。后续 OpenSpec Change 需要重点确认前后端校验、OpenAPI / Orval、数据库字段约束、测试夹具，以及管理端列表/树、小程序和 Web 展示入口的 15 字符展示回归。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖 15 字符通过、16 字符拒绝、API 兜底、Orval、DB 与展示回归。
- [x] 优先级与依赖合理，P1，父需求为 `REQ-0005-tile-category-management`。
- [x] UI 类原型或实现策略已决，包含 `prototype/web/category-name-max-length-15.html` 与 `prototype-context.md`。
- [x] 与现有 REQ 重复关系已说明，明确覆盖 `REQ-0067-admin-category-edit-modal-validation` 中的 10 字符长度规则。
- [x] Knowledge-base 横切 AC 已写入 acceptance，覆盖 `admin-list` 与 `admin-modal`。

## 条件通过项

- [ ] 后续 `/req-opsx` 的 design.md MUST 引用 trace 中的 `knowledge_base_refs`。
- [ ] 后续实现前 MUST 检查数据库字段是否存在 10 字符限制；如存在，Change 必须纳入迁移方案。
- [ ] 纳入 Sprint 前需确认 sprint.md 横切预防清单覆盖本 REQ 的 `admin-list` 与 `admin-modal` AC-XCUT。

## 后续建议

1. `/req-opsx REQ-0077-category-name-max-length-15`
2. `/sprint-propose` 纳入迭代后再执行实现
