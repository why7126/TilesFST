# issues/bugs

缺陷（BUG）池。生命周期阶段目录见 `rules/issues-lifecycle.md`。

| 目录 | 含义 |
|---|---|
| `plan/` | 规划中并完成评审（capture → 评审通过前；reject/defer 留此） |
| `review/` | 已评审通过，修复/验收中，未 archive |
| `archive/` | 已修复并 OpenSpec 归档 |
| `_registry.yaml` | 序号注册表（根目录，勿移动） |

**新建**：`/bug-capture` → `plan/BUG-NNNN-slug/`  
**评审通过**：迁入 `review/`  
**归档完成**：迁入 `archive/`

遗留扁平 `BUG-*` 目录仍可读，勿再新建。
