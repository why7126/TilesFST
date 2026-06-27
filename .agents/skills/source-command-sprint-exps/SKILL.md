---
name: "source-command-sprint-exps"
description: "Sprint 经验复盘 - 总结整迭代流程、需求、开发与质量经验，沉淀到 docs/knowledge-base"
---

# source-command-sprint-exps

Use this skill when the user asks to run the migrated source command `sprint-exps`.

## Command Template

**Input**：`sprint-xxx`（必填或可推断）；可选 `--dry-run`、`--focus`、`--skip-best-practices`

**Output**：Experience Analysis Report + `docs/knowledge-base/retrospectives/<sprint-id>-retrospective.md` + 可选 best-practices/incidents + 索引与 sprint.md 回链

**禁止**：`src/`、apply/archive、自动改 `rules/`

**推荐时机**：`/sprint-archive` 之后

---

## Steps

1. 读 sprint 四件套、全部 REQ/BUG/Change trace 与 review/root-cause/tasks
2. 构建 Sprint Fact Sheet
3. 四维分析：流程、需求设计、开发质量、可复用抽象
4. 聚类 → 行动项 → 写入 knowledge-base（除非 dry-run）
5. 输出 Experience Analysis Report

详见 `.cursor/commands/sprint-exps.md`。

---

## 分析要点

- **重复 BUG**：UI 不一致、上传、登录等模式 → 预防建议 + 是否 best-practice
- **需求文档**：缺原型/acceptance 与 fix-* 数量的关联
- **组件抽象**：多 REQ 相似页面 → AdminListPage / 共享弹窗等建议
- **流程**：review/opsx/apply/archive 卡点与容量

行动项含优先级与下一命令（`/req-capture`、`/sprint-propose` 等）。
