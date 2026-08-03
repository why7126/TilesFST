---
change_id: add-versioned-product-usage-docs
status: archived
created_at: 2026-08-01 09:53:42
updated_at: 2026-08-02 17:58:38
source_requirement: REQ-0088-versioned-product-usage-docs
source_requirement_path: issues/requirements/archive/REQ-0088-versioned-product-usage-docs
change_type: add
sprint: sprint-017
capabilities:
  modified:
    - product-release-management
---

# Change Trace

## 来源

- REQ：`REQ-0088-versioned-product-usage-docs`
- 需求路径：`issues/requirements/archive/REQ-0088-versioned-product-usage-docs`
- 评审状态：approved

## 影响范围

```yaml
impact:
  backend: false
  web: false
  miniapp: false
  admin: false
  database: false
  storage: false
  api: false
  release_governance: true
  docs: true
  scripts: true
capabilities:
  new: []
  modified:
    - product-release-management
```

## 关键决策

- 产品使用文档不是每个版本都自动生成。
- `/release-prepare <version>` 必须先确认是否需要生成或更新产品文档。
- 用户确认不需要时，记录 skipped rationale，不创建空 usage docs 版本目录。
- 旧版本产品内容默认冻结，非内容性维护和安全修复可自动化，内容性更正需授权留痕。

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-02 17:58:38 | /opsx-archive add-versioned-product-usage-docs | Change 已归档到 `openspec/archive/2026-08-02-add-versioned-product-usage-docs`；REQ-0088 已迁移到 archive，Workflow Sync 与 archive evidence 校验通过。 |
| 2026-08-01 11:54:37 | /opsx-modify add-versioned-product-usage-docs | 验收返修：补充 `usage-docs-generate`、`usage-docs-update`、`usage-docs-validate` 三个 Skill，作为 usage docs 生成、更新和校验的 AI 命令入口。 |
| 2026-08-01 11:54:37 | /opsx-modify add-versioned-product-usage-docs | 验收返修：确认 usage docs Skill 采用项目级轻量结构，不内嵌脚本；三个 Skill 均补充 Bundled Resources 说明，指向项目级 `scripts/`。 |
| 2026-08-01 11:13:21 | /opsx-apply add-versioned-product-usage-docs | 完成 usage docs 发布治理实现：规则、模板、生成/校验脚本、release skill、Mintlify 配置、部署说明与测试均已同步；保留 `releases/mint.json`，不迁移到 `docs.json`。 |
| 2026-08-01 10:35:08 | /sprint-propose sprint-017 | Change 纳入 `sprint-017` 正式范围，等待 `/opsx-apply add-versioned-product-usage-docs` 实现。 |
| 2026-08-01 09:53:42 | /req-opsx | 基于 REQ-0088 创建 OpenSpec Change，生成 proposal、design、delta spec、tasks 与 trace。 |

## 实现验证摘要

| 时间 | 命令 | 结果 |
|---|---|---|
| 2026-08-01 11:13:21 | `uv run pytest tests/test_release_validation.py` | 21 passed |
| 2026-08-01 11:13:21 | `python scripts/validate-directory-structure.py` | 通过 |
| 2026-08-01 11:13:21 | `python scripts/validate-release.py --release-dir releases/v0.3.2 --stage prepare` | 通过 |
| 2026-08-01 11:13:21 | `openspec validate add-versioned-product-usage-docs --strict` | 通过 |
| 2026-08-01 11:54:37 | `/opsx-modify add-versioned-product-usage-docs` | 新增三个 usage docs Skill；复核命令见本次返修输出 |
| 2026-08-02 17:58:38 | `/opsx-archive add-versioned-product-usage-docs` | OpenSpec archive、archive evidence、Workflow Sync、REQ promote、目录结构、OpenSpec specs strict 与 AI Usage hook 均通过 |

## 部署选择说明

- 本次实现保留现有 `releases/mint.json`，未迁移到 Mintlify `docs.json`。
- `域名/docs` 的真实承载方式由后续部署选择 Mintlify base path、Cloudflare/Vercel/CDN rewrite、Nginx 反向代理或等价方案；仓库内只记录边界，不提交外部凭据。
