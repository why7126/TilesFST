---
sprint_id: sprint-007
title: Sprint 007 发布说明
status: planning
lifecycle_stage: change
created_at: 2026-07-11 23:39:00
updated_at: 2026-07-12 00:07:29
owner: product
source: /sprint-propose sprint-007
---

# Sprint 007 发布说明

## 发布范围

本 Sprint 正式纳入：

- `REQ-0036-clipboard-helper-best-practice-docs`
- `add-clipboard-helper-best-practice-docs`
- `REQ-0035-ai-usage-snapshot-sprint-close-exps`
- `update-ai-usage-snapshot-sprint-close-exps`

## 用户可见变化

- 面向开发、QA 与 reviewer 的 Clipboard helper best-practice 文档将作为长期知识库沉淀。
- Web README / 知识库索引将提供可发现入口，便于后续新增复制入口时复用。
- 面向 AI 工作流维护者，Sprint close / exps 将默认检查或消费 AI usage snapshot，真实统计不可用时显式 fallback。

## 治理与验收变化

- 后续新增主题相关页面时，必须复用 `REQ-0020-theme-comfort-refine` 的主题验收矩阵。
- 验收材料必须补充截图或等价视觉材料，并补充 DOM 契约检查，避免只凭人工视觉判断。
- Clipboard helper 调用方文案、fallback 策略、敏感值边界与 checklist 将被文档化，避免复制入口体验漂移。
- AI usage snapshot 将纳入 Sprint close / exps 默认流程，避免 `/sprint-exps` 静默继续 estimated fallback。
- Sprint close / exps 输出必须区分 `actual` 与 `estimated_fallback`，并提供 snapshot 缺失、过期或失败时的 recommended action。

## 影响范围

| 范围 | 影响 |
|---|---|
| API | 无 |
| 数据库 | 无 |
| Web | 仅文档入口影响；不修改运行时代码 |
| 小程序 | 无 |
| 管理端 | 无运行时界面变更；后续复制入口按 best-practice 文档验收 |
| Orval | 无 |
| Docker Compose | 无 |

## 发布风险

文档示例不得包含真实密钥、真实 Token、真实客户隐私数据或真实生产签名 URL。AI usage snapshot 生成与检查必须保持脱敏，不得写入 prompt、系统指令、本机绝对路径或工具输出全文。若本地 session 数据不可访问，`/sprint-exps` 必须显式 fallback，不得伪装真实统计。若后续纳入主题相关页面新增，必须在 release note 中列出页面、主题、截图、DOM 检查和 N/A 项。
