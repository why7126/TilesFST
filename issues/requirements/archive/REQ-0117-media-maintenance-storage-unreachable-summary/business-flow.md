---
requirement_id: REQ-0117-media-maintenance-storage-unreachable-summary
title: 媒体维护 dry-run 增加对象存储不可达快速摘要 - 业务流程
created_at: 2026-08-22 17:14:59
updated_at: 2026-08-22 17:14:59
---

# 业务流程

## 1. 总体流程

```text
运维选择媒体维护任务
  |
  v
执行 dry-run
  |
  v
读取数据库候选范围
  |
  v
访问对象存储元信息或对象内容
  |
  +--> 对象存储不可达 / 权限异常 / endpoint 错误
  |       |
  |       v
  |     返回 blocked 快速摘要
  |       |
  |       v
  |     停止 apply 判断，先修复对象存储环境
  |
  +--> 对象真实不存在
  |       |
  |       v
  |     记录 missing 类统计，继续生成 dry-run 摘要
  |
  v
输出正常 dry-run 摘要
  |
  v
按 REQ-0097 流程判断备份、apply、二次审计
```

## 2. 快速失败摘要流程

```text
对象访问异常
  |
  +-- MEDIA_NOT_FOUND / NoSuchKey / NoSuchObject
  |     |
  |     v
  |   missing_original / missing_thumbnail / object_missing
  |
  +-- STORAGE_UNAVAILABLE / 网络超时 / 权限不可用 / endpoint 配置错误
        |
        v
      object_storage_unreachable
        |
        v
      summary.status = blocked
        |
        v
      acceptance_summary.object.status = blocked
        |
        v
      recommended_action = 检查 endpoint、region、bucket、权限、网络与 env 注入
```

## 3. 聚合任务流程

```text
bug-0116-media-drift
  |
  +-- sku_pending_formalization
  +-- certificate_image_key_migration
  +-- brand_logo_and_certificate_thumbnail_backfill
  `-- object_key_audit
        |
        v
任一对象相关子任务发现统一不可达
        |
        +-- 顶层 summary 标记 blocked
        +-- affected_tasks 列出受影响子任务
        +-- 后续对象相关子任务 skipped / blocked
        `-- 不输出可进入 apply 的结论
```

## 4. 与父 REQ 差异

| 关联需求 | 差异 |
|---|---|
| REQ-0097-prod-compose-media-maintenance-job | REQ-0097 定义生产维护任务入口、安全边界、dry-run/apply、备份和二次审计；本 REQ 专注 dry-run 中对象存储不可达的快速失败摘要和分类准确性。 |
| REQ-0090-media-five-point-acceptance-template | REQ-0090 定义五联验收维度；本 REQ 要求对象维度在不可达时表达 blocked，而不是误报 pass 或 missing。 |
| REQ-0091-media-bug-four-point-acceptance-template | REQ-0091 定义媒体 BUG 四联验收；本 REQ 避免对象存储不可达被写成对象缺失证据。 |

## 5. 失败与恢复流程

```text
dry-run 返回 object_storage_unreachable
  |
  +-- 检查生产 env provider / endpoint / region / bucket
  |
  +-- 检查对象存储权限、凭据有效性和 bucket/prefix 快照
  |
  +-- 检查后端容器到对象存储 endpoint 的网络连通性
  |
  +-- 修复对象存储环境
  |
  `-- 重新执行 dry-run，再判断是否进入备份确认和 apply
```
