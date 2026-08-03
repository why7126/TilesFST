---
review_id: REV-REQ-0082-001
requirement_id: REQ-0082-admin-category-name-special-characters
date: 2026-07-30
result: approved
participants:
  - product
created_at: 2026-07-30 22:18:32
updated_at: 2026-07-30 22:18:32
---

# 需求评审

## 评审结论

`REQ-0082-admin-category-name-special-characters` 评审通过。

该需求是 `REQ-0005-tile-category-management` 的类目名称规则 refinement，并承接 `REQ-0077-category-name-max-length-15` 的长度上限。范围聚焦于将管理后台瓷砖类目名称从“最多 15 个字符，只能包含中文、英文和数字”调整为“最多 15 个字符，允许中文、英文、数字和特殊字符”，不改变类目层级、编码、排序、启停、同层级唯一和历史数据清洗策略。

## 评审检查清单

- [x] 范围清晰，Out of Scope 明确。
- [x] 验收标准可测试，覆盖前端表单、后端兜底、OpenAPI / Orval、测试夹具和展示回归。
- [x] 优先级与依赖合理，优先级为 P1，父需求与关联需求已说明。
- [x] UI 类原型或实现策略已决，低保真 prototype 与弹窗 / 列表回归点已提供。
- [x] 无与现有 REQ 重复未说明；与 `REQ-0077` 的关系为字符集规则补充。

## 条件通过项

- [ ] 后续 `/req-opsx` 生成 OpenSpec Change 时，必须明确特殊字符策略采用“允许常见可见业务符号、禁止换行 / 制表符 / 不可见控制字符”，并同步前后端校验口径。
- [ ] 实现阶段必须确认数据库字段、CHECK 约束、OpenAPI pattern、Orval 生成物和测试夹具是否存在旧字符集限制。
- [ ] 实现阶段必须保留 `acceptance.md` 中 7 条 `AC-XCUT` 的管理端列表 / 弹窗横切验收。

## 后续动作

1. `/req-opsx REQ-0082-admin-category-name-special-characters`
2. `/sprint-propose` 纳入 Sprint 后再进入实现
