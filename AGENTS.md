---
purpose: AI行为入口
content: AI开发流程入口、规则加载路由、OpenSpec红线、目录与部署边界
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
created_at: 2026-06-13 00:00:00
updated_at: 2026-07-11 16:25:13
note: 适用于瓷砖信息管理平台；AI执行任务前必须优先阅读本文档
---

# AI Agent 工作指南

## 1. 项目定位

本项目采用 OpenSpec + Codex Skills 规范编程方式开发，包含店主 Web 展示端、微信小程序、企业内部 Web 管理端、FastAPI 后端、SQLite/MySQL、MinIO 和 Docker Compose 环境。

技术栈硬约束：

- 后端：Python 3.12、FastAPI、Pydantic、uv、SQLite（本地/demo）、MySQL 8.0+（生产）、MinIO。
- 前端：React 19、TypeScript、Tailwind、shadcn/ui、Axios、Orval、pnpm。
- 部署：优先支持 `docker-compose.yml`。

## 2. 执行前读取路由

所有任务先读：

```text
AGENTS.md
openspec/project.md
rules/global.md
rules/language.md
rules/coding.md
rules/testing.md
rules/security.md
rules/directory-structure.md
rules/document-governance.md
rules/agent-context-budget.md
```

按任务类型追加读取：

| 任务类型 | 追加读取 |
|---|---|
| REQ / BUG 流程 | `rules/requirement-management.md`、`rules/bug-management.md`、`rules/issues-lifecycle.md`、`.agents/skills/workflow-sync/SKILL.md` |
| Sprint 流程 | `rules/iterations-lifecycle.md`、相关 `iterations/change|archive/<sprint>/` 片段 |
| OpenSpec Change | 当前 `openspec/changes/<change-id>/` 或归档目标片段 |
| API 变更 | `rules/api.md`、`docs/README.md`、`docs/03-api-index.md` 相关段、`docs/standards/api-governance.md`、`docs/standards/error-codes.md`、`src/web/orval.config.ts`、`scripts/generate-openapi-client.sh` |
| DB / 数据模型 | `rules/database.md`、`docs/04-database-design.md` 相关表段、schema / migration 文件 |
| UI / Design System | `rules/ui-design.md` 相关章节、`src/web/README.md`、`src/web/src/styles/globals.css`、`src/shared/design-system/tokens/`、`src/web/src/pages/dev/DesignSystemPage.tsx` |
| Docker / 发布部署 | `rules/environment.md`、`rules/release.md`、`docs/02-deployment.md`、`docker-compose*.yml`、`src/backend/Dockerfile`、`src/web/Dockerfile`、`src/web/nginx.conf` |
| data / media / object storage | `rules/data-management.md`、`rules/media.md`、`rules/object-storage.md`、`data/README.md`、`docs/06-video-asset-management.md`、`docs/07-object-storage-strategy.md` |
| 端口 | `rules/port-management.md`、`.env.example` |

读取原则：先定位文件和章节，再分段读取；禁止为普通任务全量 `cat docs/**`、`cat rules/*.md` 或宽泛搜索历史归档；大范围搜索和生成物/diff 复核必须遵守 `rules/agent-context-budget.md`。

## 3. Codex Skills 入口

当前项目只维护 `.agents/skills/` 作为 AI 工具入口。

| 路径 | 说明 |
|---|---|
| `.agents/skills/source-command-*` | req / bug / opsx / sprint / build 工作流技能 |
| `.agents/skills/workflow-sync` | 状态同步技能 |
| `.agents/skills/openspec-*` | OpenSpec 基础操作技能 |

不维护 `.cursor/`、`.codex/`、`.claude/`、`.opencode/`、`.kiro/`。如需恢复其他工具入口，必须先通过 OpenSpec Change 更新本文件、`rules/directory-structure.md` 与目录校验脚本。

## 4. 开发流程总览

```text
需求 / BUG（类型未决先 /capture）
→ issues/requirements 或 issues/bugs
→ /req-* 或 /bug-* 完成记录、生成、完善、评审
→ /req-opsx 或 /bug-opsx 创建 openspec/changes
→ /sprint-propose 纳入 iterations/change（仅 approved / in_sprint）
→ /sprint-apply 或 /opsx-apply 实现
→ /sprint-archive 或 /opsx-archive 归档
→ /sprint-exps 可选沉淀复盘
```

## 5. 命令族速查

| 域 | 命令链 |
|---|---|
| 智能收集 | `/capture` |
| 需求 | `/req-capture` → `/req-generate` → `/req-complete` → `/req-review --approve` → `/req-opsx` |
| 缺陷 | `/bug-capture` → `/bug-generate` → `/bug-complete` → `/bug-review --approve` → `/bug-opsx` |
| Change | `/opsx-propose`、`/opsx-explore`、`/opsx-apply`、`/opsx-archive` |
| Sprint | `/sprint-propose`、`/sprint-explore`、`/sprint-apply`、`/sprint-archive`、`/sprint-exps` |
| Bootstrap | `/initialize-project`、`/build-design-system`、`/build-api-standard`、`/build-test-framework` |

旧命令已废弃：`/requirement-to-change`、`/requirement-to-opsx`、`/bug-to-change`、`/create-iteration`。

## 6. 强制红线

