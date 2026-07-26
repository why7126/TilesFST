---
change_id: fix-miniapp-home-device-acceptance
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 18:14:29
---

# Design: 小程序首页设备验收闭环

## 1. 根因与设计目标

`BUG-0068` 的本质不是已确认的接口或数据库缺陷，而是设备验收 evidence 没有成为可追踪交付物。设计目标是让实现阶段可以先补齐可复核 evidence，再根据真实截图决定是否需要修复小程序 UI，避免把自动化测试通过误写成真机通过。

## 2. 修复策略

### 2.1 evidence 先行

实现阶段应先建立本 BUG 的验收记录，至少覆盖：

- 微信开发者工具版本或可识别版本摘要。
- 小程序基础库版本。
- 页面路径 `pages/index/index`。
- 320、375、390、430 pt 和 320-430 pt 常见宽度。
- 首页首屏核心模块是否真实展示。
- 微信原生胶囊、状态栏、fixed header、底部 TabBar 和安全区避让结论。
- 截图、录屏或人工验收摘要引用。

如果真机无法执行，必须标记 `blocked` 或 `follow_up`，不得写作真机通过。

### 2.2 布局缺陷按截图修复

若 evidence 发现 UI 缺陷，修复范围限定在：

- `src/miniapp/pages/index/` 首页结构、样式或运行入口。
- `src/miniapp/components/custom-navigation/` 或等价自定义导航组件。
- 小程序安全区、胶囊避让、顶部 offset、底部 TabBar spacer 或页面状态样式。
- 小程序静态测试或针对设备验收边界的脚本检查。

默认不改 API、DB、Orval、Web、管理端和 Docker Compose。若 evidence 发现接口或数据缺陷，应另行 capture 或提独立 Change。

### 2.3 验收结论边界

验收材料必须区分：

| 类型 | 可证明 | 不可证明 |
|---|---|---|
| 静态测试 | 运行入口、自定义导航声明、禁止伪胶囊、基础点击尺寸样式存在 | DevTools 真实渲染、真机安全区、真实胶囊坐标 |
| DevTools 截图 | 模拟器环境首页真实预览、逻辑宽度视觉结果 | 真机通过，除非另有真机 evidence |
| 真机截图 | 指定设备和微信版本下的真实视觉结果 | 所有机型全量通过 |

## 3. 测试设计

- 保留并运行 `uv run pytest tests/test_miniapp_static.py`。
- 如修改小程序首页或导航栏，补充静态测试覆盖新增避让、spacer、禁止手绘胶囊或点击尺寸规则。
- 人工验收覆盖 `acceptance.md` 中 AC-001 到 AC-008。

## 4. 回滚与失败处理

- evidence 不充分时不合并为完成态，标记 `follow_up` 或 `blocked`。
- 设备截图发现缺陷但无法在本 Change 内修复时，保留失败截图和复现宽度，输出标准 capture 文案，未授权时不自动创建新 Issue。
- UI 修复回滚时只撤销小程序相关文件，保留 BUG 与 Change trace。
