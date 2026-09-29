---
title: sprint-029 发布说明
created_at: 2026-08-30 15:36:34
updated_at: 2026-09-11 09:12:44
---

# sprint-029 发布说明

## 范围摘要

- 强化发布流程产品版本号门禁：release prepare 和 publish 必须校验 Web 与小程序用户可见 `PRODUCT_VERSION` 等于发布版本。
- 任一版本源不一致时，发布确认必须阻断，并提示更新版本源后重跑 `/image-prepare` 与 `/image-build`。
- 纳入腾讯 WorkBuddy 自定义连接器支持需求，第一阶段规划本地 stdio MCP + Skill 只读 PoC，后续通过 OpenSpec Change 落地。
- 纳入 BUG-0148 小程序商品列表 grid 卡片图片展示修复，仅覆盖复用 `density="grid"` 商品卡片的列表场景。

## 用户可见变化

- REQ-0132 远程入口补齐 Streamable HTTP JSON 版本/请求校验与安全错误，新增非 root 单实例部署包和本地 SDK/容器验收入口。写工具默认关闭、JSON 默认上限 8 MiB；真实 HTTPS 原生和企业策略验收仍未完成，不代表正式发布。

- REQ-0132：SKU 下架明确使用 DISABLED，DRAFT 保留为旧下架别名；上传拒绝无扩展名、扩展名/MIME 不符、含路径文件名及空/非法 Base64；品牌/类目连接器写入补 Task Trace。新增独立本地验收脚本，仍不代表 HTTPS 原生和跨主机验收通过。

- WorkBuddy 增加运行时参数校验、基础业务字段预览、错误安全摘要和中文 Skill；重复写操作通过持久化账本阻断，不确定结果需先核对。
- 远程入口改为按用户凭据映射与后端身份验证，旧共享 Bearer 不再生效；部署需迁移密钥配置并挂载持久化幂等目录。真实 HTTPS 与写入全链路仍待验收。

- 修复 WorkBuddy 原生 MCP 工具结果解析失败，采用标准文本内容块，并完成本机搜索与目录摘要原生调用验证。

- WorkBuddy SKU 搜索兼容非标准整数分页（例如 5 自动转为 10）；目录摘要按指定样本数截取，避免后端拒绝非标准分页。

- 当前规划动作不直接改变产品用户界面；后续连接器实现将影响企业内部 WorkBuddy 使用者的 SKU 查询、目录摘要和受控管理操作体验，BUG-0148 实现后将改善小程序商品 grid 列表整图展示。

## 技术变化

- 治理范围涉及发布技能、发布规则、release validator 和聚焦测试。
- REQ-0132 后续 Change 预计涉及 `src/mcp/workbuddy/`、`connectors/workbuddy/`、后端 API 调用、鉴权审计、Task Trace、请求日志、媒体上传链路、Docker/HTTPS 部署与测试。
- BUG-0148 后续 Change 预计涉及 `src/miniapp/components/product-card/` grid 样式、复用该卡片的商品列表/品牌详情/首页 grid 场景，以及 `tests/test_miniapp_static.py` 静态断言；不涉及 API、DB、Orval、对象存储或 Docker Compose。

## 状态

```yaml
sprint_id: sprint-029
status: active
requirements:
  - REQ-0132-workbuddy-custom-connector
bugs:
  - BUG-0148-miniapp-product-list-card-image-fit
changes:
  - enforce-product-version-release-gates
  - simplify-single-release-target-governance
  - automate-product-version-release-prepare
  - make-release-propose-next-step-prepare
  - converge-release-prepare-automation
  - deactivate-environment-tiered-evidence-gates
  - rename-evidence-source-specs
  - define-connector-directory-boundaries
```

## REQ-0133 计划交付

小程序有效金额统一红色展示，涵盖共享商品卡片、详情推荐和收藏；无价及失效文案使用中性色。已纳入正式范围并关联update-miniapp-price-red-display，尚未完成实现，不表述为已发布功能。API、DB、Orval与Docker无新增影响。

## REQ-0134 计划交付

补齐11个公开页面朋友及朋友圈分享、完整筛选恢复、安全卡片、发现页现有搜索入口和分享事件语义。已纳入sprint-029并关联 `add-miniapp-public-page-sharing`，尚未完成实现；不表述为已发布能力。仅预期影响小程序和usage_events，API、DB、Web、管理端、Orval及Docker不新增影响。

## REQ-0134 图片分享返修

公开轻量图片验证成功后，分享复用已解码的本地文件，避免原地址随后过期影响卡片。原生异常素材开发验收已完成；当前不表示已发布。

## REQ-0135 计划交付

计划新增后端授权的COS媒体直传：视频先行，随后图片及既有附件；提供进度、确认、重试、取消、派生状态与受控业务绑定。保持已有读取兼容，REQ-0136读取刷新不在本次范围。尚未实现或发布；按媒体灰度及回滚，最终完整交付需两阶段通过。容量35/30人天，无剩余修复缓冲，排期存在延期风险。
