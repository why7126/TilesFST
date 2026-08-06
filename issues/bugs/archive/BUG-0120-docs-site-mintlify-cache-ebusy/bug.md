---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
title: tilesfst-docs-site Mintlify 缓存 volume 导致 EBUSY 启动失败
severity: medium
status: done
owner:
discovered_at: 2026-08-06 10:39:49
environment: docker
related_requirement: REQ-0094-mintlify-versioned-docs-directory
related_change:
created_at: 2026-08-06 10:53:38
updated_at: 2026-08-06 11:24:20
---

# tilesfst-docs-site Mintlify 缓存 volume 导致 EBUSY 启动失败

## 现象

启用 `docs-site` profile 启动 `tilesfst-docs-site` 时，Mintlify 本地预览停留在 preparing local preview 阶段，并反复输出：

```text
error EBUSY: resource busy or locked, rename '/home/node/.mintlify' -> '/home/node/.mintlify-last'
```

该问题导致文档站预览服务无法稳定启动，影响本地、演示或生产等价环境中的 Mintlify 文档站验证。

## 复现步骤

1. 确认项目中存在 `mintlify/docs.json` 与 `mintlify/docs/**`。
2. 执行 `docker compose --profile docs-site up -d --build tilesfst-docs-site`，或通过本地启动脚本启用 `docs-site` profile。
3. 查看 `tilesfst-docs-site` 容器日志。

## 期望结果

`tilesfst-docs-site` 能稳定启动 Mintlify 本地预览，文档站可通过 `HOST_PORT_MINTLIFY_DOCS` 对应宿主机端口访问。Mintlify 预览缓存不应依赖会被 CLI 重命名的 Docker volume 挂载点。

## 实际结果

Mintlify CLI 尝试将容器内 `/home/node/.mintlify` 重命名为 `/home/node/.mintlify-last`，但当前 Compose 将 Docker named volume `tilesfst-docs-site-cache` 直接挂载到 `/home/node/.mintlify`，该路径作为挂载点无法按普通目录完成 rename，触发 `EBUSY` 并导致服务启动失败或反复重启。

## 影响范围

- 影响 Docker Compose `docs-site` profile 下的 `tilesfst-docs-site` 服务。
- 影响本地、演示和生产等价的 Mintlify 文档站预览/承载验证。
- 不影响后端 API、数据库、Web 业务 UI、小程序、管理端权限、Orval 或对象存储上传链路。

## 严重等级说明

严重等级为 `medium`。该问题不会阻断核心业务 API 或用户端功能，但会阻断文档站预览服务启动，影响发布验收、部署验证和公开文档站交付链路。若当前发布必须依赖 docs-site 验收，可在评审时提升优先级。
