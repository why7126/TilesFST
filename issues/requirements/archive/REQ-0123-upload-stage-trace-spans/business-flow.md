---
requirement_id: REQ-0123-upload-stage-trace-spans
title: 上传链路阶段级耗时写入 trace spans - 业务流程
owner: product
source: requirement.md
created_at: 2026-08-25 18:43:20
updated_at: 2026-08-25 18:43:20
---

# 业务流程

## 1. 成功路径

```text
管理端用户选择图片
  ↓
后端鉴权与上传入口接收文件
  ↓
[span:file_read] 读取上传文件内容
  ↓
文件大小 / MIME / 扩展名 / 对象 key 策略校验
  ↓
[span:original_put_object] 原图写入对象存储
  ↓
[span:thumbnail_generate] 生成 thumbnail
  ↓
[span:thumbnail_put_object] thumbnail 写入对象存储
  ↓
[span:display_generate] 生成 display
  ↓
[span:display_put_object] display 写入对象存储
  ↓
写入或更新业务记录 / 构造 URL
  ↓
返回上传结果，并可通过 task trace 定位 spans
```

## 2. 失败路径

```text
任一阶段开始
  ↓
记录 span started_at 或计时起点
  ↓
阶段执行成功？
  ├─ 是：记录 duration_ms + status=success，进入下一阶段
  └─ 否：记录 duration_ms + status=failed + 脱敏错误摘要
          ↓
       根据媒体降级策略判断是否继续、跳过后续阶段或返回错误
          ↓
       保留失败前已完成 spans 与失败阶段 span
```

## 3. 跳过路径

```text
上传格式或入口不适用某派生规格
  ↓
记录对应阶段 status=skipped 或在设计中声明 N/A
  ↓
metadata 记录脱敏跳过原因
  ↓
继续执行适用阶段或返回上传结果
```

## 4. 与父 REQ 差异

| 对比项 | 父 REQ-0115 | 本 REQ-0123 |
|---|---|---|
| 能力目标 | 建立 `thumbnail / display / original` 三规格资源模型和多端消费策略。 | 为头像上传与通用图片上传补齐阶段级耗时 trace spans。 |
| 关注对象 | 图片派生对象、URL 字段、端侧消费、历史补生成。 | 上传处理阶段、耗时、成功/失败/跳过状态和排障证据。 |
| 对象存储影响 | 定义派生对象 key、URL 和直出/代理边界。 | 不改变 key / bucket，仅记录对象写入阶段耗时和失败状态。 |
| API/DB 影响 | 多规格字段可能影响接口与存储模型。 | 默认优先复用现有 task trace；是否暴露 API 或新增 DB 需 OpenSpec 明确。 |

## 5. 横切复盘吸收

- 来自 sprint-025 复盘：媒体能力验收应覆盖 key、object、URL、render/Network 与收益指标；本需求将“耗时收益/阶段瓶颈”纳入媒体证据口径。
- 来自媒体上传 best-practice：上传状态机、同会话回显、Docker Web `:3000` 入口和 `/media/{object_key}` 代理一致性仍是后续实现的横切验收底线。
