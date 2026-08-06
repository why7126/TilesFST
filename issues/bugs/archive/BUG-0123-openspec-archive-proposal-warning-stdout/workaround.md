---
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
created_at: 2026-08-06 13:18:13
updated_at: 2026-08-06 13:18:13
---

# Workaround

## 临时规避

暂无稳定自动化规避方式。执行 `/opsx-archive` 或 `scripts/archive-change.sh <change-id>` 时，如归档最终成功且仅出现已知 proposal scaffold warning，可人工忽略该 warning。

## 注意事项

- 不应为了消除该 warning 回填英文脚手架标题，这会违背项目中文优先 OpenSpec 文档规范。
- 不应在 shell 层粗暴丢弃全部 stdout/stderr，否则可能掩盖未知异常、OpenSpec CLI 真实错误或诊断信息。

## 后续处理

通过 OpenSpec Change 修复 `scripts/archive-change.sh` 输出过滤策略，并补充成功路径与未知输出保留的回归测试。
