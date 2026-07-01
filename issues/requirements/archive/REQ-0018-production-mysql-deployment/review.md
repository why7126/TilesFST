---
review_id: REV-REQ-0018-001
requirement_id: REQ-0018-production-mysql-deployment
title: REQ-0018 生产环境部署与 MySQL 数据库支持评审
date: 2026-06-29 09:11:17
participants: []
result: approved
created_at: 2026-06-29 09:11:17
updated_at: 2026-06-29 09:11:17
---

# 需求评审

## 评审结论

REQ-0018 文档包已达到评审通过标准，批准进入 OpenSpec Change 阶段。

本需求范围聚焦生产环境部署、外部 MySQL 8.0+ 支持、生产 Compose、MinIO 持久化、环境变量与部署文档同步。Out of Scope 已明确排除内嵌 MySQL、SQLite 到 MySQL 业务数据迁移、高可用、K8s/Helm/Terraform、云厂商专有集成和前端/小程序 UI 变更。

验收标准 AC-001 至 AC-045 可测试，覆盖数据库连接、MySQL 初始化、管理员 seed、生产 Docker Compose、MinIO、文档、测试与不回归要求。该需求为基础设施 / 部署 / 数据库类需求，无 UI 原型要求，N/A 处理合理。

## 评审清单

- [x] 范围清晰，Out of Scope 明确
- [x] 验收标准可测试
- [x] 优先级与依赖合理
- [x] UI 类：原型或实现策略已决（N/A，无 UI 变更）
- [x] 无与现有 REQ 重复未说明

## 条件通过项

- [ ] `/req-opsx` 创建 OpenSpec Change 时，必须在 `design.md` 中明确 SQLite 与 MySQL 双 dialect 初始化策略。
- [ ] 实现阶段必须补充 MySQL baseline DDL 与类型映射说明，建议落入 `implementation/db.md`。
- [ ] 生产部署文档必须显式提示不得使用 `.env.example` 默认密钥，且不得在 Compose 中内嵌 MySQL 服务。

## 后续动作

| 动作 | 说明 |
|---|---|
| `/req-opsx REQ-0018-production-mysql-deployment` | 创建建议 Change：`add-production-mysql-deployment` |
| `/sprint-propose` | 仅在 OpenSpec Change 准备纳入迭代时执行 |
