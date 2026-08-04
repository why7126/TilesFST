## 任务清单

- [x] 1. 定位 fresh gate stale 判定来源，确认读取的 snapshot 路径、payload、`generated_at` 和 Sprint scope 更新时间来源。
- [x] 2. 修正 fresh gate 判定顺序，确保当前且覆盖完整的 snapshot 输出 fresh/pass，过期、缺失、失败、coverage 不足和矩阵缺失仍输出 blocker。
- [x] 3. 修正或补齐 usage mode 映射，确保 `actual`、`estimated_fallback`、`skipped`、`unavailable` 不会覆盖已刷新 snapshot 的真实状态。
- [x] 4. 增强 Fact Sheet summary 的 compact fresh gate 诊断字段，保留 snapshot status、usage mode、coverage、矩阵 presence、warning_count 和 recommended_action。
- [x] 5. 补充 pytest：fresh snapshot 通过、stale snapshot 阻断、缺失 snapshot 阻断、coverage 不足阻断、usage mode fallback 映射。
- [x] 6. 同步相关技能或治理文档：如 `/sprint-exps`、AI usage hook 或 Fact Sheet 消费规则发生口径变化，更新对应 Skill / rules / docs。
- [x] 7. 运行聚焦验证：`pytest` 相关测试、`python scripts/validate-openspec-language.py`、`openspec validate fix-fact-sheet-ai-usage-fresh-gate-snapshot --strict`。
- [x] 8. 回填 BUG-0113 acceptance 证据，确认 AC-001 至 AC-006。
- [x] 9. 评估是否需要沉淀 `docs/knowledge-base/incidents/`；若定位结果具备复用价值，补充故障知识，否则在归档说明中记录不适用。
