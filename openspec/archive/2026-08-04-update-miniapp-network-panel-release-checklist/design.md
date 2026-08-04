## 上下文

REQ-0096 已评审通过，目标是将小程序 DevTools/体验版网络面板验证纳入 release/miniapp 准备清单。当前 `/miniapp-prepare` 已由 `scripts/miniapp-env.py prepare` 完成 prod 策略切换、`urlCheck=true`、静态测试和生产接口 smoke，并输出上传体验版 checklist；但该 checklist 还没有把 Network evidence 明确为发布前人工验收项。

相关事实源：

- `issues/requirements/archive/REQ-0096-miniapp-network-panel-release-checklist/`
- `docs/knowledge-base/retrospectives/sprint-014-retrospective.md`
- `docs/standards/miniapp-device-evidence-template.md`
- `rules/media.md`
- `rules/object-storage.md`

## 目标 / 非目标

**目标：**

- 让 `/miniapp-prepare` 输出 DevTools Network 与体验版 Network 人工检查项。
- 让 `/miniapp-confirm` 的记录口径能承接 DevTools Network、体验版 Network、阻塞项和剩余风险。
- 扩展小程序 evidence 标准，明确 `network_devtools` 与 `network_trial` 的字段、状态和安全边界。
- 增加静态测试，确认 checklist 和文档不会把人工 Network evidence 误写为自动通过。

**非目标：**

- 不实现自动抓包、HAR 导出、自动截图、真机云测或微信开发者工具自动化。
- 不修改小程序业务页面、后端 API、数据库、Orval、Docker Compose 或对象存储策略。
- 不回填历史 release/Sprint 的 Network evidence。

## 设计决策

### D1：复用 evidence 模板，而不是创建全新模板

`docs/standards/miniapp-device-evidence-template.md` 已定义 `required`、`passed`、`failed`、`blocked`、`not_applicable`、`follow_up` 状态、页面路径、安全边界和证据引用方式。本变更在该模板中新增 Network evidence 来源：

```yaml
source: network_devtools | network_trial
```

这样可以复用现有状态语义，避免 release、Sprint、Change trace 中出现第二套不兼容证据模型。

### D2：`/miniapp-prepare` 只输出人工 checklist，不伪造通过

`/miniapp-prepare` 可以自动确认 prod 策略、`urlCheck=true`、静态测试和生产接口 smoke；DevTools Network 与体验版 Network 是人工动作，命令输出只能标记为待执行 checklist。若后续用户完成验证，应通过 `/miniapp-confirm` 记录 `passed`、`blocked` 或 `follow_up`。

### D3：体验版验证缺失必须显式记录风险

体验版 Network evidence 不能被 DevTools evidence 替代。若账号、设备、体验版二维码或网络环境不可用，记录必须使用 `blocked` 或 `follow_up`，并写明重试条件、剩余风险和责任人。

### D4：媒体资源按 URL/render 证据思路确认

SKU 图片、视频、证书图片等资源加载问题与媒体/对象存储规范相关。本变更只要求 release/miniapp checklist 记录资源加载结论和失败态；不新增 object key 审计或对象存储迁移能力。

## 风险与取舍

| 风险 | 缓解 |
|---|---|
| 人工 checklist 被误读为自动通过 | `/miniapp-prepare` 文案明确“待人工执行”，测试断言不出现自动 passed 语义。 |
| 体验版 Network 工具不可用 | `/miniapp-confirm` 支持 blocked/follow_up notes，记录替代观察方式和剩余风险。 |
| checklist 过长影响发布效率 | 只保留首页、一个列表页、一个详情或媒体资源页面作为最小必验主路径，扩展页面按发布范围执行。 |
| 证据泄露敏感信息 | evidence 标准继续禁止 token、Cookie、Authorization header、`.env`、真实密钥、真实隐私和未脱敏日志。 |

## 迁移计划

1. 更新小程序 evidence 标准，新增 Network evidence 来源、字段和示例。
2. 更新 miniapp prepare / confirm 技能说明和 `scripts/miniapp-env.py` checklist。
3. 更新 `src/miniapp/README.md` 的 release/miniapp 准备说明。
4. 补充静态测试，覆盖 checklist 文案和“人工 evidence 不等于自动通过”的边界。
5. 运行 `uv run pytest tests/test_miniapp_static.py` 或聚焦测试。

## 原型与冲突处理

本 REQ 没有 prototype；不涉及 Web UI 或小程序可见 UI。冲突优先级中 acceptance、标准文档和 specs 一致：本 Change 只扩展发布准备 checklist 与 evidence 记录口径，不修改页面视觉或交互。
