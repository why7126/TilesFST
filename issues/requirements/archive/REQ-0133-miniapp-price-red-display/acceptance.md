---
requirement_id: REQ-0133-miniapp-price-red-display
title: 价格展示验收清单
created_at: 2026-09-05 22:03:58
updated_at: 2026-09-06 14:19:46
acceptance_status: passed
---

# 价格展示验收清单

## 验收口径

以下复选框记录本次归档范围的开发验收结果；已完成的部分与未覆盖边界见 [实施证据](../../../../openspec/archive/2026-09-06-update-miniapp-price-red-display/implementation/evidence.md)。开发验证不代表业务或真机验收通过。功能事实源为 [需求文档](requirement.md)，局部视觉参照见 [原型说明](prototype/miniapp/context.md)。

## 功能 AC

- [x] AC-001（FR-001）可查看商品的 `¥128.00`、`￥1,280.50` 等有效金额，货币符号和数值均引用同一价格语义色，显示内容不被重新计算或改写。
- [x] AC-002（FR-002）“参考价格”、单独单位及门店确认说明为辅助色；原金额格式保持稳定。
- [x] AC-003（FR-002）空值、零价、负值、无法识别的输入和既有无价文案不使用价格红色，文案沿用现有无价处理。
- [x] AC-004（FR-002）失效收藏即使留有历史金额，也显示既有不可查看文案及中性色，不显示为有效报价。
- [x] AC-005（FR-003）逐项验证下方覆盖矩阵，全部实际价格入口与密度遵循相同规则。
- [x] AC-006（FR-003）有效→无价→有效、有效→失效的数据变化后颜色正确，无组件复用或异步刷新残留。
- [x] AC-007（FR-004）价格使用独立 semantic token；未散落页面红色常量、未替换品牌金或错误色；Web、管理端及非价格元素无视觉变动。
- [x] AC-008（FR-005）在 320、375、430 CSS px 对应预览宽度及目标手机环境检查长金额、推荐区小字号，未新增截断、遮挡、溢出或布局变化；金额与实际背景对比度≥4.5:1。
- [x] AC-009（FR-004）小程序用色规范与 token 适用范围同步，按实际 token 变更完成生成同步和 Design System 预览检查。
- [x] AC-010（FR-003）若调整状态逻辑，`.ts` 与实际加载的 `.js` 同步，聚焦状态测试和相关小程序静态回归通过。

## 页面覆盖矩阵

| 入口 | 价格节点 | 必测状态 |
|---|---|---|
| 首页新品／热门 | compact 商品卡片 | 有价、无价 |
| 首页全部产品 | grid 商品卡片 | 有价、无价、长金额 |
| 商品列表／品牌详情商品列表 | 共享商品卡片实际密度 | 有价、无价、状态更新 |
| 搜索最佳匹配／综合 SKU／SKU Tab | 共享商品卡片实际密度 | 有价、无价、切换结果 |
| 商品详情 | 主价格 | 有价、无价、加载与错误 |
| 同系列／同品牌推荐 | 独立推荐价格 | 有价、无价、长金额 |
| 收藏列表 | 独立收藏价格 | 有价、无价、失效、刷新 |

## 原型与证据 AC

- [x] AC-PROTOTYPE-001 在 Change 中建立 UI Contract，明确局部原型只约束价格颜色与状态，既有页面承担布局事实源；记录 Mock/API 边界及最终采用的价格色值。
- [x] AC-PROTOTYPE-002 实施时完成 UI Skeleton 首轮确认及 1440px 预览证据，再完成细节；补充小程序 DevTools／真机或等价视觉证据，记录默认及关键状态。
- [x] AC-PROTOTYPE-003 记录有效金额、占位文案、辅助文案的 computed style 或等价证据：选择器、页面、视口、color、背景、字号、透明度及对比度。更新 UI 后重新取证。
- [x] AC-PROTOTYPE-004 归档前核对原型、实际实现和范围矩阵一致性；不得以 HTML Mock 截图或静态计算冒充体验版、真机通过。

## 产品数据采集与链路观测 AC

- [x] AC-OBS-001 核对 `not_applicable`：差异仅为小程序展示、token 和必要规范；API、DB、请求日志、行为事件、Task Trace 及端请求封装未改动。
- [x] AC-OBS-002 未新增采集、个人数据、日志字段或存储，脱敏与保留周期保持既有策略；原型只使用合成数据，无请求、密钥或真实客户内容。
- [x] AC-OBS-003 Orval 与 Docker Compose 为 N/A，理由为接口契约、数据结构和部署输入不变；若实现扩大范围，先调整需求及验证声明，不以 N/A 掩盖影响。

## 横切 AC（knowledge-base）

未命中 `admin-list`、`admin-form`、`admin-modal`、`media-upload`：本需求只涉及小程序价格显示，无横切 AC，新增 AC-XCUT 共 0 条。

已阅读 `docs/knowledge-base/README.md` 和 `docs/knowledge-base/retrospectives/sprint-028-retrospective.md`。后者的环境证据边界经验由 AC-PROTOTYPE-004 承接；不引入无关的管理端确认框、分页或上传要求。

## 归档验收依据

用户在获知实施结果与验证边界后于2026-09-06执行 `/opsx-archive REQ-0133`。本次按已披露的开发验证范围归档，复测40/40通过；采用既有UI Contract、1440局部原型、移动组件与微信模拟器证据。未将该命令记录为用户亲自真机测试通过；真机、体验版及逐路由端到端未覆盖，Web全量类型检查与全局样式预览限制保持实施证据中的说明。

证据：[实施与视觉证据](../../../../openspec/archive/2026-09-06-update-miniapp-price-red-display/implementation/evidence.md)。

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-09-06 14:19:46
accepted_by: workflow-sync
source_change: update-miniapp-price-red-display
source_sprint: sprint-029
evidence: []
failed_items: []
source_event: opsx.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

