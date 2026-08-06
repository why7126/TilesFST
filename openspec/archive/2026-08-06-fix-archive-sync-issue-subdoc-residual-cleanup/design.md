---
change_id: fix-archive-sync-issue-subdoc-residual-cleanup
status: proposed
created_at: 2026-08-06 11:52:40
updated_at: 2026-08-06 11:52:40
---

# 设计

## 根因分析

归档链路依赖 Workflow Sync 写入 Issue 主状态与子文档状态，再由 `promote-issues-for-archive` 执行物理归档门禁。当前流程虽然能报告可安全 reconcile 的子文档残留，但没有在归档同步阶段自动应用或在 promote 前形成稳定的一键修复路径，导致安全残留继续进入 promote 门禁。

## 修复方案

1. 复用现有 Issue 子文档扫描分类，区分可安全同步、需人工判断、缺验收结果、缺 trace/交付证据和不建议自动修复项。
2. 在归档同步阶段或 promote 前置流程中，对已闭环 Issue 的可安全同步残留执行自动 reconcile，刷新被修改 Markdown 的 `updated_at`。
3. 对语义不明、缺少闭环证据或缺少验收结论的残留继续输出 warning/blocker，不自动写入。
4. 保持 dry-run / apply-reconcile 手动命令可用，成功路径输出 compact summary。
5. 确保重复执行不产生无意义 diff。

## 数据与接口

不新增数据库表，不修改 Pydantic Schema，不修改 FastAPI API，不需要 Orval。

## 测试策略

- 构造已闭环 BUG/REQ 且 `capture.md` 残留 `captured` 的 fixture，验证归档同步后 promote 不再被该安全残留阻断。
- 构造未闭环或语义不明状态残留，验证仍报告 warning/blocker 且不写入。
- 验证 dry-run 不写文件，apply 只写 dry-run 分类为可安全同步的字段。
- 验证幂等：第二次运行无 delta。

## 风险

- 最大风险是把仍需人工判断的状态误同步为闭环态。缓解方式是复用分类结果，仅处理明确可安全同步项，并保留未闭环 Issue 的阻断门禁。
