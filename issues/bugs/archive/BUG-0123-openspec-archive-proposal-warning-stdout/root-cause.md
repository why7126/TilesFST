---
bug_id: BUG-0123-openspec-archive-proposal-warning-stdout
cause_category: code
created_at: 2026-08-06 13:18:13
updated_at: 2026-08-06 13:18:13
---

# Root Cause

## 直接原因

`scripts/archive-change.sh` 对归档命令输出的噪音吸收范围不完整。当前 wrapper 已处理 BUG-0119 涉及的项目自定义固定说明噪音，但没有覆盖 OpenSpec CLI stdout 中已知的 proposal scaffold warning 块，因此归档成功时仍会把该 warning 透传到用户可见输出。

## 根本原因

归档成功路径缺少对“已知兼容性 warning”和“未知诊断输出”的分层处理策略：应精确吸收项目已确认可忽略的 proposal scaffold warning，同时保留未知 stdout/stderr，避免为了安静输出而吞掉真实异常。

## 触发条件

- Change 采用中文优先文档结构，未回填 OpenSpec CLI 英文脚手架标题。
- OpenSpec CLI 在归档过程中通过 stdout 输出 proposal scaffold warning。
- `scripts/archive-change.sh` 成功路径直接展示或未充分过滤该 stdout 块。

## 分类

- 类型：code
- 影响面：workflow / OpenSpec wrapper
- 关联历史缺陷：BUG-0119-openspec-archive-scaffold-warning-noise

## 修复关注点

- 精确匹配并吸收已知 proposal scaffold warning 块。
- 未知 stdout/stderr 继续展示。
- 成功路径保持简洁，失败路径保留足够诊断信息。
