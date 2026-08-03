## Context

当前项目已经通过 `product-release-management` capability 管理 `releases/<version>/release.json`、`announcement.mdx`、Mintlify 公告和发布门禁。REQ-0088 要求在此基础上增加“产品使用文档”治理，但有两个关键约束：

- 产品文档不是每个版本都必须生成或更新，`/release-prepare <version>` 必须先确认本次是否需要生成或更新。
- 旧版本产品文档默认是已发布快照，不能让自动化无授权改写产品行为说明，但允许非内容性维护和安全修复。

因此本 Change 设计为扩展产品发布治理，而不是新增运行时业务模块。不新增后端 API、数据库表、管理端菜单、小程序入口或店主 Web 入口。

## Goals / Non-Goals

**Goals:**

- 在 release 事实源中表达产品文档生成决策：`generated`、`skipped`、`pending_confirmation`。
- 支持按需生成 `releases/<version>/usage-docs/**` 与 `usage-docs/manifest.json`。
- 支持按需校验 usage docs manifest、Mintlify 导航、broken links、敏感信息、覆盖度和旧版本误改。
- 将 `usage_docs_preview` gate 纳入发布准备/发布确认。
- 明确 `/docs` 浏览方式只记录项目内部署边界，不在本 Change 中完成外部域名配置。

**Non-Goals:**

- 不实现真实 Mintlify 线上站点、DNS、Cloudflare/Vercel/CDN 或 Nginx 生产配置。
- 不新增运行时产品文档 API、数据库表、管理端菜单或小程序入口。
- 不生成截图、视频教程或交互式培训课件。
- 不让 `/release-prepare` 默认每版生成 usage docs。

## Decisions

### D1. 将 usage docs 放入现有 `product-release-management`

使用现有 capability，而不是新增 `product-usage-docs` capability。原因是 usage docs 的生命周期、事实源和门禁都以 release 为中心：`release.json`、Mintlify 导航和 `release-prepare` 是主要接入点。

替代方案是新增 capability。缺点是会把发布对象和产品文档门禁拆开，导致 `/release-prepare` 需要跨 capability 汇总语义，反而更分散。

### D2. release.json 记录生成决策

`release.json` 增加 `usage_docs` 对象：

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

`pending_confirmation` 表示 release-prepare 发现需要用户判断，但尚无确认；`skipped` 表示用户确认本次不生成/更新；`generated` 表示已生成并通过必要校验。

### D3. 不需要时不创建空版本目录

当用户确认不需要生成或更新产品文档时，流程只在 `release.json` 记录 skipped rationale，不创建空的 `releases/<version>/usage-docs/`，也不更新 Mintlify 当前版本文档导航。

这样可以避免“每个版本都有空文档版本”的噪音，也避免误导公开读者。

### D4. 生成与校验可由脚本或技能承载

实现可以新增脚本，例如：

```text
scripts/generate-usage-docs.py
scripts/validate-usage-docs.py
```

也可以由 release prepare 内部调用等价函数。无论实现形态，验收以 release gate、manifest、Mintlify 校验和敏感信息扫描为准。

### D5. 旧版本维护区分内容性与非内容性

旧版本产品文档默认快照化：

- 内容性变更：产品行为、操作步骤、功能可用性、版本差异、已知问题历史语义，需要明确授权并留痕。
- 非内容性维护：broken links、frontmatter/manifest 补齐、Mintlify 配置迁移、格式/导航引用、安全修复，可以自动化执行但必须记录范围。

### D6. `/docs` 只在项目内记录部署边界

本 Change 不完成外部托管配置，但必须在项目文档中说明 `域名/docs` 的实现方式由 Mintlify base path、Cloudflare/Vercel/CDN rewrite 或 Nginx 反向代理承载，并说明公开产品文档和内部敏感文档分离。

## Risks / Trade-offs

- [Risk] release-prepare 需要用户确认，可能阻塞自动化发版。→ Mitigation：允许记录 `skipped` 或 `pending_confirmation`，输出下一步，不伪造 generated。
- [Risk] usage docs 内容可能由 AI 生成导致事实不准确。→ Mitigation：以 `release.json` 正式范围和 manifest input 为事实源，待确认内容必须标注，不得把推断写成事实。
- [Risk] Mintlify `mint.json` 与较新的 `docs.json` 配置存在迁移选择。→ Mitigation：本 Change 允许继续使用现有配置，也允许在实现中迁移，但必须同步校验和文档。
- [Risk] 公开文档泄露内部运维信息。→ Mitigation：安全扫描覆盖 usage docs、manifest、announcement 和 release metadata。

## Migration Plan

1. 扩展 release 规则、目录规则和文档治理规则。
2. 增加 usage docs 模板和 manifest schema。
3. 扩展 release prepare/publish 技能或脚本，加入生成决策和门禁。
4. 扩展 `validate-release.py` 或新增 usage docs 校验脚本。
5. 增加测试覆盖 generated / skipped / pending_confirmation 三种路径。
6. 更新 `releases/README.md` 和 Mintlify 配置。

回滚策略：若 usage docs 生成或校验能力出现问题，可在 release 对象中将 `usage_docs.status` 标记为 `skipped` 或 `pending_confirmation`，不影响公告和镜像门禁；已生成的 usage docs 源文件通过 Git 回退。

## Open Questions

- 是否在本 Change 中将 `releases/mint.json` 升级为 Mintlify 推荐的 `docs.json`，还是保留现有 `mint.json` 并只扩展 navigation？
- `generation_decision.confirmed_by` 是否固定为 `operator`，还是允许记录 reviewer / release owner / external approval id？
- 旧版本内容性更正的唯一留痕事实源最终放在 `manifest.json`、页面 frontmatter 还是 `release.json`？
