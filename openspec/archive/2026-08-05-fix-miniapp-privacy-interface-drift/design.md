## 设计目标

本 Change 只收敛小程序隐私接口边界，不新增新的咨询、客服、分享或文件分发能力。目标是让真实产品能力、提交包代码、后端响应合约、文档测试和微信提审隐私声明保持一致。

## 影响分析

```yaml
impact:
  backend: true
  web: false
  miniapp: true
  admin: false
  database: false
  storage: false
  api: true
capabilities:
  new: []
  modified:
    - miniapp-home
    - miniapp-certificate-list-page
```

## D1 小程序隐私接口收敛

小程序提交包不得包含以下调用：

```text
wx.makePhoneCall
wx.setClipboardData
```

门店信息页不再根据 `services[].action_type` 触发电话或剪贴板动作。若服务项仅用于展示，点击应无电话、剪贴板或隐私接口副作用；如需要用户反馈，可使用普通 toast 提示当前服务信息暂不可操作。

小程序 `.ts` 源码与运行 `.js` 文件必须同步修改，避免微信开发者工具实际加载旧 `.js`。

## D2 后端 home 合约收敛

`GET /api/v1/miniapp/home` 的 `services[].action_type` 不再允许：

- `phone`
- `copy_wechat`

后端应移除 `miniapp.contact_phone` 与 `miniapp.contact_wechat` 对小程序服务动作的输出影响。系统可以继续返回 `none` 类型的门店服务说明，也可以隐藏缺少安全动作的服务项；但不得把电话或微信号作为可复制/可拨打动作下发给小程序。

该响应合约变化需要同步 Pydantic Schema、OpenAPI、Orval、`docs/03-api-index.md` 和后端测试。

## D3 证书详情文件失败兜底

证书详情页继续优先使用 `wx.downloadFile` + `wx.openDocument` 打开 PDF 或未知文件。失败时只展示稳定错误提示，例如“文件暂不可打开”，不得复制受控 URL，不得展示“文件链接已复制”。

该调整不改变后端受控媒体 URL 的生成和访问边界，也不暴露对象存储原始 object key。

## D4 测试策略

测试必须覆盖：

- `src/miniapp` 静态扫描无 `wx.makePhoneCall`。
- `src/miniapp` 静态扫描无 `wx.setClipboardData`。
- 门店信息页运行入口 `.ts` / `.js` 同步，不存在电话或剪贴板分支。
- 证书详情页文件失败路径不复制 URL。
- 后端 home 响应不返回 `phone` 或 `copy_wechat`。
- `miniapp.contact_phone` 或 `miniapp.contact_wechat` 配置存在时也不暴露电话/剪贴板动作。

## D5 API / Orval 同步

`MiniappServiceItem.action_type` 枚举收窄属于 API 契约变化，必须：

- 更新后端 Pydantic Schema。
- 导出 OpenAPI。
- 运行 Orval。
- 更新小程序或 Web 侧使用到的生成类型与测试断言。
- 复核生成物使用 diff/stat，不在验收报告中展开 generated 全文。

## D6 风险与边界

- 该 Change 不负责新增微信客服、在线咨询或文件分享能力。
- 若运营仍需要门店联系方式展示，应另行确认是否属于隐私能力，并通过新需求同步隐私声明。
- 若微信平台仍提示其它隐私接口，应记录接口清单并按独立 BUG 处理，避免扩大本 Change 范围。
