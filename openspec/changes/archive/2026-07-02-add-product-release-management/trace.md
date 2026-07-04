---
change_id: add-product-release-management
requirement_id: REQ-0026-product-release-management
status: applied
created_at: 2026-07-02 14:55:51
updated_at: 2026-07-02 15:27:00
---

# Change Trace

## 基本信息

```yaml
change_id: add-product-release-management
change_type: add
status: applied
source_requirement: REQ-0026-product-release-management
sprint: sprint-004
impact:
  backend: false
  web: true
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
  commands: true
capabilities:
  new:
    - product-release-management
  modified:
    - web-client
strategy: governance-static-docs-mintlify
```

## Requirement Readiness Report

| 项 | 状态 | 说明 |
|---|---|---|
| requirement.md | ready | 已生成并评审，status `in_sprint` |
| user-stories.md | ready | 覆盖产品负责人、开发测试、运维实施、公开访客与 AI Agent |
| business-flow.md | ready | 覆盖发布范围、发布前校验、PRODUCT_VERSION 与 Mintlify 公告流程 |
| acceptance.md | ready | AC-001..038 与 AC-KB-001..003 已齐 |
| trace.md | ready | status `in_sprint`，iteration `sprint-004` |
| prototype/web | N/A | 本需求不新增应用内 UI，无 prototype |

结论：Ready，可创建 OpenSpec Change。

## Impact Analysis

```yaml
impact:
  backend: false
  web: true
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  docs: true
  commands: true
capabilities:
  new:
    - product-release-management
  modified:
    - web-client
```

说明：

- Web impact 来自 `src/shared/product-version.ts` 的发布一致性校验，不新增管理端、店主端或登录页入口。
- API/database/storage/backend impact 均为 false；本 Change 不新增后端公告 API、数据库表或对象存储策略。
- `releases/` 顶层目录必须由本 OpenSpec Change 在实现阶段先更新目录规范后再创建。

## Conflict Report

| 来源 | 优先级 | 结论 |
|---|---:|---|
| prototype | N/A | 无 prototype，无 UI 冲突 |
| acceptance.md | 1 | 作为行为验收清单 |
| rules/directory-structure.md | 2 | 约束新增顶层 `releases/` 必须先通过 OpenSpec |
| rules/release.md | 3 | 约束 `PRODUCT_VERSION` 与发布检查 |
| openspec/specs/web-client | 4 | 通过 MODIFIED delta 扩展版本号一致性要求 |

无冲突阻塞。

## Validation Results

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-07-02 14:55:51 | `openspec validate add-product-release-management --strict` | pass |
| 2026-07-02 15:27:00 | `python scripts/validate-release.py` | pass，无版本目录时仅校验模板边界并安全跳过 |
| 2026-07-02 15:27:00 | `uv run pytest tests/test_release_validation.py` | pass，4 tests |
| 2026-07-02 15:27:00 | `python scripts/validate-directory-structure.py` | pass |

## Implementation Result

| 项 | 结果 | 说明 |
|---|---|---|
| 目录治理 | implemented | `rules/directory-structure.md`、`AGENTS.md`、README、目录校验脚本已登记 `releases/` |
| 发布规则 | implemented | `rules/release.md` 已补产品发布对象、公告、门禁、命令族与版本一致性要求 |
| 发布模板 | implemented | 新增 `releases/README.md`、`mint.json`、`templates/release.json`、`templates/announcement.mdx` |
| 发布校验 | implemented | 新增 `scripts/validate-release.py`，覆盖版本、门禁、影响范围、敏感信息与 Mintlify 配置检查 |
| 自动化测试 | implemented | 新增 `tests/test_release_validation.py`，覆盖通过、版本不一致、敏感信息、缺 gate |
| 命令族 | implemented | 新增 `.cursor/commands/release-propose.md`、`release-prepare.md`、`release-publish.md` 并完成 agent 命令同步 |
| 应用入口 | not changed | 未新增管理端、登录页、店主端或小程序公告入口 |
| 后端/API/数据库 | not changed | 未新增公告 API、数据库表、Orval 或迁移 |

## Change Log

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-07-02 14:55:51 | `/req-opsx REQ-0026` | 创建 OpenSpec Change，生成 proposal/design/specs/tasks/trace |
| 2026-07-02 15:27:00 | `/opsx-apply add-product-release-management` | 完成发布目录治理、模板、校验脚本、release 命令族、测试与同步 |
