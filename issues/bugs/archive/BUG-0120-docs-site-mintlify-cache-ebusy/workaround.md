---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
created_at: 2026-08-06 11:03:45
updated_at: 2026-08-06 11:03:45
---

# 临时规避方案

## 可选规避

在正式修复前，可临时停止 docs-site 并清理已创建的缓存 volume 后重试：

```bash
docker compose --profile docs-site down
docker volume rm tilesfst_tilesfst-docs-site-cache
docker compose --profile docs-site up -d --build tilesfst-docs-site
```

该方式只清理缓存数据，不能改变 `/home/node/.mintlify` 仍是 volume 挂载点的事实。如果 Mintlify CLI 每次启动都尝试重命名该目录，问题仍可能复现。

## 推荐处置

将该问题纳入正式 BUG 修复流程，移除 docs-site 对 `/home/node/.mintlify` 的 named volume 挂载，并同步根 Compose、local/prod Compose、部署文档和目录结构测试断言。

## 风险说明

- 清理 Docker volume 会丢失 Mintlify 预览缓存，但该缓存不是业务数据。
- 不应通过挂载宿主机 `~/.mintlify*` 规避，否则会违背当前部署文档中“不污染宿主机 Mintlify 缓存目录”的约束。
