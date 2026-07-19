---
sprint_id: sprint-007
title: Sprint 007 迭代经验复盘
status: draft
created_at: 2026-07-15 13:31:45
updated_at: 2026-07-16 08:59:46
owner: product
related_iteration: iterations/archive/sprint-007/
related_requirements:
  - REQ-0036-clipboard-helper-best-practice-docs
  - REQ-0035-ai-usage-snapshot-sprint-close-exps
  - REQ-0037-auto-token-fact-source-for-workflow-commands
  - REQ-0038-brand-certificate-management
related_bugs: []
related_changes:
  - add-clipboard-helper-best-practice-docs
  - update-ai-usage-snapshot-sprint-close-exps
  - add-auto-token-fact-source-for-workflow-commands
  - add-brand-certificate-management
source: /sprint-exps sprint-007
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 007 迭代经验复盘

## 1. 迭代概况

### Fact Sheet

| 指标 | 值 |
|------|-----|
| 计划周期 | 2026-07-11 23:39:00 ~ 2026-07-15 13:20:00 |
| 当前状态 | completed / archive |
| REQ | 4（全部 archive） |
| BUG | 0 |
| Change | 4（3 add-* + 1 update-*） |
| Change archived | 4/4；readiness gate PASS |
| 估算 | 28 SP / 17.0 人天 |
| 容量 | 30 人天；占用 57%；fix buffer 43% |
| tasks 完成度 | 73/73 |
| AI usage snapshot | actual / present；coverage pass；warning_count 0 |
| 主要质量簇 | Clipboard helper best-practice、Sprint close AI usage snapshot、工作流命令 Token fact source、品牌证书管理 |

证据来源：`scripts/generate-sprint-fact-sheet.py --sprint sprint-007 --json`、`iterations/archive/sprint-007/sprint.yaml`、`iterations/archive/sprint-007/acceptance-report.md`、`data/ai-usage/sprints/sprint-007.json`。

### 交付主线

| 主线 | 交付 |
|------|------|
| 知识沉淀 | `REQ-0036` 将 Clipboard helper fallback、调用方文案与敏感值边界沉淀到长期 best-practice |
| 复盘观测 | `REQ-0035` 让 Sprint close / exps 默认消费 AI usage snapshot，避免 Sprint 006 的 estimated fallback |
| 命令治理 | `REQ-0037` 将 Token 事实源构建前移到工作流命令后置 hook，并控制成功路径输出 |
| 业务能力 | `REQ-0038` 完成管理端品牌证书 DB/API/上传/Orval/Web/验收链路 |

## 2. 流程复盘

### 做得好的

1. **Sprint 006 行动项兑现率高**：A-001、A-005 直接转化为 `REQ-0035`、`REQ-0036`，并继续深化为 `REQ-0037`。
2. **容量规划更稳**：17.0 / 30 人天，fix buffer 43%，相比 Sprint 006 的 27% 更适合承载一个 XL 业务能力。
3. **Fact Sheet 成为复盘主事实源**：本次 warnings 为空、`needs_detail=false`，复盘无需展开全部 trace/tasks。
4. **AI usage 从估算进入真实统计**：Sprint 总 snapshot 为 `actual` / `present`，覆盖 4 个 REQ 与 4 个 Change。
5. **治理能力与业务能力并行但未互相拖累**：3 个工具/文档治理 Change 先归档，`REQ-0038` 后续完成主业务交付。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Token 消耗总量极高 | snapshot 统计 total tokens 40,104,228，model call 338，tool call 650 | 虽然 snapshot 已真实可见，但流程仍需要继续降本 |
| 单个业务 Change 偏大 | `REQ-0038` 估算 8.0 人天，25/25 tasks | DB/API/上传/Orval/Web/Docker 验证集中在一个 Change，回归面较宽 |
| Sprint 文档历史链接容易滞后 | 本次 `/sprint-exps` 发现并修正 `sprint.md` 关联文档区的 `iterations/change/sprint-007/*` 旧路径 | 归档后若无检查，读者可能误跳到不存在或过期路径 |
| 后置 hook 可能带来二次输出成本 | Sprint 规划已标记“自动构建输出反向增加上下文成本” | 若 hook 成功路径输出过多，会抵消 Token 节省目标 |

