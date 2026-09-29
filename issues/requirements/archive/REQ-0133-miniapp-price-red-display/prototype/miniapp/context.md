---
requirement_id: REQ-0133-miniapp-price-red-display
title: 价格状态局部原型说明
created_at: 2026-09-05 22:03:58
updated_at: 2026-09-05 23:04:16
---

# 价格状态局部原型说明

## 原型策略

[price-states.html](price-states.html) 是小程序价格状态的局部视觉原型，展示共享卡片、详情价格和收藏状态，不是完整页面重设计。合成名称、尺寸与金额仅供演示，无真实客户数据、外部资源、API 或埋点。

## 约束优先级

价格颜色与状态：HTML → 后续 PNG → 本说明 → acceptance → 需求及项目 UI 规范。页面布局、导航、图片比例、点击行为不由该局部原型改写，继续采用既有小程序实现。冲突时以需求范围为界，在 UI Contract 中明确处理。

## 视觉契约

- 价格候选 `--price: #F87171`；品牌金保留 `--brand: #C8A055`。
- 背景对应 `#18160F`、`#211E16`、`#252116`；有效金额不透明，中性与辅助色与金额分离。
- 稳定选择器为 `[data-role="amount"]`、`[data-role="placeholder"]`、`[data-role="label"]`；状态按钮只切换原型示例，不新增产品操作入口。
- `¥` 与金额同色，单位单独辅助色；有效、无价、失效状态分别展示。
- 颜色最终值在视觉验收中确认，HTML 候选不代表已通过用户验收。

## 交付与证据策略

HTML 与 [PNG 参考图](price-states.png) 已提供；实施侧已完成 Skeleton 自检与 DevTools 取证，详见 Change implementation/evidence.md，用户验收仍待确认。实施前需按 `docs/standards/prototype-ui-acceptance.md` 建立 UI Contract、完成 Skeleton 确认；实施及归档需补齐 1440px 与移动视口、实际小程序、computed style 和最终一致性证据。

原型 HTML 预览只能证明候选配色和演示状态，不证明原页面布局未变化，也不证明 API、体验版或真机已经通过。
