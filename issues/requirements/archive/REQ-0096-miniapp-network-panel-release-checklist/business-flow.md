---
requirement_id: REQ-0096-miniapp-network-panel-release-checklist
created_at: 2026-08-04 08:42:00
updated_at: 2026-08-04 08:42:00
---

# Business Flow

## 1. 发布准备主流程

```text
发布负责人运行 /miniapp-prepare
  |
  +-- 自动门禁
  |     |
  |     +-- 切换小程序策略到 prod
  |     +-- project.private.config.json urlCheck=true
  |     +-- uv run pytest tests/test_miniapp_static.py
  |     +-- 生产接口 smoke: /miniapp/home
  |     +-- 生产接口 smoke: /miniapp/brands
  |
  +-- 输出人工 checklist
        |
        +-- 微信开发者工具重新上传开发版本
        +-- 微信公众平台设为体验版
        +-- 手机删除旧体验版入口并重新扫码
        +-- DevTools Network evidence
        +-- 体验版 Network evidence
        |
        +-- /miniapp-confirm 记录结论
              |
              +-- passed -> 可进入提审或发布确认
              +-- failed -> 阻断，返修或重新准备
              +-- blocked -> 记录阻塞原因与重试条件
              +-- follow_up -> 记录剩余风险、责任人与承接方式
```

## 2. Network evidence 检查流程

```text
选择验证入口
  |
  +-- DevTools
  |     |
  |     +-- 记录 DevTools 版本 / 基础库 / 运行策略 / urlCheck
  |     +-- 打开关键页面
  |     +-- 观察 Network 请求域名、HTTP 状态、业务 code
  |     +-- 观察图片、视频、证书、静态资源加载
  |     +-- 记录结论：不等同体验版或真机网络验收
  |
  +-- 体验版
        |
        +-- 确认最新开发版本已设为体验版
        +-- 手机删除旧入口并重新扫码
        +-- 访问首页、列表、详情、证书或媒体页面
        +-- 观察生产域名和资源加载
        +-- 记录 passed / failed / blocked / follow_up
```

## 3. 关键页面范围

| 页面 / 场景 | 必验原因 | 主要网络关注点 |
|---|---|---|
| 首页 | 用户进入小程序的主路径 | 首页聚合接口、Banner、推荐商品、错误态。 |
| 分类或品牌入口 | 列表导航主路径 | 列表接口、分页、空态、网络失败提示。 |
| 品牌列表或品牌详情 | 品牌公开展示路径 | Logo、品牌商品、类目汇总、图片资源。 |
| SKU 列表 | 商品浏览主路径 | 商品卡片、主图、缩略图、分页稳定性。 |
| SKU 详情 | 转化和媒体展示主路径 | 详情接口、图片、视频、受控媒体 URL、失败态。 |
| 证书列表或详情 | 资质展示路径 | 证书图片、证书文件、资源加载失败态。 |

## 4. 异常与决策

| 异常 | 处理 |
|---|---|
| 自动门禁失败 | `/miniapp-prepare` 不通过，优先修复环境、静态测试或生产接口 smoke。 |
| DevTools 请求错误环境 | 标记 failed，阻断发布准备通过，检查 miniapp env 策略和运行入口同步。 |
| 体验版请求错误域名 | 标记 failed，阻断发布准备通过，检查合法域名、体验版版本和环境策略。 |
| 核心页面 API 失败 | 标记 failed，记录页面、接口、HTTP 状态、业务 code 和影响范围。 |
| 媒体资源加载失败 | 按资源类型记录 URL/render 失败，可引用媒体或对象存储验收模板。 |
| 账号、设备或体验版不可用 | 标记 blocked，记录责任环境、重试条件和当前发布风险。 |
| 非核心页面未覆盖 | 可标 follow_up，但必须记录剩余风险、责任人和承接方式。 |

## 5. 与既有 REQ / 模板差异

| 对象 | 差异 |
|---|---|
| `REQ-0052-miniapp-device-evidence-template` | 关注 DevTools/真机设备 evidence 的通用口径；本 REQ 聚焦 release/miniapp 发布前 Network evidence。 |
| `REQ-0091-media-bug-four-point-acceptance-template` | 关注媒体 BUG 的 key/object/URL/render 闭环；本 REQ 只在发布前对小程序资源加载做清单化确认。 |
| `/miniapp-prepare` 现有流程 | 已有 prod、urlCheck、静态测试和生产 smoke；本 REQ 增加人工 DevTools/体验版 Network checklist。 |

## 6. Prototype 策略

本 REQ 为发布与小程序准备清单治理，不新增小程序可见页面，也不涉及 Web 管理端表单、列表或弹窗。因此 prototype 为 N/A。
