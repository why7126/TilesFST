---
change_id: add-miniapp-share-add-guide
status: archived
type: add
source_requirement: REQ-0061-miniapp-share-add-guide
created_at: 2026-07-20 08:11:32
updated_at: 2026-07-20 23:23:22
owner: product
iteration: sprint-009
---

# Change Trace

## 基本信息

```yaml
change_id: add-miniapp-share-add-guide
change_type: add
status: archived
source_requirement: REQ-0061-miniapp-share-add-guide
requirement_path: issues/requirements/archive/REQ-0061-miniapp-share-add-guide/
iteration: sprint-009
capabilities:
  new:
    - miniapp-share-add-guide
  modified: []
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
orval_required: false
docker_compose_required: false
knowledge_base_refs:
  - docs/knowledge-base/best-practices/miniapp-custom-navigation.md
  - docs/knowledge-base/retrospectives/sprint-008-retrospective.md
device_evidence:
  devtools_320: recorded_static_pass_devtools_unavailable
  devtools_375: recorded_static_pass_devtools_unavailable
  devtools_430: recorded_static_pass_devtools_unavailable
  real_device: passed
```

## Requirement Readiness Report

| 项 | 结论 |
|---|---|
| REQ status | approved |
| Readiness | Ready |
| 六件套 | capture、requirement、user-stories、business-flow、acceptance、trace、review、prototype 已存在 |
| Knowledge-base gate | N/A for admin cross-cutting；引用小程序自定义导航 best-practice |
| Next gate | 必须先纳入 Sprint 后才能 `/opsx-apply` |

## Impact Report

```yaml
impact:
  backend: false
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: false
capabilities:
  new:
    - miniapp-share-add-guide
  modified: []
```

## Conflict Report

| 来源 | 结论 |
|---|---|
| prototype/miniapp/prototype.html | 表达气泡位置和视觉意图，非强制像素稿 |
| prototype/miniapp/context.md | 明确安全降级可不展示 |
| acceptance.md | 明确关闭后至少当前会话内不再展示 |
| miniapp-global-custom-navigation-bar spec | 胶囊 reserve 与禁止手绘系统胶囊优先 |
| miniapp-device-evidence-template spec | 静态测试、DevTools 与真机 evidence 必须分层 |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-20 23:23:22 | `/opsx-apply add-miniapp-share-add-guide` | 补充静态视口 evidence，覆盖 320/375/430 pt 引导语、关闭按钮、胶囊 reserve 与首屏内容无重叠约束；当前环境仍未运行微信开发者工具截图 |
| 2026-07-20 18:33:08 | `/opsx-archive add-miniapp-share-add-guide` | Change 已归档到 `openspec/changes/archive/2026-07-20-add-miniapp-share-add-guide/`；带 warning 归档，DevTools 320/375/430 pt evidence 任务未补齐 |
| 2026-07-20 18:28:41 | 用户验收反馈 | 用户确认已完成真机验收；implementation/device-evidence.md real_device 更新为 passed，仍缺设备型号、系统类型和微信版本细节 |
| 2026-07-20 15:45:32 | 文档同步 | 更新 implementation evidence、REQ trace 与 Sprint 验收摘要，记录两行文案、三点符号和 right 52px 定位策略 |
| 2026-07-20 13:06:05 | 用户预览反馈 | 将引导语从页面流式位置调整为基于原生胶囊 bottom/right 的 fixed 定位，贴近右上角分享按钮下方 |
| 2026-07-20 13:06:05 | 用户预览反馈 | 引导语整体左移 12px，凸起位置更靠近右上角分享按钮中心 |
| 2026-07-20 13:06:05 | 用户预览反馈 | 引导语再次左移 12px，进一步让凸起对准分享按钮中部 |
| 2026-07-20 13:06:05 | 用户预览反馈 | 引导语继续左移 12px，按预览反馈微调凸起对齐 |
| 2026-07-20 13:06:05 | 用户文案反馈 | 将引导语文案调整为点击右上角三点提示符后添加到我的小程序，方便下次找回 |
| 2026-07-20 13:06:05 | 用户排版反馈 | 将引导语固定为两行展示，避免文案换成三行 |
| 2026-07-20 09:44:43 | `/opsx-apply --sprint auto` | 完成首页轻量引导语、当前会话关闭状态、胶囊 reserve fallback、静态测试与 implementation/device-evidence.md；DevTools 320/375/430 当前环境 blocked，真机 evidence follow_up |
| 2026-07-20 08:34:38 | `/sprint-propose sprint-009` | 纳入 sprint-009 正式范围；后续可通过 `/opsx-apply add-miniapp-share-add-guide --sprint auto` 执行 |
| 2026-07-20 08:11:32 | `/req-opsx` | 从 REQ-0061 创建 OpenSpec Change，新增 miniapp-share-add-guide capability |
