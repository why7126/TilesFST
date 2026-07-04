---
sprint_id: sprint-004
title: Sprint 004 迭代经验复盘
status: draft
created_at: 2026-07-04 12:34:17
updated_at: 2026-07-04 12:34:17
owner: product
related_iteration: iterations/archive/sprint-004/
related_requirements:
  - REQ-0018-production-mysql-deployment
  - REQ-0019-admin-superuser-protection
  - REQ-0022-admin-api-docs-menu
  - REQ-0023-api-docs-swagger-detail-link
  - REQ-0025-brand-logo-fst-favicon
  - REQ-0026-product-release-management
  - REQ-0024-product-usage-logging
related_bugs:
  - BUG-0050-user-create-validation-message-unclear
  - BUG-0051-api-docs-swagger-ui-link-wrong
  - BUG-0052-api-docs-metric-cards-inconsistent
  - BUG-0053-api-docs-list-layout-pagination-inconsistent
  - BUG-0054-admin-content-padding-too-large
  - BUG-0055-admin-list-layout-unification
related_changes:
  - add-production-mysql-deployment
  - update-admin-superuser-protection
  - fix-user-create-validation-message-unclear
  - add-admin-api-docs-menu
  - add-api-docs-swagger-detail-link
  - fix-api-docs-swagger-ui-link-wrong
  - fix-api-docs-metric-cards-inconsistent
  - fix-api-docs-list-layout-pagination-inconsistent
  - update-brand-logo-fst-favicon
  - add-product-release-management
  - add-product-usage-logging
  - fix-admin-content-padding-too-large
  - fix-admin-list-layout-unification
source: /sprint-exps
note: 由 AI 初稿生成，须人工 Review 后改为 published
---

# Sprint 004 迭代经验复盘

## 1. 迭代概况

### Fact Sheet

| 指标 | 值 |
|------|-----|
| 计划周期 | 2026-06-29 10:03:38 ~ 2026-07-13 18:00:00 |
| 实际归档 | 2026-07-04 08:13:26（`/sprint-archive sprint-004`） |
| REQ | 7（全部 done / archive） |
| BUG | 6（全部 done / archive） |
| Change | 13（5 add-* + 2 update-* + 6 fix-*） |
| Change archived | 13/13；`openspec list --json` 无活动 change |
| 估算 | 83 SP / 60.5 人天 |
| fix-* 占比 | 6/13 ≈ 46% |
| 中途追加 | 12 项追加：REQ-0019、BUG-0050、REQ-0022、BUG-0051/0052/0053、REQ-0025/0023/0026/0024、BUG-0054/0055 |
| 主要质量簇 | 接口文档页 3 个 BUG；管理端列表/布局 2 个 BUG |
| 已知校验残留 | API governance 多次记录既有 admin route `tags` 缺口；2 个已归档 Change 的 tasks 仍有未勾选项 |

### 交付主线

| 阶段 | 事件 |
|------|------|
| 2026-06-29 | REQ-0018 作为基础设施主线进入 Sprint，完成 MySQL / 生产 Compose / MinIO smoke |
| 2026-06-30 | 追加超级管理员保护与创建用户错误提示修复，形成用户管理安全与体验闭环 |
| 2026-07-01 ~ 2026-07-02 | 追加接口文档页及 3 个接口文档 UI/代理修复；同步引入行级 Swagger 深链 |
| 2026-07-02 | 追加品牌展示、产品发布治理、产品使用日志能力 |
| 2026-07-03 ~ 2026-07-04 | 追加 Admin Shell padding 与 8 个管理端列表页统一，最后完成归档 |

证据：`iterations/archive/sprint-004/sprint.md` §Sprint 目标、§Scope、§变更记录；`iterations/archive/sprint-004/acceptance-report.md` §验收记录。

## 2. 流程复盘

### 做得好的

1. **归档闭环完整**：13 个 Change 全部进入 `openspec/changes/archive/`，Sprint 迁入 `iterations/archive/sprint-004/`，release-note 标记为 published。
2. **评审门禁基本有效**：BUG-0051 首次纳入时曾因未评审只进入延后项，评审通过后才写入正式范围。
3. **跨 Sprint 知识有被引用**：REQ-0019、REQ-0022、REQ-0023、REQ-0024 均显式引用 `admin-list-page-consistency.md` 或 sprint-003 复盘，并写入横切 AC。
4. **高风险基础设施有 smoke**：REQ-0018 记录了 MySQL schema init、admin seed、登录、MinIO 上传和 `/media/{object_key}` 读取验证。
5. **测试记录密集**：REQ-0024、BUG-0055 等记录了多轮 pytest / Vitest / build / OpenSpec strict / directory validate，覆盖面比早期 Sprint 更强。

### 问题