### 优化建议

1. **把高 token 命令拆成摘要优先**：Fact Sheet、Workflow Sync、AI usage hook 成功路径只输出 status、计数、warning 与 recommended_action。
2. **继续控制 archive 读取边界**：复盘和 close 命令从 `sprint.yaml` 精确解析 Change archive path，不全扫 `openspec/changes/archive/**`。
3. **XL 业务能力前置拆层验收**：后续 DB/API/上传/Web 同时出现时，在 tasks 中强制分层验证和失败日志摘要。
4. **归档后自动修正文档路径**：Sprint archive 或 exps 可检查四件套中 `iterations/change/<sprint>` 的残留引用。

## 模型 Token 使用分析

### Token Usage Fact Sheet

| 指标 | 值 | 证据/说明 |
|------|----|-----------|
| 精确 token 统计 | 有 | 来源：`data/ai-usage/sprints/sprint-007.json`，由 Fact Sheet 暴露 |
| AI usage mode | actual | Fact Sheet: `ai_usage_snapshot.ai_usage_mode` |
| Snapshot status | present | Fact Sheet: `ai_usage_snapshot.snapshot_status` |
| Command run 数 | 16 | snapshot totals |
| Model call 数 | 338 | snapshot totals |
| Tool call 数 | 650 | snapshot totals |
| Input tokens | 39,694,597 | snapshot totals |
| Cached input tokens | 38,245,888 | snapshot totals |
| Output tokens | 193,657 | snapshot totals |
| Reasoning output tokens | 21,099 | snapshot totals |
| Total tokens | 40,104,228 | snapshot totals |
| Retry count | 0 | snapshot totals |
| 主要输入消耗 | 高 | 4 个 Change、73 tasks、工作流命令集成、品牌证书全链路、规则与技能读取 |
| 主要输出消耗 | 中 | Workflow Sync、OpenSpec archive/validate、AI usage snapshot/hook、测试与 Docker 验证摘要 |
| 重复/浪费来源 | 中 | 规则/技能重复读取、archive 历史检索风险、长测试日志和同步报告输出 |
| 已采用节省策略 | 有 | Fact Sheet 优先、`needs_detail=false` 不展开 trace/tasks、索引/样例分段读取 |

### 高消耗来源

| 来源 | 影响 | 证据 | 优化方案 |
|------|------|------|----------|
| 工作流命令 Token fact source | high | `REQ-0037` 涉及 `/req-*`、`/bug-*`、`/opsx-*`、`/sprint-*` 后置 hook | 成功路径只输出紧凑 summary；失败时保留 recommended_action，不阻断主流程 |
| 品牌证书管理全链路 | high | `REQ-0038` 覆盖 DB/API/上传/Orval/Web/Docker，25 tasks | 按 DB/API、上传、Orval/Web、Docker 边界分段验证；测试失败只贴关键失败段 |
| Sprint 四件套 | high | Fact Sheet 标记 `sprint.md` >= 200 行 | `/sprint-exps` 默认读自动 Fact Sheet；只有 warnings/needs_detail 时分段回读 |
| OpenSpec changes | medium | 4 个 Change，73/73 tasks | 复盘只引用 Change 计数、状态和 archive path，不复制 tasks 原文 |
| Archive lookup | medium | Fact Sheet 标记 archive lookup 风险 | 从 `sprint.yaml` 解析精确 archive 目录，默认排除 `openspec/changes/archive/**` 宽泛搜索 |
| 规则与 Skill 读取 | medium | AGENTS、通用 rules、Sprint skill 是命令前置要求 | 同一会话复用已读规则摘要；仅在文件变更或任务类型切换时补读 |
| Workflow Sync / 校验输出 | medium | close 和 archive 类命令会产生 updated/skipped、readiness、validate 输出 | 成功路径保留摘要和计数；失败路径再展开具体 marker、文件和短片段 |

