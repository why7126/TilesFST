---
change_id: fix-miniapp-home-device-acceptance
created_at: 2026-07-19 18:14:29
updated_at: 2026-07-19 21:13:20
---

# Tasks

- [x] 1. 建立 BUG-0068 小程序首页 DevTools / 真机验收 evidence 记录，包含设备、版本、逻辑宽度、截图或人工摘要、验收时间和结论。
- [x] 2. 使用微信开发者工具打开 `src/miniapp/`，验证 `pages/index/index` 真实加载首页运行脚本和首页核心模块。
- [x] 3. 覆盖 320、375、390、430 pt 及 320-430 pt 常见宽度，检查无横向滚动、关键文本不可读、卡片挤压或首屏大面积空白。
- [x] 4. 检查首页品牌导航、微信原生胶囊、状态栏、自定义 fixed header、搜索入口、Banner、推荐模块和底部 TabBar 是否互不遮挡。
- [x] 5. 检查 Banner 为空、商品为空、图片加载失败或首页请求失败时的降级状态仍满足设备布局验收。
- [x] 6. 若 evidence 发现遮挡、重叠、横向滚动、关键模块缺失或内容不可读，修复 `src/miniapp/` 中对应首页或自定义导航 UI。
- [x] 7. 运行并按需补充 `uv run pytest tests/test_miniapp_static.py`，确保自动化侧证覆盖运行入口、自定义导航、禁止伪胶囊和基础布局边界。
- [x] 8. 回归 `BUG-0068` 的 AC-001 到 AC-008，明确区分自动化、DevTools、真机和人工结论。
- [x] 9. 更新 BUG / Sprint / Change trace 与验收材料，不得把缺少真机 evidence 的结果写作真机通过。
- [x] 10. 若本缺陷暴露可复用事故经验，评估是否补充 `docs/knowledge-base/incidents/`。

## Apply Notes

- Task 2-5 已由用户在 2026-07-19 21:13:20 确认“已人工验证”；本记录不伪造设备型号、版本或截图路径。
- Task 6 当前未发现可由自动化/源码侧证触发的遮挡或重叠修复项；若 DevTools / 真机截图发现 UI 问题，再修改 `src/miniapp/`。
- Task 10 评估结果：已有 `docs/knowledge-base/incidents/miniapp-runtime-entry-drift.md` 与 `docs/standards/miniapp-device-evidence-template.md` 覆盖本次经验，本轮不新增 incident 文档。
