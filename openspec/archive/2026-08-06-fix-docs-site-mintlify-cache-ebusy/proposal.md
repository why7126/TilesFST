---
change_id: fix-docs-site-mintlify-cache-ebusy
title: 修复 docs-site Mintlify 缓存挂载导致 EBUSY 启动失败
status: applied
source_bug: BUG-0120-docs-site-mintlify-cache-ebusy
created_at: 2026-08-06 11:09:17
updated_at: 2026-08-06 11:18:25
---

# 提案

## 背景

BUG-0120 记录了 `tilesfst-docs-site` 在启用 Docker Compose `docs-site` profile 后启动失败的问题。Mintlify CLI 在 preparing local preview 阶段尝试将容器内 `/home/node/.mintlify` 重命名为 `/home/node/.mintlify-last`，但当前根 Compose、local Compose 和 prod Compose 都把 Docker named volume `tilesfst-docs-site-cache` 直接挂载到 `/home/node/.mintlify`，该路径作为挂载点无法按普通目录完成 rename，导致 `EBUSY`。

该缺陷影响 Mintlify 文档站本地预览、演示部署和生产等价验收，但不影响后端 API、数据库、Web 业务 UI、小程序、管理端权限、Orval 或对象存储上传链路。

## 目标

- 移除 docs-site 对 `/home/node/.mintlify` 的 Docker named volume 挂载，避免 Mintlify CLI 重命名挂载点。
- 保持 `mintlify/` 站点源目录只读挂载，不写宿主机 `~/.mintlify*`。
- 同步根 Compose、deploy local/prod Compose、部署文档和测试断言。
- 通过 Compose config、目录结构校验和 docs-site 启动验证证明问题闭环。

## 非目标

- 不修改后端 API、数据库 schema、Web 业务 UI、小程序或管理端运行时代码。
- 不修改 Mintlify CLI 上游行为。
- 不引入宿主机 `~/.mintlify*` 挂载或真实 Mintlify 账号、token、生产域名配置。
- 不新增文档站功能、页面信息架构或 release usage docs 内容。

## 影响范围

- `docker-compose.yml`、`deploy/local/compose.yml`、`deploy/prod/compose.tencent-cos.yml` 中的 `tilesfst-docs-site` 服务。
- `deploy/docs-site/Dockerfile` 注释或缓存目录准备逻辑，若实现需要同步。
- `docs/02-deployment.md`、`deploy/local/README.md`、`deploy/prod/README.md` 等部署说明。
- `tests/test_validate_directory_structure.py` 与目录结构校验。
- BUG-0120 追溯状态与验收回填。

## 回滚方案

若移除 docs-site 缓存 volume 后出现 Mintlify 预览性能或缓存复用问题，可回滚 Compose 与文档中的无持久缓存配置；若仍需缓存持久化，应改为挂载 CLI 不会重命名的父级或备用缓存路径，并补充启动验证。回滚不得引入宿主机 `~/.mintlify*` 挂载或真实凭据。
