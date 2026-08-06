---
bug_id: BUG-0119-openspec-archive-scaffold-warning-noise
title: OpenSpec 归档反复暴露英文脚手架兼容 warning 根因分析
created_at: 2026-08-06 10:27:26
updated_at: 2026-08-06 10:27:26
---

# 直接原因

`scripts/archive-change.sh` 在 OpenSpec CLI 归档成功、项目中文语言校验通过后，仍把已知的英文脚手架标题兼容 warning 传递到最终归档说明中。

该 warning 的内容与项目规则存在已知差异：上游 CLI 期待 `proposal.md` 保留英文 `## Why` / `## What Changes` 标题，而项目 `rules/language.md` 要求 OpenSpec Change 文档中文优先，且不得为了消除 CLI 提示回填英文脚手架标题。

# 根本原因

归档封装层没有把“上游 CLI 兼容 warning”和“项目真实归档风险”拆成两个不同信号处理：

- 已知兼容 warning 没有稳定匹配和吸收规则。
- 最终输出没有基于项目语言校验结果判断该 warning 是否可静默处理。
- `/opsx-archive` 面向验收者的成功结论仍暴露低价值重复提示，导致非阻塞信息与真实错误混在一起。

# 触发条件

满足以下条件时会稳定触发：

1. Change 文档符合项目中文语言规范。
2. `proposal.md` 未包含英文 `## Why` / `## What Changes` 标题。
3. 执行 `/opsx-archive <change-id>` 或底层 `scripts/archive-change.sh <change-id>`。
4. OpenSpec CLI 返回成功但 stderr 包含英文脚手架标题兼容提示。
5. `python scripts/validate-openspec-language.py` 通过。

# 缺陷分类

| 维度 | 结论 |
|---|---|
| 类型 | governance / workflow tooling |
| 位置 | OpenSpec 归档封装脚本、opsx archive 输出口径 |
| 数据库 | 不涉及 |
| API | 不涉及 |
| 前端 | 不涉及 |
| 小程序 | 不涉及 |
| 安全 | 不直接涉及权限或敏感信息泄露 |

# 修复方向

建议在后续 `fix-*` Change 中处理：

1. 在 `scripts/archive-change.sh` 或归档封装层中识别该固定 OpenSpec CLI 兼容 warning。
2. 当该 warning 是唯一 stderr 且项目中文语言校验通过时，不再把固定说明输出为最终归档提示。
3. 保留真实错误、未知 stderr、目录结构错误和中文语言校验失败的阻断或 warning 输出。
4. 为“仅已知 CLI warning + 语言校验通过”“未知 stderr”“语言校验失败”三类场景补充脚本级回归测试。
