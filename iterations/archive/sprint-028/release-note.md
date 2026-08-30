---
title: sprint-028 发布说明
created_at: 2026-08-30 08:50:35
updated_at: 2026-08-30 14:44:32
---

# sprint-028 发布说明

## 范围摘要

- 完成纯治理 Change `standardize-ai-usage-session-discovery`，统一 AI Usage 本地 session 默认发现规范和命令输出口径。
- 完成高优先级 BUG `BUG-0147-miniapp-certificate-list-images-missing`，修复生产小程序证书列表页图片类证书缺少 URL/缩略图导致全部显示占位的问题。
- 完成发布状态决策面板与环境分层证据门禁治理，发布/归档命令可区分开发、体验版和生产证据边界。

## 用户可见变化

- 产品用户界面无变化。
- 小程序证书列表页可显示图片类证书缩略图，非图片或缺失媒体才显示占位。
- workflow 命令在本地存在 Codex session 时，会优先尝试自动提取真实 AI usage 事实；失败时输出更明确的补救动作。

## 技术变化

- 治理范围涉及 Skill、规则、OpenSpec Change、治理日志、AI Usage 脚本文案、发布状态决策面板和环境分层证据脚本门禁。
- BUG-0147 涉及后端 miniapp certificates API、证书媒体 key/URL/缩略图回填与小程序端渲染验收；DB 结构变更和 Orval 不适用。

## 状态

```yaml
sprint_id: sprint-028
status: published
published_at: 2026-08-30 14:44:32
bugs:
  - BUG-0147-miniapp-certificate-list-images-missing
changes:
  - standardize-ai-usage-session-discovery
  - fix-miniapp-certificate-media-urls
  - add-release-status-decision-panel
  - standardize-environment-tiered-evidence-gates
  - enforce-environment-tiered-evidence-gates
```
