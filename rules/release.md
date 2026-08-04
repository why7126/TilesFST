---
purpose: 全局规则
content: 团队研发规范和AI约束
source: AI自动生成初稿，项目团队确认
update_method: 项目初始化后由人工确认；后续由AI辅助更新并经人工Review
note: 适用于瓷砖信息管理平台项目模板
created_at: 2026-06-13 00:00:00
updated_at: 2026-08-03 19:10:00
---

# 发布规范

发布前必须完成测试、OpenSpec校验、接口生成、变更归档和发布说明。

## 发版检查清单（Web 产品版本）

对外发布 Web 管理端或店主端时，若本次发版包含产品版本语义变更，MUST 人工更新：

```text
src/shared/product-version.ts  →  PRODUCT_VERSION（如 v0.0.1）
```

MUST NOT 依赖 `package.json`、FastAPI `version`、OpenAPI 版本、Git commit 或 CI 构建号作为用户可见产品版本。

## 产品版本发布对象

产品版本发布对象用于表达一次对外产品发版，放入：

```text
releases/vX.Y.Z/release.json
```

产品版本发布对象 MUST 支持：

- 一个产品版本关联一个或多个 Sprint。
- 追踪关联 REQ、BUG 和 OpenSpec Change。
- 区分 Sprint `release-note.md` 与产品版本公告：Sprint release note 描述迭代交付，产品版本公告描述对外版本。
- 阻止未评审、未纳入交付或未归档闭环的内容进入正式发布范围。

## 公开发布公告

公开发布公告源文件放入：

```text
releases/vX.Y.Z/announcement.mdx
```

发布公告 MUST：

- 面向公开页面展示。
- 使用 Mintlify 静态文档生成或预览校验。
- 可纳入 Git Review。
- 不依赖后端运行时 API 或数据库才能展示。
- 包含版本号、发布时间、关联 Sprint、新增功能、修复 BUG、发布注意事项、已知问题、升级步骤、回滚说明和影响范围。
- 不泄露密钥、真实客户数据、内部数据库连接串、MinIO 凭据、不可公开域名或敏感运维信息。

## 产品使用文档

产品使用文档是面向公开读者的版本化产品操作说明，按需放入：

```text
releases/vX.Y.Z/usage-docs/
```

产品使用文档不是每个版本都必须生成或更新。`/release-prepare <version>` MUST 先确认本次是否需要生成或更新产品使用文档，并在 `release.json` 记录 `usage_docs` 决策：

| 状态 | 含义 | 目录要求 | 门禁 |
|---|---|---|---|
| `generated` | 用户确认需要，且当前版本 usage docs 已生成 | MUST 存在 `usage-docs/manifest.json` 与页面源文件 | `usage_docs_preview=pass`，含命令、路径、时间或校验证据 |
| `skipped` | 用户确认本版本不需要生成或更新 | MUST NOT 创建空的 `usage-docs/` 目录 | `usage_docs_preview=na`，含确认来源、确认时间和跳过原因 |
| `pending_confirmation` | 尚未确认是否需要生成或更新 | MUST NOT 自动生成目录 | 发布准备 / 发布确认 MUST 阻断或记录 blocker |

`usage_docs` SHOULD 至少包含：

```json
{
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
```

当 `status=generated` 时，`usage-docs/manifest.json` MUST 记录 version、generated_at、source_version、source_release、input_files、pages、coverage、screenshots、manual_overrides 和 automation_policy。校验 MUST 覆盖 manifest 结构、页面清单与实际文件一致性、系统截图覆盖、Mintlify 导航、broken links 或等价静态校验、公开安全扫描、覆盖摘要和旧版本改写策略。

当前版本 usage docs MUST 以前一个已生成 usage docs 的产品版本为完整基线：若 `releases/<previous>/usage-docs/manifest.json` 存在，则新版本 `manifest.pages` MUST 覆盖前一版本全部页面，并在 `source_version`、`input_files` 或 `manual_overrides` 中记录继承来源。除非用户明确授权页面下线或内容收敛，否则不得退回只包含模板页、增量页或当前 Sprint 页的文档集。

`mintlify/` 是 Mintlify 文档站源目录，`releases/vX.Y.Z/usage-docs/` 是全量产品使用文档快照和 manifest 事实源。`status=generated` 时，系统 SHOULD 将 release 快照同步或投影到 `mintlify/docs/vX.Y.Z/`，更新 `mintlify/docs/latest/`，并将公告投影到 `mintlify/releases/vX.Y.Z/announcement.mdx`。站点投影 MUST 在 manifest 中记录 source_release、source_manifest、target_site_root、latest_target、mode、content_hashes、synced_at 和 manual_overrides。

生成的产品使用文档 MUST 包含系统截图：

