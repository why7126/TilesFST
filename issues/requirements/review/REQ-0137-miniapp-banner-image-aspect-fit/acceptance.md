---
requirement_id: REQ-0137-miniapp-banner-image-aspect-fit
title: 验收清单
created_at: '2026-09-07 22:58:53'
updated_at: '2026-09-11 09:07:09'
acceptance_status: not_started
---

# 验收清单

## 功能验收

- [ ] AC-001：首页 Banner 的展示图与缩略图回退分支均等比完整适配，边缘标记及文字不被裁切。（FR-001）
- [ ] AC-002：品牌列表 Banner 同样覆盖两种图片分支；既有遮罩不得导致图片关键信息不可读。（FR-001、003）
- [ ] AC-003：品牌详情头图两种图片分支均完整适配；图片绘制区与品牌文字区无交叠，名称、英文名、简介保留。（FR-001、003）
- [ ] AC-004：商品详情顶部每个图片项完整适配，横图、方图、竖图均不拉伸或裁切。（FR-001）
- [ ] AC-005：在 320、375、430 pt 等价宽度记录四类区域截图，包含宽图、方图、竖图和边缘文字；切图、加载及回退前后高度一致，不产生横向溢出。（FR-002）
- [ ] AC-006：留白使用既有背景语义；品牌详情在 380rpx 总高内验证 220rpx 图片区与 160rpx 文字区，覆盖长品牌名、长简介及可选文案为空；沿用既有截断规则且不遮住图片。（FR-003）
- [ ] AC-007：Banner 原跳转、指示状态、商品图预览与媒体切换可用；视频本体、视频封面、播放操作和非 Banner 图片展示保持原行为。（FR-004）
- [ ] AC-008：展示图失败到缩略图、全部失败、空数据、加载中均有可定位验证记录；占位沿用原契约且无新增破图。（FR-002、005）
- [ ] AC-009：差异核对及聚焦静态测试证明目标分支全部覆盖，URL/变体选择、懒加载、错误回退和预览 URL 规则未变，不新增原图下载。（FR-005）

## 原型与实现一致性

- [ ] AC-PROTOTYPE-001：后续 Change 建立 UI Contract，以 prototype/web/banner-fit.html 为局部布局事实源，context.md 说明适用区域和 Mock 边界；设计核对控件不进入产品。
- [ ] AC-PROTOTYPE-002：实现先完成 Skeleton 首轮确认，记录 1440px 设计核对视口及小程序 DevTools 或等价视觉证据；再完成四页面和关键状态检查。
- [ ] AC-PROTOTYPE-003：记录图片区/文字区尺寸、mode 或 object-fit、背景 token、overflow 和层级的 computed style 或小程序等价证据；实现与原型最终对照后才允许归档，返修后更新证据。

## 产品数据采集与链路观测

- [ ] AC-OBS-001：对照实现差异确认 status=not_applicable、affected_layers=[wechat_miniapp]；仅渲染和布局调整，API、DB、请求日志、行为事件、Task Trace、端请求封装无变更。若范围扩大，重做适用性声明及对应测试。
- [ ] AC-OBS-002：确认无新采集字段及保留周期，脱敏与现有日志策略不变；证据不含完整签名 URL、凭据、客户数据或本机路径。OpenAPI/Orval、SQLite/MySQL 迁移和 Docker Compose 验证均因无契约或部署输入变化而 N/A；完成小程序聚焦静态测试和视觉验证。

## 证据与当前结论

当前 acceptance_status=not_started，全部复选框保留未勾选；本命令仅完善需求和 HTML 原型。后续记录页面、选择器、素材比例、逻辑宽度、证据来源、脱敏引用、执行时间和结论。浏览器 HTML 原型只能证明设计方案，不证明小程序实现、DevTools、真机或线上通过。

## 横切 AC（knowledge-base）

固定场景标签 admin-list、admin-form、admin-modal、media-upload 均未命中：本需求是小程序图片展示，无管理端 CRUD 或上传。无上述标签的横切 AC；主动复用小程序媒体实践，增加以下三条专项预防项。

来源：`docs/knowledge-base/best-practices/miniapp-media-four-part-acceptance-practice.md`，结合 `docs/knowledge-base/retrospectives/sprint-028-retrospective.md` 的媒体验收经验。

- [ ] AC-XCUT-001：为四类区域记录 key/object/URL/render 四联结论；key/object 无改动时说明沿用对象及 N/A 证明边界，URL 核对既有来源，render 以实际截图验证，不以对象存在或 HTTP 200 代替展示通过。
- [ ] AC-XCUT-002：代表正常加载和回退场景记录脱敏 Network 摘要，包含页面、资源类型、URL 类型、HTTP 状态、大小、耗时及 render 结论；明确区分 HTML、DevTools、真机和体验版，未执行环境不能标通过。
- [ ] AC-XCUT-003：静态检查保留 src 回退、预览 data-url 和懒加载契约；视频播放及 poster 作为未变回归点，历史对象批量审计与回填为 N/A（本需求不改 key/object，不发起存储写入）。

## 验收结果回填

```yaml
acceptance_status: not_started
accepted_at: null
accepted_by: null
source_change: fix-miniapp-banner-image-aspect-fit
source_sprint: sprint-030
evidence: []
failed_items: []
source_event: req.opsx
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```



## 实施进度证据（未完成产品验收）

三个页面五个图片节点已使用aspectFit；品牌详情分区仍待确认。聚焦4项静态测试通过，现有静态套件37通过/1端口配置基线失败。开发工具仅观察到首页图片、品牌列表无Banner回退、商品整图留白和动态视频，未覆盖17项AC的完整验证条件；不勾选整体验收通过。详细来源、证据边界与剩余矩阵见openspec/changes/fix-miniapp-banner-image-aspect-fit/implementation-evidence.md。产品数据采集与链路观测仍not_applicable；无API/DB、请求封装、Orval或Compose变更。
