---
requirement_id: REQ-0114-version-deployment-upgrade-rollback-governance
title: 版本部署升级与回滚治理能力 - 业务流程
created_at: 2026-08-21 18:34:27
updated_at: 2026-08-21 22:09:09
owner: product
---

# 业务流程

## 1. 总体流程

```text
选择目标版本 to_version
        |
        v
读取 releases/<to_version>/release.json
        |
        v
选择来源版本 from_version
   |             |                |
   | fresh       | previous       | older version
   v             v                v
首次部署计划   相邻升级计划      跨版本升级计划
   |             |                |
   +-------------+----------------+
                 |
                 v
聚合证据与风险
                 |
                 +-- release / image manifest / Git ref
                 +-- env diff / deploy env safety
                 +-- DB schema drift / smoke / backup
                 +-- Docker Compose / image tag
                 +-- object storage / maintenance dry-run
                 |
                 v
输出支持级别
                 |
      +----------+-----------+
      |                      |
      v                      v
supported              blocked / manual review
      |                      |
      v                      v
执行升级前检查        补证 / 人工确认 / 调整路径
      |
      v
人工执行升级或后续自动化执行
      |
      v
升级后 smoke + 证据回填
      |
      v
升级完成或执行回滚计划
```

## 2. 首次部署流程

```text
/upgrade-plan --from fresh --to vX.Y.Z
        |
        v
校验目标版本 release.json / image-manifest.json
        |
        v
校验生产 env 必填项和安全边界
        |
        v
校验 Docker Compose config
        |
        v
部署目标版本镜像
        |
        v
后端启动 init_database()
        |
        +-- MySQL: schema.mysql.sql + mysql_migrations.py
        +-- SQLite: schema.sql + migrations.py
        |
        v
健康检查 / 登录 / 核心 API / 对象存储 smoke
        |
        v
记录 fresh-install-supported 证据
```

## 3. 相邻升级流程

```text
/upgrade-plan --from vN.N.N --to vN.N.N+1
        |
        v
读取来源版本与目标版本事实源
        |
        v
生成 env diff + image manifest 校验 + DB 影响判断
        |
        v
确认升级前备份
        |
        v
更新 TILESFST_IMAGE_TAG 为目标版本
        |
        v
重启或滚动更新服务
        |
        v
升级后 smoke
        |
        +-- pass: 记录 adjacent-upgrade-supported 证据
        |
        +-- fail: 执行回滚计划
```

## 4. 跨版本升级流程

```text
/upgrade-plan --from vOld --to vTarget
        |
        v
按 SemVer / release_time 收集中间版本
        |
        v
聚合每个中间版本 impact_scope / gates / upgrade_steps / rollback
        |
        v
分析跨版本影响
        |
        +-- DB schema / migration / drift
        +-- env 示例差异
        +-- Docker / image manifest
        +-- API / Orval
        +-- object storage / media maintenance
        |
        v
判定支持级别
        |
        +-- 证据完整且演练通过: cross-version-upgrade-supported
        +-- 证据不足或需人工补证: cross-version-upgrade-requires-manual-review
        +-- 存在破坏性阻断: unsupported
```

## 5. 回滚流程

```text
升级失败或验收不通过
        |
        v
检查回滚前置证据
        |
        +-- previous_image
        +-- env_snapshot
        +-- database_backup
        +-- object_storage_backup / read-only confirmation
        |
        v
恢复旧镜像 tag / 旧离线包
        |
        v
恢复旧 env 或人工确认的 env 摘要
        |
        v
按条件恢复 DB 备份
        |
        v
处理对象存储写入影响
        |
        v
回滚后 smoke
        |
        v
记录 rollback evidence
```

## 6. 与既有发布流程的差异

| 现状 | 新流程 |
|---|---|
| release 按目标版本记录发布事实 | upgrade plan 按 `from_version -> to_version` 记录升级路径 |
| `upgrade_steps` 多为文本说明 | 升级步骤、阻塞项、证据和回滚要求结构化 |
| env 校验关注目标环境安全 | env diff 关注来源版本到目标版本的变量变化 |
| DB migration 存在即容易被视为可升级 | DB 升级必须有 drift/smoke、备份和路径验证证据 |
| 回滚说明依赖人工记忆 | 回滚证据记录旧镜像、旧 env、DB 备份、对象存储影响和 smoke |

## 7. 异常流程

| 异常 | 处理 |
|---|---|
| 目标版本缺少 `release.json` | 阻断，提示先完成发布对象。 |
| 目标版本缺少 image manifest | image_required=true 时阻断，提示先执行 `/image-prepare` 和 `/image-build`。 |
| Git tag 缺失 | 按规则输出 warning 或 blocker；必须至少记录 commit。 |
| 来源版本 release 事实源缺失 | 标记 `source_confidence=reconstructed|partial`，跨版本升级默认进入人工复核。 |
| env diff 无法解析 | 标记 manual_review，不得输出真实 env。 |
| DB drift 命中缺表或缺字段 | 阻断或要求先完成迁移/备份/复查。 |
| 对象存储维护任务需要写入 | 必须先 dry-run 和备份确认，不得自动 apply。 |
| 回滚证据缺失 | 升级计划 blocked 或 requires manual review。 |