- 不允许绕过 OpenSpec Change 直接开发功能。
- 不允许直接修改 `openspec/specs/`，除归档合并动作外。
- 新功能、治理扩展、目录边界变化必须先有 OpenSpec Change。
- 未评审的 REQ/BUG 不得进入 Sprint 正式规划，不得 `/req-opsx`、`/bug-opsx`、`/sprint-apply`。
- 来源于 REQ/BUG 的 OpenSpec Change 在 `/opsx-apply` 前必须先纳入某个 `sprint-xxx`；未出现在 `iterations/change|archive/<sprint>/sprint.yaml` 正式范围内时不得运行 `/opsx-apply`。
- `openspec/changes/` 必须通过 OpenSpec CLI 创建；归档才可合并到 `openspec/specs/`。
- 新建业务代码不得放根目录；目录边界以 `rules/directory-structure.md` 为准。
- 禁止创建或恢复 `docs/product/`、`docs/prd/`、`docs/bugs/`、`docs/iterations/`。
- `.env`、真实密钥、真实客户数据、运行时数据库文件、临时大文件不得提交。
- 上传必须走后端鉴权和 MinIO 适配层；前端不得直连未授权对象存储。
- 管理端与店主端必须区分权限边界。
- API 变更必须同步 OpenAPI / Orval / docs / tests。
- DB 结构变更必须同步 schema、数据库文档和测试。
- UI 变更必须遵守 Design System semantic token，禁止裸 Hex。

## 7. 文档与时间规范

新增或更新 Markdown：

- Frontmatter 必须含 `created_at` 与 `updated_at`。
- 时间字段统一 `YYYY-MM-DD HH:mm:ss`，默认 `Asia/Shanghai`。
- 更新文档只改 `updated_at`，不得改 `created_at`。
- 长期文档、issues、iterations、OpenSpec trace 均适用。

详见 `rules/document-governance.md`。

## 8. 目录边界速查

| 内容 | 位置 |
|---|---|
| 需求 | `issues/requirements/{plan,review,archive}/REQ-*` |
| BUG | `issues/bugs/{plan,review,archive}/BUG-*` |
| Sprint | `iterations/{change,archive}/sprint-*` |
| OpenSpec 变更 | `openspec/changes/<change-id>/` |
| 正式规格 | `openspec/specs/<capability>/spec.md` |
| 复盘 / 事故知识 | `docs/knowledge-base/` |
| 发布对象 | `releases/vX.Y.Z/` |
| 本地数据 | `data/`（不得提交真实客户数据和运行时数据库） |

目录迁移和校验详见 `rules/issues-lifecycle.md`、`rules/iterations-lifecycle.md`、`rules/directory-structure.md`。

## 9. Design System 执行摘要

Web 端采用“工业石材 · 暗色旗舰风”。UI 任务必须：

- 优先复用 `src/web/src/shared/templates/`、`shared/business/`、`shared/ui/`、`components/ui/`。
- 使用 `bg-page`、`text-primary`、`text-brand-gold`、`border-border-default` 等 semantic token。
- 使用 `cn()` 合并 className。
- Token 变更同步 `src/shared/design-system/tokens/`、`globals.css` 或 `pnpm sync:tokens`，并更新 `/design-system`。
- 有 prototype 时优先级：HTML > PNG Golden Reference > context > acceptance > `rules/ui-design.md` > archived specs。

详细组件、颜色、页面结构只在 UI 任务中读取 `rules/ui-design.md` 对应章节。

## 10. data / env / media / port 摘要

- `data/` 仅用于本地开发、演示、测试样例和运行时承载；禁止真实客户数据。
- `.env.example` 必须保留；新增或修改环境变量时同步说明用途、默认值和安全边界。
- MinIO 使用单 Bucket + 前缀策略：`MINIO_BUCKET`、`MINIO_PREFIX_*`。
- 默认内部端口保留 Backend `8000`、Web `3000`；宿主机端口通过 `HOST_PORT_BACKEND`、`HOST_PORT_WEB` 覆盖。
- 视频转码/压缩/多清晰度属于增强能力，必须经 OpenSpec Change。

## 11. 输出要求

回复默认中文。涉及代码必须说明：

- 文件路径与修改原因。
- 是否影响 API、数据库、Web、小程序、管理端。
- 是否需要 Orval。
- 是否需要 Docker Compose 验证。
- 是否补充或更新测试。
- 遵循了哪些 `rules/` 文件。

涉及接口：说明请求、响应、错误码。涉及数据模型：说明 SQLite/MySQL 表结构与 Pydantic Schema。

## 12. 完成检查清单

```text
□ 是否遵守 OpenSpec Change 流程
□ 来源于 REQ/BUG 的 Change 是否已纳入某个 sprint-xxx 后再 opsx-apply
□ 是否更新 issues / openspec / iterations / docs / releases（按需）
□ 是否运行 Workflow Sync（状态变化时）
□ 是否补充或更新 tests
□ 是否同步 API / DB / Orval / .env.example（按需）
□ 是否遵守目录结构与禁止目录
□ 是否遵守 MinIO 单桶策略
□ UI 是否使用 semantic token 且复用 DS 组件
□ 是否完成必要校验：目录结构、OpenSpec、Agent 上下文预算、测试、Docker（按需）
```
