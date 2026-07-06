---
bug_id: BUG-0057-api-governance-tags-known-debt
title: API governance route tags 历史债清理未闭环临时规避
status: approved
created_at: 2026-07-04 22:27:55
updated_at: 2026-07-04 22:32:37
---

# 临时规避方案

在正式修复前，API 相关任务验收时不要只依赖 `python scripts/validate-api-standard.py` 的通过结果判断 tags 已治理完成。

临时检查方式：

1. 执行现有 API 标准校验：

   ```bash
   python scripts/validate-api-standard.py
   ```

2. 额外检查最终 OpenAPI 中是否存在多 tag、重复 tag 或非 kebab-case tag。
3. 若本次变更新增接口，至少确认新增 operation 没有扩大 tags 漂移。

# 风险与限制

- 临时人工检查无法替代自动化门禁，容易遗漏。
- 现有历史 tags 噪声仍会影响 Swagger UI 与管理端接口文档展示。
- 每个 API 相关 Change 都需要额外说明是否触碰该历史债，增加验收成本。

# 是否可不修

不建议长期不修。

理由：该问题虽然不阻断业务接口调用，但会削弱 API governance 校验脚本可信度，并持续污染 OpenAPI 契约质量。