- 每个 `usage-docs/**/*.mdx` 页面 MUST 至少引用 1 张共享真实系统截图，引用路径使用 `/assets/screenshots/<file>`。
- 截图 MUST 放入 `mintlify/assets/screenshots/` 共享资产目录并按内容 hash 命名；release 快照通过 manifest 引用共享截图资产，禁止在每个版本目录复制截图。
- `releases/<version>/usage-docs/assets/` MUST NOT 存在；usage docs 页面引用共享截图时使用 `/assets/screenshots/<file>`。
- `usage-docs/manifest.json` 的 `screenshots[]` MUST 记录 `path=/assets/screenshots/<file>`、`site_asset=mintlify/assets/screenshots/<file>`、覆盖页面、caption、source、source_type、content_hash、first_used_in、used_by_versions、covered_pages 和 reuse_reason。
- 截图不得直接引用 `issues/**`、`openspec/**`、本机绝对路径、外部私有链接、生产私有域名或任何含敏感信息的图片。
- source_type MUST 只能使用 `runtime_system`、`qa_system`、`accepted_system_evidence`、`miniapp_devtools` 或 `manual_system_capture`。
- 截图 MUST 来自真实系统运行界面、QA/验收真实截图、小程序真机/开发者工具预览，或人工从当前系统捕获的截图；MUST NOT 使用产品原型图、设计稿、线框图、Figma/HTML prototype 或任何 `prototype/原型` 来源。
- 如某页面确实无法提供真实系统截图，MUST 阻断 usage docs 校验并补充截图证据；不得用原型图兜底，也不得只保留纯文字页面。

已发布旧版本 usage docs 默认是发布快照。自动化在无明确授权时 MUST NOT 改写旧版本产品行为说明、操作步骤、功能可用性、版本差异或已知问题历史语义。broken links、Mintlify 配置迁移、frontmatter/manifest 补齐、格式修复、导航引用修复、敏感信息移除和目录结构迁移等非内容性维护 MAY 自动执行，但 MUST 记录维护范围。旧版本内容性更正 MUST 记录原因、确认来源、时间、文件范围和变更说明。

`域名/docs` 是部署边界，不由 release 源文件单独完成。项目 MUST 记录采用 Mintlify base path、Cloudflare/Vercel/CDN rewrite、Nginx 反向代理或等价方案；若方案未确认，`/release-prepare` MUST 记录 blocker 或待确认项。公开产品使用文档 MUST 与内部运维、API、数据库、对象存储凭据、生产私有域名或敏感配置文档分离。

## 发布前门禁

发布确认前 MUST 校验：

| 门禁 | 要求 |
|---|---|
| OpenSpec | 关联 Change 已 archive，相关能力已合并到 `openspec/specs/`；未归档项不得进入正式发布范围 |
| 测试 | 按变更范围执行并记录结果 |
| API / Orval | 涉及 API 变更时，OpenAPI 与 Orval 已同步 |
| Docker Compose | 涉及部署变更时，Compose 配置与部署文档已同步 |
| 数据库 | 涉及数据库迁移或 schema 影响时，迁移脚本、数据库文档、回滚说明、MySQL schema drift 或目标 MySQL smoke 证据已同步 |
| 环境变量 | 涉及环境变量时，`.env.example` 与相邻注释已同步 |
| 产品版本 | `src/shared/product-version.ts` 的 `PRODUCT_VERSION` 与发布对象版本一致；如不更新，必须记录原因 |
| Mintlify | 公告 build / preview 或等价校验通过 |
| 产品使用文档 | 已确认 generated / skipped / pending_confirmation；generated 时 `usage_docs_preview` 通过，skipped 时记录不适用原因，pending_confirmation 阻断 |
| Mintlify 多版本站点 | generated usage docs 已同步或投影到 `mintlify/`，导航、`latest`、公告投影、共享截图 hash 和公开安全校验通过；未确认生产承载方式时记录 blocker 或待确认项 |
| 镜像准备 | 当 `image_required=true` 时，`releases/<version>/image-build-plan.json` 已生成、校验通过并被 `release.json` 引用 |
| 镜像构建 | 当 `image_required=true` 或包含离线镜像交付时，`releases/<version>/image-manifest.json` 已生成、未过期并被 `release.json` 引用；外部构建证据必须受控 |

任一必填门禁失败时，发布流程 MUST 阻断，并输出失败原因与修复建议。

当发布范围涉及后端运行代码、Web 构建产物、Dockerfile、Compose、`.env.example`、镜像构建脚本、构建 env 示例、数据库 schema / migration、API / Orval 生成物或离线镜像交付时，发布对象 MUST 将 `image_required` 设为 `true`，并按以下顺序执行：

```text
/release-propose <version>
  → /release-prepare <version>
  → /image-prepare <version>
  → /image-build <version>
  → /release-publish <version>
```

`/image-prepare` 只生成或更新 `releases/<version>/image-build-plan.json`，记录版本、image tag、source scope、build env 安全摘要、Dockerfile、Compose、构建脚本、构建 env 示例、Nginx、schema、migration、数据库文档 input hash、required commands、auto actions、warnings 和 blockers。默认构建 env 缺失或 `IMAGE_BUILD_TAG` 与版本不一致时，命令 MAY 只自动创建/更新安全白名单变量并记录 auto action。Compose fallback tag 与当前版本不同但实际发布 env 明确设置 `TILESFST_IMAGE_TAG=<version>` 时 SHOULD 记录 warning，不得作为 blocker 要求每次 release 改 Compose 默认值。Docker 不可用、网络不可用、构建 env 示例异常、自动修正后仍版本不一致或真实构建前置条件不满足时可以写 blocked plan，但不得写 pass 证据。

