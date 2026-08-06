---
purpose: 小程序隐私接口漂移事故复盘
content: 记录电话与剪贴板隐私接口残留导致提审隐私声明不匹配的经验
source: BUG-0117-miniapp-privacy-clipboard-phone-drift
created_at: 2026-08-05 14:42:11
updated_at: 2026-08-05 14:42:11
---

# 小程序隐私接口漂移

## 现象

小程序提交审核时，微信提示代码中检测到隐私接口调用，但当前产品真实面向用户不提供电话拨打、复制门店微信号或复制证书文件链接能力。

## 根因

产品隐私能力口径收敛后，旧咨询方式和证书文件兜底没有同步从端到端合约中移除：

- 小程序运行 `.js` 仍保留 `wx.makePhoneCall` 和 `wx.setClipboardData`。
- 后端 home 聚合仍可能返回 `phone` 或 `copy_wechat` 动作。
- 文档、OpenSpec 和测试仍描述旧能力。

## 预防规则

- 小程序提审前必须静态扫描提交包，确认不含未声明或非产品能力范围内的隐私接口。
- 同一页面的 `.ts` 与运行 `.js` 必须同步维护，不能只改类型化源码。
- 后端响应合约、Pydantic Schema、OpenAPI、Orval、API 文档和小程序 README 必须与隐私声明口径一致。
- 文件打开失败兜底不得默认使用剪贴板；若需要复制、电话、定位、相册、摄像头等能力，必须先确认产品能力和微信隐私声明。

## 验证建议

- 运行 `uv run pytest tests/test_miniapp_static.py::test_miniapp_submission_bundle_has_no_phone_or_clipboard_privacy_api`。
- 运行 miniapp home 相关后端测试，确认服务动作不返回 `phone` 或 `copy_wechat`。
- 提审前在微信公众平台或开发者工具预检中确认选择“未采集用户隐私”不再提示电话或剪贴板接口。
