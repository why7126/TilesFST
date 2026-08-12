---
title: 原型上下文
purpose: 描述用户管理页联系信息维护增量原型的范围与验收方式
content: UI prototype context
source: REQ-0110 requirement.md
update_method: 原型或验收策略变化时同步更新
owner: product
created_at: 2026-08-11 22:09:55
updated_at: 2026-08-11 22:17:22
---

# 原型上下文

## 文件

- `admin-user-contact-info.html`

## 原型目标

展示用户管理页在既有列表与弹窗基础上新增联系邮箱、手机号码维护能力后的信息层级。

## 视觉边界

- 继承管理端暗色工业风、品牌金主按钮、低圆角和细分割线。
- 本原型只表达增量字段和列表联系信息展示，不替代 `REQ-0005-user-management` 的完整列表/弹窗原型。
- PNG Golden Reference 待 OpenSpec apply 阶段按 1440px 视口导出。

## 交互边界

- 添加/编辑弹窗支持邮箱、手机号填写与清空。
- 列表在「状态」后新增「联系邮箱」「手机号码」独立列，空值显示 `-`。
- 搜索文案表达用户名、昵称、邮箱、手机号均可检索。
- 不包含邮件/短信通知、验证码、找回密码或手机号/邮箱登录。
