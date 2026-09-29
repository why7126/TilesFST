---
change_id: update-miniapp-price-red-display
requirement_id: REQ-0133-miniapp-price-red-display
created_at: 2026-09-05 22:23:57
updated_at: 2026-09-05 23:04:16
---

## 1. 视觉合同与首轮确认

- [x] 1.1 复核REQ验收矩阵、现有价格入口及BUG-0148图片适配，记录实现前状态和UI Contract对应关系。
- [x] 1.2 导出局部原型PNG，完成价格状态Skeleton、1440预览及移动视口首轮视觉确认；未通过不得关闭后续细节任务。

## 2. 价格状态与样式实现

- [x] 2.1 增加独立价格semantic token及小程序统一映射，同步规范端侧适用说明，保持品牌金及其他端样式。
- [x] 2.2 统一最小价格展示状态helper，覆盖有效、无价、非正、无法识别及不可查看输入，不重算price_display。
- [x] 2.3 接入共享商品卡片全部实际密度，拆分金额与辅助文案样式，保持TS/JS一致及grid图片适配。
- [x] 2.4 接入详情主价格、同系列/同品牌推荐与收藏价格，处理失效优先及异步状态切换。

## 3. 回归与视觉验收

- [x] 3.1 补充聚焦状态分支与数据切换测试，运行相关tests/test_miniapp_static.py回归并记录结果。
- [x] 3.2 按REQ页面矩阵完成价格入口、长金额、小字号、移动视口及实际小程序视觉验证，取得最终价格色值确认。
- [x] 3.3 记录金额、占位、辅助文字的computed style或等价证据及背景对比度≥4.5:1；更新过UI的旧证据重新取证。
- [x] 3.4 完成token同步/预览及无其他端变化检查，验证AC-OBS-001至003并记录API、DB、Orval、Docker、采集层级N/A依据。

## 4. 文档与交付一致性

- [x] 4.1 同步小程序说明、UI规范、REQ验收与Change trace证据，明确Mock、DevTools、真机来源及未覆盖边界。
- [x] 4.2 完成原型与实现最终一致性检查，运行OpenSpec、中文、目录及适用门禁；按流程同步状态，保留未完成验收项。

开发工作已执行；测试与视觉的证明边界、共享工作区回归失败及正式待验收项见 implementation/evidence.md 和 REQ acceptance.md。
