---
bug_id: BUG-0117-miniapp-privacy-clipboard-phone-drift
title: 小程序残留电话与剪贴板隐私接口能力导致提审隐私声明不匹配
severity: high
status: done
owner:
discovered_at: 2026-08-05 09:36:21
environment: miniapp-review
related_requirement:
related_change:
created_at: 2026-08-05 09:38:53
updated_at: 2026-08-05 22:40:58
---

# 缺陷说明

## 现象

小程序提交微信审核时，平台提示当前代码中检测到隐私接口调用，但产品真实面向用户不应提供电话拨打、复制门店微信号或复制证书文件链接能力。

如果提审时选择“未采集用户隐私”，审核提示发布后相关隐私接口权限会被回收，残留代码路径可能无法正常调用。若改为声明电话或剪贴板能力，又会与当前产品口径不一致。

## 复现步骤

1. 使用当前小程序代码包提交微信小程序审核。
2. 在提审隐私信息处选择“未采集用户隐私”。
3. 观察审核提示：代码中检测到隐私接口调用，发布后相关隐私接口权限将被回收。
4. 静态排查小程序运行代码，确认存在电话与剪贴板接口调用路径。

## 期望 vs 实际

期望：

- 小程序真实面向用户不提供电话拨打、复制门店微信号、复制证书文件链接能力。
- 小程序提交包不包含 `wx.makePhoneCall` 或 `wx.setClipboardData` 调用。
- `GET /api/v1/miniapp/home` 不返回电话或复制微信号服务动作。
- 产品文档、OpenSpec、后端 Schema、后端服务、小程序运行代码和测试口径保持一致。
- 提审选择“未采集用户隐私”时，不因电话或剪贴板接口触发隐私接口检测提示。

实际：

- 小程序门店信息页仍根据服务动作调用 `wx.makePhoneCall` 或 `wx.setClipboardData`。
- 证书详情页在文件打开失败时仍使用 `wx.setClipboardData` 复制文件 URL。
- 后端服务仍允许返回 `phone` 与 `copy_wechat` 动作。
- 后端 Schema、OpenSpec、README、API 文档和测试仍残留电话、复制微信号或复制证书链接相关口径。

## 影响范围

- 微信小程序提审隐私声明与发布权限。
- 小程序门店信息页服务区咨询动作。
- 小程序证书详情页 PDF/文件打开失败兜底路径。
- `GET /api/v1/miniapp/home` 的 `services[].action_type` 响应合约。
- 小程序相关 OpenSpec、README、API 文档、静态测试与后端测试。

## 严重等级说明

严重等级为 `high`。

该问题会阻断或误导小程序提审隐私声明，影响发布合规与正式版权限表现；同时涉及前端运行代码、后端响应合约、Schema、文档与测试多处口径漂移。问题不属于线上全站不可用或数据破坏，因此未评为 `critical` 或 `blocker`。

## 初步证据

- `src/miniapp/pages/store-info/index.ts` 与同目录 `.js` 存在 `wx.makePhoneCall` 和 `wx.setClipboardData`。
- `src/miniapp/pages/certificate-detail/index.ts` 与同目录 `.js` 存在 `wx.setClipboardData`，成功提示为“文件链接已复制”。
- `src/backend/app/services/miniapp_home_service.py` 仍读取 `miniapp.contact_phone`，并默认返回 `miniapp.contact_wechat` 对应的 `copy_wechat` 服务动作。
- `src/backend/app/schemas/miniapp_home.py` 的 `MiniappServiceItem.action_type` 仍允许 `phone` 与 `copy_wechat`。
- `openspec/specs/miniapp-home/spec.md` 与 `openspec/specs/miniapp-certificate-list-page/spec.md` 仍存在电话、复制微信号或复制提示相关口径。
