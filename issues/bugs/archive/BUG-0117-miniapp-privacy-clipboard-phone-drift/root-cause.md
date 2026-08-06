---
bug_id: BUG-0117-miniapp-privacy-clipboard-phone-drift
created_at: 2026-08-05 09:43:30
updated_at: 2026-08-05 09:43:30
classification: design
---

# Root Cause

## 直接原因

小程序运行代码中仍保留了电话与剪贴板隐私接口调用：

- 门店信息页根据后端 `services[].action_type` 调用 `wx.makePhoneCall` 或 `wx.setClipboardData`。
- 证书详情页在文件打开失败时调用 `wx.setClipboardData` 复制文件 URL。

这些接口会被微信小程序提审流程识别为隐私相关能力，但当前产品真实面向用户不应提供电话拨打、复制门店微信号或复制证书文件链接功能。

## 根本原因

产品隐私能力口径收敛后，旧的咨询方式和证书文件兜底设计没有同步从端到端合约中移除，导致实现、Schema、文档和测试仍允许或描述旧能力：

- 后端服务仍允许 `miniapp.contact_phone` 触发 `phone` 动作。
- 后端服务仍默认返回 `miniapp.contact_wechat` 对应的 `copy_wechat` 动作。
- Pydantic Schema 仍允许 `phone` 与 `copy_wechat`。
- 小程序 `.ts` 和运行 `.js` 入口仍实现电话和剪贴板调用。
- OpenSpec、README、API 文档和测试仍保留电话、复制微信号或复制证书链接口径。

## 触发条件

1. 小程序提交审核。
2. 提审隐私信息选择“未采集用户隐私”。
3. 微信审核扫描到提交包中残留的 `wx.makePhoneCall` 或 `wx.setClipboardData` 调用。

## 缺陷分类

- `design`：产品隐私能力边界与旧规格/实现不一致。
- `code`：小程序运行代码和后端服务仍保留隐私接口触发路径。
- `docs`：OpenSpec、README、API 文档存在旧口径漂移。
- `test`：现有测试仍允许 `phone` 或 `copy_wechat` 动作，未约束小程序提交包不含隐私接口。

## 修复方向

后续修复应通过 OpenSpec Change 收敛产品能力边界，移除电话和剪贴板路径，并同步更新后端响应合约、小程序运行代码、文档与测试。
