---
change_id: fix-miniapp-home-preview-runtime-entry
change_type: fix
status: proposed
created_at: 2026-07-16 13:13:44
updated_at: 2026-07-16 13:13:44
related_bug: BUG-0065-miniapp-home-preview-deviation
related_requirement: REQ-0041-miniapp-home
source_change: add-miniapp-home
---

# Proposal: 修复小程序首页预览运行入口脱节

## Why

`BUG-0065-miniapp-home-preview-deviation` 已评审通过，微信开发者工具预览中的小程序首页与 `REQ-0041-miniapp-home` 原型和验收标准差异明显。

当前预览只展示静态搜索框、空商品提示和部分标题，未展示 Banner、快捷入口、新品推荐、热销推荐和完整服务卡片。根因分析显示：首页业务逻辑写在 `src/miniapp/pages/index/index.ts`，但微信开发者工具实际运行入口 `src/miniapp/pages/index/index.js` 仍是空模板，导致首页数据加载与交互逻辑未执行。

该问题阻断小程序首页首屏验收，必须通过 OpenSpec fix change 修复，避免绕过流程直接改源码。

## What Changes

- 修复小程序页面运行入口，使微信开发者工具实际预览加载首页业务逻辑。
- 明确 `.ts` 与 `.js` 的事实源策略：运行时 `.js` 必须与业务逻辑同步，或建立可验证的 TypeScript 编译链。
- 补充小程序运行入口脱节的静态/自动化回归测试，防止空模板 `.js` 再次覆盖业务 `.ts`。
- 复验首页首屏在微信开发者工具中展示品牌导航、搜索、Banner、快捷入口和至少一个推荐模块。
- 默认不修改后端 API、数据库 schema、Pydantic Schema、Orval、Docker Compose 或小程序业务范围。

## Scope

### In Scope

- `src/miniapp/` 页面运行脚本与构建/同步策略。
- 小程序首页、搜索页、商品详情页、门店信息页等关键页面的空模板脚本清理或同步。
- 小程序静态测试或等价 smoke 测试。
- BUG-0065 对应 trace、测试证据和验收记录。

### Out of Scope

- 新增小程序业务能力。
- 修改首页聚合 API 契约。
- 修改 SQLite/MySQL 数据库结构。
- 修改 Orval 生成物，除非实现中确认 API 契约发生变化。
- 快捷入口后台配置、服务入口后台配置、收藏、预约、到店询价规则或复杂用户画像。

## Rollback Plan

如修复导致小程序无法编译或预览：

1. 回滚本 Change 对 `src/miniapp/` 运行入口和构建/同步策略的修改。
2. 保留或恢复修复前可打开的小程序工程状态。
3. 回滚本 Change 新增或调整的相关测试。
4. 不回滚 `BUG-0065` 文档状态；如需重新设计修复方案，追加新的修订任务或后续 fix change。

## Risks

| 风险 | 缓解 |
|---|---|
| 手工同步 `.ts` 到 `.js` 后再次漂移 | 增加静态测试，禁止关键页面 `.js` 保持空模板或缺少关键逻辑 |
| 启用 TS 编译链影响微信开发者工具配置 | 优先选择与当前项目最小兼容的策略，并在验收中记录预览步骤 |
| 误判为后端无数据 | 分别验证运行入口执行、接口请求发起、无商品时模块级降级 |
| 修复扩大到 API/DB | tasks 中设置范围检查，默认不改 API/DB/Orval/Docker |

## Success Criteria

- 微信开发者工具首页预览实际执行首页业务逻辑。
- 首页首屏展示 REQ-0041 核心模块，并符合 BUG-0065 acceptance。
- 运行测试可捕获关键页面 `.js` 与 `.ts` 脱节问题。
- `openspec validate fix-miniapp-home-preview-runtime-entry` 通过。
