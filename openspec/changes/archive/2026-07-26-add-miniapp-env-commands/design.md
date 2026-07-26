## Context

当前小程序环境配置位于 `src/miniapp/utils/env.ts` 与 `src/miniapp/utils/env.js`，其中 `.js` 是微信开发者工具真实运行入口，`.ts` 保留类型化源码意图。近期发布排障中，项目临时将所有运行形态强制切到生产环境，解决了体验版与手机缓存验证问题，但也留下“手工修改、容易忘记恢复、缺少命令记录”的风险。

现有项目命令风格为两段式 `<domain>-<action>`，例如 `release-publish`、`opsx-apply`。新增小程序环境命令应保持该风格，且不应误导为能直接调用微信平台发布。

## Goals / Non-Goals

**Goals:**

- 提供 `/miniapp-env`、`/miniapp-check`、`/miniapp-prepare`、`/miniapp-confirm`、`/miniapp-restore` 五个命令入口。
- 用确定性脚本维护 `dev`、`prod`、`auto` 环境策略，避免 `.ts` 与 `.js` 漂移。
- 发布前自动检查生产公开接口、静态测试和人工上传/体验版 checklist。
- 发布确认与恢复命令记录可审计的验证事实或输出标准记录结构。

**Non-Goals:**

- 不调用微信公众平台 API，不自动上传、提审或发布小程序。
- 不新增后端 API、数据库表、Orval 生成物或 Docker Compose 服务。
- 不解决微信手机端体验版缓存，只将清理缓存作为 checklist 输出。

## Decisions

1. **使用 `scripts/miniapp-env.py` 作为机械事实源**

   脚本提供 `set`、`check`、`prepare`、`confirm`、`restore` 子命令。Skill 不直接手写配置，避免重复实现字符串替换。脚本只维护已知文件：

   - `src/miniapp/utils/env.ts`
   - `src/miniapp/utils/env.js`
   - `src/miniapp/README.md` 的环境说明片段

2. **保留三种策略**

   - `dev`：所有运行形态使用本地地址和 fallback。
   - `prod`：所有运行形态使用 `https://tilesfst.wjoyhappy.site`，无 fallback。
   - `auto`：`develop` 使用本地，`trial` 与 `release` 使用生产。

   项目默认恢复策略采用 `auto`，发布前准备命令可将策略切到 `prod`。

3. **五个 Skill 保持薄入口**

   - `/miniapp-env <dev|prod|auto>`：调用脚本切换并运行静态检查。
   - `/miniapp-check`：报告策略、文件同步状态、生产接口 smoke 结果。
   - `/miniapp-prepare`：切到 `prod`，运行 `tests/test_miniapp_static.py`，curl 生产小程序首页/品牌接口，并输出微信上传 checklist。
   - `/miniapp-confirm`：记录或输出体验版/正式版验证结论；不自动发布。
   - `/miniapp-restore`：恢复 `auto` 并运行检查。

4. **测试覆盖以静态测试为主**

   现有 `tests/test_miniapp_static.py` 已覆盖小程序环境配置、`.ts/.js` 同步和运行入口。新增脚本单元/集成测试可用临时工作区验证 `dev/prod/auto` 输出，避免污染真实项目文件。

## Risks / Trade-offs

- [Risk] 脚本修改源码仍可能与人工未提交改动冲突 → Mitigation：脚本在写入前报告目标文件和当前策略，Skill 输出 `git status --short` 摘要。
- [Risk] `curl` 生产接口依赖外网和生产状态，可能在本地沙箱失败 → Mitigation：命令报告 blocker，不伪造通过；允许用户按日志手工补验。
- [Risk] 微信体验版缓存导致“代码正确但手机仍旧包” → Mitigation：`miniapp-prepare` 和 `miniapp-confirm` checklist 明确删除旧入口、重新扫码最新体验版。
- [Risk] 发布后忘记恢复环境策略 → Mitigation：`miniapp-prepare` 输出下一步 `/miniapp-restore`，`miniapp-confirm` 也提示恢复策略。

## Migration Plan

1. 新增 OpenSpec Change 与命令 specs。
2. 新增脚本、五个 `.agents/skills/miniapp-*` 目录和 README/test 更新。
3. 运行 `uv run pytest tests/test_miniapp_static.py` 与脚本相关测试。
4. 后续发布流程中使用 `/miniapp-prepare` 替代手工修改环境配置。
