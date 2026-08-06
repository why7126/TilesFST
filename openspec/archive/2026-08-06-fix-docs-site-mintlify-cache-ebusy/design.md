---
change_id: fix-docs-site-mintlify-cache-ebusy
title: 修复 docs-site Mintlify 缓存挂载导致 EBUSY 启动失败设计
status: applied
source_bug: BUG-0120-docs-site-mintlify-cache-ebusy
created_at: 2026-08-06 11:09:17
updated_at: 2026-08-06 11:18:25
---

# 设计

## 根因

`tilesfst-docs-site-cache:/home/node/.mintlify` 把 Mintlify CLI 内部缓存目录变成 Docker volume 挂载点。Mintlify CLI 启动预览时会把 `/home/node/.mintlify` 重命名为 `/home/node/.mintlify-last`，挂载点不能按普通目录 rename，因此触发 `EBUSY`。

该配置的初衷是避免污染宿主机 Mintlify 缓存目录，但它把 CLI 内部实现细节固化为部署契约。文档站预览缓存不是业务数据，持久化收益低于运行时冲突风险。

## 修复方案

采用无持久化预览缓存方案：

- 保留 `mintlify/` 到 `/workspace/mintlify` 的只读挂载。
- 移除 `tilesfst-docs-site-cache:/home/node/.mintlify` 服务 volume。
- 移除对应顶层 `tilesfst-docs-site-cache` volume 声明。
- 保持镜像内 `HOME=/home/node`，让 Mintlify CLI 在容器临时文件系统内管理 `.mintlify` 与 `.mintlify-last`。
- 同步根、local、prod 三个 Compose 入口，避免不同部署矩阵行为漂移。

## 文档与治理

部署文档应从“运行缓存写入 Docker named volume”调整为“预览缓存不持久化，不写宿主机 `~/.mintlify*`”。目录结构测试应验证 docs-site 不再挂载 `/home/node/.mintlify`，并继续验证 docs-site profile 可选、工作目录、端口和命令不回归。

## 测试策略

- 运行 `docker compose --profile docs-site config --quiet`，确认根 Compose config 可解析。
- 对 deploy local/prod Compose 运行等价 config 校验，确认 docs-site profile、端口和挂载结构合法。
- 运行 `python3 scripts/validate-directory-structure.py`。
- 运行相关 pytest，例如 `python3 -m pytest tests/test_validate_directory_structure.py`。
- 在具备 Docker 权限的环境执行 `docker compose --profile docs-site up -d --build tilesfst-docs-site` 并查看日志，确认不再出现 `EBUSY`。

## 风险

- 首次启动可能重新生成 Mintlify 缓存，预览启动耗时可能略有增加。
- 若 Mintlify CLI 后续改变缓存路径，当前方案仍比固定挂载内部目录更稳健，因为不再绑定 CLI 会重命名的路径。
- 若生产选择 Compose 内 docs-site 长期承载，应确认容器重启后缓存丢失不影响服务可用性。
