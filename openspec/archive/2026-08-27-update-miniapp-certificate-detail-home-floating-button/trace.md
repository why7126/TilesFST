---
change_id: update-miniapp-certificate-detail-home-floating-button
change_type: update
status: archived
source_requirement: REQ-0125-miniapp-certificate-detail-home-floating-button
sprint: sprint-026
created_at: 2026-08-25 22:55:41
updated_at: 2026-08-27 23:12:50
---

# Change 追踪

## 基本信息

```yaml
change_id: update-miniapp-certificate-detail-home-floating-button
change_type: update
status: archived
source_requirement: REQ-0125-miniapp-certificate-detail-home-floating-button
sprint: sprint-026
affected_capabilities:
  - miniapp-certificate-list-page
  - miniapp-global-custom-navigation-bar
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
```

## 需求来源

- REQ：`issues/requirements/archive/REQ-0125-miniapp-certificate-detail-home-floating-button/`
- Sprint：`iterations/archive/sprint-026/`
- 目标：小程序证书详情页新增【返回首页】悬浮按钮，复用 `home-floating-button offset="list"`。

## UI / 小程序证据清单

| 证据 | 状态 | 说明 |
|---|---|---|
| UI Contract | done | 已写入 `design.md`。 |
| Skeleton | done | 已在 `src/miniapp/pages/certificate-detail/index.json` 声明组件，并在 `index.wxml` 页面根末尾挂载 `<home-floating-button offset="list" />`，覆盖 loading / error / content 三类状态。 |
| 静态检查 | passed | `uv run pytest tests/test_miniapp_static.py -q`，36 passed；覆盖证书详情页组件声明、WXML 引用、`offset="list"`、品牌卡片同宽规则和证书信息卡恢复非避让 padding。 |
| TS/JS 同步 | passed | 本次未修改 `index.ts` / `index.js`；静态测试同时读取 runtime JS/TS 入口，未发现证书详情逻辑漂移。 |
| 全局组件回归 | passed | 静态测试覆盖商品详情、品牌详情、商品列表等既有返回首页按钮页面；`home-floating-button` 组件源码未改动。 |
| DevTools 320 pt | passed | 用户附件 `codex-clipboard-d6418c82-819f-4ced-b484-898953630eb1.png` 显示品牌卡片外框同宽，右侧箭头未额外调整，证书信息卡恢复非避让排版。 |
| DevTools 375 pt | passed | 用户附件 `codex-clipboard-200c58ca-aef8-4637-bfe8-5f7639900aa7.png` 显示品牌卡片外框同宽，右侧箭头未额外调整，证书信息卡恢复非避让排版。 |
| DevTools 430 pt | passed | 用户附件 `codex-clipboard-0cafc797-25f6-4e4d-a380-d70d7034c14a.png` 显示品牌卡片外框同宽，证书信息卡恢复非避让排版；悬浮按钮局部覆盖证书信息字段为验收允许项。 |
| 分享直达兜底 | static_pass | 证书详情页在页面根挂载按钮；全局组件负责 `/pages/index/index`、`wx.switchTab`、`wx.reLaunch` 和失败提示。实际分享直达操作需验收阶段补 DevTools / 真机证据。 |
| 重复点击导航锁 | static_pass | 全局组件保留 `navigating`、`LOCK_TIMEOUT_MS`、`pageLifetimes.show()` 重置和 fallback unlock；聚焦静态测试覆盖状态流断言。 |
| 真机 evidence | follow_up | 当前环境不可用；不得写作真机通过，需体验版或真机验收补证。 |

## 实现记录

| 文件 | 变更 | 验证 |
|---|---|---|
| `src/miniapp/pages/certificate-detail/index.json` | 新增 `home-floating-button` usingComponents 声明 | `tests/test_miniapp_static.py` |
| `src/miniapp/pages/certificate-detail/index.wxml` | 页面根末尾新增 `<home-floating-button offset="list" />`；按验收反馈撤回品牌入口 `custom-class` 内部避让 | `tests/test_miniapp_static.py` |
| `src/miniapp/pages/certificate-detail/index.wxss` | 保留底部滚动安全留白；移除品牌入口右侧缩窄规则；证书信息卡 `.panel` padding 恢复为 `26rpx`，不再为悬浮按钮做右侧避让 | `tests/test_miniapp_static.py` |
| `tests/test_miniapp_static.py` | 将证书详情页纳入返回首页悬浮按钮覆盖范围和 `offset="list"` 断言 | `uv run pytest tests/test_miniapp_static.py -q` |

## 变更记录

