---
purpose: docs 目录总索引
content: 主文档（编号）与治理细则（standards）导航
source: rules/document-governance.md
update_method: 新增 docs 顶层或 standards 文档时同步更新
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-21 08:36:38
---

# 文档索引

## 层 1：主文档（`docs/00–08`，按阅读顺序）

| 文档 | 说明 |
|------|------|
| [00-product-overview.md](00-product-overview.md) | 产品定位与核心场景 |
| [01-architecture.md](01-architecture.md) | 系统架构 |
| [02-deployment.md](02-deployment.md) | Docker Compose 与部署 |
| [03-api-index.md](03-api-index.md) | **API 接口清单**（实现索引） |
| [04-database-design.md](04-database-design.md) | SQLite 表结构 |
| [05-compatibility-matrix.md](05-compatibility-matrix.md) | 兼容性矩阵 |
| [06-video-asset-management.md](06-video-asset-management.md) | 视频资产 |
| [07-object-storage-strategy.md](07-object-storage-strategy.md) | 对象存储策略 |
| [08-production-image-release.md](08-production-image-release.md) | 生产镜像包构建与云服务器部署手册 |

新增主文档占用下一序号（如 `09-*.md`），**仅**用于根目录导航型文档。

## 层 2：治理细则（`docs/standards/`）

| 文档 | 说明 |
|------|------|
| [standards/api-governance.md](standards/api-governance.md) | REST、统一响应、OpenAPI First |
| [standards/error-codes.md](standards/error-codes.md) | 错误码分段与登记 |
| [standards/openapi-rules.md](standards/openapi-rules.md) | FastAPI 注解与契约 |
| [standards/authentication.md](standards/authentication.md) | JWT 鉴权 |
| [standards/file-upload.md](standards/file-upload.md) | 上传与 MinIO |
| [standards/testing-governance.md](standards/testing-governance.md) | 测试金字塔与治理 |
| [standards/unit-test-standard.md](standards/unit-test-standard.md) | 后端单元测试 |
| [standards/frontend-test-standard.md](standards/frontend-test-standard.md) | 前端 Vitest |
| [standards/test-coverage.md](standards/test-coverage.md) | 覆盖率目标 |
| [standards/xl-admin-page-acceptance-template.md](standards/xl-admin-page-acceptance-template.md) | XL 管理端页面分层验收模板 |
| [standards/admin-list-field-display-adapters.md](standards/admin-list-field-display-adapters.md) | 管理端列表 image/name/fallback adapter 检查表 |
| [standards/miniapp-device-evidence-template.md](standards/miniapp-device-evidence-template.md) | 小程序 DevTools/真机验收 evidence 模板 |
| [standards/media-five-point-acceptance-template.md](standards/media-five-point-acceptance-template.md) | 媒体五联验收模板 |
| [standards/production-media-maintenance-runbook.md](standards/production-media-maintenance-runbook.md) | 生产媒体维护作业 Runbook |
| [standards/prototype-ui-acceptance.md](standards/prototype-ui-acceptance.md) | 带 prototype 的 UI Contract、Skeleton、截图和最终一致性验收 |
| [standards/command-execution-order.md](standards/command-execution-order.md) | workflow 命令顺序与治理脚本门禁矩阵 |
| [standards/document-prose-hygiene.md](standards/document-prose-hygiene.md) | 长期文档表达卫生、slop 与 CoT 泄漏审计 |

细则文档 **不加** `00–` 序号；新增标准放入 `standards/`。

## 层 3：知识库（`docs/knowledge-base/`）

故障、事故与防御性模式沉淀，按主题命名，见 [knowledge-base/README.md](knowledge-base/README.md)。可复用预防策略优先使用 [knowledge-base/best-practices/defensive-pattern-template.md](knowledge-base/best-practices/defensive-pattern-template.md)。

## 层 4：规范工程日志（`docs/spec-logs/`）

