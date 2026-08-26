---
change_id: refine-skill-final-output-contract
created_at: 2026-08-26 20:52:46
updated_at: 2026-08-26 20:58:03
---

# 测试计划

## 聚焦校验

- `python scripts/validate-agent-context-budget.py`
- `python scripts/validate-openspec-language.py`
- `openspec validate refine-skill-final-output-contract --strict`
- `python scripts/validate-directory-structure.py`

## 文档卫生

- `python scripts/validate-doc-prose-hygiene.py <focused governance files>`

## 业务测试

本 Change 不修改业务 API、DB、Web、小程序、管理端或 Orval 生成物，业务测试不适用。

## 执行结果

- `python scripts/validate-agent-context-budget.py`：通过。
- `python scripts/validate-openspec-language.py`：通过。
- `openspec validate refine-skill-final-output-contract --strict`：通过。
- `python scripts/validate-directory-structure.py`：通过。
- `python scripts/validate-doc-prose-hygiene.py <focused governance files>`：通过并返回 7 条启发式 warning，未阻断。
