---
bug_id: BUG-0065-miniapp-home-preview-deviation
status: done
lifecycle_stage: archive
severity: high
created_at: 2026-07-16 11:33:39
updated_at: 2026-07-19 15:35:19
lifecycle:
  captured: 2026-07-16 11:33:39
  generated: 2026-07-16 13:01:18
  completed: 2026-07-16 13:03:12
  reviewed: 2026-07-16 13:08:24
  approved: 2026-07-16 13:08:24
iteration: sprint-008
related_requirement: REQ-0041-miniapp-home
related_change: fix-miniapp-home-preview-runtime-entry
source_change: add-miniapp-home
openspec_changes:
  - change_id: fix-miniapp-home-preview-runtime-entry
    type: fix
    status: archived
related_bugs: []
captured_via: capture
classification_rationale: 已有小程序首页能力实现后出现原型/验收偏差，属于 BUG。
---

```yaml
bug_id: BUG-0065-miniapp-home-preview-deviation
status: done
severity: high
lifecycle:
  captured: 2026-07-16 11:33:39
  generated: 2026-07-16 13:01:18
  completed: 2026-07-16 13:03:12
  reviewed: 2026-07-16 13:08:24
  approved: 2026-07-16 13:08:24
iteration: sprint-008
related_requirement: REQ-0041-miniapp-home
related_change: fix-miniapp-home-preview-runtime-entry
source_change: add-miniapp-home
openspec_changes:
  - change_id: fix-miniapp-home-preview-runtime-entry
    type: fix
    status: archived
related_bugs: []
evidence:
  - issues/bugs/archive/BUG-0065-miniapp-home-preview-deviation/screenshots/miniapp-preview-deviation.png
scope:
  terminal: wechat_miniapp
  page: home
  suspected_areas:
    - UI visual mismatch
    - layout mismatch
    - data loading / empty state
    - prototype alignment
readiness:
  bug: done
  root_cause: done
  workaround: done
  acceptance: done
  review: done
  trace: done
  next: /opsx-apply fix-miniapp-home-preview-runtime-entry
```

## 来源

| 类型 | ID / 路径 | 说明 |
|---|---|---|
| REQ | `REQ-0041-miniapp-home` | 微信小程序首页原始需求与验收标准 |
| Source Change | `add-miniapp-home` | 当前已 apply 的小程序首页实现，不是本 BUG 的修复 Change |
| Screenshot | `screenshots/miniapp-preview-deviation.png` | 微信开发者工具预览截图 |

## 实施证据

| 时间 | 类型 | 证据 |
|---|---|---|
| 2026-07-16 13:40:44 | runtime-entry | `src/miniapp/pages/index/index.js` 已同步首页 `data`、`loadHome()`、分享、咨询、Banner、快捷入口和商品跳转逻辑 |
| 2026-07-16 13:40:44 | runtime-entry | `src/miniapp/pages/search/index.js`、`src/miniapp/pages/tile-detail/index.js`、`src/miniapp/pages/store-info/index.js` 已替换空模板 |
| 2026-07-16 13:40:44 | regression-test | `uv run pytest tests/test_miniapp_static.py`：7 passed |
| 2026-07-16 13:40:44 | compatibility-test | `uv run pytest tests/test_miniapp_home.py`：3 passed |
| 2026-07-16 13:40:44 | syntax-check | `find src/miniapp -name '*.js' -maxdepth 4 -print -exec node --check {} \\;`：通过 |
| 2026-07-16 13:40:44 | remaining-manual | 当前环境未打开微信开发者工具；实际预览截图与 375x812、390x844、320-430 pt 视口验收仍需人工执行 |
| 2026-07-16 14:00:29 | network-fix | 微信开发者工具出现“网络开小差”后，确认本地 Docker 后端映射为 `HOST_PORT_BACKEND=8010`，小程序请求层已增加 8010 本地备用地址并关闭开发工具 URL 校验 |
| 2026-07-16 14:00:29 | regression-test | `uv run pytest tests/test_miniapp_static.py`：8 passed |
| 2026-07-16 15:23:39 | network-fix | 确认 `project.private.config.json` 仍覆盖为 `urlCheck: true`，已改为 `false`；首页加载失败时现在输出 `[miniapp-home] loadHome failed` 诊断日志 |
| 2026-07-16 15:23:39 | regression-test | `uv run pytest tests/test_miniapp_static.py`：8 passed |
| 2026-07-16 15:26:23 | diagnostics | 请求层记录每个候选 API URL 的 `errMsg` / HTTP 状态，并在首页错误区展示 `诊断：...` |
| 2026-07-16 15:26:23 | regression-test | `uv run pytest tests/test_miniapp_static.py`：8 passed |
| 2026-07-16 23:30:32 | visual-alignment | 对照 REQ-0041 `prototype.html` 重构首页顶部品牌栏、黑金 Hero、五宫格快捷入口、新品横滑卡、热销深色信息层和服务区 |
| 2026-07-16 23:30:32 | regression-test | `uv run pytest tests/test_miniapp_static.py`：9 passed |
| 2026-07-16 23:49:43 | data-alignment | 首页 Logo 改用 `src/web/public/logos` 产品 Logo；Banner 使用后台 Banner 聚合数据；新品/热门卡使用 SKU 主图和 `price_display` |
| 2026-07-16 23:49:43 | tabbar | 启用自定义 tabBar，补首页/分类/找砖/我的图标，并放大底部文字到 24rpx |
| 2026-07-16 23:49:43 | regression-test | `uv run pytest tests/test_miniapp_static.py tests/test_miniapp_home.py`：13 passed |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-07-19 15:32:20 | lifecycle-stage-migrate | review → archive（/sprint-archive sprint-008 --force confirmed blockers: remaining wx devtools/device checks accepted as manual follow-up） |
| 2026-07-17 23:01:19 | /opsx-archive | Change `fix-miniapp-home-preview-runtime-entry` 已归档，状态同步完成。 |
| 2026-07-16 13:18:30 | /sprint-propose | 纳入 sprint-008 正式范围，容量估算 13.0/30.0 人天 |
| 2026-07-16 13:15:14 | /bug-opsx | 创建 OpenSpec Change `fix-miniapp-home-preview-runtime-entry`，状态 proposed |
| 2026-07-16 13:09:03 | lifecycle-stage-migrate | plan → review（/bug-review --approve） |
| 2026-07-16 13:08:24 | /bug-review --approve | 评审通过，状态更新为 approved，准备迁入 review 阶段 |
| 2026-07-16 13:03:12 | /bug-complete | 补齐 root-cause、workaround、acceptance；状态更新为 pending_review |
| 2026-07-16 13:01:18 | /bug-generate | 生成 bug.md，状态更新为 draft |
| 2026-07-16 11:33:39 | /capture | 记录微信小程序首页预览与原型/验收差异明显的缺陷 |

- 2026-07-17 23:01:19 workflow-sync：状态同步为 done（Change archived）
