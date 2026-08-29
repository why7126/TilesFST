---
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
title: 小程序证书详情页新增返回首页悬浮按钮验收标准
acceptance_status: passed
owner: product
source: requirement.md
created_at: 2026-08-25 22:39:27
updated_at: 2026-08-28 16:21:48
---

# 验收标准

## 功能 AC

- [ ] AC-001 证书详情页 `pages/certificate-detail/index` 声明并挂载 `home-floating-button` 组件。
- [ ] AC-002 悬浮按钮复用已有 `components/home-floating-button/`，不新增页面私有返回首页按钮结构、样式或跳转逻辑。
- [ ] AC-003 悬浮按钮默认使用 `offset="list"`，与品牌详情页、商品列表页以及商品详情页无底部操作区状态保持一致。
- [ ] AC-004 点击悬浮按钮后返回 `/pages/index/index`，优先沿用组件内 `wx.switchTab` 策略，失败时沿用组件兜底。
- [ ] AC-005 连续快速点击悬浮按钮时，不出现重复跳转、多次 toast、页面栈异常或导航锁无法恢复。
- [ ] AC-006 证书详情页原有自定义导航左上返回能力保持可用，无页面栈时仍可兜底到首页。
- [ ] AC-007 证书详情正常态、加载失败、证书不可查看、网络失败和分享直达场景均有可恢复的回首页路径。
- [ ] AC-008 新增悬浮按钮不改变证书详情数据加载、媒体展示、品牌入口、文件预览和分享路径。
- [ ] AC-009 `.ts` 与 `.js` 实现同步，避免小程序构建或上传时出现源文件漂移。

## UI AC

- [ ] AC-UI-001 悬浮按钮视觉、图标、文案、尺寸、按压态和忙碌态与现有 `home-floating-button` 保持一致。
- [ ] AC-UI-002 在 320 / 375 / 430 pt DevTools 视口下，按钮不遮挡证书主图、品牌入口、错误态按钮或底部安全区；证书信息字段被按钮覆盖可接受，页面不得为证书信息卡新增右侧避让。
- [ ] AC-UI-003 页面滚动时，悬浮按钮位置稳定，不造成横向滚动或页面内容跳动。
- [ ] AC-UI-004 按钮触控热区满足小程序触控体验，不小于现有组件标准。
- [ ] AC-UI-005 悬浮按钮不得覆盖品牌卡片主要点击区域；若与品牌入口距离过近，需通过既有 offset 或页面内容间距解决，不新增私有 offset。

## 小程序导航与证据 AC

来源：`docs/knowledge-base/best-practices/miniapp-custom-navigation.md`

- [ ] AC-NAV-001 分享卡片、扫码或外部入口直达证书详情页时，左上返回与悬浮返回首页入口均不得失效、报错或无反馈。
- [ ] AC-NAV-002 加载态、空状态、错误态和网络失败提示不被自定义导航栏或悬浮按钮遮挡。
- [ ] AC-NAV-003 返回首页或返回兜底涉及导航锁时，验收覆盖首次点击成功、再次进入同一页面、快速重复点击和失败兜底后的可恢复状态流。
- [ ] AC-NAV-004 DevTools 320 / 375 / 430 pt evidence 记录标题、返回、原生胶囊 reserve、内容 offset、品牌入口同宽和证书信息非避让排版结论。
- [ ] AC-NAV-005 真机 evidence 不可用时必须标记 `blocked` 或 `follow_up`，不得写作真机通过。

## 测试 AC

- [ ] AC-TEST-001 小程序静态检查覆盖证书详情页 `index.json` 组件声明、`index.wxml` 组件引用和页面路径注册。
- [ ] AC-TEST-002 静态检查或等价脚本确认 `home-floating-button` 在证书详情页使用 `offset="list"`。
- [ ] AC-TEST-003 回归既有已接入 `home-floating-button` 的商品详情页、品牌详情页和商品列表页，确认新增接入未改动全局组件行为。

## Knowledge-base 横切检查

| 标签 | 引用文档 | 将写入 AC-XCUT 条数 | 说明 |
|---|---|---:|---|
| 无匹配标签 | - | 0 | 本 REQ 为小程序页面导航体验，不属于 `admin-list`、`admin-form`、`admin-modal` 或上传链路 `media-upload`。 |
| miniapp-navigation | `docs/knowledge-base/best-practices/miniapp-custom-navigation.md` | 0 | 非 req-complete 强制横切标签；已转化为上方 `AC-NAV-*` 功能验收。 |

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-27 23:11:40
accepted_by: workflow-sync
source_change: update-miniapp-certificate-detail-home-floating-button
source_sprint: sprint-026
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

