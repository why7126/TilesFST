---
title: sprint-030 发布候选说明
created_at: '2026-09-08 08:39:14'
updated_at: 2026-09-10 19:20:59
---

# sprint-030 发布候选说明

## 计划范围

- REQ-0138-knowledge-model-lifecycle-sync：计划建立本体驱动知识模型及归档、Sprint、发布同步与恢复，完整小规模快照提交Git。

- REQ-0137-miniapp-banner-image-aspect-fit：拟统一小程序四类大图的完整适配展示，允许留白并保持布局稳定。

- REQ-0136-signed-cos-direct-media-read：计划三端媒体COS直读、过期恢复、历史兼容及受控回退。

- BUG-0149-opsx-apply-premature-stop：已完善一次apply持续交付及真实行为验收，减少用户反复发送“继续”；仅治理流程；48项单测与14次真实Agent受控运行通过，用户确认归档，验收passed。

## 用户可见变化

验收完成后：首页与品牌Banner、品牌头图、商品详情图片完整露出；品牌信息和图片互不遮挡。当前仅规划，尚未实现或发布。

## 技术与兼容边界

REQ-0137只影响小程序渲染及相关测试；视频、非Banner图片、既有URL/变体、API、DB、Web和管理端保持原契约。无需Orval或Docker Compose验证。

REQ-0136后续涉及后端API、三端请求与观测；同步OpenAPI/Orval与测试，需要Compose及COS/小程序证据，DB若变更同步SQLite/MySQL。与REQ-0137组合回归保持完整图片展示。

## 发布状态

两个REQ的Change已创建；BUG-0149修复Change为fix-apply-continuous-execution-behavior，尚无本Sprint整体产品版本或上线结论。先完成REQ验收及Change归档，再按release工作流确定版本和公开公告；本说明不作为正式公告。


BUG-0149不变更业务端、API、DB，无Orval或Compose要求；治理完成不自动发布、部署或归档。

## REQ-0138交付边界

已纳入规划、关联Change为add-knowledge-model-lifecycle-sync，尚未实施；无产品页面、API和数据库行为变更，无Orval或Compose要求。知识快照由prepare构建、publish确认；当前没有产品版本或发布结论，不用测试夹具冒充正式发布。
