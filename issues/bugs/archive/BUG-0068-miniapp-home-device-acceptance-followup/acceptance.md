---
bug_id: BUG-0068-miniapp-home-device-acceptance-followup
status: done
created_at: 2026-07-19 17:36:58
updated_at: 2026-07-19 21:39:11
related_requirement: REQ-0041-miniapp-home
related_bug: BUG-0065-miniapp-home-preview-deviation
suggested_fix_change:
related_requirements:
  - REQ-0041-miniapp-home
---

# 回归验收标准

> 本 BUG 的闭环目标是补齐 Sprint 008 小程序首页 DevTools / 真机验收 evidence，并在发现真实遮挡或重叠时进入后续 fix。默认不修改后端 API、数据库、Orval、Web、管理端或 Docker Compose。

## AC-001 验收 evidence MUST 区分来源

**Given** 团队准备关闭 `BUG-0068`  
**When** 汇总验收材料  
**Then** MUST 明确区分自动化测试结果、微信开发者工具截图、真机截图和人工结论  
**And** MUST NOT 将静态测试通过表述为真机验收通过  
**And** MUST 记录验收时间、设备或模拟器、逻辑宽度和结论

## AC-002 首页 DevTools 真实预览 MUST 可用

**Given** 使用微信开发者工具打开 `src/miniapp/`  
**When** 进入 `pages/index/index`  
**Then** 首页 MUST 展示品牌导航、搜索入口、Banner 或品牌化降级、快捷入口、推荐模块或空状态、全部产品区域和底部 TabBar  
**And** 页面 MUST NOT 出现首屏大面积空白、运行脚本未执行或关键模块整体缺失

## AC-003 320-430 pt 视口 MUST 覆盖

**Given** 首页 DevTools 或真机预览可打开  
**When** 分别在 320、375、390、430 pt 及 320-430 pt 常见宽度检查首页  
**Then** 页面 MUST 无横向滚动  
**And** 关键文本 MUST 可读或按预期单行省略  
**And** 卡片、搜索框、快捷入口和推荐模块 MUST 不发生不可接受的挤压或重叠

## AC-004 微信原生胶囊 MUST 被避让

**Given** 首页使用自定义导航栏  
**When** 在微信开发者工具或真机检查右上角微信原生分享 / 关闭胶囊区域  
**Then** 品牌名称、品牌副标题、Logo、返回区域或其他自定义导航内容 MUST NOT 进入原生胶囊区域  
**And** WXML / WXSS MUST NOT 新增手绘分享、关闭或胶囊控件  
**And** 胶囊区域必须在截图中可辨认且未被页面内容覆盖

## AC-005 fixed header 与底部 TabBar MUST 不遮挡内容

**Given** 首页存在 fixed 自定义导航和 custom TabBar  
**When** 检查首屏、滚动中段和页面底部  
**Then** fixed header MUST 通过 spacer 或等价方式为内容让位  
**And** 底部 TabBar 与安全区 MUST 不遮挡商品卡片、加载状态、空状态或主要点击目标  
**And** 主要点击目标 SHOULD 不小于 44x44 pt

## AC-006 图片、数据为空和网络失败 MUST 有可验收状态

**Given** 首页数据或图片资源不可用  
**When** 触发 Banner 为空、商品为空、图片加载失败或首页请求失败  
**Then** 页面 MUST 显示品牌化降级、空状态或错误提示  
**And** 降级状态下仍需满足 320-430 pt、胶囊避让和内容不遮挡要求  
**And** 错误诊断信息 MUST 不泄露敏感路径、密钥或后台字段

## AC-007 自动化侧证 MUST 保留但不得越界

**Given** 执行小程序相关自动化或静态测试  
**When** `tests/test_miniapp_static.py` 通过  
**Then** 可作为运行入口、自定义导航声明、禁止伪胶囊和基础点击尺寸侧证  
**And** MUST 在验收结论中注明该结果不替代 DevTools / 真机截图  
**And** 若测试失败，MUST 先修复或解释失败原因，不得继续声称设备验收通过

## AC-008 默认不扩大技术范围

**Given** 后续创建 fix Change 或验收任务  
**When** 检查变更范围  
**Then** 默认 MUST 聚焦小程序首页、导航栏和验收 evidence  
**And** MUST NOT 修改后端 API、SQLite/MySQL schema、Pydantic Schema、Orval 生成物、Web 管理端或 Docker Compose  
**And** 如设备验收发现接口、数据或环境问题，MUST 在后续 BUG / REQ 或 OpenSpec Change 中单独说明
