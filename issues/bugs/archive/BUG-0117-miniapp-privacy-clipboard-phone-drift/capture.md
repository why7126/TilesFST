---
bug_id: BUG-0117-miniapp-privacy-clipboard-phone-drift
status: done
created_at: 2026-08-05 09:36:21
updated_at: 2026-08-05 22:41:16
severity_hint: high
environment: miniapp-review
related_requirement:
related_bug:
lifecycle_stage: plan
---

# 现象

小程序提交审核时，微信检测到代码中存在隐私接口调用，但当前产品真实面向用户不应提供电话拨打、复制门店微信号或复制证书文件链接能力。若提审选择“未采集用户隐私”，审核通过并发布后相关隐私接口权限可能被回收，导致残留代码路径无法正常调用；若改为声明这些隐私能力，则与当前产品口径不一致。

# 复现步骤

1. 使用当前小程序代码包提交微信小程序审核。
2. 在提审隐私信息处选择“未采集用户隐私”。
3. 审核提示代码中检测到隐私接口调用，发布后相关隐私接口权限将被回收。
4. 静态排查小程序运行代码，确认存在 `wx.makePhoneCall` 与 `wx.setClipboardData` 调用。

# 期望 vs 实际

- 期望：小程序真实面向用户不提供电话拨打、复制门店微信号、复制证书文件链接能力；提交审核时不应检测到电话或剪贴板隐私接口；产品文档、OpenSpec、后端 Schema、后端服务、小程序运行代码和测试口径保持一致。
- 实际：后端仍允许 `phone` 与 `copy_wechat` 服务动作；小程序门店信息页仍根据服务动作调用 `wx.makePhoneCall` 或 `wx.setClipboardData`；证书详情页在文件打开失败时仍使用 `wx.setClipboardData` 复制文件 URL；部分 OpenSpec/README/API 示例仍保留旧能力口径。

# 影响范围

- 微信小程序提审隐私声明与发布权限。
- 小程序门店信息页服务区咨询动作。
- 小程序证书详情页 PDF/文件打开失败兜底路径。
- `GET /api/v1/miniapp/home` 的 `services[].action_type` 合约。
- 小程序相关 OpenSpec、README、API 文档和静态/后端测试。

# 初步线索

- `src/miniapp/pages/store-info/index.ts` 与同目录 `.js` 中存在 `wx.makePhoneCall` 和 `wx.setClipboardData`。
- `src/miniapp/pages/certificate-detail/index.ts` 与同目录 `.js` 中存在 `wx.setClipboardData`，成功提示为“文件链接已复制”。
- `src/backend/app/services/miniapp_home_service.py` 会读取 `miniapp.contact_phone`，并在无电话时默认返回 `miniapp.contact_wechat` 对应的 `copy_wechat` 服务动作。
- `src/backend/app/schemas/miniapp_home.py` 的 `MiniappServiceItem.action_type` 仍允许 `phone` 与 `copy_wechat`。
- `openspec/specs/miniapp-home/spec.md` 与 `openspec/specs/miniapp-certificate-list-page/spec.md` 仍存在电话、复制微信号或复制提示相关口径。

# 建议验收或复现要点

- [ ] `src/miniapp` 提交包代码中不再出现 `wx.makePhoneCall` 或 `wx.setClipboardData`。
- [ ] `GET /api/v1/miniapp/home` 不再返回 `services[].action_type=phone` 或 `copy_wechat`。
- [ ] 后端 Schema、服务实现、API 文档与测试同步移除电话/复制微信号动作口径。
- [ ] 证书文件打开失败时仅展示稳定错误提示或非剪贴板兜底，不再复制文件 URL。
- [ ] OpenSpec 与 `src/miniapp/README.md` 同步删除电话、复制微信号、复制证书文件链接的产品口径。
- [ ] 小程序提审选择“未采集用户隐私”时不再因电话或剪贴板接口触发隐私接口检测提示。

# 附件

- 暂无。
