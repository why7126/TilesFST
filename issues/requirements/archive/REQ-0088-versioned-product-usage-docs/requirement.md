---
requirement_id: REQ-0088-versioned-product-usage-docs
title: 版本化产品使用文档生成与发布治理
terminal: multi
version: v1
status: done
owner: product
source: capture.md
priority: P1
parent_requirement:
created_at: 2026-08-01 08:18:25
updated_at: 2026-08-02 17:59:12
---

# REQ-0088 版本化产品使用文档生成与发布治理

## 1. 需求背景

项目已建立产品版本发布目录 `releases/`、产品版本发布对象 `release.json`、Mintlify 公告源文件 `announcement.mdx` 和发布门禁。当前 Mintlify 主要用于发布公告，尚未形成“产品使用文档”这一层对外可浏览、可版本化、可按需随发版生成和校验的治理能力。

产品方希望基于 Mintlify 搭建产品使用文档站，并计划通过 `域名/docs` 访问。产品文档并非每个产品版本都必须生成或更新；发版准备阶段应先向用户确认本次是否需要生成或更新产品使用文档。只有确认需要时，才生成当前版本产品文档，使客户、店主、实施、运维和项目团队能够查看与该版本一致的操作说明、功能入口、注意事项和版本差异。

如果产品文档仅靠人工临时维护，会出现以下风险：

- 发版时缺少“是否需要更新产品文档”的显式确认，导致该更新时漏更，或不该更新时生成无意义版本。
- 文档内容与当前 `release.json`、管理端菜单、小程序页面或已归档 Change 不一致。
- 新版本文档覆盖旧版本产品行为说明，导致无法回看历史版本。
- 旧版本文档完全禁止自动化维护，又会导致 broken links、Mintlify 配置升级、frontmatter 补齐、安全修复等长期维护成本过高。
- 产品文档生成、更新、发布校验缺少明确命令和规范，难以纳入 Review 与 CI。

本需求用于把产品使用文档从“人工补充材料”升级为发布治理能力：定义版本化目录、生成与校验命令、发布门禁、Mintlify 导航、`/docs` 浏览方式、安全扫描和旧版本维护策略。

## 2. 目标用户

| 角色 | 诉求 |
|---|---|
| 店主 / 客户 / 公开访客 | 通过 `/docs` 查看当前或历史版本的产品使用说明、功能入口和操作注意事项。 |
| 企业内部员工 | 查看管理端功能的操作说明，例如 SKU、品牌、类目、规格、证书、Banner、用户、系统设置和日志审计。 |
| 实施 / 运维 | 在上线和培训时使用与发布版本一致的产品说明，减少口头同步和临时截图。 |
| 产品负责人 / 项目负责人 | 在发版准备阶段确认本次是否需要生成或更新产品文档；需要时确认覆盖范围，不需要时记录跳过原因。 |
| 开发 / 测试 | 通过固定命令校验文档 manifest、导航、broken links、敏感信息和页面覆盖。 |
| AI Agent | 按规则生成、更新、校验产品文档，不随意改写旧版本产品行为说明。 |
| 评审者 | 通过 `release.json`、`usage-docs/manifest.json` 和 Mintlify 配置追踪文档来源与更新边界。 |

## 3. 范围

### 3.1 本期包含

- 定义版本化产品使用文档目录，例如 `releases/vX.Y.Z/usage-docs/`。
- 定义当前版本文档 manifest，例如 `releases/vX.Y.Z/usage-docs/manifest.json`。
- 定义产品文档生成命令，例如 `/usage-docs-generate <version>` 或等价脚本。
- 定义产品文档校验命令，例如 `/usage-docs-validate <version>` 或等价脚本。
- 将“是否需要生成或更新产品文档”的确认点接入 `/release-prepare <version>`，仅在确认需要时执行生成与校验。
- 扩展 `release.json`，增加 `usage_docs` 元数据和 `usage_docs_preview` 发布门禁。
- 更新 Mintlify 配置，使版本公告和产品使用文档都能在文档站导航中访问。
- 支持文档站通过 `域名/docs` 浏览，并明确子路径、反向代理或托管平台 rewrite 的部署边界。
- 定义当前版本、旧版本、人工修改、自动化维护和安全修复的规则。
- 基于管理端导航、小程序页面配置和发布范围，校验产品文档覆盖度。
- 增加文档安全扫描，避免公开文档泄露密钥、真实客户数据、内部连接串或不可公开运维信息。
- 增加测试或校验，覆盖 manifest、导航、broken links、敏感信息和旧版本改写策略。

