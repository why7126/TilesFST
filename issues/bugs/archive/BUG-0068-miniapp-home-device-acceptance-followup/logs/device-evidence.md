---
purpose: BUG-0068 小程序首页 DevTools / 真机验收 evidence 记录
source: fix-miniapp-home-device-acceptance
template_ref: docs/standards/miniapp-device-evidence-template.md
created_at: 2026-07-19 19:40:29
updated_at: 2026-07-19 21:13:20
---

# BUG-0068 小程序首页设备验收 Evidence

## 1. Target

```yaml
miniapp_device_evidence:
  template_ref: docs/standards/miniapp-device-evidence-template.md
  target:
    type: bug
    id: BUG-0068-miniapp-home-device-acceptance-followup
    related_change: fix-miniapp-home-device-acceptance
    related_requirement: REQ-0041-miniapp-home
  pages:
    - page_path: "pages/index/index"
      title: "首页"
      query: ""
      scenarios:
        - "首页首屏真实预览"
        - "320-430 pt 视口"
        - "微信原生胶囊避让"
        - "fixed header 与底部 TabBar 内容不遮挡"
        - "Banner / 商品 / 图片 / 网络失败降级状态"
```

## 2. Evidence Items

| ID | 来源 | 状态 | 页面 / 场景 | 环境 | 证据 | 结论 | 剩余风险 / 原因 |
|---|---|---|---|---|---|---|---|
| static-001 | static_test | passed | `pages/index/index` / 运行入口与核心模块 | `uv run pytest tests/test_miniapp_static.py` | 19 passed | 静态测试覆盖运行入口、首页数据加载、首页核心模块、自定义导航声明、禁止伪胶囊、图片 fallback、底部安全区和基础点击尺寸侧证 | 不证明 DevTools 或真机真实渲染通过 |
| source-001 | source_review | passed | `pages/index/index` / 首页结构 | WXML / WXSS / JS 静态片段 | `src/miniapp/pages/index/index.*`、`src/miniapp/components/custom-navigation/index.*` | 首页存在品牌导航、搜索、Banner 或品牌化降级、快捷入口、新品推荐、热销推荐、全部产品、加载/错误/空状态和底部 TabBar 安全区样式 | 仅为源码静态侧证，不证明真实设备坐标 |
| devtools-320 | devtools | passed | `pages/index/index` / 320 pt 首页首屏 | 用户人工验证；DevTools 版本与基础库版本未随本消息提供 | 用户在 2026-07-19 21:13:20 确认“已人工验证” | 320 pt 首页首屏人工验收通过 | 建议后续补截图路径、DevTools 版本和基础库版本 |
| devtools-375 | devtools | passed | `pages/index/index` / 375 pt 首页首屏 | 用户人工验证；DevTools 版本与基础库版本未随本消息提供 | 用户在 2026-07-19 21:13:20 确认“已人工验证” | 375 pt 首页首屏人工验收通过 | 建议后续补截图路径、DevTools 版本和基础库版本 |
| devtools-390 | devtools | passed | `pages/index/index` / 390 pt 首页首屏 | 用户人工验证；DevTools 版本与基础库版本未随本消息提供 | 用户在 2026-07-19 21:13:20 确认“已人工验证” | 390 pt 首页首屏人工验收通过 | 建议后续补截图路径、DevTools 版本和基础库版本 |
| devtools-430 | devtools | passed | `pages/index/index` / 430 pt 首页首屏 | 用户人工验证；DevTools 版本与基础库版本未随本消息提供 | 用户在 2026-07-19 21:13:20 确认“已人工验证” | 430 pt 首页首屏人工验收通过 | 建议后续补截图路径、DevTools 版本和基础库版本 |
| device-001 | real_device | passed | `pages/index/index` / 胶囊、状态栏、fixed header、底部 TabBar | 用户人工验证；设备型号、系统、微信版本与基础库版本未随本消息提供 | 用户在 2026-07-19 21:13:20 确认“已人工验证” | 真机或等效设备人工验收通过 | 建议后续补设备型号、系统、微信版本、基础库版本和截图/录屏路径 |

## 3. AC 回归结论

| AC | 状态 | 结论 |
|---|---|---|
| AC-001 evidence 来源区分 | passed | 本记录已区分 static/source/DevTools/real device，并明确静态侧证不替代设备验收。 |
| AC-002 首页真实预览 | passed | 用户确认已人工验证首页真实预览。 |
| AC-003 320-430 pt 覆盖 | passed | 用户确认已人工验证 320、375、390、430 pt 及 320-430 pt 常见宽度。 |
| AC-004 微信原生胶囊避让 | passed | 用户确认已人工验证胶囊避让；静态侧证显示未手绘胶囊且有 reserve 区域。 |
| AC-005 fixed header 与底部 TabBar 不遮挡 | passed | 用户确认已人工验证 fixed header 与底部 TabBar 不遮挡；静态侧证显示 spacer 与 safe-area 样式存在。 |
| AC-006 降级状态可验收 | passed | 用户确认已人工验证降级状态；静态侧证显示加载、错误、空商品和图片 fallback 状态存在。 |
| AC-007 自动化侧证保留但不越界 | passed | 自动化侧证已保留且未写成 DevTools / 真机通过。 |
| AC-008 技术范围不扩大 | passed | 本次记录未修改 API、数据库、Web、管理端、Orval 或 Docker Compose。 |

## 4. Summary

```yaml
summary:
  status: passed
  conclusion: "自动化与源码侧证已补齐，tests/test_miniapp_static.py 为 19 passed；用户已确认 DevTools / 真机或等效设备人工验收通过。"
  blockers: []
  remaining_risks:
    - "本次对话未提供截图路径、DevTools 版本、基础库版本、设备型号、系统版本或微信版本；建议后续补充以增强可复核性。"
  next_owner: "tester"
  recommended_next_step: "如需发布级审计，可追加截图/录屏路径和设备元数据；不阻塞本 Change apply。"
```
