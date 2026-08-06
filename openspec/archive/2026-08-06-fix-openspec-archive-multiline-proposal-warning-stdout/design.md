---
change_id: fix-openspec-archive-multiline-proposal-warning-stdout
created_at: 2026-08-06 14:56:07
updated_at: 2026-08-06 14:56:07
---

# 设计说明

## 根因

`scripts/archive-change.sh` 当前按单行判断是否吸收已知 proposal warning：当某一行同时包含 `proposal.md` 与 `Why` 或 `What Changes` 时跳过该行。真实 OpenSpec CLI stdout 可能输出一个多行 warning 块，标题行和详情行分离，导致后续 `Missing required sections` 等详情行未被识别为同一已知 warning，最终透传到成功路径。

## 修复方案

- 将输出过滤从纯单行判断扩展为块级判断。
- 识别到 OpenSpec CLI proposal warning 块起始行后，进入 known-warning block 状态。
- 在 block 状态下吸收属于该 warning 的详情行，例如缺失章节列表、缩进项目和空行。
- 遇到未知 stdout/stderr 行时退出 block 或直接透传，确保诊断信息不丢失。
- 对 stdout 与 stderr 使用同一过滤策略，但仍分别输出到原流。

## 测试策略

- 在 `tests/test_archive_change_script.py` 的 fake `openspec` 中构造真实多行 stdout warning。
- 断言成功路径不展示 `Proposal warnings in proposal.md`、`Missing required sections` 等已知块内容。
- 断言未知 stdout 和未知 stderr 仍保留。
- 保留既有单行 warning 测试，防止 BUG-0123 回归。
- 保留失败路径测试，确保 OpenSpec CLI 失败时 stdout/stderr 诊断仍输出。

## 非目标

- 不回填英文脚手架标题。
- 不修改 OpenSpec CLI。
- 不隐藏所有 stdout/stderr。
- 不改业务 API、数据库、Web、小程序、管理端或 Docker。