`/spec-study` 学习其他项目 Harness 工程后生成的学习报告和 `/spec-opt` 本项目规范、技能、脚本迭代日志统一放入 [spec-logs/](spec-logs/)，通过文件名区分：`YYYYMMDDhhmmss-study-xxx.md` 与 `YYYYMMDDhhmmss-governance-xxx.md`。

[spec-logs/CHANGELOG.md](spec-logs/CHANGELOG.md) 是规范工程变更历史总账，用于汇总规范、脚本、技能、命令和治理文档更新记录；详细事实仍以单次日志、OpenSpec Change、Sprint 或 Issue 为准。

该目录只记录治理结论和脱敏摘要，不得包含用户隐私数据、真实客户数据、密钥、访问令牌、未脱敏日志、学习对象源码或截图中的个人信息。

## 需求与迭代（不在 docs/ 根目录）

| 类型 | 路径 |
|------|------|
| 需求 | `issues/requirements/{plan,review,archive}/REQ-*` |
| 缺陷 | `issues/bugs/{plan,review,archive}/BUG-*` |
| 需求/缺陷当前态看板 | `issues/requirements/CHANGELOG.md`、`issues/bugs/CHANGELOG.md` |
| 迭代 | `iterations/change/sprint-xxx/`（进行中）、`iterations/archive/sprint-xxx/`（已归档） |
| 产品版本发布 | `releases/vX.Y.Z/` |

禁止恢复 `docs/prd/`、`docs/bugs/`、`docs/iterations/`。

## AI 命令入口提示

项目级 AI 命令入口统一维护在 `.agents/skills/`，总入口与命令链以仓库根目录 [AGENTS.md](../AGENTS.md) 为准。已评审 REQ/BUG 的推荐顺序为先 `/sprint-propose` 纳入 Sprint，再 `/req-opsx` 或 `/bug-opsx` 创建并回填 Change。

规范优化入口使用 `/spec-opt`。新增或修改 `.agents/skills` 命令、`rules/` 文档、`docs/` 文档规范或 `scripts/` 治理脚本时，以 `/spec-opt` 和对应 OpenSpec Change 为准；该命令只服务治理资产，不修改业务 `src/` 代码。

推送前安全检测入口使用 `/git-check`，默认运行 `python scripts/git-check.py` 扫描 staged、modified tracked 和 untracked 文件中的真实 env、运行时数据、密钥、连接串、本机绝对路径和大文件风险。

问题排查、BUG 完善和验收返修遵守 [../rules/root-cause-evidence.md](../rules/root-cause-evidence.md)，根因状态必须区分 `unknown`、`hypothesis`、`probable`、`confirmed`；confirmed 根因必须绑定脱敏证据链。

长期文档、规则、技能说明和知识库新增或更新时遵守 [standards/document-prose-hygiene.md](standards/document-prose-hygiene.md)：事实只放在唯一归属文档，正文不写会话推理、临时草稿、review 对话、不可解析引用或未脱敏本机路径；必要时运行 `python scripts/validate-doc-prose-hygiene.py <focused-paths>`。

所有 OpenSpec Change 在 `/opsx-apply` 前都必须纳入 Sprint 正式范围。通过 `/opsx-propose` 或 `/spec-opt` 直接创建的非 REQ/BUG Change，也需要先进入 `iterations/change|archive/<sprint>/sprint.yaml` 的 `changes[]`，不得因“纯治理”或“无 REQ/BUG 来源”跳过 Sprint。

下一步命令参数保持来源对象一致：REQ 链路后续 `/opsx-apply`、`/opsx-archive` 使用原始 `REQ-*`；BUG 链路后续 `/opsx-apply`、`/opsx-archive` 使用原始 `BUG-*`；非 REQ/BUG 的直接 Change 才使用 `<change-id>`。

命令完成输出必须区分「下一步」与「待用户决策/处理」：已在「下一步」中给出的命令或动作不得重复写入「待用户决策/处理」。
