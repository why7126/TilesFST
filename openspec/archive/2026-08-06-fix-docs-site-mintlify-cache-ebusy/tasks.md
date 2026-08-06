---
change_id: fix-docs-site-mintlify-cache-ebusy
title: 修复 docs-site Mintlify 缓存挂载导致 EBUSY 启动失败任务
status: applied
source_bug: BUG-0120-docs-site-mintlify-cache-ebusy
created_at: 2026-08-06 11:09:17
updated_at: 2026-08-06 11:18:25
---

# 任务

- [x] 1. 移除根 `docker-compose.yml` 中 `tilesfst-docs-site-cache:/home/node/.mintlify` 挂载和顶层 `tilesfst-docs-site-cache` volume 声明。
- [x] 2. 同步移除 `deploy/local/compose.yml` 与 `deploy/prod/compose.tencent-cos.yml` 中相同的 docs-site 缓存 volume 挂载和 volume 声明。
- [x] 3. 复核 `deploy/docs-site/Dockerfile` 中 `/home/node/.mintlify` 目录准备逻辑是否仍需要保留；若保留，应明确该目录属于容器临时文件系统。
- [x] 4. 更新 `docs/02-deployment.md`、`deploy/local/README.md`、`deploy/prod/README.md` 中关于 Mintlify 运行缓存写入 Docker named volume 的说明，改为预览缓存不持久化且不写宿主机 `~/.mintlify*`。
- [x] 5. 更新 `tests/test_validate_directory_structure.py`，断言 docs-site 不再挂载 `tilesfst-docs-site-cache:/home/node/.mintlify`，并继续覆盖 profile、工作目录、只读 `mintlify/` 挂载、端口和命令。
- [x] 6. 运行 `docker compose --profile docs-site config --quiet`，并对 deploy local/prod Compose 执行等价 config 校验。
- [x] 7. 运行 `python3 scripts/validate-directory-structure.py` 和相关 pytest。
- [x] 8. 在可访问 Docker 的环境启动 `tilesfst-docs-site` 并检查日志，确认不再出现 `/home/node/.mintlify` 到 `/home/node/.mintlify-last` 的 `EBUSY`。
- [x] 9. 复核不涉及 API、数据库、Web 业务 UI、小程序、管理端权限、Orval 或对象存储上传链路。
- [x] 10. 若修复经验具备复用价值，归档前评估是否需要沉淀到 `docs/knowledge-base/incidents/`。
