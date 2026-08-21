---
requirement_id: REQ-0111-miniapp-media-four-part-acceptance-practice
created_at: 2026-08-12 14:29:30
updated_at: 2026-08-12 14:29:30
---

# Business Flow

## 1. 四联验收闭环

```text
媒体类 REQ / BUG / Change
  |
  v
识别是否影响小程序媒体展示、预览、播放或性能
  |
  v
按四联收集证据
  |
  +--> key：业务记录、脱敏 key、前缀、原图/缩略图/视频/poster 关系
  |
  +--> object：object 存在、MIME、大小、权限、缩略图收益
  |
  +--> URL：受控 /media URL、HTTP 状态、业务错误码、resolved/fallback、缓存证据
  |
  +--> render：页面路径、组件、DevTools/真机/体验版 evidence、用户可见行为
  |
  v
任一维度 fail / blocked？
  |
  +-- 是 --> 记录失败/阻塞、影响范围、重试条件；必要时 /bug-capture 或返修
  |
  +-- 否 --> 汇总验收结论，进入 Sprint / Release 证据
```

## 2. 测试 helper 使用流程

```text
后端接口或小程序页面测试
  |
  v
构造媒体样例：图片、视频、Logo、证书、Banner、商品卡片图
  |
  v
调用测试 helper
  |
  +--> 断言展示 URL 优先缩略图
  +--> 断言 preview URL 保留原图
  +--> 断言视频 URL 与 poster / cover 语义分离
  +--> 断言 fallback、lazy-load、页面模板绑定
  +--> 断言受控 /media URL 语义和 raw key 暴露边界
  |
  v
测试摘要进入 acceptance / OpenSpec validation
```

## 3. 审计 helper 使用流程

```text
历史媒体对象审计需求
  |
  v
选择资源类型和范围
  |
  +--> SKU 图片 / 视频 poster
  +--> 品牌 Logo / Banner / 证书
  +--> 小程序商品卡片图
  |
  v
dry-run 审计 helper
  |
  +--> object 存在性
  +--> MIME / 大小 / 扩展名
  +--> 缩略图存在性与轻量收益
  +--> URL fallback 风险
  +--> 失败原因枚举与脱敏统计
  |
  v
是否需要写入回填或重生成？
  |
  +-- 否 --> 记录审计摘要与剩余风险
  |
  +-- 是 --> 另行确认 apply、备份、幂等、失败重试和验收证据
```

## 4. 与既有需求差异

| 对象 | 差异 |
|---|---|
| `REQ-0090` | 五联模板是通用媒体链路维度；REQ-0111 聚焦小程序媒体场景、BUG-0125/0126 经验和 helper 落地。 |
| `REQ-0091` | BUG 四联模板定义缺陷修复闭环；REQ-0111 补充小程序 Network evidence、历史对象审计和可复用 helper。 |
| `REQ-0101` | 三段模板组织列表字段、生成策略、历史对象维护；REQ-0111 强化小程序真实请求与 render 证据。 |
| `docs/standards/miniapp-device-evidence-template.md` | 设备 evidence 模板定义通用字段；REQ-0111 将其嵌入小程序媒体验收链路。 |

## 5. Prototype 策略

本需求不新增 Web 管理端、店主 Web 或小程序页面，不需要 prototype。若后续在文档站或验收工具中展示该实践，另行在对应 OpenSpec Change 中提供 UI Contract 与视觉验收证据。
