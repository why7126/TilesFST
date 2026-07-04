---
description: 产品版本发布计划 - 创建或更新 releases/vX.Y.Z 发布对象
---

**Input**：产品版本号，例如 `v0.1.0`，可选关联 Sprint 列表。

示例：

```text
/release-propose v0.1.0 --sprint sprint-004,sprint-005
```

**Output**：`releases/<version>/release.json` + `announcement.mdx` 初稿。

**禁止**：不写 `src/`；不绕过 OpenSpec；不把未评审、未纳入交付或未归档闭环的内容写入正式发布范围。

---

## Steps

1. 读取 `rules/release.md`、`rules/directory-structure.md`、`releases/README.md`。
2. 校验版本号为 SemVer 风格，例如 `v0.1.0`。
3. 根据输入选择一个或多个 Sprint；若未指定，列出候选已完成或待发布 Sprint 供确认。
4. 从 Sprint 四件套汇总 REQ、BUG 与 OpenSpec Change。
5. 将未评审、未交付或未归档闭环的内容排除出正式发布范围；如需保留，仅写入已知问题或后续计划。
6. 从 `releases/templates/release.json` 与 `releases/templates/announcement.mdx` 创建版本目录。
7. 记录影响范围初稿、升级步骤初稿、回滚说明初稿和待校验门禁。
8. 运行：

```bash
python scripts/validate-release.py --release-dir releases/<version>
```

校验失败时输出失败项，允许发布计划保留为待完善材料，但不得进入 `/release-publish`。

## Release Object 要求

`release.json` MUST 包含：

- `version`
- `release_time`
- `owner`
- `formal_scope_only: true`
- `sprints`
- `requirements`
- `bugs`
- `changes`
- `gates`
- `known_issues`
- `upgrade_steps`
- `rollback`
- `impact_scope`
- `announcement`

## Next

执行：

```text
/release-prepare <version>
```