### 3.2 本期不包含

- 不在 PRD 阶段直接实现命令、脚本、Mintlify 配置或目录迁移。
- 不新增后端数据库表或产品文档 API。
- 不把产品使用文档入口加入管理端菜单、登录页、小程序或店主 Web，除非后续 Change 另行确认。
- 不要求产品文档覆盖内部运维密钥、数据库连接、MinIO 凭据、生产私有域名等敏感内容。
- 不自动生成完整截图、视频教程或交互式培训课件。
- 不实现 Mintlify 账号、域名、DNS、Cloudflare、Vercel 或生产 Nginx 的真实线上配置；本期只定义项目内源文件、校验和部署边界。
- 不替代 `docs/` 长期技术文档、`openspec/specs/` 正式能力规格、`issues/` 需求/缺陷记录或 `iterations/` Sprint 四件套。
- 不把旧版本产品内容设置为绝对不可自动维护；旧版本内容默认冻结，但允许受控的非内容性维护和安全修复。

## 4. 功能要求

### FR-001 版本化产品使用文档目录

系统 MUST 为每个产品版本提供独立的产品使用文档目录。

推荐结构：

```text
releases/
└── vX.Y.Z/
    ├── release.json
    ├── announcement.mdx
    └── usage-docs/
        ├── manifest.json
        ├── overview.mdx
        ├── admin/
        └── miniapp/
```

`usage-docs/` MUST 只承载该版本公开产品使用文档、文档 manifest 和必要的 Mintlify 页面源文件。

`usage-docs/` MUST NOT 存放运行时站点构建产物、真实客户数据、密钥、数据库连接串、Authorization header、Cookie 或不可公开运维信息。

### FR-002 产品文档 manifest

每个版本的 `usage-docs/manifest.json` MUST 作为该版本产品文档事实源，记录生成来源、版本、输入、人工维护和自动化策略。

manifest SHOULD 至少包含：

| 字段 | 说明 |
|---|---|
| `version` | 产品版本，例如 `v0.3.2`。 |
| `generated_at` | 文档生成时间，格式为 `YYYY-MM-DD HH:mm:ss`。 |
| `source_version` | 从哪个历史版本复制或迁移。 |
| `source_release` | 对应 `release.json` 路径和 hash。 |
| `input_files` | 参与生成或覆盖校验的导航、路由、小程序配置、发布对象等文件。 |
| `pages` | 当前版本文档页面清单。 |
| `coverage` | 管理端菜单、小程序页面、发布影响范围的覆盖摘要。 |
| `manual_overrides` | 人工修改记录或声明。 |
| `automation_policy` | 当前版本和旧版本的自动化维护策略。 |

manifest MUST 支持发布校验判断当前版本产品文档是否存在、是否过期、是否覆盖必要入口，以及是否有旧版本内容性改写风险。

### FR-003 产品文档生成决策

发布准备阶段 MUST 先确认本次是否需要生成或更新产品文档。

确认规则：

- `/release-prepare <version>` SHOULD 向用户展示本次发布影响范围、上一版本文档状态和可能触发文档更新的变更，并要求用户确认是否生成或更新 `usage-docs/`。
- 若用户确认需要生成或更新，流程 MUST 执行产品文档生成与校验。
- 若用户确认不需要生成或更新，流程 MUST 在 `release.json` 中记录跳过原因、确认时间和确认人或确认来源。
- 若用户未确认，流程 MUST 不得自动生成新版本产品使用文档，并应记录 blocker 或待确认项。