| 时间 | 命令 | 说明 |
|---|---|---|
| 2026-08-26 08:32:09 | 用户三视口复验截图 | 320 / 375 / 430 pt 复验通过：品牌卡片外框同宽、右侧箭头未额外调整、证书信息卡非避让排版；证书信息字段局部覆盖为验收允许项 |
| 2026-08-26 08:28:56 | `/opsx-modify` | 按验收反馈恢复证书信息卡 `.panel` 原始 `26rpx` padding；悬浮按钮遮挡证书信息可接受 |
| 2026-08-26 08:21:44 | `/opsx-modify` | 按验收反馈「返回上一步的效果，不要调整右侧箭头」撤回 `brand-card` 内部避让方案，恢复上一版品牌卡片外框同宽效果 |
| 2026-08-26 08:13:44 | 用户三视口复验截图 | 品牌卡片外框已恢复同宽，但 320 / 375 pt 中【首页】按钮仍压到品牌卡右侧箭头；已新增品牌卡内容安全区，待重新复验 |
| 2026-08-25 23:24:38 | `/opsx-modify` | 验收反馈指出 430 pt 截图中品牌卡片被缩窄；已移除 `.brand-card-section` 右侧缩窄规则，保留底部安全留白和证书信息卡右侧字段安全区，待 320 / 375 / 430 pt 重新复验 |
| 2026-08-25 23:18:41 | 用户 430 pt 复验截图 | 430 pt 复验通过；按钮位于内容下方安全区，未遮挡品牌入口和证书信息字段值 |
| 2026-08-25 23:14:52 | 用户三视口截图反馈 | 320 / 375 / 430 pt 复验截图仍显示悬浮按钮压到品牌入口或证书信息；已二次补充右侧内容安全区，待重新截图复验 |
| 2026-08-25 23:08:45 | 用户截图反馈 | 375 视口截图显示悬浮按钮遮挡证书信息；已补底部安全留白，待重新截图复验 |
| 2026-08-25 23:03:10 | `/opsx-apply` | 完成证书详情页组件声明、WXML 挂载和静态测试；DevTools / 真机 evidence 需验收阶段补证 |
| 2026-08-25 22:55:41 | `/req-opsx` | 从 REQ-0125 创建 OpenSpec Change，等待 Workflow Sync 回填 Sprint scope |

## 附件截图逐项视觉对照表

| 附件 / 视口 | 期望 | 实际反馈 | 返修处置 | 复验状态 |
|---|---|---|---|---|
| `codex-clipboard-d6418c82-819f-4ced-b484-898953630eb1.png` / 320 pt | 品牌卡片外框同宽，右侧箭头不额外调整，证书信息卡不做右侧避让 | 符合期望 | 记录为 320 pt 正常态复验通过 | passed |
| `codex-clipboard-200c58ca-aef8-4637-bfe8-5f7639900aa7.png` / 375 pt | 品牌卡片外框同宽，右侧箭头不额外调整，证书信息卡不做右侧避让 | 符合期望 | 记录为 375 pt 正常态复验通过 | passed |
| `codex-clipboard-0cafc797-25f6-4e4d-a380-d70d7034c14a.png` / 430 pt | 品牌卡片外框同宽，证书信息卡不做右侧避让；按钮局部覆盖证书信息字段可接受 | 符合期望 | 记录为 430 pt 正常态复验通过 | passed |
| `codex-clipboard-1b4e8a33-f7a8-4a45-815f-dd50dec85311.png` / 430 pt | 证书信息卡不做右侧避让，按钮遮挡证书信息可接受 | 证书信息卡右侧字段被挤到中间，仍有避让效果 | `.panel` padding 恢复为 `26rpx`，删除证书信息字段右侧避让 | needs_recheck |
| `codex-clipboard-e658eadb-3a84-4567-938d-5625c243d5b9.png` / 375 pt | 品牌卡片外框同宽，不调整右侧箭头；证书信息卡不做右侧避让 | 复验截图用于确认当前视觉状态 | 保持品牌卡片外框同宽，不调整箭头；恢复 `.panel` padding | needs_recheck |
| `codex-clipboard-fb12f0e6-d6fc-496e-bff1-9059be325dea.png` / 320 pt | 品牌卡片外框同宽，不调整右侧箭头；证书信息卡不做右侧避让 | 复验截图用于确认当前视觉状态 | 保持品牌卡片外框同宽，不调整箭头；恢复 `.panel` padding | needs_recheck |
| `codex-clipboard-ff430a03-c964-4613-a7d2-ca3b1cabcae0.png` / 320 pt | 返回上一版效果：品牌卡片外框同宽，不调整右侧箭头 | 品牌卡片外框已同宽；用户要求不要调整右侧箭头 | 撤回 `brand-card` 内部内容安全区，仅保留上一版页面级安全留白和证书信息字段安全区 | needs_recheck |
| `codex-clipboard-26d5f798-e918-43e2-8cd7-646a4a66899a.png` / 375 pt | 返回上一版效果：品牌卡片外框同宽，不调整右侧箭头 | 品牌卡片外框已同宽；用户要求不要调整右侧箭头 | 同上，撤回内部箭头避让 | needs_recheck |
| `codex-clipboard-f7c00aa1-3052-4ce7-8e9c-dabc007f14e0.png` / 430 pt | 返回上一版效果：品牌卡片外框同宽，不调整右侧箭头 | 品牌卡片外框已同宽，证书信息字段基本安全 | 同上，等待三视口复验 | needs_recheck |
| `codex-clipboard-e3a61098-8762-48b8-87af-fbba7faf50fc.png` / 430 pt | 品牌卡片与上方标题卡、下方证书信息卡外框同宽；【返回首页】悬浮按钮不遮挡内容 | 【返回首页】按钮未遮挡证书信息，但品牌卡片因右侧避让规则被缩窄 | 移除 `.brand-card-section { margin-right: 158rpx; }`；保留证书信息卡右侧字段安全区和页面底部滚动安全留白 | needs_recheck |
| `codex-clipboard-7f4341ff-e6f0-4cc6-a4e9-46607e8b0e57.png` / 320 pt | 品牌卡片外框同宽，按钮不遮挡品牌入口与证书信息 | 旧截图中按钮贴近品牌入口覆盖区，且后续避让方案会缩窄品牌卡片 | 改为不缩窄品牌卡片，仅保护证书信息卡字段区和底部滚动区 | needs_recheck |
| `codex-clipboard-42720017-e48c-453d-9b0b-5edfa5eb8aa4.png` / 375 pt | 品牌卡片外框同宽，按钮不遮挡品牌入口与证书信息 | 旧截图中品牌入口区域为避让按钮被缩窄 | 恢复品牌卡片同宽，等待同视口复验 | needs_recheck |
