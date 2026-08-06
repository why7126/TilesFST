## 背景与原因

BUG-0117 已评审通过并纳入 sprint-020。当前小程序真实面向用户不应提供电话拨打、复制门店微信号或复制证书文件链接能力，但代码包、后端服务合约和文档测试仍残留 `wx.makePhoneCall`、`wx.setClipboardData`、`phone`、`copy_wechat` 等旧能力口径。

微信小程序提审时选择“未采集用户隐私”会检测到这些隐私接口调用，导致提审声明与产品实际能力不一致。若改为声明电话或剪贴板能力，又违背当前产品口径。因此需要通过修复 Change 收敛小程序隐私接口边界。

## 变更内容

- 移除小程序提交包中的电话拨打与剪贴板调用路径。
- 收敛 `GET /api/v1/miniapp/home` 的门店服务动作，不再返回 `phone` 或 `copy_wechat`。
- 调整后端 `MiniappServiceItem.action_type` 合约，移除电话和复制微信号动作口径。
- 证书详情页 PDF/文件打开失败时只展示稳定错误提示，不再复制受控 URL。
- 同步 OpenSpec、`src/miniapp/README.md`、`docs/03-api-index.md`、静态测试、后端测试、OpenAPI 与 Orval。
- 提审前验收需确认代码包不含 `wx.makePhoneCall` / `wx.setClipboardData`，选择“未采集用户隐私”时不再触发电话或剪贴板隐私接口提示。

## 能力影响

### 新增能力

- 无。

### 修改能力

- `miniapp-home`: 门店服务和咨询入口不再暴露电话或复制微信号动作；小程序端不得触发电话或剪贴板隐私接口。
- `miniapp-certificate-list-page`: 证书详情 PDF/文件失败兜底不再复制文件 URL，仅展示稳定错误提示或非隐私接口兜底。

## 影响范围

- 小程序：门店信息页服务动作、证书详情文件打开失败路径、`.ts` 与运行 `.js` 双入口同步。
- 后端：`GET /api/v1/miniapp/home` 服务聚合、Pydantic Schema、相关测试。
- API：公开小程序 home 响应合约变化，需要同步 OpenAPI、Orval 和 API 文档。
- 文档：OpenSpec、`src/miniapp/README.md`、`docs/03-api-index.md`。
- 测试：小程序静态测试、后端 home 测试、提审隐私接口验收。
- 数据库：不新增或修改 SQLite/MySQL 表结构。
- Web 管理端与店主 Web：不涉及。

## 回滚计划

- 若修复后发现门店服务缺失导致用户无法理解服务区，可仅恢复非隐私接口的展示文案或静态说明，不恢复电话或剪贴板调用。
- 若证书文件打开失败体验不足，可增加非剪贴板的错误提示、重试或返回证书列表入口。
- 不建议回滚到 `wx.makePhoneCall`、`wx.setClipboardData` 或隐私声明偏差方案；如业务重新确认需要电话/剪贴板能力，必须另建需求并同步隐私声明。
