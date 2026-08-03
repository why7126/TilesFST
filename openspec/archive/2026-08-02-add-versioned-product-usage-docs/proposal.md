## Why

当前发布治理已支持 `release.json` 和 Mintlify 公告，但产品使用文档仍缺少版本化、按需生成、发布确认和旧版本维护策略。REQ-0088 已明确产品文档不是每个版本都必须生成，`/release-prepare` 需要先确认本次是否生成或更新，避免该更新时漏更、不该更新时生成空版本，或自动化误改历史版本产品语义。

## What Changes

- 在产品发布治理中增加版本化产品使用文档能力，文档源文件位于 `releases/<version>/usage-docs/`。
- 为 `release.json` 增加 `usage_docs` 元数据，用于记录生成决策、状态、manifest、来源版本和 skipped rationale。
- 为发布门禁增加 `usage_docs_preview`，需要生成或更新产品文档时校验 manifest、Mintlify 导航、broken links、公开安全扫描和覆盖度。
- 在 `/release-prepare <version>` 中增加“是否需要生成或更新产品文档”的确认点；未确认时不得自动生成，新版本不需要时记录 skipped。
- 定义旧版本产品文档维护策略：产品内容默认冻结，非内容性维护和安全修复可自动化，内容性更正需明确授权并留痕。
- 明确 `/docs` 浏览方式的部署边界需要文档化，公开产品使用文档和内部敏感文档必须分离。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `product-release-management`: 扩展产品版本发布管理，增加按需生成的版本化产品使用文档、`usage_docs` 元数据、`usage_docs_preview` 门禁和旧版本维护策略。

## Impact

- 影响 `releases/<version>/release.json` 结构、`releases/<version>/usage-docs/` 文档源、Mintlify 导航配置和发布校验脚本。
- 影响 `/release-prepare`、`/release-publish`、可能新增的 `/usage-docs-generate` 与 `/usage-docs-validate` 技能或脚本。
- 影响 `rules/release.md`、`rules/directory-structure.md`、`rules/document-governance.md`、`releases/README.md` 和发布相关测试。
- 不直接影响后端 API、数据库 schema、Web 管理端运行时、小程序运行时、对象存储或 Orval 生成客户端。