| 问题 | 证据 | 影响 |
|------|------|------|
| Scope 持续膨胀 | `sprint.md` 从单一 REQ-0018 扩到 7 REQ + 6 BUG，fix_buffer 最终为 0 | 容量管理失真，Sprint 从基础设施主线变成多主线并行 |
| 接口文档页连续出 3 个 BUG | BUG-0051/0052/0053 均关联 REQ-0022 | 首版 add-* 功能验收偏功能正确，结构/代理/分页细节需追加 fix |
| 管理端列表抽象仍未落地 | BUG-0055 根因指出 8 个页面分别拼装标题、指标卡、筛选、表格、分页 | 横切一致性依赖批量修复，仍缺 `AdminListPage` 级契约 |
| 已归档 Change tasks 不完全干净 | `add-product-usage-logging` tasks 30/2，`fix-admin-content-padding-too-large` tasks 18/4 | 归档状态与 tasks 勾选不一致，影响后续审计可信度 |
| API governance 既有债反复出现 | 多个 trace 记录 `validate-api-standard.py` 因既有 admin route tags 失败 | 新 Change 可通过但全局质量门禁噪声高，容易掩盖新增问题 |
| workflow-sync check 存在时间漂移 | sprint-archive 后 `--check` 因 trace `updated_at` 派生时间反复漂移 | 工具链幂等性不足，归档后 check 不能稳定作为 CI gate |

### 优化建议

1. **Sprint scope 冻结**：进入 apply 后只接受 P0/P1 阻断项；其他项先 `/req-capture` 或 `/bug-capture`，下一 Sprint 排期。
2. **归档前 tasks gate**：`/sprint-archive` 前脚本化检查 sprint 内所有 archived change 的 `tasks.md` 是否仍有 `- [ ]`。
3. **治理债单独清理**：API governance route tags 作为独立修复 Change，避免每个 API 相关任务都带着同一条 known-debt。
4. **workflow-sync 幂等修复**：将派生的 archived 时间固定为 change archive trace，而不是每次 trace `updated_at`，或 check 模式忽略同步脚本自身 touch 时间。

## 3. 需求与设计

### PRD 与原型

- **REQ-0018** 是基础设施需求，无 UI 原型，acceptance 可测性强，能直接映射到配置、DDL、Compose、MinIO 与测试项。
- **REQ-0022 / REQ-0023 / REQ-0024** 均有 HTML/context，REQ-0024 还补齐 PNG Golden Reference；但接口文档页仍连续产生结构与交互类 BUG，说明 HTML 原型之外还需要共享 DOM 契约和跨页面矩阵。
- **REQ-0025** 明确原型承载页与真实需求边界，避免 Banner 管理页面主体被误纳入范围，这是本 Sprint 文档质量的正向例子。
- **REQ-0026** 将发布治理、`releases/` 顶层目录、Mintlify 公告和校验脚本一次性纳入 OpenSpec，避免绕过目录治理。

### 评审深度

| 需求 | 观察 | 经验 |
|------|------|------|
| REQ-0022 | 功能范围覆盖接口目录、Swagger、Orval，但 BUG-0051/0052/0053 说明 Web 代理、metric DOM、分页 DOM 未在首版验收中强制穿透 | 管理端新页面 review 应同时检查功能、部署代理、列表页横切 DOM |
| REQ-0024 | 日志能力同时涉及后端日志、事件字典、脱敏、管理端页面和 Golden PNG | 大型治理需求必须在 design 中拆出数据模型、事件字典、安全脱敏和 UI gate |
| REQ-0026 | 发布治理明确不新增管理端入口、不新增后端 API | “明确不做”有效压住范围膨胀，适合复制到治理类 REQ |

### 文档模板建议

| 字段/门禁 | 建议 |
|-----------|------|
| 管理端新列表页 | acceptance MUST 含模块顺序、metric DOM、filter reset、sticky action column、最多 5 页码 |
| Swagger / docs 入口 | design MUST 声明 dev / Docker / production 代理路径和 Try It Out 策略 |
| 大型治理 REQ | design MUST 含“不包含”边界、敏感信息清单、数据保留周期和发布/回滚说明 |
| Sprint archive | acceptance-report 与 tasks.md 勾选状态必须一致后再关闭 |

## 4. 开发与质量

### 重复 BUG / 模式

| 模式 | 次数 | 关联 BUG | 根因摘要 | 预防建议 |
|------|------|----------|----------|----------|
| 接口文档页代理/结构/分页不足 | 3 | BUG-0051/0052/0053 | REQ-0022 首版聚焦功能，未完整覆盖 Web 代理、metric DOM、列表分页 | 新管理端页面增加代理与 DOM 基线 checklist |
| 管理端列表页横切不一致 | 2 | BUG-0054/0055 | Admin Shell spacing、content width、列表结构缺统一事实源 | `/req-capture` AdminListPage + Shell layout contract |
| 表单校验错误结构不统一 | 1 | BUG-0050 | Schema 层 Pydantic 校验早于业务校验，统一错误 envelope 未覆盖默认 422 | 建立 RequestValidationError 统一转换或字段校验收敛策略 |
| 发布/归档门禁噪声 | 多次 | API governance known-debt、workflow-sync check drift | 工具链本身有已知失败与非幂等行为 | 将工具链缺陷单独列 REQ/BUG，不混在业务 Change 中 |

