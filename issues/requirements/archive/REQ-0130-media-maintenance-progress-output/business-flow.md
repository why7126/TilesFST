---
requirement_id: REQ-0130-media-maintenance-progress-output
lifecycle_stage: plan
created_at: 2026-08-29 18:08:25
updated_at: 2026-08-29 18:08:25
---

# 业务流程

## 1. 总体流程

```text
需求评审
  ↓
纳入 Sprint
  ↓
OpenSpec Change 设计 CLI 进度输出
  ↓
确认 stdout / stderr 兼容边界
  ↓
实现 --progress 或等价开关
  ↓
覆盖单任务与聚合任务进度
  ↓
补充测试与 Runbook
  ↓
dry-run 验证 JSON 兼容
  ↓
apply 模式验证进度、失败计数和脱敏
  ↓
验收通过后归档
```

## 2. 生产使用流程

```text
执行环境确认
  ├─ app_env / database_backend / object_storage_provider
  ├─ Compose 文件与后端服务名
  └─ 备份与执行窗口
      ↓
选择维护任务
  ├─ backfill-brand-certificate-thumbnails
  ├─ backfill-image-variants
  └─ media-drift-reconcile
      ↓
dry-run
  ├─ 不加 --progress：仅最终 JSON
  └─ 加 --progress：stderr 展示扫描进度，stdout 保持最终 JSON
      ↓
人工复核
  ├─ failed / retry_candidates
  ├─ estimated_writes
  └─ failure_reasons
      ↓
apply
  ├─ stderr 查看 total / completed / percent
  ├─ 观察 failed 是否持续增加
  └─ stdout 保存最终 JSON
      ↓
执行后复核
  ├─ dry-run 幂等结果
  ├─ key / object / URL / benefit
  └─ render evidence
```

## 3. 输出通道流程

```text
维护任务内部计数
  ↓
ProgressReporter
  ├─ disabled：不输出进度
  └─ enabled：stderr 输出进度行
      ↓
任务完成
  ↓
stdout 输出完整 JSON summary / items / acceptance_summary
```

规则：

- stdout 继续承载最终 JSON。
- stderr 承载进度行和人工可读执行过程信息。
- 生产脚本保存结果时可继续重定向 stdout 到 JSON 文件。
- 需要保存进度日志时，可单独重定向 stderr。

## 4. 与父需求差异

| 项目 | REQ-0097 生产媒体维护任务 | REQ-0130 媒体维护任务进度输出 |
|---|---|---|
| 目标 | 建立生产可执行的媒体维护入口和备份确认门禁 | 增强长耗时维护命令的执行过程可见性 |
| 交付物 | 维护任务、Docker Compose 执行方式、安全输出和 Runbook | 可选进度参数、输出通道约定、阶段/计数输出、测试和 Runbook 更新 |
| 数据写入 | 可涉及数据库和对象存储写入 | 不改变既有写入策略，仅展示执行过程进度 |
| 风险重点 | 误连环境、未备份写入、对象漂移处理错误 | stdout JSON 兼容被破坏、进度输出泄露敏感信息、百分比口径误导 |

## 5. 异常流程

```text
任务启动前无法计算 total
  └─ 使用阶段级 total 或明确 total_unknown，不展示误导性百分比

对象存储不可达
  └─ 进度输出停止在 blocked 阶段，最终 JSON 保留既有 blocked summary

单项处理失败
  └─ failed 计数增加，最终 JSON 记录脱敏失败 item 与 failure_reasons

进度输出通道不可用
  └─ 不影响最终 JSON；命令仍以最终 summary 作为事实源
```
