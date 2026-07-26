## Why

微信小程序相关变更已经覆盖首页、分类、搜索、商品列表、SKU 详情和自定义导航栏等多条链路，但 DevTools 预览、真机验收、静态测试和人工 follow-up 的证据口径仍容易散落在 REQ、Change、tasks、Sprint 验收报告和归档备注中。需要建立统一的设备验收 evidence 模板，避免把自动化或静态检查误写成真实设备验收已完成。

## What Changes

- 新增小程序 DevTools/真机验收 evidence 模板能力，定义 `miniapp_device_evidence` 的结构、字段、状态和引用方式。
- 明确自动化/静态测试、脚本测试、DevTools 预览和真机验收的证据边界。
- 要求 DevTools evidence 记录工具版本、基础库、页面路径、视口、截图/录屏或人工摘要，并明确不等同于真机验收。
- 要求真机 evidence 记录设备、系统、微信版本、基础库、安全区、状态栏、胶囊避让、截图/录屏和剩余风险。
- 约定模板优先沉淀到 `docs/standards/miniapp-device-evidence-template.md`，供后续小程序 REQ、OpenSpec Change、Sprint 验收报告和 release note 引用。
- 不新增小程序业务功能，不回填全部历史 evidence，不引入自动化截图、真机云测、API、数据库、Orval、Docker Compose 或 MinIO 变更。

## Capabilities

### New Capabilities

- `miniapp-device-evidence-template`: 定义微信小程序 DevTools 预览、真机验收、自动化证据、N/A、blocked 和 follow-up 的统一 evidence 模板与引用规则。

### Modified Capabilities

- 无。

## Impact

- 后端：无运行时代码、API、权限或上传链路变更。
- Web / 管理端：无运行时代码变更；仅可能在长期文档中引用标准模板。
- 小程序：无页面、组件、样式、服务或配置变更；只新增设备验收治理模板。
- 数据库 / 存储 / Orval / Docker：无变更。
- 文档：实现阶段新增 `docs/standards/miniapp-device-evidence-template.md`，并在 Change trace / acceptance / tasks 中记录模板引用与 evidence 边界。
- 测试：实现阶段至少补充文档存在性、模板字段和敏感信息边界的轻量校验，避免纯手工文档无法回归。