### 对照预算规则

| 行为 | 结论 | 说明 |
|------|------|------|
| Fact Sheet 优先 | 符合 | 先运行 `generate-sprint-fact-sheet.py --json`，并使用 `warnings` / `needs_detail` 决定回读范围 |
| 搜索排除 | 符合 | 复盘阶段没有全量读取 `openspec/changes/archive/**`、generated、node_modules、dist |
| 分段读取 | 符合 | 只读取知识库索引、Sprint 006 样例和 Sprint 007 相关片段 |
| 大输出处理 | 基本符合 | Fact Sheet 输出较长但结构化；后续 hook 应继续压缩为紧凑 summary |
| 精确 token 计量 | 符合 | 本 Sprint 已提供 actual snapshot，未使用 estimated fallback |

### 优化行动项

| ID | 优先级 | 描述 | 建议下一步 | 状态 |
|----|--------|------|------------|------|
| T-001 | P1 | 为 Workflow Sync 与 AI usage hook 固化 compact summary 输出，成功路径不展示完整文件列表或 snapshot 明细 | `/opsx-propose` | open |
| T-002 | P1 | 为 Sprint archive / exps 增加归档后路径残留检查，自动发现 `iterations/change/<sprint>` 旧链接 | `/opsx-propose` | open |
| T-003 | P2 | 对 XL 业务 Change 建立“DB/API/上传/Web/Docker”分层验收模板，降低单 Change 回归展开成本 | `/req-capture` | open |
| T-004 | P2 | 将已读规则摘要复用写入命令运行上下文，减少连续 Sprint 命令重复读取 `rules/` 与 Skill 文件 | `/req-capture` | open |

## 3. 需求与设计

### 正向经验

| 条目 | 经验 |
|------|------|
| REQ-0036 | 把跨页面 Clipboard 行为从“经验提醒”沉淀为可索引 best-practice，降低复制入口重复踩坑概率 |
| REQ-0035 | 把 AI usage snapshot 接入 Sprint close / exps，让复盘有真实统计并能识别 coverage 状态 |
| REQ-0037 | 命令级后置 hook 把成本观测从 Sprint 末尾前移到每次工作流命令，方向正确 |
| REQ-0038 | 品牌证书管理一次性覆盖数据、接口、上传、前端和横切 UI gate，避免只交付孤立页面 |

### 设计缺口

| 缺口 | 表现 | 建议 |
|------|------|------|
| Compact 输出规范仍需继续产品化 | 本 Sprint 识别了输出反向增加成本的风险 | 下一 Sprint 用 Change 明确各命令成功/失败输出契约 |
| XL Change 验收模板尚未长期沉淀 | `REQ-0038` 依靠 tasks 分层推进，但模板化不足 | 抽象为 best-practice 或 OpenSpec task checklist |
| 归档路径残留缺自动门禁 | `sprint.md` 关联文档中存在 change/archive 路径漂移 | 在 `/sprint-archive` 或 `/sprint-exps` 加轻量检查 |

## 4. 开发与质量

### 重复模式与预防

| 模式 | 关联条目 | 根因摘要 | 预防建议 |
|------|----------|----------|----------|
| 文档/流程能力产品化 | REQ-0035、REQ-0036、REQ-0037 | Sprint 006 复盘行动项需要进入正式 Issue/Change 才能闭环 | 复盘行动项必须标注下一命令和优先级，下一 Sprint planning 时逐项承接 |
| 管理端上传链路复合风险 | REQ-0038 | 文件大小、MIME、MinIO、Nginx、前端状态机和权限同时参与 | 继续复用 `admin-media-upload-chain.md`，并保留 Docker `:3000` 上传边界验收 |
| 管理端列表/弹窗一致性 | REQ-0038 | 证书管理命中列表、弹窗、toast、分页、确认框多项横切 UI 契约 | 新管理端页面默认引用 admin-list / admin-modal best-practice |
| Token 成本可见但仍偏高 | REQ-0035、REQ-0037 | 观测能力建成后暴露真实成本规模 | 将“compact summary、分段读取、archive 精确路径”作为命令验收标准 |

