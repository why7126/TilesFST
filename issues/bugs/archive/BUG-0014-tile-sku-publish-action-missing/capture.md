---
bug_id: BUG-0014-tile-sku-publish-action-missing
status: captured
created_at: 2026-06-27 12:03:34
updated_at: 2026-06-27 12:03:34
severity_hint: high
environment: local|docker
related_requirement: REQ-0006-tile-sku-management
related_bug: BUG-0001-tile-category-enable-missing
captured_via: capture
classification_rationale: 瓷砖 SKU 列表对已下架行应提供上架操作，与类目停用行缺少启用入口（BUG-0001）同类；属已有 SKU 管理能力下的功能缺失，非新需求。
---

# 现象

瓷砖 SKU 列表页中，状态为「已下架」的行缺少「上架」操作入口，运营无法从列表直接恢复上架，与同类管理列表（如类目停用行可启用）的预期不一致。

# 复现步骤

1. 以 admin 登录管理端。
2. 进入「瓷砖SKU」列表页。
3. 找到状态为「已下架」的 SKU 行。
4. 查看该行操作列（或行内菜单）是否提供「上架」按钮/链接。
5. 对比瓷砖类目列表中「已停用」行是否提供「启用」操作。

# 期望 vs 实际

| | 说明 |
|---|---|
| **期望** | 已下架 SKU 行 MUST 提供「上架」操作，使运营可从列表恢复上架状态（与 REQ-0006 及类目管理对称行为一致）。 |
| **实际** | 已下架 SKU 行缺少上架操作入口，无法从列表直接执行上架。 |

# 附件

- 暂无截图。