### 测试覆盖

- **后端**：REQ-0018 覆盖 MySQL schema/admin seed/API；REQ-0024 多轮 `test_product_usage_logging.py` 与 `test_auth.py`。
- **前端**：接口文档页回归最高频，REQ-0023 多轮 19 tests；BUG-0055 覆盖 9 files / 49 tests，并追加全量相关测试 43 files / 193 tests。
- **构建/部署**：BUG-0051 记录 Web build 与 `docker compose build web`，REQ-0018 记录外部 MySQL + MinIO smoke。
- **缺口**：BUG-0054 的浏览器视觉验收因当前环境缺少可启动浏览器保持 pending；REQ-0024 / BUG-0054 tasks 未全部勾选但已归档。

### 归档质量

本 Sprint 归档结果“目录状态”已闭环，但“任务清单状态”暴露两个问题：

| Change | tasks | 说明 |
|--------|-------|------|
| `add-product-usage-logging` | 30/2 | tasks 仍有验证项未勾选，但 trace 记录多轮 pytest/Vitest/Orval/OpenSpec/目录校验 |
| `fix-admin-content-padding-too-large` | 18/4 | 浏览器视觉验收 pending，仍归档 |

建议下一轮 `/sprint-archive` 将 `tasks_incomplete > 0` 作为强阻断，除非用户显式 `--force` 并在 acceptance-report 写明。

## 5. 可复用抽象

| 机会 | 涉及 REQ/页面 | 建议 |
|------|---------------|------|
| `AdminListPage` 模板 | SKU、品牌、类目、规格、Banner、用户、日志、接口文档 | 统一标题、指标卡、筛选、列表、分页、sticky action column |
| `MetricCard` / summary strip | SKU、接口文档、日志审计 | 防止 `.metric-value` / `.metric-desc` DOM 再次漂移 |
| `PaginationWindow` 工具 | 8 个管理端列表页 | 已在 BUG-0055 形成测试基础，建议提升为共享 util + 页面契约 |
| `SwaggerLinkPolicy` 文档/工具 | `/admin/api-docs` | 统一 `/docs#/{tag}/{operationId}`、非 OpenAPI 禁用态、无 token 泄露 |
| `RequestValidationError` envelope | 用户管理及后续表单 API | 将 Pydantic 默认 422 纳入统一响应，避免页面兜底文案 |
| `ReleaseGate` 校验 | REQ-0026 及后续发布 | 将产品版本、OpenSpec archive、测试、Orval、Docker、DB、env、Mintlify 作为发布前事实源 |

## 6. 行动项

| ID | 优先级 | 描述 | 建议下一步 | 负责人建议 | 状态 |
|----|--------|------|------------|------------|------|
| A-001 | P0 | 修复 `/sprint-archive` 前 tasks 未完成也可归档的问题 | `/bug-capture` 归档门禁 tasks_incomplete 漏检 | 工具链 | open |
| A-002 | P1 | 落地 `AdminListPage` / 管理端列表页契约，吸收 BUG-0055 经验 | `/req-capture` AdminListPage 模板与验收页 | 前端 | open |
| A-003 | P1 | 抽象 `MetricCard` 与分页窗口工具，减少页面局部 DOM 漂移 | `/req-capture` 管理端列表基础组件 | 前端 | open |
| A-004 | P1 | 清理 API governance 既有 route tags 失败 | `/bug-capture` API governance tags known-debt | 后端 | open |
| A-005 | P1 | 修复 workflow-sync `--check` 时间漂移幂等性 | `/bug-capture` workflow-sync check drift | 工具链 | open |
| A-006 | P2 | 将 Swagger Web 代理和生产 Try It Out 策略写入接口文档页模板 checklist | `/req-capture` 或下一次 API docs refine | 前端/DevOps | open |
| A-007 | P2 | 将统一 422 envelope 设计扩展到所有管理端表单 API | `/req-capture` API validation envelope governance | 后端 | open |
| A-008 | P2 | 复核 `acceptance-report.md` 中仍显示待 sign-off / unchecked 的历史内容 | 人工 QA review 后更新 accepted 报告 | QA | open |

## 7. 知识库沉淀清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `retrospectives/sprint-004-retrospective.md` | 新建 | 本文档 |
| `best-practices/admin-list-page-consistency.md` | 建议更新 | 已有未归属本命令的工作区修改；本次不覆盖，建议人工合并 BUG-0055 的 8 页面矩阵 |
| `best-practices/admin-form-page-consistency.md` | 沿用 | 继续作为 REQ-0022 等管理端页面横切参考 |
| `best-practices/admin-modal-width-css-cascade.md` | 沿用 | BUG-0050 表单错误提示仍需避免弹窗宽度回归 |

## 8. 变更记录

| 时间 | 说明 |
|------|------|
| 2026-07-04 12:34:17 | 初稿（`/sprint-exps sprint-004`） |
