## 任务清单

- [x] 1. 后端契约收敛
  - [x] 1.1 收窄 `MiniappServiceItem.action_type`，移除 `phone` 与 `copy_wechat`。
  - [x] 1.2 调整 miniapp home 服务聚合，不再读取或下发 `miniapp.contact_phone` / `miniapp.contact_wechat` 对应动作。
  - [x] 1.3 确认 `GET /api/v1/miniapp/home` 仅返回无隐私接口副作用的服务项或安全降级为空动作。

- [x] 2. 小程序运行入口清理
  - [x] 2.1 移除门店信息页 `.ts` 中的 `wx.makePhoneCall` 与 `wx.setClipboardData` 分支。
  - [x] 2.2 同步移除门店信息页运行 `.js` 中的电话与剪贴板分支。
  - [x] 2.3 移除证书详情页 `.ts` 中复制文件 URL 的兜底。
  - [x] 2.4 同步移除证书详情页运行 `.js` 中复制文件 URL 的兜底。
  - [x] 2.5 文件打开失败时展示稳定错误提示，不调用剪贴板。

- [x] 3. API / Orval / 文档
  - [x] 3.1 重新导出 OpenAPI。
  - [x] 3.2 运行 Orval 生成前端客户端与类型。
  - [x] 3.3 更新 `docs/03-api-index.md` 的 miniapp home 示例和字段说明。
  - [x] 3.4 更新 `src/miniapp/README.md`，删除电话、复制微信号、复制证书文件链接口径。

- [x] 4. 测试与验收
  - [x] 4.1 更新小程序静态测试，断言 `src/miniapp` 不含 `wx.makePhoneCall` / `wx.setClipboardData`。
  - [x] 4.2 更新后端 home 测试，断言服务动作不返回 `phone` 或 `copy_wechat`。
  - [x] 4.3 覆盖配置存在 `miniapp.contact_phone` / `miniapp.contact_wechat` 时仍不暴露隐私接口动作。
  - [x] 4.4 覆盖证书详情文件失败路径不展示“文件链接已复制”。
  - [x] 4.5 小程序提审或预检证据确认选择“未采集用户隐私”不再触发电话或剪贴板接口提示。

- [x] 5. 校验
  - [x] 5.1 运行小程序静态测试。
  - [x] 5.2 运行后端 miniapp home 相关 pytest。
  - [x] 5.3 运行 OpenSpec 语言与结构校验。
  - [x] 5.4 如修复后有复用价值，补充 `docs/knowledge-base/incidents/` 事故沉淀或说明无需沉淀。
