---
bug_id: BUG-0120-docs-site-mintlify-cache-ebusy
created_at: 2026-08-06 11:03:45
updated_at: 2026-08-06 11:03:45
classification: design
---

# 根因分析

## 直接原因

`tilesfst-docs-site` 的 Compose 配置将 Docker named volume `tilesfst-docs-site-cache` 直接挂载到容器内 `/home/node/.mintlify`。Mintlify CLI 启动本地预览时会尝试把该目录重命名为 `/home/node/.mintlify-last`，但 `/home/node/.mintlify` 是 volume 挂载点，容器内无法像普通目录一样完成 rename，因此返回 `EBUSY`。

## 根本原因

docs-site profile 为避免污染宿主机 `~/.mintlify*`，把 Mintlify 运行缓存持久化到 Docker named volume；但该设计把 Mintlify CLI 的内部缓存目录当作稳定外部契约，并且挂载到了 CLI 会主动重命名的精确路径。缓存目录不是业务数据，持久化收益有限，却引入了挂载点与 CLI 原子重命名行为之间的冲突。

## 触发条件

- 启用 `docs-site` profile。
- 启动 `tilesfst-docs-site`。
- Compose 中存在 `tilesfst-docs-site-cache:/home/node/.mintlify` 挂载。
- Mintlify CLI 在 preparing local preview 阶段执行 `/home/node/.mintlify` 到 `/home/node/.mintlify-last` 的重命名。

## 分类

- 缺陷类型：部署 / Compose 设计缺陷。
- 影响层级：Docker Compose 文档站预览服务。
- 非影响层级：后端 API、数据库、Web 业务 UI、小程序、管理端权限、Orval、对象存储上传链路。

## 修复方向

推荐移除 `tilesfst-docs-site-cache:/home/node/.mintlify` 挂载和对应顶层 volume 声明，让 Mintlify 预览缓存留在容器临时文件系统内，不作为跨容器持久化数据管理。
