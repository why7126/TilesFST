## Why

Web 端管理端和展示端当前部分标准弹窗允许点击遮罩或弹窗外空白区域自动关闭。用户在编辑 SKU、品牌、类目、证书、Banner、上传媒体或执行确认操作时，误点外部区域可能中断流程、丢失输入状态或取消确认上下文。

REQ-0084 已评审通过，要求 Web 端电脑端标准 Dialog / Modal 统一禁用外部点击关闭，并保留明确关闭入口，以降低误触风险并沉淀为可复用交互规范。

## What Changes

- 将 Web 管理端和 Web 展示端标准 Dialog / Modal 的默认交互调整为：点击遮罩或弹窗外空白区域不关闭。
- 保留明确关闭路径：关闭图标、取消按钮、返回按钮、确认 / 保存成功后的业务关闭，以及经评审确认的 Esc 键关闭策略。
- 更新已有弹窗规格中与 REQ-0084 冲突的旧表述，例如“遮罩关闭弹窗”。
- 要求统一 Dialog / Modal 封装或等价基础组件默认禁用 outside click close；历史未复用组件的弹窗需盘点补齐。
- 继承 admin-modal 与 media-upload 横切验收：弹窗宽度 CSS 层叠、矮视口滚动、上传状态机和即时回显不得回退。
- 明确非目标范围：微信小程序弹窗、Popover、Dropdown、Tooltip、Select 下拉层、日期选择器、未保存改动二次确认、弹窗视觉重设计、后端 API / DB / 存储链路。

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- `web-client`: 更新 Web 管理端和展示端标准弹窗关闭策略，修改已有品牌确认弹窗、SKU 弹窗和管理端表单弹窗移动端规格中的关闭行为约束。
- `design-system`: 补充 Dialog / Modal 默认交互治理，要求共享弹窗组件默认禁用外部点击关闭并保留明确关闭入口。

## Impact

- Web: 影响管理端和展示端标准 Dialog / Modal 关闭交互；需要盘点共享组件和历史自定义弹窗。
- Admin: 影响 SKU、品牌、类目、证书、Banner、用户、系统设置确认等管理端标准弹窗。
- Miniapp: 不影响。
- Backend / API / Database / Storage: 不影响；不得新增或修改接口、错误码、Pydantic Schema、OpenAPI、Orval、数据库迁移、MinIO 或 Nginx 上传配置。
- Tests: 需要补充前端组件测试或 Playwright smoke，覆盖外部点击不关闭、明确关闭入口可关闭、表单状态保留、确认弹窗保持打开和上传弹窗状态不丢失。
