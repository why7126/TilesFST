---
requirement_id: REQ-0097-prod-compose-media-maintenance-job
title: 生产 Docker Compose 环境支持媒体历史数据维护任务安全执行 - 业务流程
created_at: 2026-08-04 10:37:36
updated_at: 2026-08-04 10:37:36
---

# 业务流程

## 1. 总体流程

```text
发现历史媒体维护需求
  |
  v
确认任务类型与影响范围
  |
  v
选择生产维护入口
  |-- 推荐：deploy/prod/compose.tencent-cos.yml + tilesfst-maintenance
  |-- 备选：deploy/prod/compose.tencent-cos.yml + tilesfst-backend 受控命令
  `-- 兼容：docker-compose.prod.external.yml，仅限明确兼容场景
  |
  v
执行 dry-run
  |
  +--> blocker: 环境不匹配 / MySQL 回退 SQLite / 对象存储不可达 / 输出含敏感信息
  |       |
  |       v
  |     停止并修复
  |
  v
完成 MySQL 快照 + 对象存储 bucket/prefix 快照
  |
  v
执行 apply（limit / batch）
  |
  v
输出结果摘要 + 失败原因 + 重试候选
  |
  v
执行二次审计
  |
  v
回填媒体四联/五联验收摘要与生产执行证据入口
```

## 2. 关键分支

### 2.1 镜像策略分支

```text
维护脚本是否需要进入生产容器？
  |
  +-- 是 --> 优先新增 tilesfst-maintenance 镜像/服务
  |          |
  |          v
  |        发布镜像治理 + Compose/env 示例同步
  |
  +-- 复用 backend --> 确认镜像内有受控命令入口
  |                    |
  |                    v
  |                  不改变在线服务 CMD/端口/健康检查
  |
  `-- 临时挂载 scripts/ --> 仅允许只读审计或应急 dry-run
                         |
                         v
                       禁止 apply，除非后续另行审批
```

### 2.2 执行安全分支

```text
准备 apply？
  |
  +-- dry-run 未通过 --> 不允许 apply
  |
  +-- 缺 MySQL 快照 --> 不允许 apply
  |
  +-- 缺对象存储快照 --> 不允许 apply
  |
  +-- 输出包含敏感值 --> 不允许 apply，先修日志脱敏
  |
  `-- 全部满足 --> 分批 apply，并记录执行摘要
```

## 3. 与父需求差异

本 REQ 当前没有父需求。它与相关需求的边界如下：

| 关联需求 | 差异 |
|---|---|
| REQ-0012-object-storage-key-layout | REQ-0012 定义对象 Key 规则；本 REQ 定义生产中如何安全执行历史迁移和审计。 |
| REQ-0018-production-mysql-deployment | REQ-0018 定义生产 MySQL 支持；本 REQ 要求维护任务不得回退 SQLite。 |
| REQ-0092-brand-certificate-image-thumbnails | REQ-0092 定义缩略图能力；本 REQ 定义存量回填、重生成和生产审计入口。 |
| REQ-0093-standardize-deployment-environment-matrix | REQ-0093 定义 deploy 矩阵；本 REQ 在该矩阵内增加维护作业执行能力。 |

## 4. 失败与回滚流程

```text
apply 失败
  |
  +-- 部分对象已写入，DB 未更新 --> 保留对象快照，二次审计后重试或清理需单独审批
  |
  +-- DB 已更新，对象写入失败 --> 依据失败摘要恢复 MySQL 快照或重试缺失对象
  |
  +-- 对象删除/移动类失败 --> 优先恢复 bucket/prefix 快照，不默认运行反向脚本
  |
  `-- 日志泄密风险 --> 立即停止，清理输出渠道并记录安全事件处理入口
```
