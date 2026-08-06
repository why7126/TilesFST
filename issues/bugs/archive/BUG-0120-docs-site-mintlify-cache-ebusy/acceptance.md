---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
acceptance_status: passed
created_at: 2026-08-06 11:03:45
updated_at: 2026-08-06 17:17:37
source_change:
source_sprint:
---

# 验收标准

## AC-001 移除冲突挂载

- GIVEN 根 `docker-compose.yml`、`deploy/local/compose.yml` 与 `deploy/prod/compose.tencent-cos.yml`
- WHEN 检查 `tilesfst-docs-site` 服务配置
- THEN 不再存在 `tilesfst-docs-site-cache:/home/node/.mintlify` 挂载
- AND 顶层 `tilesfst-docs-site-cache` volume 声明被同步移除

## AC-002 文档站可启动

- GIVEN `mintlify/docs.json` 与 `mintlify/docs/**` 已存在
- WHEN 执行 `docker compose --profile docs-site up -d --build tilesfst-docs-site`
- THEN `tilesfst-docs-site` 不再因 `rename '/home/node/.mintlify' -> '/home/node/.mintlify-last'` 输出 `EBUSY`
- AND 文档站可通过 `HOST_PORT_MINTLIFY_DOCS` 对应宿主机端口访问

## AC-003 部署文档同步

- GIVEN docs-site 缓存不再持久化为 Docker named volume
- WHEN 查看部署文档与 deploy README
- THEN 不再宣称 Mintlify 运行缓存写入 Docker named volume
- AND 明确预览缓存不属于业务数据，可留在容器临时文件系统内

## AC-004 回归校验同步

- GIVEN 目录结构测试覆盖 docs-site Compose profile
- WHEN 运行相关目录结构测试或 `python3 scripts/validate-directory-structure.py`
- THEN 测试断言与新的无缓存 volume 配置一致
- AND 不影响 backend、web、minio 与对象存储相关服务配置

## 验收结果回填

```yaml
acceptance_status: passed
accepted_at: 2026-08-06 17:17:37
accepted_by: workflow-sync
source_change: fix-docs-site-mintlify-cache-ebusy
source_sprint: sprint-021
evidence: []
failed_items: []
source_event: sprint.archive
notes: 由 Workflow Sync 根据 Change/Sprint 状态回填。
```

