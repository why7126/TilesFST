---
purpose: 规范工程迭代日志
content: PRODUCT_VERSION 发布准备自动同步
source: /spec-opt automate-product-version-release-prepare
update_method: 本日志记录单次治理变更事实；后续变更另开日志或更新 CHANGELOG 摘要
created_at: 2026-08-30 22:41:57
updated_at: 2026-08-30 23:00:41
---

# PRODUCT_VERSION 发布准备自动同步治理日志

## 迭代目标

将版本号更新从人工编辑前移为 `/release-prepare <version>` 的自动化步骤，确保 Web 与小程序用户可见 `PRODUCT_VERSION` 在镜像计划和发布确认前已经对齐发布版本。

## 变更摘要

- `scripts/validate-release.py` 新增 `--sync-product-version`，自动同步受控版本源、`release.json` product version gate evidence、`product_version_sync` 和公告版本状态。
- `scripts/validate-image-build.py` 在 image prepare 阶段检查版本源一致性，不一致时写入 blocker 并要求先运行 `/release-prepare <version>`。
- `/release-status` 的产品版本 mismatch 修复路径指向 `/release-prepare <version>`，已有镜像证据时追加 `/image-prepare` 与 `/image-build`。
- `/release-publish` 明确只做确认，不写 Web 或小程序版本源。
- `rules/release.md`、`rules/agent-context-budget.md`、`AGENTS.md` 与 release / image 技能说明已同步。
- `releases/v1.2.2` 已通过同步命令刷新 product version metadata 与公告版本状态证据。

## 影响范围

| 层级 | 影响 |
|---|---|
| API | 不适用，未修改接口。 |
| DB | 不适用，未修改 schema、migration 或数据模型。 |
| Web | 不修改业务逻辑；后续 release-prepare 会自动同步 Web shared `PRODUCT_VERSION`。 |
| 小程序 | 不修改业务逻辑；后续 release-prepare 会自动同步小程序 `PRODUCT_VERSION`。 |
| 管理端 | 不适用。 |
| Orval | 不适用。 |
| Docker Compose | 不适用，未修改 Compose；版本源同步发生在 image-prepare 前。 |

## 更新文件

- `scripts/validate-release.py`
- `scripts/validate-image-build.py`
- `tests/test_release_validation.py`
- `.agents/skills/release-prepare/SKILL.md`
- `.agents/skills/release-status/SKILL.md`
- `.agents/skills/release-publish/SKILL.md`
- `.agents/skills/image-prepare/SKILL.md`
- `rules/release.md`
- `rules/agent-context-budget.md`
- `AGENTS.md`
- `releases/v1.2.2/release.json`
- `releases/v1.2.2/announcement.mdx`
- `openspec/changes/automate-product-version-release-prepare/`
- `iterations/change/sprint-029/`

## 关键决策

- 已采纳：版本源写入归属 `/release-prepare`，因为它位于 release scope 确认之后、image stable input 固化之前。
- 已采纳：`/image-prepare` 只检查并阻断，不代写版本源，避免镜像流程产生隐式源文件变更。
- 已采纳：`/release-publish` 只确认不写版本源，避免发布确认阶段改变镜像稳定输入。
- 未采纳：要求操作员手工编辑版本源或公告状态。该方式已在 v1.2.2 返修中暴露流程风险。

## 验证结果

- 脚本编译：`python -m py_compile scripts/validate-release.py scripts/validate-image-build.py` 通过。
- 聚焦测试：`tests/test_release_validation.py` 中 PRODUCT_VERSION 自动同步、image-prepare mismatch blocker、publish mismatch、release-status remediation、image input candidates 共 5 passed。
- v1.2.2：release prepare、release publish、release status、image plan、image manifest 校验通过。
- 治理校验：OpenSpec、目录结构、上下文预算与 Sprint scope 校验通过。
- Workflow Sync 与 AI Usage hook 已运行并回填 `sprint-029`。

## 后续建议

- 后续新增 App、桌面端或其他用户可见版本源时，应先通过 `/spec-opt` 将其加入 release prepare sync 白名单与 image prepare 前置检查。
