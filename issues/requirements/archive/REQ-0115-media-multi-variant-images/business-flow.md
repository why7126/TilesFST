---
requirement_id: REQ-0115-media-multi-variant-images
title: 媒体图片多规格展示图能力 - 业务流程
created_at: 2026-08-22 11:00:33
updated_at: 2026-08-22 11:00:33
---

# 业务流程

## 1. 新上传图片生成流程

```text
管理端用户选择图片
  |
  v
Web 上传控件进入 uploading
  |
  v
FastAPI uploads/media API 校验大小、MIME、扩展名、鉴权
  |
  v
对象存储适配层写入 original
  |
  v
图片派生服务生成 thumbnail / display
  |
  +--> 成功：记录或派生三规格 key / URL，上传控件进入 done 并即时回显
  |
  +--> 失败：记录错误与降级策略，上传控件进入 failed 或展示可恢复 warning
```

## 2. 商品接口返回与前端选择流程

```text
商品 / SKU / 媒体查询
  |
  v
后端组装媒体字段
  |
  +--> thumbnail_url：列表、卡片、轻量预览
  |
  +--> display_url：详情普通展示、图册浏览
  |
  +--> original_url：高清预览、下载或保真场景
  |
  v
小程序 / Web 根据场景选择 URL
  |
  +--> 列表：thumbnail_url
  +--> 详情：display_url
  +--> 预览：original_url
  |
  v
目标 URL 缺失或失败时按 fallback 顺序处理
```

## 3. 存量媒体治理流程

```text
维护人员选择治理范围
  |
  v
dry-run 扫描历史媒体
  |
  +--> 已闭环：跳过
  +--> 缺 thumbnail：列入补生成候选
  +--> 缺 display：列入补生成候选
  +--> object 不存在 / URL 风险：列入失败分类
  |
  v
人工确认风险、备份和执行窗口
  |
  v
apply 显式执行补生成
  |
  v
输出成功、失败、跳过、重试建议和脱敏统计
```

## 4. 与父需求差异

| 项 | `REQ-0012-object-storage-key-layout` | 本需求 |
|---|---|---|
| 关注点 | 对象存储 key 布局、Bucket / prefix 策略和对象访问边界。 | 图片多规格资源模型、生成策略、多端 URL 选择和历史媒体补生成。 |
| 输出形态 | 稳定的对象 key 与存储治理规则。 | `thumbnail / display / original` 三规格图与接口字段。 |
| 端上体验 | 主要提供存储基础。 | 明确小程序列表、详情、预览的实际使用策略和性能证据。 |
| 历史对象 | 关注 key 布局和兼容。 | 关注存量图片是否生成派生资源、dry-run / apply 和收益证据。 |

## 5. 边界说明

- 本流程不直接实现外部 CDN 正式接入，但 URL 生成应为后续 CDN 或对象存储直出预留适配层。
- 本流程不覆盖视频转码、多清晰度视频或视频封面生成。
- 生产历史媒体写入必须先 dry-run、脱敏输出并由人工确认执行窗口。