触发确认的参考因素 SHOULD 包括：

- 本次发布新增或修改用户可见功能。
- 管理端菜单、页面、字段、操作流程或权限边界变化。
- 小程序页面、入口、TabBar、搜索、详情、证书、品牌或收藏流程变化。
- 产品使用步骤、公开说明、已知问题、版本差异或培训材料需要更新。
- Mintlify 导航、文档目录、旧版本维护策略或公开安全边界变化。

### FR-004 产品文档生成命令

系统 SHOULD 提供产品文档生成命令，例如：

```text
/usage-docs-generate <version>
```

生成命令 MUST：

- 读取 `releases/<version>/release.json`。
- 校验本次发布已确认需要生成或更新产品文档；未确认时必须阻断。
- 识别上一产品版本的 `usage-docs/`，并可作为当前版本文档基础。
- 生成或更新当前版本 `releases/<version>/usage-docs/**`。
- 生成或更新当前版本 `usage-docs/manifest.json`。
- 从管理端导航、Web 路由、小程序页面配置和本次发布影响范围中提取文档覆盖线索。
- 对当前版本文档执行增量生成或覆盖更新。
- 不在无明确授权时改写旧版本产品行为、操作步骤、功能说明或版本差异。
- 记录无法自动生成或需要人工补充的待确认项。

生成命令 MAY 使用模板方式先生成草稿，再由人工 Review；不得把未确认推断伪装成已发布事实。

### FR-005 产品文档校验命令

系统 SHOULD 提供产品文档校验命令，例如：

```text
/usage-docs-validate <version>
```

校验命令 MUST 检查：

- `releases/<version>/usage-docs/manifest.json` 存在且结构合法。
- 当前版本产品文档页面清单与 Mintlify 导航一致。
- 当前版本公告和产品使用文档均可被 Mintlify 导航访问。
- Mintlify broken links、build、preview 或等价静态校验通过。
- 产品文档不包含密钥、真实客户数据、数据库连接串、Authorization header、Cookie 或不可公开运维信息。
- 管理端主要菜单、小程序主要页面和本次发布影响范围有文档覆盖或明确豁免理由。
- 自动化没有在无明确授权时改写旧版本内容性文档。

校验失败时 MUST 输出失败原因、涉及文件和建议修复方向。

### FR-006 release-prepare 集成

`/release-prepare <version>` MUST 集成产品文档生成决策，并在确认需要时执行产品文档生成和校验。

发布准备阶段 SHOULD 执行：

```text
生成 announcement.mdx
确认本次是否需要生成或更新 usage-docs
  ├─ 需要：生成 usage-docs/** → 校验 usage-docs manifest → 校验 Mintlify 导航和 broken links → 记录 usage_docs_preview gate
  └─ 不需要：记录 usage_docs status=skipped、确认来源和跳过原因
校验 release.json
```

`release.json` SHOULD 增加：

```json
{
  "usage_docs": {
    "status": "generated | skipped | pending_confirmation",
    "root": "usage-docs",
    "manifest": "usage-docs/manifest.json",
    "source_version": "vX.Y.Z",
    "manual_overrides_allowed": true,
    "overwrite_policy": "current-version-only-by-default",
    "generation_decision": {
      "required": true,
      "confirmed_at": "YYYY-MM-DD HH:mm:ss",
      "confirmed_by": "operator",
      "rationale": "本次发布包含用户可见操作变化"
    }
  }
}
```

`gates` SHOULD 增加：

```json
{
  "usage_docs_preview": {
    "status": "pass",
    "evidence": "usage-docs manifest validated; Mintlify broken-links passed."
  }
}
```

`usage_docs_preview` 为 `pass` 时，MUST 具备具体命令、路径、时间或校验结果证据，禁止无证据标记为 `pass`。当用户确认本次不需要生成或更新产品文档时，`usage_docs_preview` SHOULD 记录为 `na`，并填写明确 rationale。

