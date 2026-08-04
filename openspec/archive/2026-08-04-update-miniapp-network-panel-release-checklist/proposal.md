## 背景

小程序发布前已有环境策略、`urlCheck=true`、静态测试和生产接口 smoke，但这些自动化门禁不能证明 DevTools 或体验版真实 Network 链路已经请求正确生产域名并能加载关键媒体资源。sprint-014 复盘已将“小程序 DevTools / 真机 / 体验版 Network evidence 前置 checklist”列为 P1 行动项，本变更把该经验固化到小程序 release/miniapp 准备流程。

## 变更内容

- 在小程序 evidence 模板中新增 Network evidence 来源与字段口径，区分 `network_devtools` 与 `network_trial`。
- 在产品发布管理发布前门禁中新增小程序 Network checklist，要求 `/miniapp-prepare` 和 `/miniapp-confirm` 承接 DevTools 与体验版网络面板验证。
- 明确人工 Network evidence 不得被自动门禁误写为通过；缺失时只能记录 `blocked`、`follow_up` 或明确的 `not_applicable`。
- 不新增自动抓包、云真机、业务 API、数据库、Orval 或小程序业务页面能力。

## 能力范围

### 新增能力

无。

### 修改能力

- `miniapp-device-evidence-template`：新增小程序 Network evidence 来源、字段、安全边界和与 DevTools/真机 evidence 的关系。
- `product-release-management`：发布前校验门禁新增小程序 DevTools/体验版 Network checklist 和确认记录要求。

## 影响范围

- 小程序发布准备技能与确认技能：`.agents/skills/miniapp-prepare/SKILL.md`、`.agents/skills/miniapp-confirm/SKILL.md`。
- 小程序环境脚本：`scripts/miniapp-env.py` 的 checklist 输出。
- 小程序说明文档：`src/miniapp/README.md`。
- 小程序 evidence 标准：`docs/standards/miniapp-device-evidence-template.md`。
- 测试：`tests/test_miniapp_static.py` 或等价静态测试需要覆盖 checklist 文案与边界。
- 不影响后端 API、数据库、Web 管理端、店主 Web、Orval 和 Docker Compose。
