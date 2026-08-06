---
change_id: fix-openspec-archive-proposal-warning-stdout
acceptance_status: pending
created_at: 2026-08-06 13:45:35
updated_at: 2026-08-06 13:55:08
---

# 验收

## 验收项

| 编号 | 验收项 | 预期 |
|---|---|---|
| AC-001 | 中文优先 Change 归档成功路径过滤已知 proposal scaffold warning | 成功输出不展示已知 proposal warning 块。 |
| AC-002 | 未知 stdout 保留 | 未知 stdout 不被静默吞掉。 |
| AC-003 | 未知 stderr 保留 | 未知 stderr 不被静默吞掉。 |
| AC-004 | BUG-0119 不回归 | 自定义固定说明噪音仍不出现在归档成功输出中。 |
| AC-005 | 失败路径诊断不丢失 | OpenSpec CLI 归档失败时返回非零并输出必要错误信息。 |

## 建议验证

```bash
python -m pytest tests/test_archive_change_output.py
python scripts/validate-openspec-language.py
python scripts/validate-directory-structure.py
```

## 文档同步复核

- 长期能力规格：已通过本 Change 的 `agent-workflow-tooling` delta spec 覆盖，归档后合并到正式 spec。
- 额外 docs：不适用。本修复不改变 API、数据库、部署、发布、Web、小程序、管理端或用户使用文档。
- 知识库 incident：不适用。该问题属于治理脚本成功路径输出噪音，不是生产事故；暂不沉淀 `docs/knowledge-base/incidents/`。

## 结果回填

待 `/opsx-apply` 与 `/opsx-archive` 后回填。
