## Why

小程序发布前需要在开发、本地验证、体验版和正式版之间切换 API 环境；当前依赖人工修改 `src/miniapp/utils/env.*`，容易遗漏 `.js` 运行入口或发布后忘记恢复。近期体验版发布排障已经暴露出环境开关、合法域名、生产接口 smoke 和手机缓存验证需要被固化为命令流程。

## What Changes

- 新增小程序环境命令族：`/miniapp-env`、`/miniapp-check`、`/miniapp-prepare`、`/miniapp-confirm`、`/miniapp-restore`。
- 新增确定性脚本用于切换和检查 `dev`、`prod`、`auto` 三种小程序环境策略。
- 将 `.ts` 源码与微信实际运行 `.js` 入口作为同一事实源维护，命令必须同步修改并由静态测试覆盖。
- 发布前准备命令必须执行环境策略、静态测试和生产小程序公开接口 smoke 检查，并输出微信开发者工具/公众平台人工 checklist。
- 发布确认与恢复命令记录体验版/正式版验证事实，并支持恢复默认环境策略。

## Capabilities

### New Capabilities

### Modified Capabilities

- `agent-workflow-tooling`: 新增小程序环境切换与发布辅助命令要求，覆盖命令入口、环境策略、校验、确认与恢复。

## Impact

- 影响 `.agents/skills/miniapp-*` 新命令入口。
- 影响 `scripts/` 中小程序环境切换/检查脚本。
- 影响 `src/miniapp/utils/env.ts`、`src/miniapp/utils/env.js` 和 `src/miniapp/README.md`。
- 影响 `tests/test_miniapp_static.py` 的环境策略静态覆盖。
- 不新增后端 API、不修改数据库、不影响 Orval、不新增 Docker Compose 服务。