### 测试覆盖

| 方向 | 观察 |
|------|------|
| 工具链 | `REQ-0035`、`REQ-0037` 覆盖 snapshot、coverage、post-command hook、失败降级与脱敏 |
| 文档 | `REQ-0036` 覆盖 best-practice 文档和知识库入口 |
| 后端 / DB / API | `REQ-0038` 覆盖品牌证书表、Schema、管理端接口、错误码和权限 |
| 媒体上传 | `REQ-0038` 覆盖证书文件上传、大小/MIME 边界、MinIO 前缀策略和 Docker `:3000` 验收 |
| 前端 | `REQ-0038` 覆盖管理端列表、弹窗、预览、上传状态和横切 UI gate |
| 归档校验 | Sprint Archive Readiness PASS，4/4 Change archived，73/73 tasks 完成 |

## 5. 可复用抽象

| 机会 | 已有成果 | 后续建议 |
|------|----------|----------|
| Clipboard helper best-practice | 长期知识库文档与索引入口 | 新复制入口必须引用 best-practice，并明确敏感值和 fallback 文案 |
| AI usage fact source | Sprint snapshot actual/present，coverage pass | 后续命令默认生成 compact hook summary，并沉淀异常处理手册 |
| 工作流命令 post-command hook | 命令运行后可刷新事实源 | 明确 hook 不阻断主流程的条件，以及 Sprint close 的强 gate 条件 |
| 品牌证书管理 | 品牌资质/检测报告/荣誉证书结构化管理 | 后续可复用证书上传、预览、状态筛选和过期提醒模式 |
| 管理端横切 UI gates | 列表、弹窗、上传、主题矩阵继续复用 | 建议形成 XL 管理端页面 task checklist |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P1 | 为 Workflow Sync 与 AI usage hook 建立 compact summary 输出 Change，压缩成功路径日志 | `/opsx-propose` | 工具链 | open |
| A-002 | P1 | 为 Sprint archive / exps 增加 change/archive 路径残留检查，避免归档后关联文档旧链接 | `/opsx-propose` | 工具链 | open |
| A-003 | P2 | 沉淀 XL 管理端页面分层验收模板，覆盖 DB/API/上传/Orval/Web/Docker/横切 UI gate | `/req-capture` | 产品 + 前后端 | open |
| A-004 | P2 | 将规则/Skill 已读摘要复用机制纳入命令上下文预算治理，减少连续命令重复读取 | `/req-capture` | 工具链 | open |
| A-005 | P2 | 为品牌证书能力补充后续运营验收观察点：过期证书提醒、证书类型统计、批量维护 | `/sprint-propose` | 产品 | planned：已承接到 `iterations/change/sprint-008/` 的待评审观察点 |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-007-retrospective.md` | 新建 | 本文档 |
| `best-practices/clipboard-fallback.md` | 已承接 | `REQ-0036` 输出长期 Clipboard helper best-practice |
| `best-practices/admin-list-page-consistency.md` | 沿用 | `REQ-0038` 管理端列表页继续复用 |
| `best-practices/admin-modal-width-css-cascade.md` | 沿用 | `REQ-0038` 弹窗宽度与矮视口滚动继续复用 |
| `best-practices/admin-media-upload-chain.md` | 沿用 | `REQ-0038` 上传链路继续复用 |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-07-15 13:31:45 | 初稿（`/sprint-exps sprint-007`） |