### FR-007 Mintlify 导航与 `/docs` 浏览

产品使用文档 MUST 能通过 Mintlify 文档站导航访问。

系统 SHOULD 支持以下导航目标：

- 当前版本产品使用文档。
- 历史版本产品使用文档。
- 当前版本发布公告。
- 历史版本发布公告。

文档站计划通过 `域名/docs` 访问。项目内 MUST 记录该访问方式的部署边界：

- 若由 Mintlify 自定义域名或 base path 支持，记录配置要求。
- 若由 Cloudflare、Vercel、CDN 或 Nginx rewrite 实现，记录 rewrite / proxy 边界。
- 若 `/docs` 子路径存在认证能力限制，公开产品使用文档与内部敏感文档 MUST 分离。

本需求允许继续使用现有 `releases/mint.json`，也允许后续 OpenSpec Change 评估升级到 Mintlify 推荐的 `docs.json`；无论采用哪种配置，发布校验 MUST 能发现导航缺页和 broken links。

### FR-008 旧版本文档维护策略

旧版本产品使用文档 MUST 默认视为已发布快照。

自动化在无明确授权时 MUST NOT 改写旧版本的以下内容：

- 产品行为说明。
- 操作步骤。
- 功能可用性。
- 版本差异。
- 已知问题和发布注意事项的历史语义。

自动化 MAY 在有明确命令或发布治理需要时，对旧版本执行非内容性维护：

- 修复 broken links。
- 适配 Mintlify 配置升级。
- 补齐 frontmatter 或 manifest 字段。
- 修复格式、标题层级、导航引用。
- 移除敏感信息或不可公开内容。
- 增加 deprecated、archived 或迁移标记。
- 批量迁移目录结构，但不得改变原含义。

旧版本内容性更正 MUST 记录原因、操作者、时间、文件范围和变更说明。记录位置 MAY 为 `manifest.json`、页面 frontmatter 或 `release.json`，后续设计阶段需明确单一事实源。

### FR-009 当前版本文档更新策略

当前版本在 `/release-prepare <version>` 阶段只有经用户确认需要生成或更新后，才允许自动化生成、覆盖或更新。

当前版本文档更新 MUST：

- 以用户确认结果为前置条件。
- 以当前 `release.json` 为发布范围事实源。
- 不纳入未评审、未归档或未进入正式发布范围的 REQ / BUG / Change。
- 对待确认内容保留 `待确认` 或人工补充提示。
- 在 manifest 中记录生成输入和时间。
- 保持公开文档安全，不泄露内部实现细节或敏感运维信息。

若用户确认本次不需要生成或更新产品文档，流程 MUST 不创建空的 `usage-docs/` 版本目录，不更新 Mintlify 当前版本文档导航，并在 `release.json` 中记录跳过原因。若当前版本发布已完成 `/release-publish <version>`，后续内容性修改 SHOULD 按旧版本策略处理。

### FR-010 文档覆盖来源

产品文档生成和校验 SHOULD 至少参考以下输入：

| 输入 | 用途 |
|---|---|
| `releases/<version>/release.json` | 发布范围、影响范围、已知问题、升级与回滚说明。 |
| `releases/<version>/announcement.mdx` | 公开公告入口与版本上下文。 |
| `src/web/src/features/admin/data/admin-nav.ts` | 管理端菜单覆盖。 |
| `src/web/src/app/App.tsx` | 管理端和公开 Web 路由覆盖。 |
| `src/miniapp/app.json` | 小程序页面和 tabBar 覆盖。 |
| `openspec/archive/**` 或发布对象引用 | 已归档能力事实。 |
| `docs/00-product-overview.md` | 产品定位与核心场景。 |

大范围读取 MUST 遵守上下文预算规则，优先使用 release scope 和目标文件片段，不默认全量读取历史归档。

### FR-011 安全与公开边界

