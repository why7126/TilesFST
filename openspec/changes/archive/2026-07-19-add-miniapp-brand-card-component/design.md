## Context

REQ-0054 已评审并纳入 `sprint-009`，目标是把微信小程序 SKU 详情页中的内联品牌信息抽成可复用 `brand-card` 组件。现有 `miniapp-sku-detail-page` 规格已要求 SKU 详情页展示品牌入口，但没有定义组件边界、Logo fallback、跳转 fallback、异常状态和埋点参数。

本 Change 的视觉来源优先级为：

1. `prototype/miniapp/brand-card-component.html`
2. `prototype/miniapp/brand-card-component-context.md`
3. `acceptance.md`
4. `rules/ui-design.md`
5. 现有 `openspec/specs/miniapp-sku-detail-page/spec.md`

## Goals / Non-Goals

**Goals:**

- 新增微信小程序 `brand-card` 可复用组件契约。
- 首版替换 SKU 详情页现有内联品牌卡片结构。
- 固化 Logo 缺失/加载失败、长品牌名、入口不可用、连续点击等卡片级行为。
- 明确跳转优先级：`brand_entry_path` > 品牌关键词搜索 fallback > 不可用提示。
- 保持组件纯展示/交互边界，不让组件直接请求品牌、SKU 或列表接口。

**Non-Goals:**

- 不新增品牌 API、数据库字段、Logo 上传、MinIO 前缀或安全策略。
- 不实现完整品牌主页、品牌故事页、品牌商品列表容器、分页或筛选状态机。
- 不建设 Web/管理端品牌卡片组件。
- 不展示品牌证书列表或证书详情。

## Decisions

### D1. UI 策略：小程序原生组件 + 现有深色轻奢视觉

采用小程序原生组件沉淀在 `src/miniapp/components/brand-card/`。样式参考 prototype 中的深色卡片、品牌金描边、固定 Logo 容器和三列布局，但实现时应映射到小程序现有 WXSS 变量/类名，不新增跨端 Web DS token。

原因：本需求影响 `miniapp`，不是 Web UI；用小程序原生组件可直接服务 SKU 详情页和后续小程序页面，避免引入 React/Web 组件边界。

### D2. 数据边界：页面容器传入单品牌展示对象

`brand-card` 接收页面容器从 SKU 详情数据中提取的品牌展示对象、来源上下文和可选入口配置。组件不直接请求品牌详情、品牌列表、SKU 列表或搜索接口。

原因：SKU 详情页已有数据加载职责；组件保持纯展示/交互后，后续品牌商品列表、同品牌推荐、首页品牌推荐也能复用同一参数结构。

### D3. 跳转策略：配置入口优先，搜索 fallback 收口

点击品牌卡时，组件优先使用 `brand_entry_path`；缺失但品牌名称可用时 fallback 到品牌关键词搜索页，并对品牌名称做 URL 编码；入口不可用或品牌名称不可用时阻止跳转并提示“品牌内容暂不可查看”或等价文案。

原因：完整品牌主页/品牌馆能力不在本 Change 范围内，搜索 fallback 可以在不新增 API/页面容器的前提下提供可用承接页。

### D4. 运行入口同步：实现时同步 `.ts` 与实际加载 `.js`

若项目当前小程序运行时实际加载编译后的 `.js`，实现阶段必须同步源码 `.ts` 与实际加载文件，或在任务输出中说明项目认可的构建同步方式。

原因：近期小程序验收复盘指出源码与微信开发者工具实际加载文件容易漂移，本组件首版需要避免同类问题。

## Conflict Resolution

- HTML prototype 与 `rules/ui-design.md` 均使用深色背景、品牌金强调和稳定卡片层级，没有冲突。
- HTML prototype 使用裸 Hex 仅作为静态原型表达；实现阶段小程序 WXSS 应复用现有小程序色彩变量或已认可样式常量，不把 prototype 裸 Hex 作为 Web TSX/CSS token 写入。
- `acceptance.md` 的 AC-022 允许 PNG Golden Reference 后续补齐；本 Change 不因缺 PNG 阻塞，但 `trace.md` 会记录 PNG checklist 为待补齐/非阻断。
- 现有 `miniapp-sku-detail-page` 只要求“品牌卡或底部品牌按钮”进入品牌承接页；本 Change 在不移除底部品牌按钮的前提下，要求页面品牌卡使用新组件，并保留原有品牌入口能力。

## Risks / Trade-offs

- [品牌主页尚未完整建设] → 使用 `brand_entry_path` 与品牌关键词搜索 fallback，避免强行新增品牌页范围。
- [Logo URL 可能缺失或加载失败] → 固定尺寸容器、首字/默认占位和图片失败埋点，保证卡片不破图、不跳高。
- [小程序窄屏布局溢出] → 验收覆盖 320/375/430 pt 宽度，长品牌名截断或按设计策略换行，不挤压箭头。
- [重复点击导致多次跳转] → 组件需要防重复点击或跳转锁，测试覆盖连续快速点击。
- [组件边界膨胀] → 规格明确组件不承接品牌商品列表分页、筛选、页面加载态和完整品牌主页。
