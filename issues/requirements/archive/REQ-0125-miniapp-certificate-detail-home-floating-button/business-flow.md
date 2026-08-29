---
requirement_id: REQ-0125-miniapp-certificate-detail-home-floating-button
title: 小程序证书详情页新增返回首页悬浮按钮业务流程
owner: product
source: requirement.md
created_at: 2026-08-25 22:39:27
updated_at: 2026-08-26 08:32:09
---

# 业务流程

## 1. 主流程

```text
用户进入证书详情页
  ↓
页面加载证书详情、媒体区、证书信息和品牌入口
  ↓
页面挂载 home-floating-button，offset 使用 list
  ↓
用户点击【首页】悬浮按钮
  ↓
home-floating-button 启动导航锁，调用 wx.switchTab('/pages/index/index')
  ↓
跳转成功，用户回到小程序首页
```

## 2. 兜底流程

```text
用户从分享、扫码或外部入口直达证书详情页
  ↓
页面栈可能没有上一页
  ↓
用户点击自定义导航返回或悬浮首页按钮
  ↓
返回策略进入首页兜底
  ↓
若 switchTab 失败，则按既有组件策略 reLaunch 到首页
```

```text
证书详情加载失败 / 证书不可查看 / 网络失败
  ↓
页面展示错误态或空态
  ↓
home-floating-button 仍作为可恢复入口保留
  ↓
用户点击后回到首页继续浏览
```

```text
用户快速连续点击悬浮按钮
  ↓
home-floating-button 使用现有 navigating 锁
  ↓
忽略重复触发或按现有锁定策略恢复
  ↓
不得出现重复跳转、多次 toast 或无法再次返回首页
```

## 3. 与父需求差异

| 对象 | 本需求边界 | 与父需求关系 |
|---|---|---|
| `REQ-0085-miniapp-global-home-floating-button` | 只补齐证书详情页缺失的悬浮按钮接入，不改变全局组件契约。 | 继承父需求的返回首页能力、首页例外和核心内容遮挡规避原则；证书信息字段可被局部覆盖。 |
| `REQ-0080-miniapp-certificate-detail-page` | 只新增页面级回首页入口，不重做证书详情媒体区、品牌入口、字段和分享能力。 | 在证书详情页既有能力上补齐导航一致性。 |
| `REQ-0121-miniapp-certificate-detail-brand-card-entry` | 只约束悬浮按钮不得遮挡 brand-card，不改变品牌入口数据和埋点。 | 与品牌入口复用能力并存，保证点击区域不冲突。 |

## 4. 角色责任

| 角色 | 责任 |
|---|---|
| 小程序页面 | 在证书详情页声明并挂载 `home-floating-button`，传入 `offset="list"`。 |
| `home-floating-button` 组件 | 继续负责首页路径、导航锁、`switchTab` 和 `reLaunch` 兜底。 |
| 自定义导航组件 | 保持左上返回与无页面栈首页兜底可用。 |
| 测试 | 验证正常态、错误态、分享直达、重复点击和 320/375/430 pt 布局一致；证书信息字段被按钮局部覆盖可接受。 |