`/image-build` MUST 读取有效且未过期的 image build plan 后再复用 `scripts/build-images.sh` 执行真实构建。构建成功后写入 `releases/<version>/image-manifest.json`，记录 version、image_tag、built_at、platform、backend_image、web_image、tarball、input_hashes、validation 和 source_plan。镜像 tar 包与 `.sha256` MUST 默认输出到仓库外 `../releases/<version>/images/`，不得提交到仓库内 `releases/`。构建后 MUST 校验 manifest 记录的 tarball sha256、`.sha256` sidecar 和实际 tarball sha256 三者一致。缺少 plan、plan blocked、版本/tag 不一致、input hash 漂移、Docker/buildx/网络/基础镜像源/验证/tar/sha256 失败时 MUST 阻断，不得伪造成功 manifest。

发布确认阶段 MUST 重新校验 manifest 的版本、tag、source plan、input hashes、tarball 路径、sidecar sha256 和实际 tarball sha256。manifest 生成后 Dockerfile、构建脚本、schema、migration、Compose 或 release stable input 漂移时，镜像证据失效，必须重新执行 `/image-prepare` 与 `/image-build`，或记录经批准的外部构建证据。公告文案不参与镜像二进制构建，MUST NOT 纳入 image build plan / manifest input hash；公告中的发布状态、usage docs 决策和镜像 evidence 描述可在发布确认前按当前 `release.json`、`image-manifest.json` 和 `.sha256` sidecar 刷新。发布输出 MUST 以当前 manifest 中的 sha256 为唯一发布 sha，并提醒在 tarball 所在目录执行 `shasum -a 256 -c <tarball>.sha256`。

`/release-publish` 是发布确认命令，不得把最终 tarball sha256、manifest sha256、发布时间或发布确认写回公告。公告中如需描述镜像校验，MUST 引用 `releases/<version>/image-manifest.json` 与离线包 `.sha256` sidecar 作为事实源。最终 sha、发布时间、公告位置和确认人只写入 `release.json.publish_confirmation` 或发布输出。若发布确认发现公告只残留 usage docs、image prepare/build、门禁状态等可由当前 release metadata 推导出的过期状态，MAY 在 publish 前刷新公告并继续校验；若公告涉及范围、功能、风险、回滚、公开安全或需人工 copy edit 的实质变更，MUST 阻断 publish 并要求先修公告。

外部构建证据只可作为受控替代证据，必须记录来源、版本、image tag、平台、镜像 digest 或 tarball sha256、校验方式、负责人确认和风险说明；不得绕过公开安全扫描、版本一致性校验或 input hash 漂移校验。

数据库影响不允许只记录 SQLite、本地测试或文档同步证据。`impact_scope.database` 非 `none` / `na` / `不涉及` 时，`database_migration` 门禁 MUST 为 `pass`，且 evidence MUST 明确包含：

- MySQL 或 `schema.mysql.sql` 目标路径证据。
- `scripts/check-mysql-schema-drift.py`、目标 MySQL smoke、`information_schema` 校验或等价证据。
- 数据库回滚或备份证据。

## 发布命令族

发布命令族以 `.agents/skills/release-*`（若存在）或对应 Codex 技能为入口；新增或修改发布命令时 MUST 更新 `.agents/skills/`。

推荐命令：

| 命令 | 目标 |
|---|---|
| `/release-propose <version>` | 创建或更新产品版本发布计划，选择关联 Sprint / REQ / BUG / Change |
| `/release-prepare <version>` | 执行发布前校验，生成或更新 Mintlify 公告源文件 |
| `/usage-docs-generate <version>` | 在确认需要后生成当前版本 usage docs 与 manifest |
| `/usage-docs-update <version>` | 更新当前版本 usage docs，或在明确授权下维护旧版本文档 |
| `/usage-docs-validate <version>` | 校验 usage docs manifest、导航、公开安全和旧版本维护策略 |
| `scripts/generate-usage-docs.py <version>` | 三个 usage-docs Skill 使用的底层生成 / skip 脚本 |
| `scripts/validate-usage-docs.py --release-dir releases/<version>` | 三个 usage-docs Skill 使用的底层校验脚本，覆盖 release 快照、`mintlify/` 投影、导航、共享截图和公开安全 |
| `/image-prepare <version>` | 生成镜像构建计划并校验 release、tag、Compose、Dockerfile、schema/migration 等输入 |
| `/image-build <version>` | 基于有效构建计划执行真实镜像构建、验证、离线包导出并生成 manifest |
| `/release-publish <version>` | 记录发布确认结果和最终公告位置 |

本项目当前不引入草稿、待发布、已发布、撤回等复杂发布状态机。发布命令只记录计划、校验和确认事实。
