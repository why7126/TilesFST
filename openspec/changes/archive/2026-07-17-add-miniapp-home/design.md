## Context

REQ-0041 已评审通过，目标是新增菲尚特微信小程序首页首期闭环。项目当前已有后台维护品牌、类目、规格、SKU、Banner、图片素材与使用行为日志的能力，但没有小程序首页能力，也没有面向终端客户的小程序首页聚合契约。

本 Change 只创建 OpenSpec 工件，不写 `src/`。实现阶段必须遵守：

- 小程序代码归属 `src/miniapp/`。
- API 变化同步 OpenAPI、Orval、docs 和测试。
- DB 变化同步 SQLite/MySQL schema、数据库文档和测试。
- 小程序端不得直连未授权对象存储。
- 来源于 REQ 的 Change 在 `/opsx-apply` 前必须纳入 Sprint。

## Goals / Non-Goals

**Goals:**

- 建立原生微信小程序首页，以及门店信息页、搜索页、商品详情页的首期闭环。
- 复用现有 SKU、品牌、类目、规格、Banner 和媒体数据，避免重复业务数据源。
- 支持首页/商品详情分享和至少一种门店咨询方式。
- 记录商品详情访问、分享、咨询等行为，用于热销推荐统计。
- 以 `prototype/miniapp/prototype.html` 与 `prototype/miniapp/prototype.png` 作为小程序 UI golden reference。

**Non-Goals:**

- 不实现收藏、预约表单、到店询价规则。
- 不实现快捷入口后台配置、服务入口后台配置。
- 不实现复杂用户画像、分享裂变活动、多渠道咨询工单管理。
- 不修改店主 Web 展示端。
- 不让小程序承载后台新增、编辑、上下架、库存、订单、客户管理等内部操作。

## Decisions

### D1. Change 类型与能力边界

本 Change 采用 `add` 类型，新建 `miniapp-home` 能力。已有 OpenSpec specs 中没有小程序首页能力；`web-client` 主要承载 Web 管理端/店主 Web，不能混入小程序页面契约。

替代方案：把小程序首页写入 `web-client`。拒绝原因是端边界不清，且 `src/miniapp/` 与 Web 的技术栈、运行环境、验收视口和 API 使用方式不同。

### D2. 首页数据聚合

首页可以新增 `GET /api/miniapp/home` 或等价聚合方式，但必须复用现有公开数据源。接口返回应至少覆盖门店摘要、Banner、新品、热销、快捷入口默认配置、服务展示和必要图片 URL。

替代方案：小程序分别请求多个后台管理接口。拒绝原因是管理端接口可能暴露内部字段、权限边界不一致，并增加首屏请求复杂度。

### D3. 行为统计策略

热销推荐以人工配置优先；行为统计作为辅助排序依据。首期至少记录 `product_detail_view`，建议记录 `product_share`、`home_share`、`product_contact_click`、`home_contact_click`。收藏量不参与首期排序，因为收藏功能不做。

替代方案：首期只按时间排序，不采集行为。拒绝原因是用户明确要求热销行为统计纳入本期，且后续推荐质量依赖可追溯事件基础。

### D4. 咨询能力降级

咨询入口至少支持微信客服、拨打电话或复制微信号中的一种。缺少配置的方式必须隐藏或安全降级，不能展示可点击失败入口。咨询事件记录不得包含敏感聊天内容或完整手机号等不必要个人信息。

### D5. 原型冲突处理

原型中出现收藏心形和底部收藏 Tab，但 REQ-0041 明确收藏不在本期。实现阶段必须隐藏、移除或置为非交互展示；不得产生半成品收藏入口。

原型优先级：

```text
prototype.html > prototype.png > prototype/miniapp/context.md > acceptance.md > rules/ui-design.md
```

若原型与 acceptance 冲突，以 acceptance 的范围控制为准。

## Risks / Trade-offs

- **行为统计引入 DB/API 变更** → 在 tasks 中单独拆分 API/DB/Orval/docs/test gate，避免小程序 UI 实现时遗漏治理同步。
- **咨询方式字段来源不清** → OpenSpec 保留“至少一种可用方式”要求；实现前确认门店配置来源，缺失方式必须隐藏。
- **Banner 配置目标可能指向未实现页面** → 小程序端必须安全降级，避免空白页或路由错误。
- **原型含收藏入口但本期不做收藏** → UI tasks 明确移除或隐藏收藏心形与收藏 Tab。
- **首屏请求复杂度上升** → 倾向使用聚合接口或后端聚合服务，控制小程序首屏请求数和失败隔离。

## Migration Plan

1. 在实现 Change 时确认 `src/miniapp/` 原生小程序骨架、构建方式和页面路由。
2. 先实现后端公开数据聚合与行为事件接收/统计契约。
3. 同步 OpenAPI、Orval、docs、SQLite/MySQL schema 和测试。
4. 再实现小程序首页、搜索、商品详情、门店信息、分享和咨询。
5. 以 acceptance 与原型完成 375x812、390x844 和 320-430pt 视口验收。

## Open Questions

- 门店咨询字段最终来源：微信客服、电话、微信号、导航配置分别在哪个配置对象中维护？
- 热销行为统计首期是否需要聚合缓存表，还是直接按 usage events 查询/聚合？
- 小程序包构建与本地验收命令是否已有项目约定，如没有需在实现阶段补齐 README 或脚本说明。
