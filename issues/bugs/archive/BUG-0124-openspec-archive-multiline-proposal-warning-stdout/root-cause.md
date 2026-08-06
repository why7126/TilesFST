---
bug_id: BUG-0124-openspec-archive-multiline-proposal-warning-stdout
cause_category: code
created_at: 2026-08-06 14:30:16
updated_at: 2026-08-06 14:30:16
---

# Root Cause

## 直接原因

`scripts/archive-change.sh` 对 OpenSpec CLI proposal warning 的过滤边界仍不完整。此前修复已覆盖单行 warning 或固定提示形态，但真实 OpenSpec CLI 输出会包含由标题行和后续详情行组成的多行 stdout 块，当前过滤逻辑未将这些连续行作为同一个已知 warning 块整体吸收。

## 根本原因

归档成功路径的输出过滤缺少“多行已知 warning 块”的状态化处理：识别到 `Proposal warnings in proposal.md` 后，需要继续消费属于该 warning 的后续详情行，直到块结束；同时仍必须保留不属于该块的未知 stdout/stderr，避免安静输出掩盖真实诊断。

## 触发条件

- Change 采用中文优先 OpenSpec 文档结构，没有回填 OpenSpec CLI 期望的英文脚手架章节。
- OpenSpec CLI 在归档成功时通过 stdout 输出 proposal warning 标题和多行详情。
- 归档 wrapper 仅过滤单行或固定字符串，未覆盖真实多行 stdout 块。

## 分类

- 类型：code
- 影响面：workflow / OpenSpec wrapper / 归档成功路径输出
- 关联历史缺陷：BUG-0123-openspec-archive-proposal-warning-stdout

## 修复关注点

- 精确识别并整体吸收真实 OpenSpec CLI 多行 proposal warning 块。
- 保留未知 stdout/stderr，不扩大为吞掉全部输出。
- 保持既有单行 warning 回归测试有效。
- 为多行 warning 样例补充回归测试。
