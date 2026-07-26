## 1. OpenSpec 与命令设计

- [x] 1.1 创建 `add-miniapp-env-commands` OpenSpec Change 并补齐 proposal、design、specs、tasks
- [x] 1.2 确认命令名保持两段式：`miniapp-env`、`miniapp-check`、`miniapp-prepare`、`miniapp-confirm`、`miniapp-restore`

## 2. 小程序环境脚本

- [x] 2.1 新增 `scripts/miniapp-env.py`，支持 `set`、`check`、`prepare`、`confirm`、`restore` 子命令
- [x] 2.2 脚本支持 `dev`、`prod`、`auto` 三种策略，并同步写入 `src/miniapp/utils/env.ts` 与 `src/miniapp/utils/env.js`
- [x] 2.3 脚本检查当前策略、`.ts/.js` 一致性、生产 API 地址和 fallback 配置
- [x] 2.4 脚本输出微信上传、体验版缓存清理和合法域名人工 checklist

## 3. Skill 命令入口

- [x] 3.1 新增 `.agents/skills/miniapp-env/SKILL.md`
- [x] 3.2 新增 `.agents/skills/miniapp-check/SKILL.md`
- [x] 3.3 新增 `.agents/skills/miniapp-prepare/SKILL.md`
- [x] 3.4 新增 `.agents/skills/miniapp-confirm/SKILL.md`
- [x] 3.5 新增 `.agents/skills/miniapp-restore/SKILL.md`

## 4. 文档与测试

- [x] 4.1 更新 `src/miniapp/README.md`，记录 `dev`、`prod`、`auto` 策略和命令使用方式
- [x] 4.2 更新或新增测试，覆盖环境策略切换、运行入口同步和生产地址断言
- [x] 4.3 运行 `uv run pytest tests/test_miniapp_static.py` 并记录结果

## 5. 工作流同步

- [x] 5.1 运行 OpenSpec 校验和 Workflow Sync
- [x] 5.2 输出命令族使用说明、影响范围和剩余风险
