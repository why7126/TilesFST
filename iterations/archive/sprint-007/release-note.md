---
sprint_id: sprint-007
title: Sprint 007 发布说明
status: published
lifecycle_stage: archive
created_at: 2026-07-11 23:39:00
updated_at: 2026-07-15 13:26:33
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
- `REQ-0037-auto-token-fact-source-for-workflow-commands`
- `add-auto-token-fact-source-for-workflow-commands`
- `REQ-0038-brand-certificate-management`
- `add-brand-certificate-management`

## 用户可见变化

- 面向开发、QA 与 reviewer 的 Clipboard helper best-practice 文档将作为长期知识库沉淀。
- Web README / 知识库索引将提供可发现入口，便于后续新增复制入口时复用。
- 面向 AI 工作流维护者，Sprint close / exps 将默认检查或消费 AI usage snapshot，真实统计不可用时显式 fallback。
- 面向 AI 工作流维护者，`/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 命令将增加统一后置 hook，自动构建或刷新脱敏 Token 使用量事实源。
- 面向企业内部管理端用户，将新增“品牌证书”一级管理页，用于维护品牌资质、检测报告、荣誉证书和前台展示状态。
- 运营人员可按品牌、证书类型、有效状态和展示状态筛选证书，并维护证书文件、有效期、显示/隐藏和删除。

## 治理与验收变化

- 后续新增主题相关页面时，必须复用 `REQ-0020-theme-comfort-refine` 的主题验收矩阵。
- 验收材料必须补充截图或等价视觉材料，并补充 DOM 契约检查，避免只凭人工视觉判断。
- Clipboard helper 调用方文案、fallback 策略、敏感值边界与 checklist 将被文档化，避免复制入口体验漂移。
- AI usage snapshot 将纳入 Sprint close / exps 默认流程，避免 `/sprint-exps` 静默继续 estimated fallback。
- Sprint close / exps 输出必须区分 `actual` 与 `estimated_fallback`，并提供 snapshot 缺失、过期或失败时的 recommended action。
- 工作流命令后置 Token fact source hook 必须区分 `actual`、`estimated_fallback` 与 `unavailable`，失败默认不阻断主命令，并继承 `REQ-0034` 脱敏边界。
- 品牌证书管理必须覆盖管理端列表页一致性、弹窗宽度 CSS 层叠和媒体上传全链路横切验收，包含 Docker Web `:3000` 上传边界验证。
- 品牌证书 HTML/PNG 原型中的旧品牌摘要栏仅作视觉参考，正式实现以 acceptance.md 的一级页结构为准。

## 影响范围

| 范围 | 影响 |
|---|---|
| API | 新增管理端品牌证书列表、创建、详情、更新、显示、隐藏、删除和证书文件上传相关接口 |
| 数据库 | 新增品牌证书表或等价 schema / migration，并维护品牌 1:N 证书关系 |
| Web | 新增管理端 `/admin/brand-certificates` 页面、导航入口、品牌快捷入口、弹窗、上传和预览交互 |
| 小程序 | 无 |
| 管理端 | 新增品牌证书主数据维护能力，权限入口、审计和展示控制需验收 |
| Orval | 需要同步生成品牌证书 API 客户端 |
| Docker Compose | 需要通过 Web `:3000` 验证证书文件上传边界和媒体回显 |

## 发布风险

文档示例不得包含真实密钥、真实 Token、真实客户隐私数据或真实生产签名 URL。AI usage snapshot 生成与检查必须保持脱敏，不得写入 prompt、系统指令、本机绝对路径或工具输出全文。若本地 session 数据不可访问，`/sprint-exps` 与工作流命令后置 hook 必须显式 fallback，不得伪装真实统计。若后续纳入主题相关页面新增，必须在 release note 中列出页面、主题、截图、DOM 检查和 N/A 项。

品牌证书能力涉及 API、DB、Web、MinIO 上传和 Orval，发布风险高于纯文档治理项。实现阶段必须先完成后端校验和上传链路，再接 Web 页面；不得前端直连未授权对象存储，不得提交真实证书文件或客户资料。

## 发布状态

2026-07-15 13:20:00 发布说明随 `/sprint-archive sprint-007` 标记为 published。4/4 Change 已归档。2026-07-15 13:26:33 已完成历史 AI usage 回溯，Sprint 总 AI usage snapshot 为 `actual` / `present`，覆盖 4 个 REQ、0 个 BUG 与 4 个对应 Change。