产品使用文档默认面向公开读者。

公开产品文档 MUST NOT 包含：

- `.env` 内容。
- 数据库连接串。
- MinIO / COS / OSS access key 或 secret。
- Authorization header、Cookie、Token。
- 真实客户数据。
- 不可公开的生产域名、内网地址或运维路径。
- 后端敏感调试信息。

内部运维、API、数据库、部署和对象存储细节 SHOULD 保持在仓库 `docs/`、受控 Review 文档或鉴权页面，不应混入公开产品使用文档。

## 5. UI / UE 约束

本需求不新增业务 UI。

产品使用文档站的 UI SHOULD 以 Mintlify 提供的文档站能力为主，不强制复用 Web 管理端 Design System。

文档内容 SHOULD 按读者路径组织：

- 产品总览。
- 管理端使用说明。
- 小程序使用说明。
- 版本公告。
- 常见问题。

管理端文档 SHOULD 按实际菜单组织；小程序文档 SHOULD 按 tabBar 和关键页面组织。

文档语言 MUST 中文优先，命令、路径、Mintlify、Docker、Orval 等专有名词可保留英文。

## 6. 非功能约束

| 项 | 要求 |
|---|---|
| 可追踪 | 每个版本产品文档应能追溯到 release、Sprint、REQ、BUG、Change 和生成输入。 |
| 可审查 | 文档源文件、manifest、导航配置和 release gate 证据应纳入 Git Review。 |
| 可维护 | 产品文档生成决策、更新、校验和旧版本维护必须有明确命令或规范。 |
| 可回看 | 历史版本产品行为说明默认保持发布快照语义。 |
| 可修复 | broken links、导航迁移、安全修复和 frontmatter 补齐允许受控自动化处理。 |
| 安全 | 公开文档不得泄露密钥、真实客户数据、连接串、内部路径或不可公开运维信息。 |
| 兼容性 | 文档站不得影响现有 Web 管理端、小程序、后端 API、Docker Compose 或对象存储运行链路。 |
| 可校验 | 发布准备必须能报告产品文档生成决策；确认需要时报告 manifest、Mintlify 导航、broken links、安全扫描和覆盖度结果。 |

## 7. 关联需求与规范

| 关联项 | 关系 |
|---|---|
| REQ-0026-product-release-management | 已有产品版本发布与公告管理，本需求扩展为产品使用文档。 |
| REQ-0081-release-image-build-governance | 已有发布门禁治理经验，本需求沿用 release gate 与 manifest 思路。 |
| `rules/release.md` | 需要增加产品文档生成、校验和 `usage_docs_preview` gate。 |
| `rules/directory-structure.md` | 需要明确 `releases/vX.Y.Z/usage-docs/` 的目录职责和边界。 |
| `rules/document-governance.md` | 需要明确旧版本文档快照、人工修改、frontmatter 与时间字段规则。 |
| `rules/security.md` | 产品使用文档公开安全扫描必须遵守。 |
| `releases/README.md` | 需要说明 usage-docs 目录、生成方式和 `/docs` 浏览入口。 |
| `.agents/skills/release-prepare/SKILL.md` | 需要接入产品文档生成和校验步骤。 |
| `scripts/validate-release.py` | 需要扩展或调用产品文档校验。 |
| `releases/mint.json` | 当前 Mintlify 配置；后续可评估迁移或升级为 `docs.json`。 |

## 8. 状态块

```yaml
requirement_id: REQ-0088-versioned-product-usage-docs
priority: P1
status: done
iteration: null
owner: product
parent_requirement: null
openspec_changes: []
expected_openspec_change: add-versioned-product-usage-docs
target_clients:
  web_admin: 文档覆盖管理端操作说明，不影响运行时
  web_catalog: 文档站公开浏览，不影响运行时
  miniapp: 文档覆盖小程序使用说明，不影响运行时
  public_docs: 本期目标
next: /req-opsx REQ-0088-versioned-product-usage-docs
```
