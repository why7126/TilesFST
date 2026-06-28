---
bug_id: BUG-0021-sidebar-menu-icons-indistinguishable
review_id: REV-BUG-0021-001
status: approved
reviewed_at: 2026-06-27 21:42:20
reviewer: ai-agent
decision: approve
severity: medium
hotfix_required: false
---

# 缺陷评审

## 1. 评审结论

`BUG-0021-sidebar-menu-icons-indistinguishable` 评审通过，状态变更为 `approved`。

该缺陷应进入修复流程，后续可执行：

```text
/bug-opsx BUG-0021-sidebar-menu-icons-indistinguishable
```

建议修复 Change：

```text
fix-sidebar-menu-icons-indistinguishable
```

## 2. 评审清单

| 检查项 | 结论 | 说明 |
|---|---|---|
| 可复现或根因充分 | 通过 | 100% 稳定复现（collapsed 态 7 项同质 CSS 方块）；`root-cause.md` 已定位 `AdminSidebar` 统一占位、`admin-nav.ts` 无 icon 字段、REQ-0011 原型未要求差异化。 |
| 严重等级合理 | 通过 | `medium` 合理；路由与 a11y 仍可用，不阻断核心功能；collapsed 态导航效率与误点风险需修复。 |
| 回归验收明确 | 通过 | `acceptance.md` AC-001～AC-010 覆盖 per-menu Lucide 图标、collapsed/expanded 双态、角色过滤、a11y、REQ-0011 无回归、vitest 与纯前端范围。 |
| 是否需 hotfix 路径 | 不需要 | 非阻断、非安全、非数据问题；常规 `fix-*` Change 即可，预计改动 `admin-nav.ts` + `AdminSidebar.tsx` + CSS + 测试。 |

## 3. 批准理由

1. REQ-0011 折叠能力已交付，本 BUG 为 collapsed icon-only 场景下的 UX 补全，与「已实现需求 + fix-* 补丁」模式一致。
2. 根因与修复面集中：导航配置增 icon 映射 + 渲染 Lucide SVG；不涉及 API/DB/Orval/Docker。
3. 项目已使用 `lucide-react`，技术路径清晰，工作量小。
4. workaround 已说明可保持 expanded 侧栏规避，但不满足 collapsed 窄栏设计意图。

## 4. 修复门禁

| 项目 | 结论 |
|---|---|
| 是否允许 `/bug-opsx` | 是 |
| 是否允许进入 Sprint | 是 |
| 建议 Change ID | `fix-sidebar-menu-icons-indistinguishable` |
| Change 类型 | `fix-*` |

## 5. 修复范围建议

1. `AdminNavItem` 增加 `icon` 字段，7 个菜单配置语义 Lucide 图标（见 `acceptance.md` AC-001 建议表）。
2. `AdminSidebar` 渲染 per-item icon，移除 CSS 伪元素方块样式。
3. 保持 `aria-label`、collapsed active 态、localStorage 与 chevron 行为不变。
4. 扩展 `AdminSidebar.collapse.test.tsx` 断言图标差异。
5. MUST NOT 修改店主端 `Sidebar`、后端或 REQ-0011 折叠机制本身。

## 6. 后续动作

1. 执行 `/bug-opsx BUG-0021-sidebar-menu-icons-indistinguishable` 创建 `fix-sidebar-menu-icons-indistinguishable`。
2. 可纳入当前或下一 Sprint（`related_requirement: REQ-0011`）。
3. 修复完成后 `/opsx-apply` → collapsed 态 icon-only 验收 → `/opsx-archive`。
