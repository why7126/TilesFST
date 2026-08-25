---
requirement_id: REQ-0122-batch-image-processing-runbook
lifecycle_stage: archive
created_at: 2026-08-25 09:26:23
updated_at: 2026-08-25 12:05:38
---

# 业务流程

## 1. 总体流程

```text
需求评审
  ↓
OpenSpec Change 设计 Runbook 与投影策略
  ↓
确认现有脚本 / 待改造脚本 / 待新增脚本
  ↓
编写长期 Runbook（docs）
  ↓
按版本发布需要投影到 releases/vX.Y.Z/usage-docs
  ↓
生产执行前安全门禁
  ↓
dry-run
  ↓
人工复核与执行确认
  ↓
apply / 分批执行
  ↓
对象存储 + DB/API + 端侧展示验收
  ↓
收尾记录 / 回滚判断 / 失败项追踪
```

## 2. 生产执行流程

```text
执行环境确认
  ├─ 生产服务器或受控堡垒环境
  ├─ Compose 文件 / 镜像 tag
  ├─ MySQL / 对象存储 provider
  └─ 最小权限凭据
      ↓
备份确认
  ├─ MySQL 快照或等价可恢复备份
  └─ bucket / prefix / 受影响对象集合快照
      ↓
dry-run
  ├─ 影响记录数
  ├─ 预计写入对象
  ├─ key 冲突 / 缺失对象 / 跳过原因
  └─ 对象存储不可达摘要
      ↓
人工确认
  ├─ 执行窗口
  ├─ 分批参数
  ├─ 中止条件
  └─ 回滚入口
      ↓
apply
  ├─ 图片转换
  ├─ thumb/display 派生生成
  ├─ 缩略图专项重建
  └─ 对象 key 迁移
      ↓
验收
  ├─ key / object / URL
  ├─ thumbnail/display benefit
  ├─ Web / 小程序 / 管理端 render
  └─ 失败清单与补证项
```

## 3. 文档投影流程

```text
docs Runbook（长期事实源）
  ↓
release 准备阶段判断是否需要 usage-docs
  ↓
releases/vX.Y.Z/usage-docs 继承或投影 Runbook
  ↓
manifest 记录来源、版本、更新时间、覆盖页面
  ↓
Mintlify 或交付文档按 release 快照发布
```

规则：

- `docs/` 承载当前长期 Runbook 事实源。
- `releases/vX.Y.Z/usage-docs/` 承载版本快照，不反向覆盖长期事实源。
- 旧版本内容性更正必须记录更正原因、操作者或确认来源、时间和文件范围。
- 发布快照不得包含真实密钥、生产私有域名、真实客户数据、对象存储备份包或生产执行原始日志。

## 4. 与父需求差异

| 项目 | REQ-0115 媒体图片多规格展示图能力 | REQ-0122 批量图片处理 Runbook |
|---|---|---|
| 目标 | 建立 `thumbnail / display / original` 多规格资源模型和多端消费策略 | 沉淀批量图片处理、派生图重建、key 迁移和生产执行的 Runbook |
| 交付物 | API 字段、对象派生、端侧消费、存量批量生成能力 | 长期 Runbook、版本 usage-docs 投影、生产步骤、安全门禁、验收模板 |
| 实现边界 | 可涉及后端、对象存储、API、Orval、小程序/Web 调整 | 本需求文档阶段不改源码；后续 Change 可按 Runbook 要求补文档、脚本或验证 |
| 风险重点 | 性能、URL 字段、派生图生成失败和 fallback | 生产误操作、密钥泄露、备份缺失、不可回滚、验收证据不足 |

## 5. 异常与回滚流程

```text
dry-run 发现风险
  ├─ key 冲突 → 停止 apply，修正映射或范围
  ├─ 对象缺失 → 记录失败清单，补对象或排除范围
  ├─ 对象存储不可达 → 停止，修复环境后重跑
  └─ 影响范围超预期 → 重新评审执行窗口

apply 失败
  ├─ 可重试失败 → 按失败原因分批重跑剩余项
  ├─ 数据库回填异常 → 使用 DB 快照或手工修复计划
  ├─ 对象写入异常 → 使用对象快照恢复或重跑派生
  └─ 端侧展示异常 → 记录 BUG 或阻断发布
```

回滚说明必须以已验证的 MySQL 快照和对象存储快照为主。未验证的反向脚本不得写作默认可靠回滚方案。
