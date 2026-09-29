---
change_id: update-miniapp-price-red-display
requirement_id: REQ-0133-miniapp-price-red-display
created_at: 2026-09-05 22:22:41
updated_at: 2026-09-05 22:22:41
---

## ADDED Requirements

### Requirement: 小程序价格语义色与展示状态

小程序 SHALL 为有效金额定义独立价格语义红色，覆盖首页、商品列表、品牌详情商品列表、搜索SKU、商品详情主价格及同系列/同品牌推荐、收藏列表。有效金额 SHALL 为可公开查看商品的可识别正数价格，保持原price_display内容。辅助文字、无价及不可查看状态 SHALL 使用中性色，品牌金与错误色 SHALL 保持独立。

#### Scenario: 有效金额统一展示

- **WHEN** 任一范围页面展示可查看商品的有效金额
- **THEN** 货币符号与金额 SHALL 使用同一价格语义红色
- **AND** 系统 SHALL 保留金额原格式，参考价格及独立单位说明使用辅助色。

#### Scenario: 无价与失效状态

- **WHEN** 价格为空、零、非正、无法识别、旧无价文案或商品不可查看
- **THEN** 该节点 SHALL 不使用有效金额红色
- **AND** 系统 SHALL 沿用既有无价或失效处理，不因缓存金额显示有效报价。

#### Scenario: 数据状态切换

- **WHEN** 组件复用、刷新或切换商品使价格从有效变无价、从无价变有效或商品失效
- **THEN** 金额状态和颜色 SHALL 同步更新，无旧状态残留。

### Requirement: 小程序价格视觉一致性与边界验证

小程序价格样式 SHALL 复用独立语义token，不全局替换品牌金或借用错误token。共享卡片和独立详情、推荐、收藏价格 SHALL 遵循一致规则；有效金额与实际背景对比度 SHALL 不低于4.5:1。变更 SHALL 保持原字号、布局、图片适配及非价格交互，不影响其他端产品样式。

#### Scenario: 多入口与小字号验证

- **WHEN** 对共享卡片各实际密度、详情、推荐和收藏进行验收
- **THEN** 验收 SHALL 覆盖长金额、小字号、320/375/430移动宽度和实际背景透明度
- **AND** 不得新增溢出、遮挡或布局变化，品牌、按钮和非价格状态样式保持原有语义。

#### Scenario: 原型与实际样式证据

- **WHEN** 实施或归档该价格UI变更
- **THEN** SHALL 记录UI Contract、Skeleton首轮确认、1440预览及实际小程序视觉证据、关键computed style或等价证据和最终一致性结果
- **AND** SHALL 明确Mock与真实数据边界，不以原型截图或静态计算替代真机/体验版验收。

#### Scenario: 接口与观测边界

- **WHEN** 交付价格视觉增强
- **THEN** SHALL 确认API、数据库、价格计算、请求日志、行为事件、Task Trace及请求封装保持原行为
- **AND** SHALL 同步必要UI规范和token说明，执行相关状态与小程序静态回归，说明Orval及Docker验证为N/A的原因。
