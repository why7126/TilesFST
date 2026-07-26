## Context

OpenSpec Change 当前存在两个归档口径：仓库规则、技能、脚本和历史归档使用 `openspec/changes/archive/`，但 `openspec/config.yaml` 使用 `openspec/archive`。用户已确认希望采用独立的 `openspec/archive/` 作为已完成 Change 的归档根目录。

这不是单文件配置修正，而是跨工作流治理迁移：`/opsx-archive`、`/sprint-archive`、Workflow Sync、issue promote、release、Fact Sheet、AI usage、readiness 和测试 helper 都会解析或输出归档路径。迁移必须同时处理历史目录和旧路径残留。

## Goals / Non-Goals

**Goals:**

- 将 canonical OpenSpec Change archive root 统一为 `openspec/archive/`。
- 迁移既有 `openspec/changes/archive/<date>-<change-id>/` 到 `openspec/archive/<date>-<change-id>/`。
- 更新所有工具、规则、技能和测试，使新增归档只写入 `openspec/archive/`。
- 在迁移期保留旧路径只读解析能力，避免历史引用或未迁移分支立即失效。
- 增加残留检查，阻止文档和脚本继续生成 `openspec/changes/archive/` 新引用。

**Non-Goals:**

- 不改变 `openspec/changes/<change-id>/` active Change 目录。
- 不改变 `openspec/specs/` 正式规格合并语义。
- 不调整 REQ/BUG 的 `issues/*/archive/` 或 Sprint 的 `iterations/archive/` 生命周期目录。
- 不修改业务 API、数据库、Web、小程序或 Docker Compose 运行时能力。

## Decisions

1. Canonical root 使用 `openspec/archive/`，目录名继续采用 `<YYYY-MM-DD>-<change-id>`。
   - 理由：archive 从 active change 根目录中独立出来，语义更清晰；保留原目录名可降低 release、trace、Fact Sheet 的数据迁移复杂度。
   - 替代方案：继续使用 `openspec/changes/archive/` 并仅修正 `openspec/config.yaml`。该方案成本最低，但无法解决用户指出的目录语义问题。

2. 路径解析 helper 先查 active，再查 canonical archive，最后兼容 legacy archive。
   - 理由：实现迁移期间的平滑读取，避免历史分支或旧 release 对象短期内无法追溯。
   - 替代方案：一次性移除 legacy 读取。该方案更干净，但对历史材料和并行分支冲击较大。

3. 新增写入、归档输出和生成事实源只允许写 canonical archive。
   - 理由：兼容读取不能变成继续写旧路径的借口；新增事实源必须收敛。
   - 替代方案：双写两个目录。该方案会制造重复事实源，后续状态同步和残留检查更容易漂移。

4. 迁移实施后保留 `openspec/changes/archive/` 为空目录或删除，并通过测试阻止其承载 Change 包。
   - 理由：若目录继续存在且包含历史包，工具很难区分遗留和新增；空目录可作为兼容过渡提示，但不能存放事实源。

## Risks / Trade-offs

- [Risk] 大量历史 Markdown、release JSON 和 trace 中存在旧路径引用 → 通过精确路径替换、残留检查和聚焦测试降低遗漏。
- [Risk] OpenSpec CLI 的实际 archive 行为可能仍由工具默认决定 → 先验证 `openspec archive` 在当前配置下的输出，必要时补充 CLI 后置迁移或 manual fallback。
- [Risk] 第三方或旧脚本仍硬编码 `openspec/changes/archive` → 用 `rg` 残留检查和 pytest helper 覆盖仓库内路径；仓库外调用以发布说明提示。
- [Risk] 迁移历史目录产生大 diff → 迁移时仅移动 Change 包，不修改包内无关内容；路径引用更新聚焦于规则、脚本、测试和长期事实源。

## Migration Plan

1. 更新 `openspec/config.yaml`、规则文档和技能文档，将 canonical archive root 改为 `openspec/archive/`。
2. 更新脚本中的 Change archive resolver，支持 active、canonical archive 和 legacy archive 读取顺序。
3. 迁移现有 `openspec/changes/archive/<date>-<change-id>/` 到 `openspec/archive/<date>-<change-id>/`。
4. 更新 release、trace、knowledge-base、tests 中的旧路径引用；对历史正文只做路径修正，不改业务结论。
5. 增加或更新测试：路径解析、readiness、residual check、Fact Sheet、AI usage、Workflow Sync time drift、release 生成。
6. 运行 OpenSpec validate、相关 pytest 和残留 `rg` 检查，确认 `openspec/changes/archive/` 不再包含 Change 包。

Rollback 策略：如迁移后关键工具阻断，可先恢复 resolver 对 legacy 路径的读取，并暂停物理目录删除；不得恢复新增归档写入旧路径，除非另起 Change 回滚目录决策。

## Open Questions

- 是否保留空的 `openspec/changes/archive/.gitkeep` 作为兼容提示，还是完全删除 `openspec/changes/archive/` 目录。
- release 历史 JSON 中的 `archive_dir` 字段是否全部重写为新路径，还是保留发布时事实并在解析层兼容。建议全部重写，避免后续公开材料传播旧路径。
