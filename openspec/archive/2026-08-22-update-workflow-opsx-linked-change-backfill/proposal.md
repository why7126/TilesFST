## 背景

`/req-opsx` 与 `/bug-opsx` 已经要求创建或确认 linked Change 后，后续 `/opsx-apply <REQ-id|BUG-id>`、`/opsx-archive <REQ-id|BUG-id>` 继续使用原始 Issue ID。但当前 linked Change 信息可能只写入 `trace.md` 或 Sprint scope，`requirement.md` / `bug.md` 主文档、REQ/BUG registry 和当前态看板仍可能滞后。

这种漂移会让人类评审者反查多个事实源，也会让后续命令解析、Sprint scope 门禁和当前态下一步推导出现不确定性。REQ-0116 已确认要同时增强 REQ 与 BUG 两条 opsx 链路的自动回填。

## 变更内容

- 增强 Workflow Sync 在 `req.opsx` / `bug.opsx` 事件中的 linked Change 回填规则。
- 同步覆盖 Issue `trace.md` 的 `openspec_changes[]`、REQ `related_changes[]` 或 BUG `related_change`、`requirement.md` / `bug.md` 主文档和 `_registry.yaml`。
- 已纳入 Sprint 的 Issue 创建 Change 后，继续补齐同一 Sprint 的 `changes[]` 与 `scope_estimates[].change`。
- 增加 focused drift check / dry-run 语义，发现 trace、主文档、registry、Sprint scope linked Change 不一致时输出可定位报告。
- 增加 REQ 与 BUG 两条链路的聚焦测试，验证回填、幂等性和 `/opsx-apply --sprint auto` 解析。
- 不修改业务 API、数据库、Web、管理端或微信小程序功能。

## 能力范围

### 新增能力

无。该变更不引入独立业务 capability。

### 修改能力

- `agent-workflow-tooling`：补强 `req.opsx` / `bug.opsx` linked Change 多入口自动回填与漂移检查要求。

## 影响

- 影响脚本：`scripts/sync-workflow-status.py` 及 `scripts/workflow_sync/**` 中 Issue trace、主文档、registry、Sprint scope 同步逻辑。
- 影响测试：新增或更新 Workflow Sync 相关测试，覆盖 REQ 与 BUG 两条 opsx 链路。
- 影响 Issue 文档派生：`requirement.md` / `bug.md` 可读入口和 `_registry.yaml` 的 `related_change` 将随 `req.opsx` / `bug.opsx` 自动刷新。
- 影响 Sprint planning：已在 Sprint 中的 REQ/BUG 创建 Change 后，Sprint scope 仍由 Workflow Sync 回填。
- 不影响 API、数据库、Web、管理端、小程序、对象存储或 Docker Compose 运行时行为。
