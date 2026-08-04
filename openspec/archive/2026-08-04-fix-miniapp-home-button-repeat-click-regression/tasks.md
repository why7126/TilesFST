## 1. 实现

- [x] 1.1 复核 `home-floating-button` 的 `navigating`、timer、`pageLifetimes.show()` 和 `detached()` 状态恢复路径。
- [x] 1.2 修复返回首页按钮在同页重复进入后第二次点击失效的问题。
- [x] 1.3 修复或确认跨页面重复进入时返回首页按钮状态互不污染。
- [x] 1.4 确保 `wx.switchTab` 成功、失败、`wx.reLaunch` 兜底成功/失败和超时路径都会释放导航锁。
- [x] 1.5 确认小程序 TypeScript 源码与运行时 JavaScript 同步，体验版不会加载旧逻辑。

## 2. 测试

- [x] 2.1 补充可执行状态流测试，覆盖“首次点击成功 → 再次进入页面 → 第二次点击仍触发返回首页”。
- [x] 2.2 补充失败与兜底路径测试，覆盖 `switchTab` fail 后 `reLaunch` complete 释放锁。
- [x] 2.3 补充快速重复点击测试，确认短时间内最多触发一次导航，防重复窗口后可再次点击。
- [x] 2.4 保留或更新小程序页面接入静态测试，确认覆盖页面仍使用统一返回首页组件。
- [x] 2.5 运行 `uv run pytest tests/test_miniapp_static.py` 或实现阶段新增的最小相关测试。

## 3. 验收与文档

- [x] 3.1 在验收材料中覆盖分类页、品牌列表页、搜索结果页、商品详情页和品牌详情页。
- [x] 3.2 验证 TabBar 页面与非 TabBar 页面第二轮点击行为一致。
- [x] 3.3 回填 BUG-0115 AC-001 至 AC-006 验收 evidence。
- [x] 3.4 若确认存在可复用导航状态陷阱，更新 `docs/knowledge-base/incidents/` 或 best-practice。
- [x] 3.5 运行 `openspec validate fix-miniapp-home-button-repeat-click-regression --strict` 和 `python scripts/validate-openspec-language.py`。
